# Validators for Entire Model

from pydantic import BaseModel , model_validator

class UserProfile(BaseModel):
    password:str
    confirm_password:str
    
    @model_validator(mode='after')
    def password_match(cls,model):
        if(model.password!=model.confirm_password):
            raise ValueError("Password do not match")
        return model
UserProfile(password="Vaibhav@123",confirm_password="Vaibhav@123")



'''
Individual Field Check: It first ensures both password and confirm_password are strings.
The Validator Trigger: Because you set mode='after', Pydantic waits until the object is built and then hands the whole model to your password_match function.
The Comparison: * If model.password == model.confirm_password, the function returns the model, and everything is fine.
If they differ, it raises a ValueError, which Pydantic wraps into a formal ValidationError.

'''

