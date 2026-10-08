import threading
import requests
import time
def download_image(img_url):
    print(f"Starting download" )
    resp = requests.get(img_url)
    print(f"Finished downloading from {img_url},size: {len(resp.content)}")
    
img_url =[
    "https://picsum.photos/200",
    "https://picsum.photos/300",

]
start = time.time()
threads=[]
for img_url in img_url:
    t = threading.Thread(target=download_image,args=(img_url,))
    t.start()
    threads.append(t)
for t in threads:
    t.join()
end = time.time()
print(f"All Donwload donw in {end -start:.2f} second")



