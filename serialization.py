from pydantic import BaseModel

class Address(BaseModel):

    city: str
    state: str
    pin: str

class Patient(BaseModel):

    name: str
    gender: str
    age: int
    address: Address

address_dict = {'city': 'gurgaon', 'state': 'haryana', 'pin': '122001'}

address1 = Address(**address_dict)

patient_dict = {'name': 'nitish', 'gender': 'male', 'age': 35, 'address': address1}

patient1 = Patient(**patient_dict)


# serilization means exporting pydantic objects as json or dict
temp=patient1.model_dump()# export as dict
temp2=patient1.model_dump_json()# as json
# we also have include paramter which doexnt expore whole object as json just included fields
# we have excluded parameter which exclude some fields from pydantic object and export all other
print(temp)
print(temp2)























# Better organization of related data (e.g., vitals, address, insurance)

# Reusability: Use Vitals in multiple models (e.g., Patient, MedicalRecord)

# Readability: Easier for developers and API consumers to understand

# Validation: Nested models are validated automatically—no extra work needed