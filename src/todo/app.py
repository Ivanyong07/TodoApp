from fastapi import FastAPI

app = FastAPI()

@app.get("/show")
def show_posts() -> dict:
    return {"message": "Hello World"}

if __name__ == "___main__":
    uvicorn.run("todo.app:app", host="0.0.0.0", port=8000, reload=True)