from pydantic import BaseSettings

class Settings(BaseSettings):
    mongodb_url: str
    database_name: str
    secret_key: str
    smtp_host: str
    smtp_port: int
    smtp_username: str
    smtp_password: str

    class Config:
        env_file = ".env"

settings = Settings() 