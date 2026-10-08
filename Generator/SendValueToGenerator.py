print(" IN THIS PART OF CODE YOU LEARN ABOUT THE GENERATOR ")
# we use yield in generator ---- IMPORTANT LINE 

def chai_customer():
    print("Welcome , what type of chai you need")
    order = yield
    while True:
        print(f"Preparing your order : {order}: ")
        order = yield
stall = chai_customer()
next(stall) #start the Generator
# my budhi
# yourorder= input("Enter your chai type : ")
# stall.send(yourorder)

stall.send("Lemon chai")
stall.send("Masala chai")