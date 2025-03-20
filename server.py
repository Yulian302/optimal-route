from fastapi import FastAPI
from routers.optimalroute import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://optimal-route-front.vercel.app",
                   "optimal-route-front.vercel.app", "localhost", "127.0.0.1"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/routes")


@app.get("/")
async def test():
    return {"message": "test"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000, host="127.0.0.1")
