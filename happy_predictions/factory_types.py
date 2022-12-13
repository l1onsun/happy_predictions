from typing import NewType

from happy_predictions.telegram.telegram_service import TelegramService

MainFullUrl = NewType("MainFullUrl", str)
MainTelegramService = NewType("MainTelegramService", TelegramService)

AdminFullUrl = NewType("AdminFullUrl", str)
AdminTelegramService = NewType("AdminTelegramService", TelegramService)
