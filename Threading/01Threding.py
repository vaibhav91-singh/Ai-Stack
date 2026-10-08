import threading
import time 

def boilEgg():
    print(f'Boling Egg...')
    time.sleep(2)
    print(f"Egg is boiled")
def toast_bun():
    print(f'Toasting bread')
    time.sleep(5)
    print(f'Bread is toasted')
start=time.time() # start time
x = threading.Thread(target=boilEgg)
y = threading.Thread(target=toast_bun)

x.start()
y.start()
x.join() #Wait for Thread to Finish
y.join()

end = time.time()
print(f"Breakfast is ready in {end-start:.2f} second") # end time


