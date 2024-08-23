from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI backend!"}


@app.get("/health")
def health_check():
    return {"status": "Healthy"}


@app.get("/test")
def test_connection():
    return {"message": "Connection to FastAPI backend is successful!"}
