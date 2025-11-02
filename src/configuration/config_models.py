from typing import Optional
from pydantic import BaseModel

class Filter(BaseModel):
    domain: list[str]
    sub_domain: list[str]

class Filters(BaseModel):
    propagate: Optional[Filter] = None
    log: Optional[Filter] = None

class MatchFullUrlsPolicy(BaseModel):
    enabled: bool = False

class MatchRelativeUrlsPolicy(BaseModel):
    enabled: bool = False
    attempt_propagation: bool = False

class Policy(BaseModel):
    match_full_urls: Optional[MatchFullUrlsPolicy] = None
    match_relative_urls: Optional[MatchRelativeUrlsPolicy] = None

class ProfileConfig(BaseModel):
    name: str
    start_url: str
    filters: Optional[Filters] = None
    policy: Optional[Policy] = None

class WorkerConfig(BaseModel):
    max_workers: int