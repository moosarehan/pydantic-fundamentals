from pydantic import BaseModel,EmailStr,AnyUrl,Field,model_validator
from typing import List,Dict,Optional,Annotated
# pydantic model
class Patient(BaseModel):
   name:str
   age:int
   email:EmailStr
   married:bool
   allergies:List[str]
   contact:Dict[str,str]



   @model_validator(mode='after')
   def validate(self,model):
       if self.age > 60 and 'emergency' not in self.contact:
           raise ValueError('patients above 60 must have emergency contact')
       return self

   
   

   


def insert(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.married)

dict={'name':'moosa','age':'70','email':'moosa@mbp.com','married':True,'allergies':['pollen','malaria'],'contact':{'phone':'10282','emergency':'032182726'}}
patient1=Patient(**dict)
insert(patient1)


