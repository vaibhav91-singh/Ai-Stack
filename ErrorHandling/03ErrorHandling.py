try:
    with open ('hello.txt','w') as myfile:
        myfile.write("Hello")
except FileExistsError:
    print("File is not exixting")
finally:
    print("Always Run")