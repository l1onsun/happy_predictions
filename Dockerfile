FROM python:3.10-alpine AS python-base
ENV PYTHONUNBUFFERED 1

WORKDIR /code/


FROM python-base as python-install
ENV PIP_CACHE_DIR=/root/.cache/pip
ENV PIP_DISABLE_PIP_VERSION_CHECK 1

RUN --mount=type=cache,target=${PIP_CACHE_DIR} pip install pip==22.0.4
COPY requirements.txt ./
RUN --mount=type=cache,target=${PIP_CACHE_DIR} pip install --prefix=/install -r requirements.txt

FROM python-base as python-app

COPY --from=python-install /install /usr/local

COPY app ./app

CMD ["uvicorn", "app.server.asgi:app", "--host", "0.0.0.0", "--port", "8443"]

