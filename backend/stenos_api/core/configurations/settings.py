from pydantic_settings import BaseSettings
from pydantic import computed_field

class Settings(BaseSettings):
    mongo_host: str
    mongo_port: int
    mongo_user: str
    mongo_password: str
    mongo_database: str

    @computed_field
    def mongo_uri(self) -> str:
        return f"mongodb://{self.mongo_user}:{self.mongo_password}@{self.mongo_host}:{self.mongo_port}"
    
    @computed_field
    def mongo_uri_masked(self) -> str:
        return f"mongodb://{self.mongo_user}:***@{self.mongo_host}:{self.mongo_port}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()