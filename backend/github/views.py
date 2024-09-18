from rest_framework.status import HTTP_200_OK, HTTP_202_ACCEPTED
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .validate import GitHubSearchParams


@api_view(["POST"])
def search_github(request: Request):
    search_params = GitHubSearchParams(**request.data)
    return Response(
        data={
            "results": [],
            "search_params": search_params.model_dump(),
        },
        status=HTTP_200_OK,
        content_type="application/json",
    )


@api_view(["GET"])
def clear_cache(request: Request):
    return Response(
        data={"success": True},
        status=HTTP_202_ACCEPTED,
        content_type="application/json",
    )
