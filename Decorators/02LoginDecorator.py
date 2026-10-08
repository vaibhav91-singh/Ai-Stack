from functools import wraps

def log_activity(func):
    @wraps(func)
    def wrapper(*args , **kwargs):
        
        result == func(*args,**kwargs)
        return result
    