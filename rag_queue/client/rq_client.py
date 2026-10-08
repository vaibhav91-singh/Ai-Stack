from radish import Redis
from rq import Queue

# Queue Setup using RQ 
queue= Queue(
    connection=Redis(
        host="localhost",
        port="6379"
    )
)

# wokers setup 

queue.enqueue