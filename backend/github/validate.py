from enum import Enum

from pydantic import BaseModel, field_validator


class SearchType(Enum):
    USER = "user"
    REPO = "repo"
    ISSUE = "issue"


class GitHubSearchParams(BaseModel):
    type: SearchType
    keyword: str

    @field_validator("type", mode="before")
    @classmethod
    def type_validator(cls, type: str):
        return SearchType(type)

    def model_dump(self, *args, **kwargs):
        org_data = super().model_dump(**kwargs)
        org_data["type"] = self.type.value
        return org_data
