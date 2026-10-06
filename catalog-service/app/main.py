from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def main():
    return {"message": "Welcome to Category-Service", "docs": "/docs"}

@app.get("/health")
async def health():
    return {"status": "200"}

