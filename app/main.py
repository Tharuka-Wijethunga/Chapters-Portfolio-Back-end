from fastapi import FastAPI
from routers.feedback import feedback

app = FastAPI()

app.include_router(feedback)


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
