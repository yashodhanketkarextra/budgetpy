import os


class Settings:
    def __init__(self):
        # set environment type
        self.PY_ENV: str = self._get_env_py_env()

        # set up env variables
        self.SECRET_KEY: str = self._get_env_secret_key()
        self.DB_URL: str = self._get_env_db_url()

        self.ALGORITHM: str = "HS256"
        self.TOKEN_EXP: int = 60

    def _get_env_secret_key(self) -> str:
        value = os.getenv("SECRET_KEY")
        if not value:
            raise ValueError("SECRET_KEY is not set")
        return value

    def _get_env_py_env(self) -> str:
        allowed = ["dev", "prod", "test"]
        value = os.getenv("PY_ENV", "dev")

        if value not in allowed:
            raise ValueError("Illegal value for PY_ENV")

        return value

    def _get_env_db_url(self) -> str:
        value = ""
        match self.PY_ENV:
            case "test":
                value = os.getenv("test_db")
            case "dev":
                value = os.getenv("dev_db")
            case "prod":
                value = os.getenv("prod_db")
            case _:
                value = None

        if not value:
            raise ValueError("DB_URL is not set")

        return value


settings = Settings()
