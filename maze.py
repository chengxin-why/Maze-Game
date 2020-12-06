# coding=gbk

import random as rd
import numpy as np
from dataStructures import Queue
from dataStructures import DisJointSet

def pointToInt(point: tuple, row, col) -> int:  # 左上角(0,0)
    return point[0] * col + point[1]

gateNum = 2

class maze:  # 迷宫类，存储迷宫的格子
    def __init__(self, row: int, col: int, unique=True, gate=True):  # row是行，col是列,unique路径是否唯一，gate是否有传送门
        self.row = row
        self.col = col
        self.grid = np.zeros((row * 2, col * 2))  # 先全变成0 - 0是墙，1可行,2-4是传送门
        self.score = np.zeros((row*2,col*2))  # 积分
        self.scoreNum = 0  # 积分块数量
        self.djs = DisJointSet(row * col + 3)  # 并查集，用于检验是否属于同一集合
        self.way = 0  # 格子数量（暂时未用）
        self.gate = {}  # 传送门
        self.s = (0,0)  # 迷宫起点
        self.t = (row-1,col-1)  # 迷宫终点
        self.makeWay(self.s[0], self.s[1], self.t[0], self.t[1], unique, gate)  # 设定起点、终点，创造一条路，可修改参数值
        self.t = (row*2-2,col*2-2)  # 实际终点在数组中的位置要翻倍
        self.grid_l = self.grid.tolist()  # 以列表形式存储
        self.solution = np.zeros((row * 2, col * 2))  # 迷宫的最短路解
        self.path = []
        self.dis = []  # 起点到终点距离

        bfs(self)  # 计算机求出最优解
        # self.printPath()  # 打印路径

    def connect(self, x1, x2, y1, y2) -> bool:
        pA = pointToInt((x1, x2), self.row, self.col)
        pB = pointToInt((y1, y2), self.row, self.col)
        return self.djs.same(pA, pB)

    def addGate(self):
        randPoint1 = (rd.randint(0, self.row - 1), rd.randint(0, self.col - 1))
        randPoint2 = (rd.randint(0, self.row - 1), rd.randint(0, self.col - 1))
        while randPoint1 == self.s or randPoint1 == self.t or (randPoint1 in self.gate):
            randPoint1 = (rd.randint(0, self.row - 1), rd.randint(0, self.col - 1))  # 传送门与起点、终点、其他传送门重叠，需重新生成
        while randPoint2 == self.s or randPoint2 == self.t or (randPoint2 in self.gate) or randPoint2 == randPoint1:
            randPoint2 = (rd.randint(0, self.row - 1), rd.randint(0, self.col - 1))  # 传送门与起点、终点、其他传送门重叠，需重新生成

        pA = pointToInt(randPoint1, self.row, self.col)
        pB = pointToInt(randPoint2, self.row, self.col)

        randPoint1 = (randPoint1[0]*2, randPoint1[1]*2)
        randPoint2 = (randPoint2[0]*2, randPoint2[1]*2)

        self.djs.merge(pA,pB)
        self.gate[randPoint1] = randPoint2
        self.gate[randPoint2] = randPoint1
        global gateNum
        self.grid[randPoint1[0]][randPoint1[1]] = gateNum
        self.grid[randPoint2[0]][randPoint2[1]] = gateNum
        gateNum += 1

    def makeWay(self, sx, sy, tx, ty, unique, gate):
        if gate:
            for i in range(3):
                self.addGate()
        while not self.connect(sx, sy, tx, ty):
            randPoint = (rd.randint(0, self.row - 1), rd.randint(0, self.col - 1))
            randDir = rd.randint(0, 1)  # 右 下 左 上
            if randDir == 0 and randPoint[1] == self.col - 1:
                continue
            if randDir == 1 and randPoint[0] == self.row - 1:
                continue
            if randDir == 0:
                nextPoint = (randPoint[0], randPoint[1] + 1)
                pA = pointToInt(randPoint, self.row, self.col)
                pB = pointToInt(nextPoint, self.row, self.col)
                if not unique or not self.djs.same(pA, pB):
                    self.djs.merge(pA, pB)
                    self.way += 1
                    self.grid[randPoint[0] * 2][randPoint[1] * 2] = max(1, self.grid[randPoint[0] * 2][randPoint[1] * 2])
                    self.grid[randPoint[0] * 2][randPoint[1] * 2 + 1] = max(1, self.grid[randPoint[0] * 2][randPoint[1] * 2 + 1])
                    self.grid[nextPoint[0] * 2][nextPoint[1] * 2] = max(1, self.grid[nextPoint[0] * 2][nextPoint[1] * 2])
                    if rd.randint(1,6)==5:
                        self.score[randPoint[0] * 2][randPoint[1] * 2 + 1] = 1
                        self.scoreNum += 1
            else:
                nextPoint = (randPoint[0] + 1, randPoint[1])
                pA = pointToInt(randPoint, self.row, self.col)
                pB = pointToInt(nextPoint, self.row, self.col)
                if not unique or not self.djs.same(pA, pB):
                    self.djs.merge(pA, pB)
                    self.way += 1
                    self.grid[randPoint[0] * 2][randPoint[1] * 2] = max(1, self.grid[randPoint[0] * 2][randPoint[1] * 2])
                    self.grid[randPoint[0] * 2 + 1][randPoint[1] * 2] = max(1, self.grid[randPoint[0] * 2 + 1][randPoint[1] * 2])
                    self.grid[nextPoint[0] * 2][nextPoint[1] * 2] = max(1, self.grid[nextPoint[0] * 2][nextPoint[1] * 2])
                    if rd.randint(1,6)==5:
                        self.score[randPoint[0] * 2 + 1][randPoint[1] * 2] = 1
                        self.scoreNum += 1

    def printPath(self):
        print("Solution:",end=' ')
        for step in self.path[:-1]:
            print("(%d,%d)->" % (step[0],step[1]),end='')
        print("(%d,%d)" % (self.path[-1][0],self.path[-1][1]))

