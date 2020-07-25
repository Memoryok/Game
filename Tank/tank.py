"""*************************************
项目名称：坦克大战游戏
作    者：Memory
开始时间：2020.01.02
完成时间：2020.01.08
调试时间：2020.01.10
更新时间：2020.01.11
项目周期：2020.01.02-2020.01.12
项目语言：Python语言
项目环境：Windows系统
当前版本：Tank 2.0
*************************************"""

# coding=utf-8

import pygame  # 导入pygame模块
import time  # 导入time模块
import random  # 导入random模块
from pygame.sprite import Sprite  # 导入精灵类Sprite模块

SCREEN_WIDTH = 780  # 窗口宽度
SCREEN_HEIGHT = 540  # 窗口高度
BG_COLOR = pygame.Color(0, 0, 0)
TEXT_COLOR = pygame.Color(255, 0, 0)


class BaseItem(Sprite):
    """定义一个基类继承精灵类"""
    def __init__(self):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)


class MainGame:
    """主类"""
    window = None
    my_tank = None
    # 存储敌方坦克的列表
    enemyTankList = []
    # 定义敌方坦克的数量
    enemyTankCount = 5
    # 存储我方子弹的列表
    myBulletList = []
    # 存储敌方子弹的列表
    enemyBulletList = []
    # 存储爆炸效果的列表
    explodeList = []
    # 存储墙壁的列表
    wallList = []

    def __init__(self):
        pass

    def startGame(self):
        """开始游戏"""
        # 加载主窗口,初始化窗口
        pygame.display.init()
        # 设置窗口的大小及显示
        MainGame.window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        # 初始化我方坦克
        self.createMytank()
        # 初始化敌方坦克，并将敌方坦克添加到列表中
        self.createEnemyTank()
        # 初始化墙壁
        self.createWall()
        # 设置窗口的标题
        pygame.display.set_caption("坦克大战2.0")
        # 循环显示窗口
        while True:
            # 使坦克移动的速度慢一点
            time.sleep(0.05)
            # 给窗口设置填充色
            MainGame.window.fill(BG_COLOR)
            # 获取事件
            self.getEvent()
            # 绘制文字
            MainGame.window.blit(self.getTextSurface
                                 ("敌方坦克剩余数量:%d" % len(MainGame.enemyTankList), 18),
                                 (10, 10))
            # 判断敌方坦克剩余为0时  胜利
            if len(MainGame.enemyTankList) <= 0:
                MainGame.window.blit(self.getTextSurface("恭喜胜利", 100), (150, 100))
                MainGame.window.blit(self.getTextSurface("你太棒了", 100), (150, 300))
            # 判断我方坦克是否是存活
            if MainGame.my_tank and MainGame.my_tank.live:
                # 调用坦克显示的方法
                MainGame.my_tank.displayTank()
            else:
                # 删除我方坦克
                del MainGame.my_tank
                MainGame.my_tank = None
            # 循环遍历敌方坦克列表，展示敌方坦克
            self.blitEnemyTank()
            # 循环遍历显示我方坦克的子弹
            self.blitMyBullet()
            # 循环遍历显示敌方坦克的子弹
            self.blitEnemyBullet()
            # 循环遍历爆炸列表，展示爆炸效果
            self.blitExplode()
            # 循环遍历墙壁列表，展示墙壁
            self.blitWall()
            # 调用坦克移动方法
            # 如果坦克的开关开启，才可以移动
            if MainGame.my_tank and MainGame.my_tank.live:
                if MainGame.my_tank.stop:
                    MainGame.my_tank.move()
                    # 检测我方坦克是否与墙壁发生碰撞
                    MainGame.my_tank.hitWall()
                    # 检测我方坦克是否与敌方坦克碰撞
                    MainGame.my_tank.myTank_hit_enemyTank()
            # 循环显示主窗口
            pygame.display.update()

    @staticmethod
    def blitExplode():
        """循环展示爆炸效果"""
        for explode in MainGame.explodeList:
            # 判断是否活着
            if explode.live:
                # 展示
                explode.displayExplode()
            else:
                # 在爆炸列表中移除
                MainGame.explodeList.remove(explode)

    @staticmethod
    def blitWall():
        """循环遍历墙壁列表，展示墙壁"""
        for wall in MainGame.wallList:
            # 判断墙壁是否存活
            if wall.live:
                # 调用墙壁的显示方法
                wall.displayWall()
            else:
                # 墙壁列表中移除
                MainGame.wallList.remove(wall)

    @staticmethod
    def createWall():
        """初始化墙壁"""
        for i in range(7):
            wall = Wall(i*120, 220)
            # 将墙壁添加到列表中
            MainGame.wallList.append(wall)

    @staticmethod
    def createMytank():
        """创建我方坦克的方法"""
        MainGame.my_tank = MyTank(360, 480)
        # 创建Music对象
        music = Music("img/start.wav")
        # 播放音乐
        music.play()

    @staticmethod
    def createEnemyTank():
        """初始化敌方坦克，并将敌方坦克添加到列表中"""
        top = 100
        # 循环生成敌方坦克
        for i in range(MainGame.enemyTankCount):
            left = random.randint(0, 600)
            speed = random.randint(1, 4)
            enemy = EnemyTank(left, top, speed)
            MainGame.enemyTankList.append(enemy)

    @staticmethod
    def blitEnemyTank():
        """循环遍历敌方坦克列表，展示敌方坦克"""
        for enemyTank in MainGame.enemyTankList:
            # 判断当前敌方坦克是否活着
            if enemyTank.live:
                enemyTank.displayTank()
                enemyTank.randMove()
                # 调用检测是否与墙壁碰撞
                enemyTank.hitWall()
                # 检测敌方坦克是否与我方坦克发生碰撞
                if MainGame.my_tank and MainGame.my_tank.live:
                    enemyTank.enemyTank_hit_myTank()
                # 发射子弹
                enemyBullet = enemyTank.shot()
                # 判断敌方子弹是否是None，如果不为None则添加到敌方子弹列表
                if enemyBullet:
                    # 将敌方子弹存储到敌方子弹列表
                    MainGame.enemyBulletList.append(enemyBullet)
            # 如果不活着，从敌方坦克列表中移除
            else:
                MainGame.enemyTankList.remove(enemyTank)

    @staticmethod
    def blitMyBullet():
        """循环遍历我方子弹存储列表"""
        for myBullet in MainGame.myBulletList:
            # 判断当前子弹是否是活着的状态，如果是进行显示及移动，否则在列表中删除
            if myBullet.live:
                myBullet.displayBullet()
                # 调用子弹的移动方法
                myBullet.move()
                # 调用检测我方子弹是否与敌方坦克发生碰撞
                myBullet.myBullet_hit_enemyTank()
                # 检测我方子弹是否与墙壁碰撞
                myBullet.hitWall()
            # 否则在列表中删除
            else:
                MainGame.myBulletList.remove(myBullet)

    @staticmethod
    def blitEnemyBullet():
        """循环遍历敌方子弹存储列表"""
        for enemyBullet in MainGame.enemyBulletList:
            # 判断当前子弹是否是活着的状态，如果是进行显示及移动，否则在列表中删除
            if enemyBullet.live:
                enemyBullet.displayBullet()
                enemyBullet.move()
                # 调用敌方子弹与我方坦克碰撞的方法
                enemyBullet.enemyBullet_hit_myTank()
                # 检测敌方子弹是否与墙壁碰撞
                enemyBullet.hitWall()
            else:
                MainGame.enemyBulletList.remove(enemyBullet)

    @staticmethod
    def endGame():
        """结束游戏"""
        print("再见,欢迎下次使用!")
        exit()

    @staticmethod
    def getTextSurface(text, size):
        """左上角文字和游戏胜利的绘制"""
        # 初始化字体模块
        pygame.font.init()
        # 查看所有的字体名称
        # print(pygame.font.get_fonts())
        # 获取字体Font对象
        font = pygame.font.SysFont("kaiti", size)
        # 绘制文字信息
        textSurface = font.render(text, True, TEXT_COLOR)
        return textSurface

    def getEvent(self):
        """获取事件"""
        # 获取所有事件
        eventList = pygame.event.get()
        # 遍历事件
        for event in eventList:
            # 判断按下键是关闭还是键盘按下
            # 如果按下是退出，则关闭窗口
            if event.type == pygame.QUIT:
                self.endGame()
            # 如果是键盘的按下
            elif event.type == pygame.KEYDOWN:
                # 当坦克不存在
                if not MainGame.my_tank:
                    # 判断按下的是Esc键，让坦克重生
                    if event.key == pygame.K_ESCAPE:
                        # 让我方坦克重生
                        self.createMytank()
                if MainGame.my_tank and MainGame.my_tank.live:
                    # 判断按下的是上、下、左、右
                    if event.key == pygame.K_LEFT:
                        # 切换方向
                        MainGame.my_tank.direction = 'L'
                        # 修改坦克开关状态
                        MainGame.my_tank.stop = True
                        # MainGame.my_tank.move()
                        # print("按下左键，坦克向左移动")
                    elif event.key == pygame.K_RIGHT:
                        # 切换方向
                        MainGame.my_tank.direction = 'R'
                        # 修改坦克开关状态
                        MainGame.my_tank.stop = True
                        # MainGame.my_tank.move()
                        # print("按下右键，坦克向右移动")
                    elif event.key == pygame.K_UP:
                        # 切换方向
                        MainGame.my_tank.direction = 'U'
                        # 修改坦克开关状态
                        MainGame.my_tank.stop = True
                        # MainGame.my_tank.move()
                        # print("按下上键，坦克向上移动")
                    elif event.key == pygame.K_DOWN:
                        # 切换方向
                        MainGame.my_tank.direction = 'D'
                        # 修改坦克开关状态
                        MainGame.my_tank.stop = True
                        # MainGame.my_tank.move()
                        # print("按下下键，坦克向下移动")
                    elif event.key == pygame.K_SPACE:
                        # 如果当前我方子弹列表的大小，小于3才可以创建
                        if len(MainGame.myBulletList) < 3:
                            # 创建我方坦克发射的子弹
                            myBullet = Bullet(MainGame.my_tank)
                            MainGame.myBulletList.append(myBullet)
                            # 我方坦克发射子弹添加音效
                            music = Music("img/fire.wav")
                            music.play()
                            # print("发射子弹")
            # 松开方向键，坦克停止移动，修改坦克的开关状态
            elif event.type == pygame.KEYUP:
                # 判断松开的键是上下左右时候才停止坦克移动
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN or \
                        event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    if MainGame.my_tank and MainGame.my_tank.live:
                        MainGame.my_tank.stop = False


