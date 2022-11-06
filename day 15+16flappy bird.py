import pygame
import random
from bird import Bird
from pipe import Pipe




pygame.init()


def generate_pipes(last_pipe_time, pipe_frequency, pipe_group):
    now=pygame.time.get_ticks()
    if now-last_pipe_time>=pipe_frequency:
        random_height=random.randint(-100,100)  #产生随机高度的管子
        pipe_btm = Pipe(SCREEN_WIDTH, SCREEB_HEIGHT / 2 + 75+random_height, pipe_img, False)
        pipe_top = Pipe(SCREEN_WIDTH, SCREEB_HEIGHT / 2 - 75+random_height, flip_pipe_img, True)
        pipe_group.add(pipe_btm)
        pipe_group.add(pipe_top)
        return now
    return last_pipe_time

def draw_scores():
    score_text=score_font.render(str(score),True,WHITE)
    window.blit(score_text,(SCREEN_WIDTH/2-score_text.get_width()/2,20))

#设定常数
FPS=60
SCREEN_WIDTH=780
SCREEB_HEIGHT=600
WHITE=(255,255,255)

window=pygame.display.set_mode((SCREEN_WIDTH,SCREEB_HEIGHT))
pygame.display.set_caption('可爱的鸟鸟')
clock=pygame.time.Clock()

bg_img=pygame.image.load('img/bg.png')
bg_img=pygame.transform.scale(bg_img,(780,600))#调整图片大小

ground_img=pygame.image.load('img/ground.png')
pipe_img=pygame.image.load('img/pipe.png')
restart_img=pygame.image.load('img/restart.png')
#颠倒图片,FALSE代表垂直翻转
flip_pipe_img=pygame.transform.flip(pipe_img,False,True)
bird_imgs=[]
for i in range(1,3):
    bird_imgs.append(pygame.image.load(f'img/bird{i}.png'))


pygame.display.set_icon(bird_imgs[0])  #改掉视窗的图标

#载入字体
score_font=pygame.font.Font('微软正黑体.ttf',60)


#游戏变数
ground_speed=4
ground_x=0
pipe_frequency=1500
last_pipe_time=pygame.time.get_ticks()-pipe_frequency#可以让管子第一次出现的时候不用等太久
game_over=False
score=0

bird=Bird(100,SCREEB_HEIGHT/2,bird_imgs) #创建三个鸟的objects
bird_group=pygame.sprite.Group()  #创建一个游戏物件群组
bird_group.add(bird)


#pipe_btm=Pipe(SCREEN_WIDTH,SCREEB_HEIGHT/2+75,pipe_img,False)
#pipe_top=Pipe(SCREEN_WIDTH,SCREEB_HEIGHT/2-75,flip_pipe_img,True)
pipe_group=pygame.sprite.Group()  #必须是全局变量，所以不能放在函数下面
#pipe_sprite.add(pipe_btm)
#pipe_sprite.add(pipe_top)


run=True
while run:
    clock.tick(FPS)

    #---取得输入---
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
             run=False
        elif event.type==pygame.MOUSEBUTTONDOWN:
            if event.button==1 and not game_over:
                bird.jump()
        #重置游戏
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE and game_over:
                game_over=False
                score=0
                last_pipe_time = pygame.time.get_ticks() - pipe_frequency
                bird.reset()
                for pipe in pipe_group.sprites():
                    pipe.kill()
    #判断鼠标按键没有一直被按住
    #buttons=pygame.mouse.get_pressed() #印出鼠标左键中键和右键有没有被按住的布林值元组
    #if buttons[0]:



    #---画面更新---
    bird_group.update()#呼叫bird_sprite这个群组里面所有的update方法
    if not game_over:
        pipe_group.update()
        last_pipe_time=generate_pipes(last_pipe_time, pipe_frequency, pipe_group)
        #判断通过管子
        if not pipe_group.sprites()[0].bird_pass:
            if pipe_group.sprites()[0].rect.right<bird.rect.left:
                score+=1
                pipe_group.sprites()[0].bird_pass=True
        #移动底板
        ground_x-=ground_speed
        if ground_x<-100:
            ground_x=0

    #碰撞判断
        # 会回传一个字典，没碰到就是空字典//布林值表示碰到的群组要不要删除掉
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or \
        bird.rect.top<=0 or \
        bird.rect.bottom>=500:
        game_over=True
        bird.game_over()


    #---画面显示---
    window.blit(bg_img,(0,0))
    bird_group.draw(window)  #把鸟画上去
    pipe_group.draw(window)
    window.blit(ground_img,(ground_x,500))
    draw_scores()
    if game_over:
        window.blit(restart_img,(SCREEN_WIDTH/2-restart_img.get_width()/2,SCREEB_HEIGHT/2-restart_img.get_height()/2))
    pygame.display.update()




pygame.quit()