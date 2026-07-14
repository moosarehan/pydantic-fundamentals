from pydantic import BaseModel,EmailStr,AnyUrl,Field
from typing import List,Dict,Optional,Annotated
# pydantic model
class Patient(BaseModel):
    name:Annotated[str,Field(max_length=30,description='name of patient',examples=['musa','tyab'])]
    age:Annotated[int,Field(default=0,gt=0,strict=True)]
    email:EmailStr
    linkedin:AnyUrl
    married:Optional[bool]=True  # optional field
    allergies:Annotated[Optional[List[str]],Field(default=None,max_length=10)]
    contact:Dict[str,str]
    weight:Optional[float]=Field(default=0.0,gt=2.0)
    

def insert(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.married)

dict={'name':'moosa','age':45,'email':'moosa@gmail.com','linkedin':'http://linkedin.com/123','married':True,'allergies':['pollen','malaria'],'contact':{'phone':'10282'}}
patient1=Patient(**dict)
insert(patient1)
#patient 1 is auto validated object

