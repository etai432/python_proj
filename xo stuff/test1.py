import time
a = time.time()
b = 0
for i in range(100000):
    b += i
print(time.time()-a)
