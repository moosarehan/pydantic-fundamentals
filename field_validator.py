from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator
from typing import List,Dict,Optional,Annotated
# pydantic model
class Patient(BaseModel):
   name:str
   age:int
   email:EmailStr
   married:bool
   allergies:List[str]
   contact:Dict[str,str]


   @field_validator('email')
   @classmethod
   def email_validate(cls,value):
       valid_domain=['hdfc.com','mbp.com']
       domain=value.split('@')[-1]
       if domain not in valid_domain:
           raise ValueError('not valid domain')
       return value
   

   @field_validator('name')
   @classmethod
   def transform(cls,value):
       return value.upper()
   

   @field_validator('age',mode='after')
   @classmethod
   def range(cls,value):
       if value >0 and value <100 :
           return value
       raise ValueError('invalid value ')


def insert(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.married)

dict={'name':'moosa','age':'45','email':'moosa@mbp.com','married':True,'allergies':['pollen','malaria'],'contact':{'phone':'10282'}}
patient1=Patient(**dict)
insert(patient1)


