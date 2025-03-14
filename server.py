from fastapi import FastAPI
from routers.optimalroute import router
import uvicorn

app = FastAPI()

app.include_router(router, prefix="/routes")


@app.get("/")
async def test():
    return {"message": "test"}
