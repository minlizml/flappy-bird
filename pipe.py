import pygame

#继承sprite这个类别
class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,img,top):
        super().__init__()
        self.image=img  #要显示的图片
        self.speedx=4
        self.rect=self.image.get_rect()  #把图片框起来做定位（9个点坐标）
        self.bird_pass=False
        if top:
            self.rect.bottomleft=(x,y)
        else:
            self.rect.topleft=(x,y)


    def update(self):
        self.rect.x-=self.speedx
        if self.rect.right<0:  #把跑出边界的管子删掉，以免占用内存
            self.kill() #来自sprite里面的函数
