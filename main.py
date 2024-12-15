from wsMainProcess import getData, wsProcess
from fastapi import FastAPI

app = FastAPI()

@app.get("/begin/{query}")
def initRead(query: str = None):
    try:
        wsProcess(query)
        return {"message": "Done", "query": query}
    except Exception as error:
        return {"message": error, "query": query}

@app.get("/")
async def readAllItems():
    try:
        result = getData()
        return {'Data': result}
    except Exception as error:
        return {"message": error}
    
    

