import random
import string

SECRET_STR = "".join(random.choice(string.ascii_lowercase) for _ in range(20))
MAIN_TELEGRAM_WEBHOOK_PATH = f"/{SECRET_STR}/main_telegram_webhook"
ADMIN_TELEGRAM_WEBHOOK_PATH = f"/{SECRET_STR}/admin_telegram_webhook"

YEAR = 2023
