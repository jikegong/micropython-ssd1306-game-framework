from machine import Pin,I2C
from time import sleep_ms,sleep
import ssd1306

def horizontal_overlap(char, obj):
    return char.x + char.w > obj.x and char.x < obj.x + obj.w
def vertical_overlap(char, obj):
    return obj.y + obj.h > char.y and obj.y < char.y + char.h

class Game:
    def __init__(self,width=128,height=32,scl=5,sda=4):
        i2c = I2C(scl=Pin(scl), sda=Pin(sda), freq=100000)
        self.display = ssd1306.SSD1306_I2C(width, height, i2c)
        self.width=width
        self.height=height
        self.player={}
        self.enemys=[]
        self.foods=[]
        self.bullets=[]
        self.bgs=[]
        self.gameover=False
        self.score=0
    def clear(self):
        self.display.fill(0)
    def set_player_sprite(self,sprite):
        self.player=sprite
        self.bak_player=sprite
    def add_bullets_sprite(self,sprite):
        self.bullets.append(sprite)
    def add_foods_sprite(self,sprite):
        self.foods.append(sprite)
    def add_enemy_sprite(self,sprite):
        self.enemys.append(sprite)
    def add_bg_sprite(self,sprite):
        self.bgs.append(sprite)

    def on_player_collision_with_food(self,player,food):
        pass
    def on_player_collision_with_enemy(self,player,enemy):
        pass
    def on_enemy_collision_with_food(self,enemy,food):
        pass
    def on_bullet_collision_with_enemy(self,bullet,enemy):
        pass
    
    def collision(self):
        # player vs enemy
        for enemy in self.enemys:
            if horizontal_overlap(self.player, enemy) and vertical_overlap(self.player, enemy):
                self.on_player_collision_with_enemy(self.player,enemy)
        
        # player vs food
        for food in self.foods:
            if horizontal_overlap(self.player, food) and vertical_overlap(self.player, food):
                self.on_player_collision_with_food(self.player,food)
        
        # bullet vs enemy
        for bullet in self.bullets:
            for enemy in self.enemys:
                if horizontal_overlap(bullet, enemy) and vertical_overlap(bullet, enemy):
                    self.on_bullet_collision_with_enemy(bullet,enemy)
        
        # enemy vs food
        for food in self.foods:
            for enemy in self.enemys:
                if horizontal_overlap(enemy,food) and vertical_overlap(enemy,food):
                    self.on_enemy_collision_with_food(enemy,food)
    
    def update(self):
        for enemy in self.enemys:
            enemy.update()
            if enemy.life==0:
                self.enemys.remove(enemy)
        for food in self.foods:
            food.update()
            if food.life==0:
                self.foods.remove(food)
        for bullet in self.bullets:
            bullet.update()
            if bullet.life==0:
                self.bullets.remove(bullet)
        for bg in self.bgs:
            bg.update()
        self.player.update()
        self.collision()
        if self.player.life==0:
            self.gameover=True
        
    def show(self):
        self.display.show()
    def render(self):
        self.clear()
        for enemy in self.enemys:
            enemy.render(self.display)
        for food in self.foods:
            food.render(self.display)
        for bullet in self.bullets:
            bullet.render(self.display)
        for bg in self.bgs:
            bg.render(self.display)
        self.player.render(self.display)
        score_x = 128 - len(str(self.score))*8
        self.display.text(str(self.score),score_x,2)
        self.show()
    def waiting_input_when_gameover(self):
        pass
    def start(self):
        while True:
            sleep_ms(10)
            if self.gameover==False:
                self.update()
                self.render()
            else:
                self.clear
                self.display.text('game over',20,16)
                self.show()
                self.waiting_input_when_gameover()
    def restart(self):
        print('restart')
        if self.gameover==True:
            self.enemys=[]
            self.foods=[]
            self.bullets=[]
            self.score=0
            self.player=self.bak_player
            self.gameover=False
        