class Tank(BaseItem):
    """坦克类"""
    # 添加距离左边left，距离上面top
    def __init__(self, left, top):
        # 保存加载图片
        super().__init__()
        self.images = {"U": pygame.image.load("img/p1tankU.gif"),
                       "D": pygame.image.load("img/p1tankD.gif"),
                       "L": pygame.image.load("img/p1tankL.gif"),
                       "R": pygame.image.load("img/p1tankR.gif")}
        # 方向,默认朝上
        self.direction = "U"
        # 根据当前图片的方向获取图片
        self.image = self.images[self.direction]
        # 根据图片获取区域
        self.rect = self.image.get_rect()
        # 设置区域的left和top
        self.rect.left = left
        self.rect.top = top
        # 速度 决定移动的快慢
        self.speed = 10
        # 坦克移动的开关
        self.stop = False
        # 是否活着
        self.live = True
        # 新增属性 原来坐标
        self.oldLeft = self.rect.left
        self.oldTop = self.rect.top

    def move(self):
        """移动"""
        # 移动后记录原始的坐标
        self.oldLeft = self.rect.left
        self.oldTop = self.rect.top
        # 判断坦克的方向进行移动
        if self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
        elif self.direction == 'D':
            if self.rect.top + self.rect.height < SCREEN_HEIGHT:
                self.rect.top += self.speed
        elif self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
        elif self.direction == 'R':
            if self.rect.left + self.rect.height < SCREEN_WIDTH:
                self.rect.left += self.speed

    def shot(self):
        """射击"""
        return Bullet(self)

    def stay(self):
        """将坐标设置为移动之前的坐标"""
        self.rect.left = self.oldLeft
        self.rect.top = self.oldTop

    def hitWall(self):
        """检测坦克是否与墙壁发生碰撞"""
        for wall in MainGame.wallList:
            if pygame.sprite.collide_rect(self, wall):
                # 将坐标设置为移动之前的坐标
                self.stay()

    def displayTank(self):
        """展示坦克的方法"""
        # 获取展示的对象
        self.image = self.images[self.direction]
        # 调用blit方法展示
        MainGame.window.blit(self.image, self.rect)


