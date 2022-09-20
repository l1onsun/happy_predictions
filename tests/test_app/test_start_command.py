import httpx
import pytest

from happy_predictions.const import TELEGRAM_WEBHOOK_PATH


@pytest.mark.asyncio
async def test_start(app_client):
    resp: httpx.Response = await app_client.post(
        TELEGRAM_WEBHOOK_PATH,
        json={
            "update_id": 1,
            "message": {
                "message_id": 2,
                "from": {
                    "id": 3,
                    "is_bot": False,
                    "first_name": "Firstname",
                    "last_name": "Lastname",
                    "username": "username",
                    "language_code": "ru",
                },
                "chat": {
                    "id": 4,
                    "first_name": "Firstname",
                    "last_name": "Lastname",
                    "username": "username",
                    "type": "private",
                },
                "text": "/start",
                "date": 1_663_669_775,
                "entities": [{"offset": 0, "length": 6, "type": "bot_command"}],
            },
        },
    )
    assert resp.status_code == 200
