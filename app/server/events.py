from app.database.get import get_db_client
from app.config.predictions import load_predictions

def init_db_client():
    # initiate lru_cache
    get_db_client()
    load_predictions()


def close_db_client():
    get_db_client().close()
    load_predictions().close()


on_startup=[init_db_client]
on_shutdown=[close_db_client]