class MyTank(Tank):
    """我方坦克"""
    def __init__(self, left, top):
        super(MyTank, self).__init__(left, top)

    def myTank_hit_enemyTank(self):
        """检测我方坦克与敌方坦克发生碰撞"""
        # 循环遍历敌方坦克列表
        for enemyTank in MainGame.enemyTankList:
            if pygame.sprite.collide_rect(self, enemyTank):
                self.stay()


class EnemyTank(Tank):
    """敌方坦克"""
    def __init__(self, left, top, speed):
        # 调用父类的初始化方法
        super(EnemyTank, self).__init__(left, top)
        # 加载图片集
        self.images = {"U": pygame.image.load("img/enemy1U.gif"),
                       "D": pygame.image.load("img/enemy1D.gif"),
                       "L": pygame.image.load("img/enemy1L.gif"),
                       "R": pygame.image.load("img/enemy1R.gif")}
        # 方向,随机生成敌方坦克的方向
        self.direction = self.randDirection()
        # 根据方向获取图片
        self.image = self.images[self.direction]
        # 区域
        self.rect = self.image.get_rect()
        # 对left和top进行赋值
        self.rect.left = left
        self.rect.top = top
        # 速度
        self.speed = speed
        # 移动开关
        self.flag = False
        # 新增一个步数变量
        self.step = 60

    def enemyTank_hit_myTank(self):
        """检测敌方坦克与我方坦克发生碰撞"""
        if pygame.sprite.collide_rect(self, MainGame.my_tank):
            self.stay()

    @staticmethod
    def randDirection():
        """随机生成敌方坦克的方向"""
        num = random.randint(1, 4)
        if num == 1:
            return 'U'
        elif num == 2:
            return 'D'
        elif num == 3:
            return 'L'
        elif num == 4:
            return 'R'

    def randMove(self):
        """敌方坦克随机移动的方法"""
        if self.step <= 0:
            # 修改方向
            self.direction = self.randDirection()
            # 让步数复位
            self.step = 60
        else:
            self.move()
            # 让步数递减
            self.step -= 1

    def shot(self):
        """重写shot()"""
        # 随机生成100以内的数
        num = random.randint(1, 100)
        if num < 6:
            return Bullet(self)


