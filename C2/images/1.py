import pygame

pygame.init()

def crop_circle(image):
    size = image.get_size()
    mask = pygame.Surface(size,pygame.SRCALPHA)
    mask.fill((0,0,0,0))
    pygame.draw.circle(mask,(255,255,255,255),(size[0] // 2,size[1] // 2),size[0] // 2)
    result = image.copy()
    result.blit(mask,(0,0),special_flags=pygame.BLEND_RGBA_MIN)
    return result

screen = pygame.display.set_mode((650,730))
black_piece = pygame.image.load("my1.png")
white_piece = pygame.image.load("my2.png")

black_piece = pygame.transform.scale(black_piece,(30,30))
white_piece = pygame.transform.scale(white_piece,(30,30))

#black_piece = crop_circle(black_piece)
#white_piece = crop_circle(white_piece)#裁剪为圆的棋子

width = 45
left = 10
right = 640

#设置大小（分辨率）
map = [0]*25
for i in range(25):
    map[i] = [0]*25

player = 1
winner = 0

#running = True

font = pygame.font.Font(None,28)

class Button:
    def clicking (self,event,game):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):#按在按钮位置才触发
                if (self.clicked):
                    #self.clicked = False
                    print("游戏开始了")
                else:
                    if game.winner == 0:
                        self.clicked = True
                        game.started = True 
                        print("点击——开始")
                    else:
                        self.clicked = True
                        game.started = True
                        game.player = 1
                        game.winner = 0
                        game.map = [0]*25
                        for i in range(25):
                            game.map[i] = [0]*15
                        print("点击——重新开始")
                        

    def __init__(self,x,y,width,height,text,color,click_color,text_color) -> None:#按钮坐标，颜色，点击后颜色
        self.text = text
        self.color = color
        self.click_color = click_color
        self.text_color = text_color
        self.rect = pygame.Rect(x,y,width,height)
        self.clicked = False
    def draw(self,screen):
        if self.clicked:
            pygame.draw.rect(screen,self.click_color,self.rect)
        else:
            pygame.draw.rect(screen,self.color,self.rect)

        text_surface = font.render(self.text,True,self.text_color)#设定颜色
        text_position = (text_surface.get_rect(center = self.rect.center))
        screen.blit(text_surface,text_position)

class Game:
    
    def check(self,row,col):
        score = 1
        for i in range(4):
            try:
                if self.map[row][col+i] == self.map[row][col+i+1]:
                    score = score + 1
                else:
                    break
            except:
                break
        for i in range(4):
            try:
                if self.map[row][col-i] == self.map[row][col-i-1]:
                    score = score + 1
                else:
                    break
            except:
                break
        if score >= 5:
            return True
        score = 1
        for i in range(4):
            try:
                if self.map[row+i][col] == self.map[row+i+1][col]:
                    score = score + 1
                else:
                    break
            except:
                break
        for i in range(4):
            try:
                if self.map[row-i][col] == self.map[row-i-1][col]:
                    score = score + 1
                else:
                    break
            except:
                break
        if score >= 5:
            return True
        score = 1
        for i in range(4):
            try:
                if self.map[row+i][col+i] == self.map[row+i+1][col+i+1]:
                    score = score + 1
                else:
                    break
            except:
                break
        for i in range(4):
            try:
                if self.map[row-i][col-i] == self.map[row-i-1][col-i-1]:
                    score = score + 1
                else:
                    break
            except:
                break
        if score >= 5:
            return True
        score = 1
        for i in range(4):
            try:
                if self.map[row+i][col-i] == self.map[row+i+1][col-i-1]:
                    score = score + 1
                else:
                    break
            except:
                break
        for i in range(4):
            try:
                if self.map[row-i][col+i] == self.map[row-i-1][col+i+1]:
                    score = score + 1
                else:
                    break
            except:
                break
        if score >= 5:
            return True

    def __init__(self) -> None:
        self.started = False
        self.player = 1
        self.winner = 0
        self.map = [0]*25
        for i in range(25):
            self.map[i] = [0]*25
    
    def start(self):
        screen.fill("#EE9A48")
        for x in range(15):#15行15列
            pygame.draw.line(screen,"#000000",[left+width*x,left],[left+width*x,right],2)#绘制黑色竖线  三个参数：起始，终止，宽度
            pygame.draw.line(screen,"#000000",[left,left+width*x],[right,left+width*x],2)

        pygame.draw.circle(screen,"#000000",[left+width*7,left+width*7],8)#标注棋盘中心

        x,y = pygame.mouse.get_pos()
        x = round((x-left)/width)*width+left
        y = round((y-left)/width)*width+left#计算对应点
        if x >= left and x <= right and y >=left and y <=right:
            pygame.draw.rect(screen,"#FFFFFF",[x-width/2,y-width/2,width,width],2)#显示鼠标位置

        button.draw(screen)

        for row in range(15):
            for col in range(15):
                    if self.map[row][col] == 1:
                        screen.blit(black_piece,(col*width-5,row*width-5))
                        #pygame.draw.circle(screen,"#000000",[col*50+25,row*50+25],15)
                    elif self.map[row][col] == 2:
                        screen.blit(white_piece,(col*width-5,row*width-5))
                        #pygame.draw.circle(screen,"#FFFFFF",[col*50+25,row*50+25],15)
        
        if (self.winner!=0):
            if self.winner == 1:
                color = (0,0,0)
                text = 'black wins!'
            else:
                color = (255,255,255)
                text = 'white wins!'
            font = pygame.font.Font(None,70)
            text_surface = font.render(text,True,color)#设定颜色
            text_position = (200,200)
            screen.blit(text_surface,text_position)
            pygame.display.update()
            pygame.time.wait(500)#3s后关闭
            button.clicked = False

    def mouse_Click(self,x,y):
        if x >= left and x <= right and y >=left and y <=right:
            if self.started:
                col = round((x-left)/width)
                row = round((y-left)/width)
                if self.map[row][col] == 0:
                    #print(row,col)
                    self.map[row][col] = self.player#下了一个子
                    if(self.check(row,col)):
                        self.winner = self.player
                        print(player)
                    else:
                        if self.player == 1:
                            self.player = 2
                        else:
                            self.player = 1
                else:
                    print("已有棋子，请勿乱搞")
            else:
                print("游戏还没开始")


button = Button(35,660,100,50,"two player",(153,51,250),(221,160,221),(255,255,255))
game=Game()
game.__init__()
while True:
    for event in pygame.event.get():
        button.clicking(event,game)
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:#若按下
            x,y = pygame.mouse.get_pos()
            game.mouse_Click(x,y)

    game.start()
    pygame.display.update()#设置棋盘背景颜色


