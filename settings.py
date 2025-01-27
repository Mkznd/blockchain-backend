import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    run_mode: str = os.environ.get("RUN_MODE")
    db_host: str = os.environ.get("DB_HOST")
    db_port: str = os.environ.get("DB_PORT")
    db_name: str = os.environ.get("DB_NAME")
    db_username: str = os.environ.get("DB_USER")
    db_password: str = os.environ.get("DB_PASS")

    blockchain_url: str = os.environ.get("BLOCKCHAIN_URL")
    blockchain_port: str = os.environ.get("BLOCKCHAIN_PORT")
    abi_port: str = os.environ.get("ABI_PORT")
    contract_address: str = os.environ.get("CONTRACT_ADDRESS")
    private_key: str = os.environ.get("PRIVATE_KEY")

    sqlite_file_name: str | None = os.environ.get("SQLITE_FILE_NAME")
    database_url: str = ""

    if run_mode == "dev":
        database_url = f"sqlite:///{sqlite_file_name}"
    else:
        database_url = (
            f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
        )

    access_toke_expire_minutes: int = 60 * 24  # 1 day
    jwt_secret: str = os.environ.get("JWT_SECRET")
    jwt_algorithm: str = os.environ.get("JWT_ALGORITHM")


settings = Settings()
