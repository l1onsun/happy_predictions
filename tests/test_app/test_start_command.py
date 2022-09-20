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
                "message_id": 1,
                "entities": [
                    {
                        "type": "bot_command",
                        "offset": 0,
                        "length": 0,
                    }
                ],
                "date": 1_663_669_775,
            },
        },
    )
    assert resp.status_code == 200
