import pygame

#继承sprite这个类别
class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y,imgs):
        super().__init__()
        self.origin_x=x
        self.origin_y=y
        self.imgs=imgs
        self.img_index=0
        self.image=imgs[self.img_index]  #要显示的图片,且根据鸟向上还是向下飞调整飞翔角度
        self.rect=self.image.get_rect()  #把图片框起来做定位（9个点坐标）
        self.rect.center=(x,y)
        self.last_pic_time=pygame.time.get_ticks()  #取得pygame.init后经过的时间的毫秒数
        self.img_frequency=200 #多久切换一次图片
        self.speedy=0
        self.ground_top=500
        self.fly=True

    def update(self):
        #飞翔动画
        if self.fly:
            now=pygame.time.get_ticks()
            if now-self.last_pic_time>self.img_frequency:
                self.img_index+=1
                #判断如果index已经大于图片类别的长度，就切换回第一张
                if self.img_index>=len(self.imgs):
                    self.img_index=0
                self.image=pygame.transform.rotate(self.imgs[self.img_index],-self.speedy) #要显示的图片,且根据鸟向上还是向下飞调整飞翔角度，顺时针为负
                self.last_pic_time=now

        #鸟收到地心引力
        self.speedy+=0.5
        if self.speedy>9:  #设置一个最大下降速度
            self.speedy=9
        self.rect.y+=self.speedy

        #鸟撞到管子之后掉下来不能穿过地板
        if self.rect.bottom>self.ground_top:
            self.rect.bottom = self.ground_top


    def jump(self):
        self.speedy=-6

    #掉下来之后停止飞翔
    def game_over(self):
        self.fly=False
        self.image=pygame.transform.rotate((self.imgs[self.img_index]),-90)  #鸟撞到之后头部朝下

    def reset(self):
        self.img_index = 0
        self.image = self.imgs[self.img_index]
        self.rect.center = (self.origin_x, self.origin_y)
        self.last_pic_time = pygame.time.get_ticks()  # 取得pygame.init后经过的时间的毫秒数
        self.speedy = 0
        self.fly = True