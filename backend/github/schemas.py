from enum import Enum
from typing import List, Optional, Union
from pydantic import BaseModel, Field, HttpUrl, model_validator
from datetime import datetime


class SearchType(Enum):
    USER = "user"
    REPO = "repo"
    ISSUE = "issue"


class GitHubSearchParams(BaseModel):
    type: SearchType
    keyword: str = Field(min_length=3)

    def model_dump(self, *args, **kwargs):
        org_data = super().model_dump(**kwargs)
        org_data["type"] = self.type.value
        return org_data


class License(BaseModel):
    key: str
    name: str
    spdx_id: str
    url: Optional[HttpUrl]
    node_id: str


class User(BaseModel):
    login: str
    id: int
    node_id: str
    avatar_url: HttpUrl
    gravatar_id: Optional[str] = ""
    url: HttpUrl
    html_url: HttpUrl
    followers_url: HttpUrl
    following_url: str
    gists_url: str
    starred_url: str
    subscriptions_url: HttpUrl
    organizations_url: HttpUrl
    repos_url: HttpUrl
    events_url: str
    received_events_url: HttpUrl
    type: str
    site_admin: bool
    score: Optional[float] = None


class Repository(BaseModel):
    id: int
    node_id: str
    name: str
    full_name: str
    private: bool
    owner: User
    html_url: HttpUrl
    description: Optional[str]
    fork: bool
    url: HttpUrl
    forks_url: HttpUrl
    keys_url: str
    collaborators_url: str
    teams_url: HttpUrl
    hooks_url: HttpUrl
    issue_events_url: str
    events_url: HttpUrl
    assignees_url: str
    branches_url: str
    tags_url: HttpUrl
    blobs_url: str
    git_tags_url: str
    git_refs_url: str
    trees_url: str
    statuses_url: str
    languages_url: HttpUrl
    stargazers_url: HttpUrl
    contributors_url: HttpUrl
    subscribers_url: HttpUrl
    subscription_url: HttpUrl
    commits_url: str
    git_commits_url: str
    comments_url: str
    issue_comment_url: str
    contents_url: str
    compare_url: str
    merges_url: HttpUrl
    archive_url: str
    downloads_url: HttpUrl
    issues_url: str
    pulls_url: str
    milestones_url: str
    notifications_url: str
    labels_url: str
    releases_url: str
    deployments_url: HttpUrl
    created_at: datetime
    updated_at: datetime
    pushed_at: Optional[datetime] = None
    git_url: str
    ssh_url: str
    clone_url: HttpUrl
    svn_url: HttpUrl
    homepage: Optional[HttpUrl | str] = ""
    size: int
    stargazers_count: int
    watchers_count: int
    language: Optional[str]
    has_issues: bool
    has_projects: bool
    has_downloads: bool
    has_wiki: bool
    has_pages: bool
    has_discussions: bool
    forks_count: int
    mirror_url: Optional[HttpUrl]
    archived: bool
    disabled: bool
    open_issues_count: int
    license: Optional[License]
    allow_forking: bool
    is_template: bool
    web_commit_signoff_required: bool
    topics: Optional[List[str]] = []
    visibility: str
    forks: int
    open_issues: int
    watchers: int
    default_branch: str
    score: float


class GitHubSearchResponse(BaseModel):
    total_count: int
    incomplete_results: bool
    items: List[Union[User, Repository]]

    @model_validator(mode="before")
    def parse_items(cls, input_data):
        items = input_data.get("items", [])
        parsed_items = []
        for item in items:
            if "full_name" in item:  # Repository items have "full_name"
                parsed_items.append(Repository(**item))
            else:
                parsed_items.append(User(**item))
        input_data["items"] = parsed_items
        return input_data
