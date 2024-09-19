import os


class Config:
    CACHE_EXPIRY = 7200  # 7200 sec: 2 hr
    GITHUB_PAT = os.getenv("GITHUB_PAT", None)
    REDIS_CONNECTION_URL = os.environ["REDIS_CONNECTION_URL"]
