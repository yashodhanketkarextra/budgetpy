import os
from unittest import mock

import pytest

from src.config import Settings


def test_settings_missing_secret_key():
    with mock.patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="SECRET_KEY is not set"):
            Settings()


def test_settings_invalid_env():
    with mock.patch.dict(os.environ, {"SECRET_KEY": "key", "PY_ENV": "invalid"}):
        with pytest.raises(ValueError, match="Illegal value for PY_ENV"):
            Settings()
