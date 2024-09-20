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


def github_search_backoff(max_retry: int = 10, max_penalty=50):
    def real_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            penalty = 1
            for _ in range(max_retry):
                try:
                    return func(*args, **kwargs)
                except HTTPError as e:
                    if e.response.reason != GITHUB_RATE_LIMIT_ERROR_REASON:
                        raise
                    time.sleep(penalty)
                    penalty *= 2
                    penalty = min(penalty, max_penalty)
            raise MaxRetryExceedException()

        return wrapper

    return real_decorator


class GitHubSearchService(AbstractGlobalInstance):
    BASE_API = "https://api.github.com"
    SEARCH_TYPE_API_MAP: Dict[SearchType, str] = {
        SearchType.USER: "/search/users",
        SearchType.REPO: "/search/repositories",
        SearchType.ISSUE: "/search/issues",
    }
    PAGE_SIZE: int = 100

    def __init__(self):
        self.__cache = GitHubSearchCacheService()
        self.__session = requests.Session()
        if Config.GITHUB_PAT is not None:
            self.__session.headers.update(
                {
                    "Authorization": f"Bearer {Config.GITHUB_PAT}",
                },
            )

    def search(self, search_params: GitHubSearchParams):
        cache_key = self.generate_cache_key(search_params)
        cache_data = self.__cache.get_cache(cache_key)
        if cache_data is not None:
            return cache_data

        search_result = self.__search_engine(search_params)
        self.__cache.store_cache(cache_key, search_result)

        return search_result

    def clear_cache(self):
        self.__cache.clear_all_cache()

    def __search_engine(
        self,
        search_params: GitHubSearchParams,
    ):
        search_results = []
        for chunk in self.__fetch_all(search_params):
            search_results.extend(chunk.model_dump(mode="json")["items"])
        return search_results

    def __fetch_all(
        self,
        search_params: GitHubSearchParams,
    ):
        first_page = self.__fetch_page(search_params, 1)
        yield first_page
        # Only the first 1000 search results are available
        # https://stackoverflow.com/questions/37602893/github-search-limit-results
        number_of_result = min(first_page.total_count, GITHUB_SEARCH_RESULT_LIMIT)
        valid_page_count = math.ceil(number_of_result / self.PAGE_SIZE)

        for page in range(2, valid_page_count + 1):
            page_content = self.__fetch_page(search_params, page)
            yield page_content

    @github_search_backoff()
    def __fetch_page(
        self,
        search_params: GitHubSearchParams,
        page: int,
    ):
        search_endpoint = self.get_api_for_type(search_params.type)
        params = {
            "q": search_params.keyword,
            "per_page": self.PAGE_SIZE,
            "page": page,
        }
        res = self.__session.get(
            url=search_endpoint,
            params=params,
        )
        res.raise_for_status()
        response_data = res.json()
        return GitHubSearchResponse(**response_data)

    @staticmethod
    def generate_cache_key(search_params: GitHubSearchParams):
        return f"{search_params.type}|{search_params.keyword}"

    @staticmethod
    def generate_cache_key_for_page(search_params: GitHubSearchParams, page: int):
        return f"{search_params.type}|{search_params.keyword}|{page}"

    @classmethod
    def get_api_for_type(cls, search_type: SearchType):
        api_path = cls.SEARCH_TYPE_API_MAP[search_type]
        return f"{cls.BASE_API}{api_path}"


class GitHubSearchCacheService:
    def __init__(self, cache_prefix=GITHUB_SEARCH_REDIS_CACHE_PREFIX):
        self.__redis_client = redis.Redis.from_url(Config.REDIS_CONNECTION_URL)
        self.__cache_prefix = cache_prefix

    def store_cache(self, key, value):
        key = f"{self.__cache_prefix}|{key}"
        value = json.dumps(value)

        self.__redis_client.set(
            name=key,
            value=value,
            ex=Config.CACHE_EXPIRY,
        )

    def get_cache(self, key):
        key = f"{self.__cache_prefix}|{key}"
        cache: bytes = self.__redis_client.get(key)
        if cache is None:
            return None
        return json.loads(cache.decode())

    def clear_all_cache(self, prefix=None):
        if prefix is None:
            prefix = self.__cache_prefix
        else:
            prefix = f"{self.__cache_prefix}|{prefix}"

        for key in self.__redis_client.scan_iter(f"{prefix}*"):
            self.clear_cache(key)

    def clear_cache(self, key):
        self.__redis_client.delete(key)
