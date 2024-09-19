import os


class Config:
    GITHUB_PAT = os.getenv("GITHUB_PAT", None)
