from pydantic import BaseModel
class UserProfile(BaseModel):
    name: str
    age:int
    email:str
user= UserProfile(name="Vaibhav Singh",age=21,email="Singhvaibhav849@gmial.com")
user2 = UserProfile(name="Vaibhav Singh",age="25",email="Singhvaibhav849@gmial.com")
print(user)
print(user2)
print(type(user2.age)) #pydantic converted age(string) in to int
print(user.model_dump()) #pydantic converted in to JSON

'''
Explaination of code

## 1. Defining the Schema (`BaseModel`)

By inheriting from `BaseModel`, you are telling Python that `UserProfile` isn't just a container—it’s a **validator**.

* **Type Hints:** You’ve explicitly defined that `name` and `email` must be strings (`str`) and `age` must be an integer (`int`).
* **Automatic Validation:** If you tried to pass `age="forty"` (a string) instead of `40` (an int), Pydantic would raise a clear error before the rest of your code even runs.

## 2. Creating the Instance

```python
user = UserProfile(name="Liam Svensson", age=40, email="liam.svensson@example.com")

```

When you run this line, Pydantic performs a "behind-the-scenes" check. It verifies that the arguments you provided match the types defined in the class. If everything looks good, it creates a `user` object.

## 3. The Output (`print`)

When you `print(user)`, Pydantic provides a clean, readable string representation (technically a `__repr__`) rather than a messy memory address like `<__main__.UserProfile object at 0x...内容>`.

**Your output will look like this:**
`name='Liam Svensson' age=40 email='liam.svensson@example.com'`

---

### Why use this over a normal class?

* **Data Parsing:** Pydantic is smart. If you passed `age="40"` (as a string), it would automatically convert it to the integer `40` for you.
* **JSON Integration:** You can easily turn this object into a dictionary using `user.model_dump()` or into a JSON string using `user.model_dump_json()`.

'''