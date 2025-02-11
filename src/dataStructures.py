class Deque:
    def __init__(self, datas=None):
        if datas is None:
            datas = []
        self.data = list(datas)
        self.size = len(self.data)

    def push_back(self, num):
        self.data.append(num)
        self.size += 1

    def pop_back(self):
        if self.size == 0:
            raise RuntimeError
        self.size -= 1
        return self.data.pop(self.size)

    def push_front(self, num):
        self.data.insert(0, num)
        self.size += 1

    def pop_front(self):
        if self.size == 0:
            raise RuntimeError
        self.size -= 1
        return self.data.pop(0)

    def empty(self):
        return self.size == 0

    def back(self):
        return self.data[self.size]

    def front(self):
        return self.data[0]

    def __len__(self):
        return self.size

class Stack:
    def __init__(self, datas=None):
        self.data = list(datas)
        self.size = len(self.data)

    def push(self, num):
        self.data.append(num)
        self.size += 1

    def pop(self):
        if self.size == 0:
            raise RuntimeError
        self.size -= 1
        return self.data.pop(self.size)

    def empty(self):
        return self.size == 0

    def top(self):
        return self.data[self.size]

    def clear(self):
        self.data = []
        self.size = 0

    def __len__(self):
        return self.size

class Queue:
    def __init__(self, datas=[]):
        self.data = list(datas)
        self.size = len(self.data)

    def push(self, num):
        self.data.append(num)
        self.size += 1

    def pop(self):
        if self.size == 0:
            raise RuntimeError
        self.size -= 1
        return self.data.pop(0)

    def empty(self):
        return self.size == 0

    def front(self):
        return self.data[self.size]

    def clear(self):
        self.data = []
        self.size = 0

    def __len__(self):
        return self.size

class DisJointSet:  # 并查集类
    def __init__(self, n):
        self.fa = [i for i in range(0, n + 3)]

    def father(self, x) -> int:
        if self.fa[x] == x:
            return x
        self.fa[x] = self.father(self.fa[x])
        return self.fa[x]

    def merge(self, x, y):
        xx = self.father(x)
        yy = self.father(y)
        if xx == yy:
            return
        self.fa[xx] = yy

    def same(self, x, y) -> bool:
        return self.father(x) == self.father(y)

if __name__ == '__main__':
    s = Stack([2,9,8])
    s.push(3)
    s.push(5)
    t = s.pop()
    while not s.empty():
        print(s.pop(), end=" ")
    print("")
    s = Queue([2, 9, 8])
    s.push(3)
    s.push(5)
    t = s.pop()
    while not s.empty():
        print(s.pop(), end=" ")

