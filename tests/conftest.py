import pytest

from happy_predictions.env import Env


@pytest.fixture
def env():
    return Env(
        mongo_uri="mongodb://localhost:27017/plarin_users_test",
        telegram_api_token="fake_telegram_api_token",
        bot_host="localhost",
        debug=True,
    )
