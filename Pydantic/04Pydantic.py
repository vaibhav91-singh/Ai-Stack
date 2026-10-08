# # pydantic Serialization
# from pydantic import BaseModel

# class Address(BaseModel):
#     streeet:str
#     city:str
#     zip_code:int
# class datetime(Basemodel):
#     hours:int
#     minutes:int
#     seconds:int

# class User(BaseModel):
#     id:int
#     name:str
#     email:str
#     is_Active:bool
#     createAt:datetime
#     address:Address
#     tags: list[str]=[]
# # old way 
#     model_config= ConfigDict(
#         json_encoders={datetime:lambda v:v.strftime("%H:%M:%S") }
#     )
# # 

# user = User(
#     id=1,
#     name="Vaibhav Singh",
    
#     email="Singhvaibhav849@gmial.com",
    
#     is_Active=True,
#     address= Address (
#         street= "Beta1",
#         city="Greater Noida",
#         zip_code=201310
#     ),
#     createdAt=datetime(2024,3,15,14,30),
#     tags =["premium User","Admin"]
# )
# print(user.model_dump_json())
# print(user.model_dump())

from pydantic import BaseModel, ConfigDict, field_serializer
from datetime import datetime

class Address(BaseModel):
    street: str  # Fixed typo
    city: str
    zip_code: int

class User(BaseModel):
    id: int
    name: str
    email: str
    is_Active: bool
    createdAt: datetime
    address: Address
    tags: list[str] = []

    # Modern V2 way to format the JSON output
    @field_serializer('createdAt')
    def serialize_dt(self, dt: datetime):
        return dt.strftime("%H:%M:%S")

user = User(
    id=1,
    name="Vaibhav Singh",
    email="Singhvaibhav849@gmial.com",
    is_Active=True,
    address=Address(street="Beta1", city="Greater Noida", zip_code=201310),
    createdAt=datetime(2024, 3, 15, 14, 30),
    tags=["premium User", "Admin"]
)

dict=(user.model_dump())
print(dict)
print("❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌")
print(user)
