<div align="center">

# 🐍 Pydantic Fundamentals

> A complete guide to data validation, type checking, and serialization in Python using Pydantic — the backbone of FastAPI and modern ML pipelines.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-V2-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Ready-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Status](https://img.shields.io/badge/Status-Learning-F5A623?style=for-the-badge)

</div>

---

## 📚 Table of Contents

| # | Topic |
|---|-------|
| 1 | [What is Pydantic?](#-what-is-pydantic) |
| 2 | [Step 1 — Pydantic Model (Blueprint)](#-step-1--pydantic-model-blueprint) |
| 3 | [Step 2 — Creating an Instance](#-step-2--creating-an-instance) |
| 4 | [Step 3 — Using the Validated Object](#-step-3--using-the-validated-object) |
| 5 | [Required vs Optional Fields](#-required-vs-optional-fields) |
| 6 | [Type Checking & Double Validation](#-type-checking--double-validation) |
| 7 | [Custom Data Types](#-custom-data-types) |
| 8 | [Field Function — 4 Use Cases](#-field-function--4-use-cases) |
| 9 | [Field Validator](#-field-validator) |
| 10 | [Model Validator](#-model-validator) |
| 11 | [Computed Field](#-computed-field) |
| 12 | [Nested Models](#-nested-models) |
| 13 | [Serialization](#-serialization) |
| 14 | [Summary](#-summary) |

---

## 🤔 What is Pydantic?

Without Pydantic, Python requires manual type checking and validation everywhere:

```python
# WITHOUT Pydantic — messy, repetitive, violates DRY
def create_patient(data: dict):
    if "name" not in data:
        raise ValueError("name is required")
    if not isinstance(data["age"], int):
        raise TypeError("age must be int")
    if data["age"] <= 0:
        raise ValueError("age must be positive")
    # 50 more lines...
```

Pydantic solves this by letting you define a **blueprint once** and reuse it everywhere — with automatic type checking, validation, and error handling built in.

```
Manual Python          Pydantic
──────────────         ────────────────────────────
type() everywhere  →   age: int          (automatic)
if/else validation →   Field(gt=0)       (one line)
scattered checks   →   one model class   (organized)
repeat every func  →   write once        (reusable)
```

---

## 🏗️ Step 1 — Pydantic Model (Blueprint)

A Pydantic model is a class that inherits from `BaseModel`. It defines the **shape and rules** of your data — written once, reused everywhere.

```
┌─────────────────────────────────┐
│        Patient (Blueprint)      │
├─────────────────────────────────┤
│  name   : str                   │
│  age    : int                   │
│  height : float                 │
│  weight : float                 │
└─────────────────────────────────┘
```

```python
from pydantic import BaseModel

class Patient(BaseModel):
    name:   str
    age:    int
    height: float
    weight: float
```

---

## ⚙️ Step 2 — Creating an Instance

When you create an instance, Pydantic **automatically validates** all fields. If validation fails, it raises a clear error immediately.

```
Client Data Comes In
        │
        ▼
┌───────────────────┐
│  Pydantic checks  │
│  ✅ types correct? │
│  ✅ required present?│
│  ✅ rules passed? │
└───────────────────┘
        │
   ┌────┴────┐
   ▼         ▼
PASS ✅    FAIL ❌
object    ValidationError
created   raised immediately
```

```python
# Valid data — works fine
patient = Patient(name="Ananya Sharma", age=28, height=1.65, weight=90.0)

# Invalid data — Pydantic raises ValidationError automatically
patient = Patient(name="Ananya", age="not_a_number", height=1.65, weight=90.0)
# ValidationError: age must be an integer
```

---

## 🚀 Step 3 — Using the Validated Object

Once created, the object is fully validated and safe to use — pass it to functions, store in DB, return as API response.

```
Validated Patient Object
        │
   ┌────┼────────────┐
   ▼    ▼            ▼
save  calculate   return as
to DB   BMI      API response
```

```python
def save_to_db(patient: Patient):
    db.insert(patient.model_dump())  # guaranteed clean data

def calculate_bmi(patient: Patient):
    return patient.weight / (patient.height ** 2)
```

---

## 🔘 Required vs Optional Fields

```python
from pydantic import BaseModel
from typing import Optional

class Patient(BaseModel):

    # REQUIRED — must be provided, no default
    name: str
    age:  int

    # OPTIONAL — with a meaningful default value
    city: str = "Unknown"

    # OPTIONAL — no value (None)
    email: Optional[str] = None
```

```
┌─────────────────┬──────────────────────┬───────────────────────────┐
│ Type            │ Syntax               │ Behaviour                 │
├─────────────────┼──────────────────────┼───────────────────────────┤
│ Required        │ name: str            │ must be provided          │
│ Default value   │ city: str = "Unknown"│ uses fallback if missing  │
│ Optional (None) │ Optional[str] = None │ fine to omit, becomes None│
└─────────────────┴──────────────────────┴───────────────────────────┘
```

---

## 🔍 Type Checking & Double Validation

Pydantic supports complex nested types from Python's `typing` module, giving you **two layers of validation** in one line.

```
List[str]
  │
  ├── Layer 1: is it a list?       ✅ or ❌
  └── Layer 2: is every item str?  ✅ or ❌

Dict[str, float]
  │
  ├── Layer 1: is it a dict?       ✅ or ❌
  ├── Layer 2: are keys strings?   ✅ or ❌
  └── Layer 3: are values floats?  ✅ or ❌
```

```python
from pydantic import BaseModel
from typing import List, Dict, Optional

class Patient(BaseModel):

    # List of strings — validates:
    # 1. is it a list?
    # 2. is every item a string?
    allergies: List[str]

    # Dict with typed keys and values
    vitals: Dict[str, float]

    # Optional list — can be None or a list of strings
    medications: Optional[List[str]] = None
```

```python
# Valid
patient = Patient(
    allergies  = ["penicillin", "dust"],
    vitals     = {"bp": 120.0, "sugar": 98.5},
    medications= ["Paracetamol"]
)

# Invalid — Pydantic catches it
patient = Patient(
    allergies = ["penicillin", 123],  # 123 is not a string
    vitals    = {"bp": "high"}        # "high" is not a float
)
```

---

## 🏷️ Custom Data Types

Pydantic provides built-in types that handle **90% of common use cases** automatically — no code needed.

```python
from pydantic import BaseModel, EmailStr, AnyUrl

class Patient(BaseModel):
    email:   EmailStr  # must be valid email format (has @, has domain)
    website: AnyUrl    # must be valid URL (has http/https, valid format)
```

```
┌───────────────────┬────────────────────────────────────┐
│ Type              │ Validates                          │
├───────────────────┼────────────────────────────────────┤
│ EmailStr          │ @ symbol, domain, format           │
│ AnyUrl            │ http/https, proper URL structure   │
│ HttpUrl           │ must specifically be http or https │
│ IPvAnyAddress     │ IP address format                  │
└───────────────────┴────────────────────────────────────┘

No code needed — just declare the type ✅
```

---

## 🛠️ Field Function — 4 Use Cases

`Field()` is used for more control over individual fields. It has 4 main use cases:

### 1️⃣ Attaching Metadata (with Annotated)

```python
from pydantic import BaseModel, Field
from typing import Annotated

class Patient(BaseModel):
    age: Annotated[int, Field(
        description = "Age of the patient in years",
        example     = 28,
        title       = "Patient Age"
    )]
```

### 2️⃣ Custom Validation (simple rules)

```python
class Patient(BaseModel):
    age:    int   = Field(gt=0, lt=120)   # 0 < age < 120
    height: float = Field(gt=0)           # must be positive
    weight: float = Field(gt=0, le=500)   # 0 < weight <= 500

# Common validators:
# gt  = greater than
# ge  = greater than or equal
# lt  = less than
# le  = less than or equal
# min_length, max_length  = for strings
```

### 3️⃣ Preventing Type Coercion (strict mode)

```python
class Patient(BaseModel):
    age: int = Field(strict=True)  # "28" will NOT be converted to 28
                                   # must be exactly int, no coercion
```

```
Without strict:  age = "28"  →  Pydantic converts to 28  ✅
With strict:     age = "28"  →  ValidationError ❌ must be int
```

### 4️⃣ Providing Default Values

```python
class Patient(BaseModel):
    city:   str           = Field(default="Unknown")
    status: Optional[str] = Field(default=None)

    # With Annotated for optional + metadata
    notes: Annotated[Optional[str], Field(
        default     = None,
        description = "Additional patient notes"
    )]
```

---

## 🔬 Field Validator

Used when `Field()` is not enough — complex business logic validation on a **single field**.

```
Raw value from client
        │
        ▼
  mode="before"          ← you get raw value here
        │                   e.g. "28" (string)
        ▼
Pydantic type coercion
"28" → 28 (int)
        │
        ▼
  mode="after"           ← you get coerced value here
        │                   e.g. 28 (int)
        ▼
Field is set on model
```

```python
from pydantic import BaseModel, field_validator

class Patient(BaseModel):
    name:  str
    email: str

    # Runs BEFORE type coercion — gets raw value from client
    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, value):
        if any(char.isdigit() for char in value):
            raise ValueError("name must not contain numbers")
        return value.strip().title()

    # Runs AFTER type coercion — gets clean converted value
    @field_validator("email", mode="after")
    @classmethod
    def validate_email(cls, value):
        if not value.endswith("@nu.edu.pk"):
            raise ValueError("must be a university email @nu.edu.pk")
        return value
```

```
mode="before"  →  raw value from client   (string, int, anything)
mode="after"   →  coerced value           (guaranteed correct type)

Use before  →  when you need to clean/transform raw input first
Use after   →  when you need to validate the final typed value
```

```
┌─────────────────────────────────────────────────┐
│          Field()   vs   @field_validator         │
├──────────────────────┬──────────────────────────┤
│ simple rules         │ complex business logic   │
│ (gt, lt, min_length) │                          │
├──────────────────────┼──────────────────────────┤
│ one liner            │ needs a function         │
├──────────────────────┼──────────────────────────┤
│ no custom code       │ custom code required     │
└──────────────────────┴──────────────────────────┘
```

---

## 🧩 Model Validator

Used when validation **depends on two or more fields together**. Field() and field_validator only work on one field at a time.

```
                    ┌──────────────┐
                    │   Patient    │
                    │  age = 65    │
                    │  emergency   │
                    │  = None      │
                    └──────┬───────┘
                           │
              @model_validator sees ALL fields
                           │
              if age > 60 AND emergency is None
                           │
                      ❌ raise Error
```

```python
from pydantic import BaseModel, model_validator

class Patient(BaseModel):
    weight:          float
    height:          float
    emergency_contact: Optional[str] = None
    age:             int

    # mode="after" — instance method, use self
    @model_validator(mode="after")
    def validate_patient(self):

        # validation using TWO fields together
        if self.age > 60 and not self.emergency_contact:
            raise ValueError("patients over 60 must have an emergency contact")

        # another cross-field validation
        if self.weight <= 0 or self.height <= 0:
            raise ValueError("weight and height must both be positive")

        return self
```

```
┌─────────────────┬────────────────────┬───────────────────┐
│                 │  @field_validator  │  @model_validator │
├─────────────────┼────────────────────┼───────────────────┤
│ fields involved │        1           │        2+         │
│ complexity      │     complex        │       any         │
│ cross-field     │        ❌          │        ✅         │
│ use case        │  business logic    │  combined fields  │
└─────────────────┴────────────────────┴───────────────────┘
```

---

## 🧮 Computed Field

A field that is **automatically calculated** from other fields. The client never sends it — Pydantic computes it for you.

```
Client sends:
{ height: 1.65, weight: 90.0 }
          │
          ▼
┌─────────────────────────┐
│  @computed_field        │
│  bmi = weight / height² │  ← auto calculated
│  verdict = "Obese"      │  ← auto calculated
└─────────────────────────┘
          │
          ▼
{ height: 1.65, weight: 90.0, bmi: 33.06, verdict: "Obese" }
```

```python
from pydantic import BaseModel, computed_field

class Patient(BaseModel):
    name:   str
    height: float   # client sends
    weight: float   # client sends

    @computed_field
    @property
    def bmi(self) -> float:        # client does NOT send this
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:   return "Underweight"
        elif self.bmi < 25:   return "Normal"
        elif self.bmi < 30:   return "Overweight"
        else:                 return "Obese"


patient = Patient(name="Ananya", height=1.65, weight=90.0)
print(patient.bmi)      # 33.06  — auto calculated
print(patient.verdict)  # Obese  — auto calculated
```

```
┌──────────────────┬──────────────────────────────────────────┐
│ Regular field    │ client sends it                          │
│ Computed field   │ Pydantic calculates from other fields ✅ │
└──────────────────┴──────────────────────────────────────────┘
```

---

## 🪆 Nested Models

When a field is itself a Pydantic model — used for structured/complex data like addresses, vitals, etc.

```python
from pydantic import BaseModel

class Address(BaseModel):
    city:    str
    zip:     str
    country: str

class Patient(BaseModel):
    name:    str
    age:     int
    address: Address   # nested model
```

**The validation flow:**

```
Step 1 — Address validated FIRST
┌─────────────────────────────────────────┐
│  Address(city="Mumbai", zip="400001")   │
│  ✅ city is str                         │
│  ✅ zip is str                          │
│  ✅ country is str                      │
│  Address object READY                   │
└─────────────────────────────────────────┘
                  │
                  ▼
Step 2 — Patient validated
┌─────────────────────────────────────────┐
│  Patient(name="Ananya", age=28,         │
│          address=address_obj)           │
│  ✅ name is str                         │
│  ✅ age is int                          │
│  ✅ address is type Address?            │
│     YES → already validated, skip ✅   │
└─────────────────────────────────────────┘
                  │
                  ▼
Step 3 — Store in MongoDB
patient.model_dump() → converts to dict

{
    "name": "Ananya",
    "age":  28,
    "address": {          ← nested document
        "city":    "Mumbai",
        "zip":     "400001",
        "country": "India"
    }
}
```

---

## 📤 Serialization

Exporting your Pydantic object as a Python dict or JSON string for storing in a database or returning as an API response.

```
Pydantic Object
      │
      ├── .model_dump()       →  Python dict  (DB insert, function passing)
      └── .model_dump_json()  →  JSON string  (API response, file storage)
```

```python
patient = Patient(name="Ananya", age=28, height=1.65, weight=90.0)

# Export as Python dict
patient.model_dump()
# {
#     "name":   "Ananya",
#     "age":    28,
#     "height": 1.65,
#     "weight": 90.0,
#     "bmi":    33.06
# }

# Export as JSON string
patient.model_dump_json()
# '{"name":"Ananya","age":28,"height":1.65,"weight":90.0,"bmi":33.06}'

# Exclude fields
patient.model_dump(exclude={"height", "weight"})

# Include only specific fields
patient.model_dump(include={"name", "age", "bmi"})

# Exclude fields that are None
patient.model_dump(exclude_none=True)
```

```
┌────────────────────┬────────────────┬───────────────────────────┐
│ Method             │ Returns        │ Use case                  │
├────────────────────┼────────────────┼───────────────────────────┤
│ model_dump()       │ Python dict    │ DB storage, passing data  │
│ model_dump_json()  │ JSON string    │ API response, file save   │
└────────────────────┴────────────────┴───────────────────────────┘
```

---

## 📊 Summary

```
┌──────────────────┬──────────────────────────────┬─────────────────────────┐
│ Feature          │ Purpose                      │ When to use             │
├──────────────────┼──────────────────────────────┼─────────────────────────┤
│ BaseModel        │ blueprint for data shape     │ always, foundation      │
│ Required fields  │ must be provided             │ critical data           │
│ Optional fields  │ can be omitted               │ non-critical data       │
│ Type hints       │ automatic type checking      │ always                  │
│ List[str], Dict  │ double/nested type validation│ collections             │
│ EmailStr, AnyUrl │ built-in complex types       │ email, url fields       │
│ Field(gt=0)      │ simple validation + metadata │ rules on one field      │
│ @field_validator │ complex logic on one field   │ business rules          │
│ @model_validator │ logic across multiple fields │ cross-field rules       │
│ @computed_field  │ auto-calculated fields       │ bmi, totals, etc        │
│ Nested models    │ structured/object fields     │ address, vitals         │
│ model_dump()     │ export as dict               │ DB storage              │
│ model_dump_json()│ export as JSON               │ API responses           │
└──────────────────┴──────────────────────────────┴─────────────────────────┘
```

---

<div align="center">

> **⚡ Next Step:** Apply all of these Pydantic concepts inside FastAPI — use models for request body validation, `Field()` for API docs metadata, and serialization for clean JSON responses.

![Made with Love](https://img.shields.io/badge/Made%20with-❤️-red?style=for-the-badge)
![Pydantic](https://img.shields.io/badge/Powered%20by-Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white)

</div>
