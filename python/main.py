import asyncio

from fastapi import FastAPI

from request_coalesce.config import RequestCoalescer

app = FastAPI()

coalescer = RequestCoalescer()


# Simulate a slow database call
async def fake_database_query():
    print("-> HIT THE DATABASE (This should only happen once!)")
    await asyncio.sleep(2)
    return {"status": "success", "data": "Valuable User Data"}


@app.get("/profile/{user_id}")
async def get_user_profile(user_id: str):
    data = await coalescer.execute(user_id, fake_database_query)
    return {"user_id": user_id, "payload": data}
