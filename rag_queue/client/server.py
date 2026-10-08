from fastapi import FastAPI

app = FASTAPI()

@app.get('/')
def root():
    return {"status" : ' Server Is Up and Running'}