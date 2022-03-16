from datetime import *

a = datetime.today()
b = datetime.now()
print(a,b)
if a == b:
    print("YES")
else:
    print("NO")

for _ in range(5):
    print("1")