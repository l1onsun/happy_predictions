# ToDo: migrate to postgres

from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


@dataclass
class PostgresStorage:
    engine: AsyncEngine

    @classmethod
    def from_postgres_uri(cls, postgres_uri: str, debug: bool):
        return cls(
            engine=create_async_engine(
                postgres_uri,
                echo=debug,
            )
        )
