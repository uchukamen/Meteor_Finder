
from collections import deque


deq = deque()

deq.append(1)
deq.append(5)
deq.append(3)
deq.append(6)
deq.append(2)
deq.append(3)

print(len(deq))
print(max(deq))
print(min(deq))

deq.popleft()
deq.append(10)
print(max(deq))
print(min(deq))

deq.popleft()
deq.append(-1)
print(max(deq))
print(min(deq))
