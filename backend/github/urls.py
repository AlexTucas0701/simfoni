from django.urls import path
from .views import (
    clear_cache,
    search_github,
)


urlpatterns = [
    path("search", search_github, name="search_github"),
    path("clear-cache", clear_cache, name="clear_cache"),
]
