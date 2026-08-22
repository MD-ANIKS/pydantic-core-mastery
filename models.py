from pydantic import BaseModel, Field, field_validator, model_validator, computed_field, ConfigDict, EmailStr, AnyUrl
from typing import Optional, Literal
from datetime import date

class Category(BaseModel): #pydantic Model
  name: Literal['starter', 'main course', 'desert', 'beverage']

#inherit
class Model(BaseModel): # For checking if the incoming data is valid or  not

  model_config = ConfigDict(
    extra= 'allow', # Extra Fields
    frozen = True, #Frozen Model
    strict= True, # Strict Pydantic Model
    validate_assignment= True # validate on Edit
  )

  #Field : value type
  id : int
  name : str = Field(..., min_length=3, max_length=50, description="Item Name") # required Field with rules and regulation
  price : float = Field(..., gt=0, description='Item Price') 
  category : Category = Field(..., description="Item Category") 
  is_available : bool = Field(default=True) # default value
  description : Optional[str] = None # optional field
  # email : EmailStr #valid email
  # url : AnyUrl -> valid URL
  # Date : date -> valid date format follow


  #field validator - worked only single field
  @field_validator('name')
  @classmethod # decorator passes the class (cls) instead of the instance (self)
  def title_name(cls,value):
    return value.title()

  # model validator - worked multiple field
  @model_validator(mode='after')
  def check_available(self):
    if self.is_available and self.price <= 0: 
       raise ValueError('Available item must have price greater than 0')
    return self

  #computed field - new field created
  @computed_field
  @property
  def price_tax(self) -> float:
    return round(self.price * 1.05, 2)

item = Model(id=2, name='Capacchino', price=20.5, category=Category(name='starter'), is_available=True)

print(item)

### IN-OUT SERIALIZATION

#this will work only inside of python
# model dump() -> object converted into dictionary
print('Dictionary model_dump()')
print(item.model_dump())

# model_dump_json() - object over the internet or the website, out of python
print('JSON model_dump_json()')
print(item.model_dump_json())