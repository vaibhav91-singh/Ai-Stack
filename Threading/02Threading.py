import threading
import time
# pass argument
def prepare_chay(type_,wait_time):
    print(f"{type_} chai:Brewing...")
    time.sleep(wait_time)
    print(f"{type_} chai:Ready")
# passign argument to thread function

t1=threading.Thread(target=prepare_chay("Masala",2))
t2=threading.Thread(target=prepare_chay("Ginger",3))

t1.start()
t2.start()
t1.join()
t2.join()
