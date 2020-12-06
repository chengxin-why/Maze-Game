#import 载入包
import pygame
import sys
import maze as why
import math
import time
import os
import easygui

#init  pygame
#from pygame.button import Button

os.chdir("./resources")  # 资源路径
Unique = False
Gate = False
if easygui.ynbox("是否开启传送门模式？"):
    Gate = True
if easygui.ynbox("迷宫路径是否唯一？"):
    Unique = True
easygui.msgbox(msg="按方向键移动\n按空格键进入传送门\n长按A键开启提示\n长按B键自动寻路\n终点一定在右下角\n吃到一定数量的铜锣烧才能过关",title="游玩说明",ok_button="开始游戏")

pygame.init()   #pygame模块的初始化

m = why.maze(10,20,Unique,Gate)
while len(m.path)==0:
    m = why.maze(10,20,False,True)  # 万一木有路，重新生成（概率很小）
count = 0
win = False
print(m.grid)
#init clock
clock = pygame.time.Clock()   #创建一个对象用来跟踪时间

# screen
screen:pygame.Surface = pygame.display.set_mode([1280,640])   #先搭建窗口，640*480是很久很久以前的显示器尺寸
pygame.display.set_caption("迷宫")
icon = pygame.image.load("people.png")
pygame.display.set_icon(icon)

#加载图标
#icon=pygame.image.load("ico.jpg").convert_alpha()
#显示图标
#pygame.display.set_icon(icon)
####
# background   背景的设置
background = pygame.Surface(screen.get_size())
bg_image = pygame.image.load("background.png")   #进行背景的加载
background.blit(bg_image,[0,0])         #进行图片的覆盖并且永远不能恢复

#classes  类

class People(pygame.sprite.Sprite):   #继承动画精灵的类

    # initializer
    def __init__(self, image_file,speed, location):
        #call super initiallizer
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('people.png')    #图片的路径
        self.rect = self.image.get_rect()                #图片矩形
        self.rect.left, self.rect.top = location          #位置进行更新
        self.speed = speed     #速度进行更新

    #move one step
    def move(self):
        # test edges
        if self.rect.left <=screen.get_rect().left or self.rect.right >= screen.get_rect().right :
            self.speed[0] = -self.speed[0]             #左右的速度进行反向

        # test top
        if self.rect.top <= screen.get_rect().top or\
           self.rect.bottom >= screen.get_rect().bottom:
            self.speed[1] = -self.speed[1]   #上下的速度进行反向

        #move one step with speed
        newpos = self.rect.move(self.speed)
        self.rect = newpos

# create my objects   #建立自己的对象
# create my objects
my_people = People('people.png', [10,0],[0,0])
#set timer
pygame.time.set_timer (pygame.USEREVENT,1000)

#animate of every step
def animate():
    screen.blit(background,(0,0))

    #my_people.move()
    screen.blit(my_people.image, my_people.rect)

    pygame.display.flip()   #更新画板后面的图像

#20*40

