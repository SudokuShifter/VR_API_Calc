from typing import Optional

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from dependencies.database.db_session import get_db
from dependencies.database.db_models import VRZifObjects, VRValidationData
from dependencies.database_pyd_schemas.VRZifObjects import VRZifObjectsPyd
from dependencies.database_pyd_schemas.VRValidationData import VRAdaptationDataPyd


class VRStorageService:

    @staticmethod
    async def get_object_by_uid(
            object_id: int,
            psql_session: AsyncSession = Depends(get_db)
    ) -> VRZifObjects:
        stmt = select(VRZifObjects).where(VRZifObjects.id == object_id)
        result = await psql_session.execute(stmt)
        db_obj = result.scalars().first()
        if db_obj:
            return VRZifObjectsPyd.from_orm(db_obj)
        raise HTTPException(status_code=404, detail="Object not found")


    @staticmethod
    async def find_validation_data_without_check(
            uid: str,
            psql_session: AsyncSession = Depends(get_db)
    ) -> Optional[VRAdaptationDataPyd]:
        stmt = select(VRValidationData).where(VRValidationData.uid == uid)
        result = await psql_session.execute(stmt)
        db_obj = result.scalars().all()
        if db_obj:
            print(db_obj)
            # Такой ответ ожидается от функции (тестировать нужно)
            # {
            #     "q_gas_timed": [
            #         9.25925925925926,
            #         10.185185185185185,
            #         11.11111111111111,
            #         12.037037037037036,
            #         12.962962962962962
            #     ],
            #     "q_gc_timed": [
            #         0.00011574074074074075,
            #         0.00012731481481481483,
            #         0.00013888888888888892,
            #         0.000150462962962963,
            #         0.0001620370370370371
            #     ],
            #     "q_wat_timed": [
            #         0.00011574074074074075,
            #         0.00012731481481481483,
            #         0.00013888888888888892,
            #         0.000150462962962963,
            #         0.0001620370370370371
            #     ]
            # }
            return VRAdaptationDataPyd.from_orm(db_obj)
        raise HTTPException(status_code=404, detail="Object not found")

