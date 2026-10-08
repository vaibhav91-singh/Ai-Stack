# decortation 
#  when function run and  you pass values to the 
#  we pass function to the decrotor 

# def mydecorator(# here we pass which thingis aklso a function)
# --------------------------------------------------------------------
from functools import wraps
def mydecorator(func):
    @wrap(func)
    def wrapper():
        print(" Before the funtion run")
        func()
        print("After the functino run")
    return wrapper
@mydecorator
def greet():
    print(" Hello  from decorator class vaibhva singh ")
# funtion calling 
greet()
print(greet.__name__) 




# ------------------------------------------------------
# def hello(func):                                                                                            
#     def inner():                                                                                            
#         print("Hello ")                                                                                     
#         func()                                                                                              
#     return inner                                                                                            
                                                                                                            
# def name():                                                                                                 
#     print("Alice")                                                                                          
                                                                                                            
                                                                                                            
# obj = hello(name)                                                                                           
# obj()  
# ------------------------------------------------------
