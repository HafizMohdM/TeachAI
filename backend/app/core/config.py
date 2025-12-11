from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Make keys optional to avoid import-time crashes; application code
    # can raise clearer errors at runtime if required.
    GEMINI_API_KEY: str | None = None
    OPENAI_API_KEY: str | None = None
    

    # pydantic-settings prefers `model_config` for configuration
    model_config = {"env_file": ".env"}


settings = Settings()
