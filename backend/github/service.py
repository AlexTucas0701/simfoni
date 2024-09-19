import math
import time
from functools import wraps
from typing import Dict

import requests
from requests.exceptions import HTTPError

from config import Config
from utils import AbstractGlobalInstance

from .constants import (
    GITHUB_DEFAULT_PAGE_SIZE,
    GITHUB_RATE_LIMIT_ERROR_REASON,
    GITHUB_SEARCH_RESULT_LIMIT,
)
from .schemas import GitHubSearchParams, GitHubSearchResponse, SearchType


def github_search_backoff(max_retry: int = 10, max_penalty=100):
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
            raise Exception("API rate limit exceeded")

        return wrapper

    return real_decorator


class GitHubSearchService(AbstractGlobalInstance):
    BASE_API = "https://api.github.com"
    SEARCH_TYPE_API_MAP: Dict[SearchType, str] = {
        SearchType.USER: "/search/users",
        SearchType.REPO: "/search/repositories",
        SearchType.ISSUE: "/search/issues",
    }

    def __init__(self):
        self.__session = requests.Session()
        if Config.GITHUB_PAT is not None:
            self.__session.headers.update(
                {
                    "Authorization": f"Bearer {Config.GITHUB_PAT}",
                },
            )

    def search(self, search_params: GitHubSearchParams):
        search_result = self.__search_engine(search_params)
        return search_result

    def __search_engine(
        self,
        search_params: GitHubSearchParams,
    ):
        search_endpoint = self.get_api_for_type(search_params.type)
        search_results = []
        for chunk in self.__fetch_all(
            search_endpoint=search_endpoint,
            keyword=search_params.keyword,
        ):
            search_results.extend(chunk.model_dump(mode="json")["items"])
        return search_results

    def __fetch_all(
        self,
        search_endpoint: str,
        keyword: str,
    ):
        first_page = self.__fetch_page(
            search_endpoint=search_endpoint,
            keyword=keyword,
        )
        yield first_page
        # Only the first 1000 search results are available
        # https://stackoverflow.com/questions/37602893/github-search-limit-results
        number_of_result = min(first_page.total_count, GITHUB_SEARCH_RESULT_LIMIT)
        valid_page_count = math.ceil(number_of_result / GITHUB_DEFAULT_PAGE_SIZE)

        for page in range(2, valid_page_count + 1):
            page_content = self.__fetch_page(
                search_endpoint=search_endpoint,
                keyword=keyword,
                page=page,
            )
            yield page_content

    @github_search_backoff()
    def __fetch_page(
        self,
        search_endpoint: str,
        keyword: str,
        page: int | None = None,
        page_size: int = GITHUB_DEFAULT_PAGE_SIZE,
    ):
        params = {
            "q": keyword,
            "per_page": page_size,
        }
        if page is not None:
            params["page"] = page
        res = self.__session.get(
            url=search_endpoint,
            params=params,
        )
        res.raise_for_status()
        response_data = res.json()
        return GitHubSearchResponse(**response_data)

    @classmethod
    def get_api_for_type(cls, search_type: SearchType):
        api_path = cls.SEARCH_TYPE_API_MAP[search_type]
        return f"{cls.BASE_API}{api_path}"
