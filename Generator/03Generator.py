
# Topic Is -----
# yield from and close them

def localChai():
    yield ("Masala chai")
    yield ("Lemon chai")


def importedchai():
    yield "matcha"
    yield "Oolang"

def full_menu():
    yield from localChai()
    yield from importedchai()
    
for chai in full_menu():
    print(chai)
    
def chai_stall():
    try:
        while True:
            order = yield "Waiting for your chai order"
    except:
        print(f"Stall closed , No more Chai")

stall = chai_stall()
print(next(stall))
stall.close() #cleanup your memory 

# yield -> pause function and start
# next() -> value from generator function
# send -> provide Value
# yield from -> vlues
# close - > clean up your memory and stop them
