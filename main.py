from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from bson.objectid import ObjectId

app = FastAPI() #instance of FastAPI

Client = MongoClient("mongodb://localhost:27017/")
db =  Client["TestDB"]
collection = db["TestCollection"]

class TestDB(BaseModel):
    name:str
    age:int


@app.get("/")
async def root():
    return {"message": "Hello World"}

#Creat
@app.post("/Test")
async def create(testdb:TestDB): #รับ parameter 
    result = collection.insert_one(testdb.dict())
    return {
        "id": str(result.inserted_id),
        "name": testdb.name,
        "age": testdb.age
    }
#Read
@app.get("/Test/{Test_id}")
async def read(Test_id:str):
    TestDB = collection.find_one({"_id": ObjectId(Test_id)})
    if TestDB:
        return {"id":str(TestDB["_id"]), "name" : TestDB["name"], "age": TestDB["age"]}
    else:
        raise HTTPException(status_code=404, detail="Not Found")
    
#Update 
@app.put("/Test/{Test_id}")
async def update(Test_id:str, TestDB:TestDB):
    result = collection.update_one(
        {"_id":ObjectId(Test_id)}, {"$set": TestDB.dict(exclude_unset=True)}
    )
    if result.modified_count == 1:
        return{"id":Test_id, "name": TestDB.name, "age":TestDB.age}
    else:
        raise HTTPException(status_code=404, detail="Not Found")

#Delete
@app.delete("/Test/{Test_id}")
async def delete(Test_id:str,TestDB:TestDB):
    result = collection.delete_one(
        {"_id":ObjectId(Test_id)}
    )

    if result.deleted_count ==1:
        return{"id":Test_id, "name": TestDB.name, "age": TestDB.age}
    else:
        raise HTTPException(status_code=404,detail="Not Found")
