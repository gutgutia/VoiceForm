from fastapi import FastAPI
from app import get_response

app = FastAPI()


@app.get("/")
async def get_response_api(user_input: str):
    response = get_response(user_input)
    print(response)
    return {"response": response}
