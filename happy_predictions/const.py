import random
import string

SECRET_STR = "".join(random.choice(string.ascii_lowercase) for _ in range(20))
TELEGRAM_WEBHOOK_PATH = f"/{SECRET_STR}/telegram_webhook"

YEAR = 2022
