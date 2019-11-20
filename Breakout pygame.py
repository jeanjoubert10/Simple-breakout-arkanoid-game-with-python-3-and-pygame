# Simply Breakout game using python 3 and pygame
# Using start screen as well as game over/restart game screen


import pygame
import random

# For using vectors
vec = pygame.math.Vector2

TITLE = 'Simple Breakout Game with Python 3 and Pygame'
WIDTH = 800
HEIGHT = 600
FPS = 120
FONT_NAME = 'arial'

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


class Player(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((90,20))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        
        # Position vector (x,y)
        self.pos = vec(400,560)
         
    def update(self):
       
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.pos.x <= 730 and self.pos.y >500:
            self.pos.x += 50
        if keys[pygame.K_LEFT] and self.pos.x >= 80 and self.pos.y > 500:
            self.pos.x -= 50
    
        self.rect.center = self.pos


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        ball_image = pygame.Surface((20, 20)) # radius x2
        pygame.draw.circle(ball_image, WHITE, (10,10), 10) # surface, color, (x,y), radius
        
        self.image = ball_image
        self.rect = self.image.get_rect() 
        
        # Position vector (x,y)
        self.pos = vec(400,300)
        self.vel = vec(17,21)
        
    def update(self):
        self.pos += self.vel
        
        if self.pos.x <=10 or self.pos.x>790:
            self.vel.x *= -1
            
        if self.pos.y <= 10:
            self.vel.y *= -1

        if self.pos.y >790:
            self.pos = vec(400,300)
            
        self.rect.center = self.pos
    

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = pygame.font.match_font(FONT_NAME)


    def new(self):
        # Start new game
        self.all_sprites = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.score = 0
        
        self.ball = Ball()
        self.player = Player(WHITE)
        self.all_sprites.add(self.ball)
        self.all_sprites.add(self.player)
        self.players.add(self.player)

        x_list = [50, 150, 250, 350, 450, 550, 650, 750]
        y_list = [20,50, 80, 110, 140, 170]

        for i in x_list:
            for j in y_list:
                enemy = Player(BLUE)
                enemy.pos = vec(i,j)
                self.all_sprites.add(enemy)
                self.enemy_list.add(enemy)
                
        
        # Run new game
        self.run()


    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
                
                
    def update(self):
        self.all_sprites.update()

        # Paddle check 
        hit_paddle = pygame.sprite.spritecollide(self.ball, self.players, False)
        if hit_paddle and self.ball.vel.y > 0: 
            self.ball.pos.y = 550  # Does not go into paddle
            self.ball.vel.y *= -1
            
        # hit enemies
        hit_enemy = pygame.sprite.spritecollide(self.ball, self.enemy_list, True)
        if hit_enemy and self.ball.pos.y > 25:
            self.ball.vel.y *= -1
            self.score += 1
        
        # Game over if no more enemies
        if len(self.enemy_list) == 0:
            self.playing = False

        
    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.draw_text('Score:  '+str(self.score),36, RED, WIDTH*3/4, 500)
        
        pygame.display.flip()

        
    def show_start_screen(self):
        self.screen.fill(BLACK)
        self.draw_text('Breakout with Python3 and Pygame', 36, RED, WIDTH/2, HEIGHT/3)
        self.draw_text('Press any key to begin', 24, WHITE, WIDTH/2, HEIGHT/2)
        pygame.display.flip()
        self.wait_for_key()


    def show_game_over_screen(self):
        # game over/continue
        if not self.running:
            return
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", 48, RED, WIDTH / 2, HEIGHT / 4)
        self.draw_text('Score:  '+str(self.score),36, RED, WIDTH/2, HEIGHT/2)
        self.draw_text("Press a key to play again", 26, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pygame.display.flip()
        self.wait_for_key()


    def wait_for_key(self): # Wait for key press in start/game over screen
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False


    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
  
    
game = Game()
game.show_start_screen()

while game.running:
    game.new()
    game.show_game_over_screen()


pygame.quit()



