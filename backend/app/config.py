from dataclasses import dataclass


@dataclass
class Config:
    ELASTIC_URL: str
    OPENAI_API_KEY: str
    DEBUG: bool = False


APP_CONFIG: Config = None
