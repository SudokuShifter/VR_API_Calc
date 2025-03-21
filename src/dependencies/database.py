from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncEngine,
    async_scoped_session
)
from asyncio import current_task
import loguru

from containers.config_container import ConfigContainer
from config import PSQLConfig, load_psql_config


class DatabaseSessionManager:
    """
    Класс отвечающий за создание/удаление сессии и инициализацию базы данных
    """
    def __init__(self):
        self.engine: AsyncEngine | None = None
        self.session_marker = None
        self.session = None
        self._config = load_psql_config()


    def init_db(self):
        if self.engine is not None:
            raise Exception('Database already initialized')

        self.engine = create_async_engine(
            url=f'postgresql+asyncpg://{self._config.PSQL_USER}:{self._config.PSQL_PASS}'
                f'@{self._config.PSQL_HOST}:{self._config.PSQL_PORT}/{self._config.PSQL_DB}',
            pool_size=100, max_overflow=100, pool_pre_ping=True,
        )

        self.session_marker = async_sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

        self.session = async_scoped_session(
            self.session_marker, scopefunc=current_task
        )
        loguru.logger.success('Database initialized')


    async def close(self):
        if self.engine is None:
            raise Exception('DatabaseSessionManager has not been initialized')
        await self.session.remove()
        await self.engine.dispose()


session_manager = DatabaseSessionManager()