class Bullet(BaseItem):
    """子弹类"""
    def __init__(self, tank):
        """加载子弹图片"""
        super().__init__()
        self.image = pygame.image.load("img/enemymissile.gif")
        # 坦克的方向决定子弹的方向
        self.direction = tank.direction
        # 获取区域
        self.rect = self.image.get_rect()
        # 子弹的left和top与方向有关
        if self.direction == 'U':
            self.rect.left = int(tank.rect.left + tank.rect.width / 2 - self.rect.width / 2)
            self.rect.top = int(tank.rect.top - self.rect.height)
        elif self.direction == 'D':
            self.rect.left = int(tank.rect.left + tank.rect.width / 2 - self.rect.width / 2)
            self.rect.top = int(tank.rect.top + tank.rect.height)
        elif self.direction == 'L':
            self.rect.left = int(tank.rect.left - self.rect.height)
            self.rect.top = int(tank.rect.top + tank.rect.width / 2 - self.rect.width / 2)
        elif self.direction == 'R':
            self.rect.left = int(tank.rect.left + tank.rect.height)
            self.rect.top = int(tank.rect.top + tank.rect.width / 2 - self.rect.width / 2)
        # 子弹的速度
        self.speed = 6
        # 子弹的状态，是否碰到墙壁，如果碰到墙壁，修改此状态
        self.live = True

    def move(self):
        """子弹的移动"""
        if self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:
                # 修改子弹的状态
                self.live = False
        elif self.direction == 'D':
            if self.rect.top + self.rect.height < SCREEN_HEIGHT:
                self.rect.top += self.speed
            else:
                # 修改子弹的状态
                self.live = False
        elif self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                # 修改子弹的状态
                self.live = False
        elif self.direction == 'R':
            if self.rect.left + self.rect.width < SCREEN_WIDTH:
                self.rect.left += self.speed
            else:
                # 修改子弹的状态
                self.live = False

    def displayBullet(self):
        """展示子弹的方法"""
        # 将图片surface加载到窗口
        MainGame.window.blit(self.image, self.rect)

    def myBullet_hit_enemyTank(self):
        """我方子弹与敌方坦克碰撞"""
        # 循环遍历敌方坦克列表，判断是否发生碰撞
        for enemyTank in MainGame.enemyTankList:
            if pygame.sprite.collide_rect(enemyTank, self):
                # 修改敌方坦克和我方子弹的状态
                enemyTank.live = False
                self.live = False
                # 创建爆炸对象
                explode = Explode(enemyTank)
                # 将爆炸对象添加到爆炸列表中
                MainGame.explodeList.append(explode)

    def enemyBullet_hit_myTank(self):
        """敌方子弹与我方坦克的碰撞"""
        if MainGame.my_tank and MainGame.my_tank.live:
            if pygame.sprite.collide_rect(MainGame.my_tank, self):
                # 产生爆炸对象
                explode = Explode(MainGame.my_tank)
                # 将爆炸对象添加到爆炸列表中
                MainGame.explodeList.append(explode)
                # 修改敌方子弹与我方坦克的状态
                self.live = False
                MainGame.my_tank.live = False

    def hitWall(self):
        """子弹是否碰撞墙壁"""
        # 循环遍历墙壁列表
        for wall in MainGame.wallList:
            if pygame.sprite.collide_rect(self, wall):
                # 修改子弹的生存状态，让子弹消失
                self.live = False
                # 墙壁的生命值减小
                wall.hp -= 1
                if wall.hp <= 0:
                    # 修改墙壁的生存状态
                    wall.live = False


