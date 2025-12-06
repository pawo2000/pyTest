from testsrv.pworker import PWorker
from fastapi import FastAPI

p1 = PWorker("localhost");
p1.start();

app = FastAPI()

import redis
r = redis.Redis(host='redis', port=6379)

#import debugpy
#debugpy.listen(("0.0.0.0", 5678))
# #debugpy.wait_for_client()

@app.get("/")
def read_root():
    return {"Hello": "World1234567890!!ss!"}

@app.get("/hits")
def read_root():
    r.incr("hits")
    return {"Number of hits": r.get("hits")}

@app.get("/add/{address}")
async def read_item(address: str):
    if(address == ""):
        return {"No address provided"}
    p = PWorker(address);
    p.start();
    return {"Thread started"}