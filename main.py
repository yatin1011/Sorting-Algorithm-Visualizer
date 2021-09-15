import time
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class TrackedArray():

    def __init__(self, arr):
        self.arr = np.copy(arr)
        self.reset()
    
    def reset(self):
        self.indices = []
        self.values = []
        self.access_type = []
        self.full_copies = []
    
    def track(self, key, access_type):
        self.indices.append(key)
        self.values.append(self.arr[key])
        self.access_type.append(access_type)
        self.full_copies.append(np.copy(self.arr))
    
    def GetActivity(self, idx=None):
        if isinstance(idx, type(None)):
            return [(i, op) for (i, op) in zip(self.indices, self.access_type)]
        else:
            return (self.indices[idx], self.access_type[idx])
    
    def __getitem__(self, key):
        self.track(key, "get")
        return self.arr.__getitem__(key)
    
    def __setitem__(self, key, value):
        self.arr.__setitem__(key, value)
        self.track(key, "set")
    
    def __len__(self):
        return self.arr.__len__()

plt.rcParams["figure.figsize"] = (12, 8)
plt.rcParams["font.size"] = 16

FPS = 60.0

N = 30
arr = np.round(np.linspace(0, 1000, N), 0)
np.random.seed(0)
np.random.shuffle(arr)

print(arr)

arr = TrackedArray(arr)

############  DEMO 1: INSERTION SORT  ##############

sorter = "Insertion"
t0 = time.perf_counter()

i = 1
while (i < len(arr)):
    j = i
    while ((j > 0) and (arr[j-1] > arr[j])):
        temp = arr[j-1]
        arr[j-1] = arr[j]
        arr[j] = temp
        j -= 1
    i += 1

dt = time.perf_counter() - t0


##############  DEMO 2: QUICK SORT  ################

# sorter = "Quick"
# t0 = time.perf_counter()

# def quicksort(A, lo, hi):
#     if lo < hi:
#         p = partition(A, lo, hi)
#         quicksort(A, lo, p - 1)
#         quicksort(A, p + 1, hi)


# def partition(A, lo, hi):
#     pivot = A[hi]
#     i = lo
#     for j in range(lo, hi):
#         if A[j] < pivot:
#             temp = A[i]
#             A[i] = A[j]
#             A[j] = temp
#             i += 1
#     temp = A[i]
#     A[i] = A[hi]
#     A[hi] = temp
#     return i

# quicksort(arr, 0, len(arr)-1)

# dt = time.perf_counter() - t0

print(arr)
print(f"--------- {sorter} Sort ---------")
print(f"Array Sorted in {dt*1E3:.1f} ms")


fig, ax = plt.subplots()
container = ax.bar(np.arange(0, len(arr), 1), arr, align='edge', width=0.8)
ax.set_xlim([0, N])
ax.set(xlabel="Index", ylabel="Value", title=f"{sorter} Sort")

def update(frame):

    for (rectangle, height) in zip(container.patches, arr.full_copies[frame]):
        rectangle.set_height(height)
        rectangle.set_color('#1f77b4')
    
    return (*container,)

ani = FuncAnimation(fig, update, frames=range(len(arr.full_copies)),
                    blit=True, interval=1000./FPS, repeat=False)

plt.show()