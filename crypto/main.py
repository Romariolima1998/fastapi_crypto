from fastapi import FastAPI

from crypto.routers.views import user_router, assets_router


app = FastAPI()

app.include_router(user_router)
app.include_router(assets_router)

@app.get('/')
def first():
    return {"hello":  "world"}