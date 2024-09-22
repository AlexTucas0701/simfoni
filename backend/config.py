import os


class Config:
    CACHE_EXPIRY = 7200  # 7200 sec: 2 hr
    GITHUB_PAT = os.getenv("_GITHUB_PAT", None)
    DEV_STAGE = os.getenv("DEV_STAGE", "prod").lower() in ["dev", "development"]
    REDIS_CONNECTION_URL = os.environ["REDIS_CONNECTION_URL"]
