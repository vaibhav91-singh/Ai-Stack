from pydantic import BaseModel , field_validator

class UserProfile(BaseModel):
    name:str
    age:int
    email:str

    @field_validator('age')
    def check_age(cls,value):
        if(value>18):
            return value
        else:
            raise ValueError('Age must be greater than 18') 
UserProfile(name="Vaibhav Singh",age=32,email="Singhvaibhav849@gmial.com")

#Explaination of code
'''
## 1. The `@field_validator` Decorator

Think of this as a "security guard" standing specifically at the `age` gate.

* **`@field_validator('age')`**: This tells Pydantic, "Before you finish creating the object, run this specific function on the `age` field."
* **The Parameters**:
* `cls`: Refers to the class (`UserProfile`).
* `value`: This is the actual data someone tried to input (in your case, `32`).

6
## 2. The Logic Flow

When you call `UserProfile(name="Vaibhav Singh", age=32, ...)`:

1. **Type Check**: Pydantic sees `32` is an integer. Success.
2. **Validator Trigger**: It sees you have a `check_age` function.
3. **The If/Else**:
* If the age is **greater than 18**, the function `return value`. This "approves" the data.
* If the age is **18 or less**, it `raise ValueError`. Pydantic catches this and turns it into a clean error message for the user.



---

## 3. What happens with your specific input?

Since you provided `age=32`:

*  is **True**.
* The validator returns `32`.
* The object is created successfully.

If you had typed `age=15`, the code would crash with a `ValidationError` saying: `Value error, Age must be greater than 18`.

---

## A Few Pro-Tips for your Code

### The "Inclusive" Catch

In your current code, if someone is exactly **18**, they will get an error because you used `value > 18`. If you want to include 18-year-olds, you should use:

```python
if value >= 18:
    return value

```

### Simpler Way (Annotated)

For simple checks like "greater than 18," Pydantic actually has a shortcut that doesn't require a whole function:

```python
from pydantic import BaseModel, Field

class UserProfile(BaseModel):
    name: str
    age: int = Field(gt=18) # "gt" stands for Greater Than
    email: str

```

**Would you like me to show you how to handle the error in a `try/except` block so your program doesn't crash when an invalid age is entered?**
'''