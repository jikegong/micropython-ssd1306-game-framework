class Sprite:
    def __init__(self,img,x,y,vx=0,vy=0):
        self.x=x
        self.y=y
        self.vx=vx
        self.vy=vy
        self.setimg(img)
        self.life=1
        
    def setimg(self,img):
        img=img.split('\n')
        img.pop(0)
        img.pop(len(img)-1)
        self.img=img
        self.w=len(img[0])
        self.h=len(img)
        
    def update(self):
        self.x+=self.vx
        self.y+=self.vy
        
    def render(self,display):
        y=0
        for line in self.img:
            x=0
            for char in line:
                if int(char)==1:
                    display.pixel(self.x+x,self.y+y,1)
                x+=1
            y+=1