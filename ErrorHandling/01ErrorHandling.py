# https://www.askpython.com/python/python-exception-handling  -->Documentation
a= int(input("a: "))
b=(input("b: "))

try:
    print(a+b)
    
except TypeError:
    print("You got TypeError")
    
finally:
    print("Enter Again")


