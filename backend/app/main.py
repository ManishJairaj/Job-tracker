from fastapi import FastAPI
from .routers import users
# models.Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="AI Job Tracker API",
    version="1.0.0"
)
app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "Hello World hiiii"}

@app.get("/health")
async def check_status():
    return {"status" : "Healthy"}
