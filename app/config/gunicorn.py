from pydantic import BaseSettings, Field
from typing import Optional
import multiprocessing
from app.config.dotenv import get_env

gunicorn_env = get_env().gunicorn


def count_workers():
    if gunicorn_env.web_concurrency:
        workers = gunicorn_env.web_concurrency
    else:
        cores = multiprocessing.cpu_count()
        default_web_concurrency = gunicorn_env.workers_per_core * cores
        workers = min(int(default_web_concurrency), gunicorn_env.max_workers)

    assert workers > 0
    return workers


# Gunicorn config
bind = f"{gunicorn_env.host}:{gunicorn_env.port}"
workers = count_workers()
timeout = gunicorn_env.timeout
keepalive = gunicorn_env.keepalive  # not a typo

keyfile = gunicorn_env.ssl_key
certfile = gunicorn_env.ssl_cert
ca_certs = gunicorn_env.ssl_chain
