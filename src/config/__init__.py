import os


class Settings:
    def __init__(self):
        self.SECRET_KEY: str = self._get_env_secret_key()
        self.ALGORITHM: str = "HS256"
        self.TOKEN_EXP: int = 60
        self.PY_ENV: str = self._get_env_py_env()

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


settings = Settings()
