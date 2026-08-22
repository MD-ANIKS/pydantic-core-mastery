# Pydantic Core Mastery 

A structured, hands-on reference guide for mastering data validation, structural parsing, and type safety using **Pydantic v2** in Python. This repository is built as a complete cheat sheet covering foundational concepts through advanced runtime configurations.

##  Core Concepts Covered

*   **Runtime Type Validation & Coercion:** Explicit control over required vs. optional fields.
*   **Advanced Model Configuration (`ConfigDict`):** Freezing instances, handling untyped extra parameters, and enabling real-time edit validations.
*   **Data Transformation Rules:** Injecting single-field adjustments via `@field_validator`.
*   **Multi-Field Dependencies:** Designing structural business constraints with `@model_validator`.
*   **Dynamic Attribute Generation:** Using `@computed_field` to calculate runtime parameters safely.
*   **In-Out Serialization:** Seamless exports into localized environments (`.model_dump()`) or web protocols (`.model_dump_json()`).

---

## Technical Reference Code

The main reference script compiles these features into a production-ready data schema:

```python
from pydantic import BaseModel, Field, field_validator, model_validator, computed_field, ConfigDict
from typing import Optional, Literal

class Category(BaseModel):
    name: Literal['starter', 'main course', 'desert', 'beverage']

class Model(BaseModel):
    # Advanced Pydantic Engine Configuration
    model_config = ConfigDict(
        extra='allow',               # Permits incoming unregistered arguments
        frozen=True,                 # Immutability configuration
        strict=True,                 # Strictly enforces declared data types
        validate_assignment=True     # Validates new updates dynamically
    )

    # Core Attributes with Custom Rules
    id: int
    name: str = Field(..., min_length=3, max_length=50, description="Item Name")
    price: float = Field(..., gt=0, description='Item Price') 
    category: Category = Field(..., description="Item Category") 
    is_available: bool = Field(default=True) 
    description: Optional[str] = None 

    # Field Validator (Runs at structural class level)
    @field_validator('name')
    @classmethod
    def title_name(cls, value: str) -> str:
        return value.title()

    # Model Validator (Runs cross-field checking)
    @model_validator(mode='after')
    def check_available(self):
        if self.is_available and self.price <= 0: 
            raise ValueError('Available item must have price greater than 0')
        return self

    # Computed Property (Creates data attributes on the fly)
    @computed_field
    @property
    def price_tax(self) -> float:
        return round(self.price * 1.05, 2)
```

---

##  How to Set Up and Run

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd pydantic-core-mastery
   ```

2. **Install Pydantic:**
   ```bash
   pip install pydantic
   ```

3. **Execute the Reference Script:**
   ```bash
   python your_script_name.py
   ```

