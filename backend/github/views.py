from rest_framework.status import HTTP_200_OK
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view

from utils import max_retry_exceed_exception_handler, pydantic_exception_handler

from .schemas import GitHubSearchParams  # Import schema for validating search params
from .service import (
    GitHubSearchService,
)  # Import the service responsible for searching GitHub


# API endpoint to handle GitHub search
# This view accepts POST requests to perform a GitHub search based on provided parameters
@api_view(["POST"])
@pydantic_exception_handler()  # Handles Pydantic validation errors
@max_retry_exceed_exception_handler()  # Handles rate-limit retry exceptions
def search_github(request: Request):
    # Parse and validate the search parameters from the request body using GitHubSearchParams schema
    search_params = GitHubSearchParams(**request.data)

    # Call the GitHubSearchService to perform the search with the validated parameters
    search_result = GitHubSearchService().search(search_params)

    # Return the search results along with the search parameters used in the request
    return Response(
        data={
            "results": search_result,  # The actual search results
            "search_params": search_params.model_dump(),  # Return the validated parameters for reference
        },
        status=HTTP_200_OK,  # Return status 200 to indicate success
        content_type="application/json",  # Specify the content type as JSON
    )


# API endpoint to clear the cache
# This view handles GET requests to clear the cached GitHub search results
@api_view(["GET"])
@pydantic_exception_handler()  # Handles any Pydantic errors, though unlikely for GET requests
def clear_cache(request: Request):
    # Call the service to clear all cached search results
    GitHubSearchService().clear_cache()

    # Return a success response indicating that the cache was cleared
    return Response(
        data={"success": True},  # Indicate success
        status=HTTP_200_OK,  # Return status 200 to indicate the cache was cleared successfully
        content_type="application/json",  # Specify the content type as JSON
    )