class Wall:
    """墙壁类"""
    def __init__(self, left, top):
        # 加载墙壁图片
        self.image = pygame.image.load("img/steels.gif")
        # 获取墙壁的区域
        self.rect = self.image.get_rect()
        # 设置位置left和top
        self.rect.left = left
        self.rect.top = top
        # 是否存活
        self.live = True
        # 设置生命值为3
        self.hp = 5

    def displayWall(self):
        """展示墙壁的方法"""
        MainGame.window.blit(self.image, self.rect)


class Explode:
    """爆炸效果类"""
    def __init__(self, tank):
        # 爆炸的位置由当前子弹打中的坦克位置决定
        self.rect = tank.rect
        self.images = [pygame.image.load("img/blast0.gif"),
                       pygame.image.load("img/blast1.gif"),
                       pygame.image.load("img/blast2.gif"),
                       pygame.image.load("img/blast3.gif"),
                       pygame.image.load("img/blast4.gif")]
        self.step = 0
        self.image = self.images[self.step]
        # 是否活着
        self.live = True

    def displayExplode(self):
        """展示爆炸效果的方法"""
        if self.step < len(self.images):
            # 根据索引获取爆炸对象
            self.image = self.images[self.step]
            self.step += 1
            # 添加到主窗口
            MainGame.window.blit(self.image, self.rect)
        else:
            # 修改活着的状态
            self.live = False
            self.step = 0


class Music:
    """音乐类"""
    def __init__(self, filename):
        self.filename = filename
        # 初始化音乐混合器
        pygame.mixer.init()
        # 加载音乐
        pygame.mixer.music.load(self.filename)

    @staticmethod
    def play():
        """播放音乐的方法"""
        pygame.mixer.music.play()


if __name__ == "__main__":
    MainGame().startGame()
