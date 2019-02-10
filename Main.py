# kmj0205 - https://github.com/kmj0205
# Space Ship Game - Kmj0205

import pygame 
import random

WIDTH = 480
HEIGHT = 600
FPS = 60

# 색 코트 지정
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# 게임을 실행하기위해 기본적인 준비
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Ship Game - Kmj0205")
clock = pygame.time.Clock()

def draw_text(arg, x, y, color):
    font = pygame.font.Font(None, 24)
    text = font.render(str(arg).zfill(0), True, (color)) 
    text_rect = text.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    screen.blit(text, text_rect)

class SpaceShip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(spaceship_img, (50,38)) 
        self.rect = self.image.get_rect()
        self.radius = 25
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0 
        self.hp = 100

    def update(self):
        self.speedx = 0
        self.speedy = 0
        #키보드로 플레이어 제어
        keysrate = pygame.key.get_pressed()
        if keysrate[pygame.K_a]:
            self.speedx = -6
            print("[keyInput] keypressed (a)")
        if keysrate[pygame.K_d]:
            self.speedx = 6
            print("[keyInput] keypressed (d)")
        if keysrate[pygame.K_w]:
            self.speedy = -4
            print("[keyInput] keypressed (w)")  
        if keysrate[pygame.K_s]: 
            self.speedy = 6
            print("[keyInput] keypressed (s)")
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH: 
            self.rect.right = WIDTH 
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom < 0:
            self.rect.bottom = 0
    
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(laser_img, (10,40))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
    
    def update(self):
        self.rect.y += self.speedy
        # 총알이 화면 밖으로 나가면 제거
        if self.rect.bottom < 0:
            self.kill()

class Mop(pygame.sprite.Sprite):
    def __init__(self):
        global score_event
        pygame.sprite.Sprite.__init__(self)
        random_asteroid_num = random.randrange(1, 21)
        if score_event == 1:
            self.image_orig = pygame.transform.scale(asteroid5_img, (160, 160))
        else:
            if random_asteroid_num < 7:
                self.image_orig = pygame.transform.scale(asteroid1_img, (35, 35))
            elif random_asteroid_num < 13:
                self.image_orig = pygame.transform.scale(asteroid2_img, (45, 45))
            elif random_asteroid_num < 19:
                self.image_orig = pygame.transform.scale(asteroid3_img, (45, 45))
            else:
                self.image_orig = pygame.transform.scale(asteroid4_img, (65, 65))
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        if score_event == 1:
            self.rect.x = 240
            self.rect.y = -200
            self.speedy = 0
            self.speedx = 1
            self.rot = 0
            self.rot_speed = 0
        else:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = -50
            self.speedy = random.randrange(5, 10)
            self.speedx = random.randrange(-2, 2)
            self.rot = 0
            self.rot_speed = random.randrange(-10, 10)
        self.last_update = pygame.time.get_ticks()
        score_event = 0
    
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 2:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(5, 10)

# 게임 오디오 불러오기
background_music = pygame.mixer.Sound("./resource/audio/BackgroundMusic.wav")
down_sound = pygame.mixer.Sound("./resource/audio/DownSound.wav")
up_sound = pygame.mixer.Sound("./resource/audio/UpSound.wav")
laser_sound = pygame.mixer.Sound("./resource/audio/LaserSound.wav")
spaceship_crash_sound = pygame.mixer.Sound("./resource/audio/SpaceShipCrashSound.wav")
spaceship_Explosion_sound = pygame.mixer.Sound("./resource/audio/SpaceShipExplosionSound.wav")
asteroid_Explosion_sound = pygame.mixer.Sound("./resource/audio/AsteroidExplosionSound.wav")
spaceship_warning_sound = pygame.mixer.Sound("./resource/audio/SpaceShipWarningSound.wav")
background_music.set_volume(0.1)
down_sound.set_volume(0.1)
up_sound.set_volume(0.1)
laser_sound.set_volume(0.3)
spaceship_warning_sound.set_volume(0.1)
spaceship_crash_sound.set_volume(0.1)
spaceship_Explosion_sound.set_volume(0.1)
asteroid_Explosion_sound.set_volume(0.7)
background_music.play() 
# 게임 이미지 불러오기
background_img = pygame.image.load("./resource/img/SpaceBackground.png")
background_img_rect = background_img.get_rect()
spaceship_img = pygame.image.load("./resource/img/Ship.png")
laser_img = pygame.image.load("./resource/img/RedLaser.png")
asteroid1_img = pygame.image.load("./resource/img/Asteroid1.png")
asteroid2_img = pygame.image.load("./resource/img/Asteroid2.png")
asteroid3_img = pygame.image.load("./resource/img/Asteroid3.png")
asteroid4_img = pygame.image.load("./resource/img/Asteroid4.png")
asteroid5_img = pygame.image.load("./resource/img/Asteroid5.png")

# 게임 오브젝트 설정
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = SpaceShip()
all_sprites.add(player)

# 게임 사용 변수
score = 0
count = 0
bullet_amount = 10
hp_event_color = YELLOW
score_event = 0
next_score_event = 2500

for i in range(10):
    m = Mop()
    all_sprites.add(m)
    mobs.add(m)

# 게임 루프
running = True
while running:
    # 루프가 원하는 속도로 돌수 있도록 만듬
    clock.tick(FPS)
    count += 1
    if count > 30:
        count = 0
        score += 10
    # 스코어 이벤트 
    if score > next_score_event:
        next_score_event += 2500
        score_event = 1
        bullet_amount += 5
    # 프로세스 인풋 or 이벤트
    for event in pygame.event.get():
        # (게임 창의 X 버튼)을 눌렀을때 게임을 정지
        if event.type == pygame.QUIT:
            running = False
        # (키보드 q 키)를 눌렀을때 게임을 일시 정지
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                print("[keyInput] keypressed (q)")
                Pause = True
                while Pause:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            print("[keyInput] keypressed (q)")
                            Pause = False
        # 플레이어가 총알을 발사시킬때
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("[keyInput] keypressed (SPACE)")
                if bullet_amount > 0:
                    bullet_amount -= 1
                    laser_sound.play()  
                    player.shoot()
            if event.key == pygame.K_SLASH:
                print("[keyInput] keypressed (/)")
                score += 500

    # 업데이트
    all_sprites.update()

    # 몹과 총알이 충돌 했는지 채크
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        bullet_amount += 2
        asteroid_Explosion_sound.play()
        score += 50
        m = Mop()
        all_sprites.add(m)
        mobs.add(m)
    
    # 몹과 플레이어가 충돌 했는지 채크
    hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
    if hits:
        if player.hp > 1:
            spaceship_crash_sound.play()
            player.hp -= 1
            if bullet_amount > 0:
                bullet_amount -= 1
            print("[system] Player Life : " + str(player.hp))
        else:
            running = False
    
    # 그리기 / 랜더러
    screen.fill(BLACK)
    screen.blit(background_img, background_img_rect)
    all_sprites.draw(screen)
    # 점수,목슴,총알갯수 표시
    if count == 1:
        if player.hp < 10:
            if hp_event_color == RED:
                hp_event_color = YELLOW
            else:
                hp_event_color = RED
                spaceship_warning_sound.play()
    draw_text("[ Hp : " + str(player.hp) + " ]", 45, 18, hp_event_color)
    draw_text(score, WIDTH / 2, 18, WHITE)
    draw_text("[ Bullet : " + str(bullet_amount) + " ]", 56, 34, GREEN)
    # 모든것을 그리거나 랜더러 시킨후 화면을 플립 시킴
    pygame.display.flip()
# 파이 게임 나가기 
pygame.quit()