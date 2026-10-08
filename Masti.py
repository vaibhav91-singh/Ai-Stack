import time
import sys

def print_lyrics():
    lyrics = [
        "Sambhaal ke rakhna wo phool mera tu",
        "Meri shayari mein zaroor raha tu",
        "Jo aankhon mein pyaari si duniya basaayi",
        "Wo duniya bhi tha tu, wo lamha bhi tha tu",
        "Haan, lagte hain mujhko ye kisse sataane",
        "Deta na dil mera tujhko bhulaane",
        "Adhoore se vaade, adhoori si raatein",
        "Ab hisse mein daakhil mere bas wo yaadein"
    ]
    
    delay = [0.7, 0.7, 0.4, 0.5, 0.5, 0.7, 0.7, 1.0]

    print("Finding Her !!\n")
    time.sleep(1.2)

    for i, line in enumerate(lyrics):
        for char in line:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.1)
        # newline after finishing the line
        print()
        # sleep for the corresponding delay (safe-guard index)
        if i < len(delay):
            time.sleep(delay[i])
            
if __name__ == "__main__":
    print_lyrics()

