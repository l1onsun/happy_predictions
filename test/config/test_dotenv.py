import pytest
from app.config.dotenv import get_env, get_mongo_env ,get_gunicorn_env

def test_base_env():
    assert get_env()

def test_telegram_env():
    assert get_env().telegram

def test_mongo_env():
    assert get_env().mongo

def test_gunicorn_env():
    assert get_env().gunicorn