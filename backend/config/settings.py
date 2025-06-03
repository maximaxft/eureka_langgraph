from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    openai_model_name: str = "gpt-4o-mini"
    recursion_limit: int = 5

    class Config:
        env_file = ".env"


settings = Settings()
