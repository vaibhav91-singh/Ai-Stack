# print("Hello vaibhav singh ")
# genewrator are used to reduce the memory use . 
# Generator ()

# dailysales = [12,34,54,654,76,546,45,3,4]
# total_cups=sum(sale for sale in dailysales )
# # print(total_cups)

# generator with yield keyword
# do not want resule immmeditely 
# lazy evaluation
# yield pause a function

# def server_chai():
#     yield "cup1: masala cahi"
#     yield "cup2: lemon chai"
    
# stall = server_chai()
# for cup in stall:
#     print(cup)

# print(next(stall))
# print(next(stall))

# print(next(stall)) ---> gives error because only have two value and you try to print three values

def infinte_chai():
    count= 1
    while True:
        yield f"Refile #{count}"
        count+=1
refile = infinte_chai()

for _ in range(5):
    print(next(refile))
    
# Profit or use of this generator function

user2 = infinte_chai()
for _  in range(6):
    print(next(user2))





