from fastapi import FastAPI

from api.routers import task, done

app = FastAPI()

# ▽Hello world
# @app.get("/hello")
# def hello():
#     return {"message": "hello world!"}

# ルーターからパスオペレーション関数（？）をインクルード
app.include_router(task.router)
app.include_router(done.router)