#####################计分#######################
# 计分板类
class ScoreBoard():
    def __init__(self, screen):
        # 初始化信息
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        # self.settings = settings
        # self.stats = stats
        # 分数图形的参数
        self.text_color = (0x66,0xcc,0xff)
        self.ok_color = (0, 238, 118)
        self.font = pygame.font.SysFont(None, 48)
        # 获取分数图形
        self.prep_score()

    def prep_score(self):
        # 将数字分数转换成字符串分数
        str_score = str(count) + '/' + str(m.scoreNum*2//3)
        # 将字符串转换成 Surface对象
        if count >= (2*m.scoreNum//3):
            self.text_color = (0, 238, 118)
        self.score_image = self.font.render(str_score, True, self.text_color)
        # 获取分数图形的坐标位置
        self.score_rect = self.score_image.get_rect()
        # 将分数图形绘制到屏幕右上角
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
        screen.blit(self.score_image,self.score_rect)
        pygame.display.update()

board = ScoreBoard(screen)
#######################################

##############倒计时####################
class Countdown:
    def __init__(self,screen):
        # 初始化信息
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        # 分数图形的参数
        self.text_color = (0, 238, 118)
        self.warn_color = (238, 238, 0)
        self.urgent_color = (255, 69, 0)
        self.font = pygame.font.SysFont(None, 48)
        # 获取分数图形
        self.time = 90 # 倒计时秒数（可修改）
        self.prep_time()
    def prep_time(self):
        str_time = str(int(self.time/60)) + ':' + ('0'+str(int(self.time)%60))[-2:]  # 转化成MM:SS字符串
        if self.time <= 10:  # 小于10s变为红色
            self.text_color = self.urgent_color
        elif self.time <= 30:  # 小于30s变为黄色
            self.text_color = self.warn_color
        self.time_image = self.font.render(str_time, True, self.text_color)
        self.time_rect = self.time_image.get_rect()
        # 将时间图形绘制到屏幕右上角
        self.time_rect.right = self.screen_rect.right - 20
        self.time_rect.top = 60
        screen.blit(self.time_image, self.time_rect)
        pygame.display.update()

timer = Countdown(screen)
########################



##########背景音乐
file=r'哆啦A梦.mp3'		# 音乐的路径
pygame.mixer.init()						# 初始化
track = pygame.mixer.music.load(file)	# 加载音乐文件
pygame.mixer.music.play(-1)				# 开始播放音乐流

##############################
#########电脑走迷宫函数####
def autoWalka():
    
    pos = (0,0)
    #direct = [(1,0),(0,1),(-1,0),(0,-1)]
    #print(m.solution)
    for i in range(19):
        for j in range(39):
            if (m.solution[i][j]-2==0):
                screen.blit(pygame.image.load("bj.png"), (j*32,i*32))

    pygame.display.update()


def autoWalkb():
    for step in m.path:
        screen.blit(pygame.image.load("people.gif"),(step[1]*32,step[0]*32))
        pygame.display.flip()
        time.sleep(0.1)
##########################
#main loop
running = True
held_down = False
while running:

    #process events
    if  pygame.key.get_pressed()[pygame.K_LEFT]  :
        if (m.grid[int(my_people.rect.top /32)][int(my_people.rect.left/32)-1]):
            my_people.rect.left = my_people.rect.left - 32
            
    if pygame.key.get_pressed()[pygame.K_SPACE] :
            if not(m.grid[int(my_people.rect.top /32)][int(my_people.rect.left/32)]==1 ):   #进行传送
                new_point = m.gate[int(my_people.rect.top /32),int(my_people.rect.left/32)]
                my_people.rect.top = new_point[0]*32
                my_people.rect.left = new_point[1]*32

                    
    if  pygame.key.get_pressed()[pygame.K_RIGHT]:
        if (m.grid[int(my_people.rect.top/32)][int(my_people.rect.left/32)+1]):
            my_people.rect.right = my_people.rect.right + 32

            

    if  pygame.key.get_pressed()[pygame.K_UP]:
        if (m.grid[int(my_people.rect.top /32)-1][int(my_people.rect.left/32)]):      # y轴的方向是向下的
            my_people.rect.top = my_people.rect.top - 32   # move 10 pixels up

    if  pygame.key.get_pressed()[pygame.K_DOWN]:
        if (m.grid[int(my_people.rect.top /32)+1][int(my_people.rect.left/32)]):    #向上
            my_people.rect.top = my_people.rect.top + 32   # move 10 pixels down

    if  pygame.key.get_pressed()[pygame.K_a]:     #长按a键生成提示
        autoWalka()
    if pygame.key.get_pressed()[pygame.K_b]:      #长按b键直接电脑自动走
        autoWalkb()
    # board.prep_score()

    if ((m.score[int(my_people.rect.top /32)][int(my_people.rect.left/32)]==1 ) ):  # 吃铜锣烧
        m.score[int(my_people.rect.top /32)][int(my_people.rect.left/32)]=0
        count+=1
        # board.prep_score()
    
    for event in pygame.event.get():   #进行事件的获取
        if event.type == pygame.QUIT:    #如果检测到退出的事件
            running = False    #开关关闭
        if event.type == pygame.KEYDOWN:    #如果键盘事件
            if(event.type == pygame.K_q and m.grid[int(my_people.rect.top /32)][int(my_people.rect.left/32)]==4):  #进行传送阵的检测
                pass
            #if (event.key == pygame.K_UP and m.grid[int(my_people.rect.top /32)-1][int(my_people.rect.left/32)] ):      # y轴的方向是向下的
                
                #my_people.rect.top = my_people.rect.top - 32   # move 10 pixels up
            #elif (event.key == pygame.K_DOWN and m.grid[int(my_people.rect.top /32)+1][int(my_people.rect.left/32)]):    #向上
                #my_people.rect.top = my_people.rect.top + 32   # move 10 pixels down
                
           # elif (event.key == pygame.K_LEFT and m.grid[int(my_people.rect.top /32)][int(my_people.rect.left/32)-1]):
                #my_people.rect.left = my_people.rect.left - 32
            #elif (event.key == pygame.K_RIGHT and m.grid[int(my_people.rect.top/32)][int(my_people.rect.left/32)+1]):
                #my_people.rect.right = my_people.rect.right + 32
                
        elif event.type == pygame.MOUSEBUTTONUP:
            held_down = False
        elif event.type ==pygame.MOUSEBUTTONDOWN:
            held_down = True
        elif event.type == pygame.MOUSEMOTION:
            if held_down:
                my_people.rect.center = event.pos
                
    screen.fill([0, 0, 0])
    for i in range(math.floor((my_people.rect.top)/32)-5,math.floor((my_people.rect.top)/32)+6):
        #try:
            if(i>=0 and i<20):
                for j in range(math.floor((my_people.rect.left)/32-5),math.floor((my_people.rect.left)/32)+6):
                    if(j>=0 and j<40):
                        if m.grid[i][j]==1 :
                            screen.blit(pygame.image.load('wall.jpg'),(j*32,i*32))
                        elif m.grid[i][j]==0 :
                            screen.blit(pygame.image.load('rode.png'),(j*32,i*32))
                        elif m.grid[i][j]==2:
                            screen.blit(pygame.image.load('wall.jpg'),(j*32,i*32))
                            screen.blit(pygame.image.load('2.png'),(j*32,i*32))
                        elif m.grid[i][j]==3:
                            screen.blit(pygame.image.load('wall.jpg'),(j*32,i*32))
                            screen.blit(pygame.image.load('3.png'),(j*32,i*32))
                        elif m.grid[i][j]==4:
                            screen.blit(pygame.image.load('wall.jpg'),(j*32,i*32))
                            screen.blit(pygame.image.load('4.png'),(j*32,i*32))
                        if(i==18 and j==38):
                            screen.blit(pygame.image.load('wall.jpg'),(j*32,i*32))
                            screen.blit(pygame.image.load('zd.png'),(j*32,i*32))
                        if m.score[i][j]==1:
                            screen.blit(pygame.image.load('tls.png'),(j*32,i*32))
            

        

        #except:
            #pass
    #my_people.move()
    screen.blit(my_people.image, my_people.rect)
    pygame.display.update()
    #animate()
    board.prep_score()
    timer.time -= 0.1
    timer.prep_time()
    clock.tick(10)        #设置帧率为10帧
    if timer.time <= 0:  # o泡时间到
        running = False
        track = pygame.mixer.music.load('o泡.mp3')  # 倒计时到了播放o泡
        pygame.mixer.music.play(-1)
    if(my_people.rect.left == 38*32 and my_people.rect.top == 18*32 and count>=(m.scoreNum*2//3)):
        running = False
        win = True
        track = pygame.mixer.music.load('胜利.mp3')
        pygame.mixer.music.play(-1)

if win:
    screen.blit(pygame.image.load("youwin2.png"), (10,10))
else:
    screen.blit(pygame.image.load("gameover.png"), (50,50))
pygame.display.update()
# exit program   退出
while(True):
    for event in pygame.event.get():   #进行事件的获取
        if event.type == pygame.QUIT:    #如果检测到退出的事件
            pygame.quit()  #结束整个pygame的程序   exit  pygame
            sys.exit()    #close  window

