import uvicorn
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}


@app.get("/api/v1/type-calculation/all")
async def all_type_calculation():
    """
    Получает все типы расчетов, доступные в системе.
    """
    pass


@app.get("/api/v1/type-calculation/{object_uid}")
async def type_calculation(
        object_uid: str = Query(..., description='Идентификатор объекта')
):
    """
    Получает тип расчета по идентификатору объекта (object_uid).
    """
    pass


@app.put('/api/v1/type-calculation/set/{object_uid}')
async def type_calculation_set(
        object_uid: str = Query(..., description='Идентификатор объекта'),
        type_value: str = Query(..., description='Значение типа расчета')
):
    """
    Устанавливает активный тип расчета для объекта по его идентификатору
    """
    pass



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


