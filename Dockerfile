FROM python:3.10-slim AS python-base

ENV PYTHONUNBUFFERED 1
ENV PIP_CACHE_DIR=/root/.cache/pip
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV BUILDER_INSTALL_PREFIX=/install

WORKDIR /code/


FROM python-base as builder

RUN --mount=type=cache,target=${PIP_CACHE_DIR} pip install pip==22.0.4
COPY requirements.txt ./
RUN --mount=type=cache,target=${PIP_CACHE_DIR} pip install --prefix=${BUILDER_INSTALL_PREFIX} -r requirements.txt

FROM python-base as app

COPY --from=builder ${BUILDER_INSTALL_PREFIX} /usr/local

COPY app ./app

CMD ["uvicorn", "app.server.asgi:app", "--host", "0.0.0.0", "--port", "8080"]

FROM app as app-dev
COPY requirements-dev.txt ./