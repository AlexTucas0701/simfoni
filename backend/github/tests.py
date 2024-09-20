from unittest.mock import patch, MagicMock

from django.test import TestCase
from polyfactory.factories.pydantic_factory import ModelFactory
from requests.exceptions import HTTPError

from config import Config
from utils import SingletonABCMeta
from utils.exceptions import MaxRetryExceedException
from .schemas import (
    GitHubSearchParams,
    GitHubSearchResponse,
    SearchType,
)
from .service import (
    GitHubSearchService,
    GitHubSearchCacheService,
    github_search_backoff,
)


class GitHubSearchResponseFactory(ModelFactory[GitHubSearchResponse]):
    __model__ = GitHubSearchResponse


class GitHubSearchServiceSingletonTestCase(TestCase):

    @patch.object(SingletonABCMeta, "_instances", {})
    @patch("github.service.GitHubSearchCacheService")
    def test_search_cache_hit(self, mock_cache_service):
        # Setup mock to return cached data
        search_params = GitHubSearchParams(type=SearchType.REPO, keyword="django")
        mock_cache_service.return_value.get_cache.return_value = ["cached_result"]

        # Create instance of the singleton service
        github_search_service = GitHubSearchService()

        result = github_search_service.search(search_params)

        self.assertEqual(result, ["cached_result"])
        mock_cache_service.return_value.get_cache.assert_called_once_with(
            github_search_service.generate_cache_key(search_params)
        )

    @patch.object(SingletonABCMeta, "_instances", {})
    @patch("github.service.GitHubSearchCacheService")
    @patch.object(GitHubSearchService, "_GitHubSearchService__search_engine")
    def test_search_cache_miss(self, mock_search_engine, mock_cache_service):
        # Setup mock cache to return None (cache miss)
        search_params = GitHubSearchParams(type=SearchType.REPO, keyword="django")
        mock_cache_service.return_value.get_cache.return_value = None
        mock_search_engine.return_value = ["api_result"]

        # Create instance of the singleton service
        github_search_service = GitHubSearchService()

        result = github_search_service.search(search_params)

        self.assertEqual(result, ["api_result"])
        mock_cache_service.return_value.store_cache.assert_called_once_with(
            github_search_service.generate_cache_key(search_params), ["api_result"]
        )

    @patch.object(SingletonABCMeta, "_instances", {})
    @patch.object(GitHubSearchService, "_GitHubSearchService__fetch_all")
    def test_search_engine_combines_results(self, mock_fetch_all):
        # Setup mock to return multiple pages of results
        search_params = GitHubSearchParams(type=SearchType.REPO, keyword="django")

        chunk_1: GitHubSearchResponse = GitHubSearchResponseFactory.build()
        chunk_2: GitHubSearchResponse = GitHubSearchResponseFactory.build()
        expected_output = (
            chunk_1.model_dump(mode="json")["items"]
            + chunk_2.model_dump(mode="json")["items"]
        )

        mock_fetch_all.return_value = [chunk_1, chunk_2]

        # Create instance of the singleton service
        github_search_service = GitHubSearchService()

        result = github_search_service._GitHubSearchService__search_engine(
            search_params
        )

        self.assertEqual(result, expected_output)


class GitHubSearchBackoffTestCase(TestCase):

    @patch("time.sleep", return_value=None)  # To avoid real sleep during tests
    def test_github_search_backoff_retry(self, mock_sleep):
        mock_func = MagicMock()
        mock_func.side_effect = HTTPError(
            response=MagicMock(reason="rate limit exceeded")
        )

        decorated_func = github_search_backoff(max_retry=3)(mock_func)

        with self.assertRaises(MaxRetryExceedException):
            decorated_func()

        self.assertEqual(mock_func.call_count, 3)

    def test_github_search_backoff_raises_non_rate_limit_error(self):
        mock_func = MagicMock()
        mock_func.side_effect = HTTPError(response=MagicMock(reason="some other error"))

        decorated_func = github_search_backoff(max_retry=3)(mock_func)

        with self.assertRaises(HTTPError):
            decorated_func()

        self.assertEqual(mock_func.call_count, 1)


class GitHubSearchCacheServiceTestCase(TestCase):

    @patch("redis.Redis.from_url")
    def test_cache_store(self, mock_redis):
        cache_service = GitHubSearchCacheService(cache_prefix="GITHUB_CACHE")
        cache_service.store_cache("test_key", {"some": "data"})

        mock_redis.return_value.set.assert_called_once_with(
            name="GITHUB_CACHE|test_key",
            value='{"some": "data"}',
            ex=Config.CACHE_EXPIRY,
        )

    @patch("redis.Redis.from_url")
    def test_cache_retrieve(self, mock_redis):
        mock_redis.return_value.get.return_value = '{"some": "data"}'.encode("utf-8")

        cache_service = GitHubSearchCacheService(cache_prefix="GITHUB_CACHE")
        result = cache_service.get_cache("test_key")

        self.assertEqual(result, {"some": "data"})
        mock_redis.return_value.get.assert_called_once_with("GITHUB_CACHE|test_key")

    @patch("redis.Redis.from_url")
    def test_cache_clear(self, mock_redis):
        mock_redis.return_value.scan_iter.return_value = ["key1", "key2"]

        cache_service = GitHubSearchCacheService()
        cache_service.clear_all_cache()

        mock_redis.return_value.delete.assert_any_call("key1")
        mock_redis.return_value.delete.assert_any_call("key2")
