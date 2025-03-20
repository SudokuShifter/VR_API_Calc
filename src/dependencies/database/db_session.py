from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.database.database import session_manager


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Функция get_db возвращает асинхронный генератор.
    Этот генератор можно использовать для получения объектов типа AsyncSession.
    """
    session = session_manager.session()
    if session is None:
        raise Exception('DatabaseSessionManager has not been initialized')
    try:
        yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()