direction = [(1,0),(0,1),(-1,0),(0,-1)]

pre = dict()  # 存储每个点的前驱（即从哪儿来到这个点的）

def out(p:tuple, m:maze) -> bool:  # 判断一个点是否出界
    return not (p[0] <= m.row*2 and p[0] >= 0 and p[1] <= m.col*2 and p[1] >= 0)

def bfs(m: maze):
    vis = set()  # 访问过的点组成的集合，以防止重复访问
    dis = dict()  # 存储每个点距离源点的距离
    q = Queue()
    dis[m.s] = 0
    vis.add(m.s)
    q.push(m.s)

    while not q.empty():
        now = q.pop()

        if now in m.gate:
            nextPoint = m.gate[now]
            if nextPoint not in vis:
                dis[nextPoint] = dis[now]
                vis.add(nextPoint)
                pre[nextPoint] = now
                q.push(nextPoint)
                # continue

        if now == m.t:  # 到终点啦
            recordPath(pre[m.t], m.s, m)  # 打印路径，并保存在m.solution中
            m.solution[m.t[0]][m.t[1]] = 2  # 终点加入路径
            m.path.append((m.t[0], m.t[1]))
            m.dis = dis[now] + 1
            return "Find Path!"

        for i in direction:
            nextPoint = (now[0] + i[0], now[1] + i[1])
            if m.grid[nextPoint[0]][nextPoint[1]] == 0 or out(nextPoint,m):
                continue
            if nextPoint not in vis:
                dis[nextPoint] = dis[now] + 1
                vis.add(nextPoint)
                pre[nextPoint] = now
                q.push(nextPoint)
        # end while
    return "Cannot find path"

def recordPath(p, s, m:maze):  # 递归找到来时的路
    if p != s:
        recordPath(pre[p], s, m)
    m.solution[p[0]][p[1]] = 2
    m.path.append((p[0],p[1]))

if __name__ == '__main__':
    r, c = input("请输入迷宫的行、列，用空格隔开").split()
    M = maze(int(r), int(c), unique=True, gate=True)
    print(M.grid)
    # bfs(M)
