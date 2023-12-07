import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.scanners import scan_router

app = FastAPI()
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def welcome():
    return {"message": "Welcome to my FastAPI application!"}


app.include_router(scan_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8800)
