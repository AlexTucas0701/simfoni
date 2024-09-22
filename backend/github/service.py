import json
import math
import time
from functools import wraps
from typing import Dict

import redis
import requests
from requests.exceptions import HTTPError

from config import Config
from utils.exceptions import MaxRetryExceedException
from utils import AbstractGlobalInstance

from .constants import (
    GITHUB_RATE_LIMIT_ERROR_REASON,
    GITHUB_SEARCH_RESULT_LIMIT,
    GITHUB_SEARCH_REDIS_CACHE_PREFIX,
)
from .schemas import GitHubSearchParams, GitHubSearchResponse, SearchType


# Decorator to implement exponential backoff for retrying GitHub API calls in case of rate-limiting errors
def github_search_backoff(max_retry: int = 10, max_penalty=50):
    def real_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            penalty = 1  # Start with a 1 second delay
            for _ in range(max_retry):  # Retry loop
                try:
                    return func(*args, **kwargs)
                except HTTPError as e:
                    # Only retry for rate-limit errors, raise other exceptions
                    if e.response.reason != GITHUB_RATE_LIMIT_ERROR_REASON:
                        raise
                    time.sleep(penalty)  # Wait before retrying
                    penalty *= 2  # Exponentially increase wait time
                    penalty = min(penalty, max_penalty)  # Cap the maximum penalty
            raise MaxRetryExceedException()  # Raise exception if max retries exceeded

        return wrapper

    return real_decorator


class GitHubSearchService(AbstractGlobalInstance):
    BASE_API = "https://api.github.com"
    # Mapping between search types and corresponding GitHub API endpoints
    SEARCH_TYPE_API_MAP: Dict[SearchType, str] = {
        SearchType.USER: "/search/users",
        SearchType.REPO: "/search/repositories",
        SearchType.ISSUE: "/search/issues",
    }
    PAGE_SIZE: int = 100  # GitHub API allows 100 results per page

    def __init__(self):
        self.__cache = (
            GitHubSearchCacheService()
        )  # Cache service to store search results
        self.__session = requests.Session()  # Create a persistent HTTP session
        if Config.GITHUB_PAT is not None:  # Use personal access token if available
            self.__session.headers.update(
                {
                    "Authorization": f"Bearer {Config.GITHUB_PAT}",
                },
            )

    # Main search method that retrieves results from cache or fetches fresh data from GitHub API
    def search(self, search_params: GitHubSearchParams):
        cache_key = self.generate_cache_key(search_params)
        cache_data = self.__cache.get_cache(cache_key)  # Check if result is cached
        if cache_data is not None:
            return cache_data

        search_result = self.__search_engine(
            search_params,
        )  # Perform search if not cached
        self.__cache.store_cache(cache_key, search_result)  # Cache the new result

        return search_result

    # Method to clear all cached data
    def clear_cache(self):
        self.__cache.clear_all_cache()

    # Core search engine method that fetches data from GitHub API and combines paginated results
    def __search_engine(
        self,
        search_params: GitHubSearchParams,
    ):
        search_results = []
        # Fetch and append all search results (paginated)
        for chunk in self.__fetch_all(search_params):
            search_results.extend(chunk.model_dump(mode="json")["items"])
        return search_results

    # Fetch all pages for the search query
    def __fetch_all(
        self,
        search_params: GitHubSearchParams,
    ):
        first_page = self.__fetch_page(search_params, 1)  # Fetch first page
        yield first_page
        # GitHub limits results to 1000, calculate valid pages accordingly
        # https://stackoverflow.com/questions/37602893/github-search-limit-results
        number_of_result = min(first_page.total_count, GITHUB_SEARCH_RESULT_LIMIT)
        valid_page_count = math.ceil(number_of_result / self.PAGE_SIZE)

        # Fetch remaining pages
        for page in range(2, valid_page_count + 1):
            page_content = self.__fetch_page(search_params, page)
            yield page_content

    # Fetch a specific page of results from GitHub API with backoff handling
    @github_search_backoff()
    def __fetch_page(
        self,
        search_params: GitHubSearchParams,
        page: int,
    ):
        search_endpoint = self.get_api_for_type(search_params.type)
        params = {
            "q": search_params.keyword,
            "per_page": self.PAGE_SIZE,  # Number of results per page
            "page": page,
        }
        res = self.__session.get(
            url=search_endpoint,
            params=params,
        )
        res.raise_for_status()  # Raise an error for HTTP errors
        response_data = res.json()
        return GitHubSearchResponse(**response_data)  # Convert to response schema

    # Generate cache key based on search type and keyword
    @staticmethod
    def generate_cache_key(search_params: GitHubSearchParams):
        return f"{search_params.type}|{search_params.keyword}"

    # Generate cache key that includes page number
    @staticmethod
    def generate_cache_key_for_page(search_params: GitHubSearchParams, page: int):
        return f"{search_params.type}|{search_params.keyword}|{page}"

    # Retrieve appropriate API endpoint based on search type
    @classmethod
    def get_api_for_type(cls, search_type: SearchType):
        api_path = cls.SEARCH_TYPE_API_MAP[search_type]
        return f"{cls.BASE_API}{api_path}"


class GitHubSearchCacheService:
    # Cache service to interact with Redis for storing and retrieving search results
    def __init__(self, cache_prefix=GITHUB_SEARCH_REDIS_CACHE_PREFIX):
        self.__redis_client = redis.Redis.from_url(
            Config.REDIS_CONNECTION_URL
        )  # Redis connection
        self.__cache_prefix = cache_prefix

    # Store search results in Redis with a key and expiration time
    def store_cache(self, key, value):
        key = f"{self.__cache_prefix}|{key}"  # Prefix the key
        value = json.dumps(value)  # Serialize value as JSON

        self.__redis_client.set(
            name=key,
            value=value,
            ex=Config.CACHE_EXPIRY,  # Set cache expiry time
        )

    # Retrieve cached result from Redis
    def get_cache(self, key):
        key = f"{self.__cache_prefix}|{key}"
        cache: bytes = self.__redis_client.get(key)  # Fetch from Redis
        if cache is None:
            return None
        return json.loads(cache.decode())  # Deserialize JSON

    # Clear all cache entries (optional: with specific prefix)
    def clear_all_cache(self, prefix=None):
        if prefix is None:
            prefix = self.__cache_prefix
        else:
            prefix = f"{self.__cache_prefix}|{prefix}"

        for key in self.__redis_client.scan_iter(
            f"{prefix}*"
        ):  # Iterate over cache keys
            self.clear_cache(key)

    # Clear specific cache entry by key
    def clear_cache(self, key):
        self.__redis_client.delete(key)
