import pygame
import random
import math
import json
import os
from enum import Enum

# 初始化pygame
pygame.init()
pygame.mixer.init()

# 游戏常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 120, 255)
YELLOW = (255, 255, 0)
PURPLE = (180, 0, 255)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)

# 游戏状态枚举
class GameState(Enum):
    MENU = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4
    SHOP = 5

# 武器类型枚举
class WeaponType(Enum):
    SINGLE = 1
    DOUBLE = 2
    TRIPLE = 3
    SPREAD = 4
    LASER = 5

# 粒子类
class Particle:
    def __init__(self, x, y, color, velocity, life, size=2):
        self.x = x
        self.y = y
        self.color = color
        self.velocity = velocity
        self.life = life
        self.max_life = life
        self.size = size
        
    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.life -= 1
        self.size *= 0.98
        
    def draw(self, screen):
        if self.life > 0:
            alpha = int(255 * (self.life / self.max_life))
            color_with_alpha = (*self.color[:3], alpha)
            surf = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
            pygame.draw.circle(surf, color_with_alpha, (self.size, self.size), self.size)
            screen.blit(surf, (self.x - self.size, self.y - self.size))

# 爆炸效果类
class Explosion:
    def __init__(self, x, y, size=30):
        self.x = x
        self.y = y
        self.particles = []
        self.create_particles(size)
        
    def create_particles(self, size):
        colors = [RED, ORANGE, YELLOW, WHITE]
        for _ in range(size * 2):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 5)
            velocity = (math.cos(angle) * speed, math.sin(angle) * speed)
            color = random.choice(colors)
            life = random.randint(20, 40)
            self.particles.append(Particle(self.x, self.y, color, velocity, life))
            
    def update(self):
        for particle in self.particles[:]:
            particle.update()
            if particle.life <= 0:
                self.particles.remove(particle)
                
    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)
            
    def is_finished(self):
        return len(self.particles) == 0

# 星星背景类
class StarField:
    def __init__(self, num_stars=100):
        self.stars = []
        for _ in range(num_stars):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            speed = random.uniform(0.5, 2)
            brightness = random.randint(100, 255)
            self.stars.append([x, y, speed, brightness])
            
    def update(self):
        for star in self.stars:
            star[1] += star[2]  # 向下移动
            if star[1] > SCREEN_HEIGHT:
                star[1] = 0
                star[0] = random.randint(0, SCREEN_WIDTH)
                
    def draw(self, screen):
        for star in self.stars:
            color = (star[3], star[3], star[3])
            pygame.draw.circle(screen, color, (int(star[0]), int(star[1])), 1)

# 玩家飞船类
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.speed = 5
        self.health = 100
        self.max_health = 100
        self.shield = 0
        self.max_shield = 100
        self.weapon_type = WeaponType.SINGLE
        self.weapon_level = 1
        self.invincible_time = 0
        self.thruster_particles = []
        
    def update(self):
        keys = pygame.key.get_pressed()
        
        # 移动控制
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < SCREEN_HEIGHT - self.height:
            self.y += self.speed
            
        # 更新无敌时间
        if self.invincible_time > 0:
            self.invincible_time -= 1
            
        # 生成推进器粒子
        if random.random() < 0.3:
            self.thruster_particles.append(Particle(
                self.x + self.width//2 + random.randint(-5, 5),
                self.y + self.height,
                ORANGE,
                (random.uniform(-0.5, 0.5), random.uniform(1, 3)),
                20,
                random.uniform(1, 3)
            ))
            
        # 更新推进器粒子
        for particle in self.thruster_particles[:]:
            particle.update()
            if particle.life <= 0:
                self.thruster_particles.remove(particle)
    
    def take_damage(self, damage):
        if self.invincible_time <= 0:
            if self.shield > 0:
                self.shield -= damage
                if self.shield < 0:
                    self.health += self.shield
                    self.shield = 0
            else:
                self.health -= damage
            self.invincible_time = 60  # 1秒无敌时间
            return True
        return False
    
    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)
    
    def add_shield(self, amount):
        self.shield = min(self.max_shield, self.shield + amount)
    
    def upgrade_weapon(self):
        if self.weapon_type == WeaponType.SINGLE:
            self.weapon_type = WeaponType.DOUBLE
        elif self.weapon_type == WeaponType.DOUBLE:
            self.weapon_type = WeaponType.TRIPLE
        elif self.weapon_type == WeaponType.TRIPLE:
            self.weapon_type = WeaponType.SPREAD
        elif self.weapon_type == WeaponType.SPREAD:
            self.weapon_type = WeaponType.LASER
    
    def get_bullets(self):
        bullets = []
        center_x = self.x + self.width // 2
        center_y = self.y
        
        if self.weapon_type == WeaponType.SINGLE:
            bullets.append(Bullet(center_x, center_y, 0, -8, YELLOW, 3))
            
        elif self.weapon_type == WeaponType.DOUBLE:
            bullets.append(Bullet(center_x - 10, center_y, 0, -8, YELLOW, 3))
            bullets.append(Bullet(center_x + 10, center_y, 0, -8, YELLOW, 3))
            
        elif self.weapon_type == WeaponType.TRIPLE:
            bullets.append(Bullet(center_x, center_y, 0, -8, YELLOW, 3))
            bullets.append(Bullet(center_x - 15, center_y, 0, -8, YELLOW, 3))
            bullets.append(Bullet(center_x + 15, center_y, 0, -8, YELLOW, 3))
            
        elif self.weapon_type == WeaponType.SPREAD:
            for angle in [-15, 0, 15]:
                rad = math.radians(angle)
                bullets.append(Bullet(
                    center_x, center_y,
                    math.sin(rad) * 8,
                    -math.cos(rad) * 8,
                    CYAN,
                    4
                ))
                
        elif self.weapon_type == WeaponType.LASER:
            bullets.append(LaserBeam(center_x, center_y, 0, -12, BLUE, 6))
            
        return bullets
    
    def draw(self, screen):
        # 绘制推进器粒子
        for particle in self.thruster_particles:
            particle.draw(screen)
            
        # 绘制飞船（简单的三角形）
        points = [
            (self.x + self.width//2, self.y),
            (self.x, self.y + self.height),
            (self.x + self.width//4, self.y + self.height - 10),
            (self.x + 3*self.width//4, self.y + self.height - 10),
            (self.x + self.width, self.y + self.height)
        ]
        
        # 无敌状态时闪烁效果
        if self.invincible_time > 0 and self.invincible_time % 10 < 5:
            color = WHITE
        else:
            color = GREEN
            
        pygame.draw.polygon(screen, color, points)
        
        # 绘制引擎火焰
        flame_colors = [RED, ORANGE, YELLOW]
        for i in range(3):
            flame_points = [
                (self.x + self.width//4 + i*5, self.y + self.height),
                (self.x + self.width//4 + i*5 + 5, self.y + self.height + 10),
                (self.x + self.width//4 + i*5 + 10, self.y + self.height)
            ]
            pygame.draw.polygon(screen, flame_colors[i], flame_points)
            
        # 绘制血条和护盾条
        bar_width = 60
        bar_height = 8
        bar_x = self.x - 10
        bar_y = self.y - 20
        
        # 护盾条
        if self.shield > 0:
            shield_ratio = self.shield / self.max_shield
            pygame.draw.rect(screen, BLUE, (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(screen, CYAN, (bar_x, bar_y, bar_width * shield_ratio, bar_height))
            pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 1)
            bar_y -= 12
            
        # 血条
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, bar_width * health_ratio, bar_height))
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 1)

# 子弹类
class Bullet:
    def __init__(self, x, y, vx, vy, color, damage=1):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.damage = damage
        self.radius = 3
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        
    def is_off_screen(self):
        return (self.x < 0 or self.x > SCREEN_WIDTH or 
                self.y < 0 or self.y > SCREEN_HEIGHT)
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius - 1)

# 激光束类
class LaserBeam:
    def __init__(self, x, y, vx, vy, color, damage=2):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.damage = damage
        self.width = 4
        self.height = 15
        self.trail = []  # 拖尾效果
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        
        # 添加拖尾
        self.trail.append((self.x, self.y))
        if len(self.trail) > 5:
            self.trail.pop(0)
        
    def is_off_screen(self):
        return (self.x < 0 or self.x > SCREEN_WIDTH or 
                self.y < 0 or self.y > SCREEN_HEIGHT)
    
    def draw(self, screen):
        # 绘制拖尾
        for i, pos in enumerate(self.trail):
            alpha = int(255 * (i / len(self.trail)))
            surf = pygame.Surface((self.width * 2, self.height), pygame.SRCALPHA)
            color_with_alpha = (*self.color[:3], alpha)
            pygame.draw.rect(surf, color_with_alpha, (0, 0, self.width * 2, self.height))
            screen.blit(surf, (pos[0] - self.width, pos[1]))
        
        # 绘制激光本体
        pygame.draw.rect(screen, self.color, 
                        (self.x - self.width//2, self.y, self.width, self.height))
        pygame.draw.rect(screen, WHITE, 
                        (self.x - self.width//2, self.y, self.width, self.height), 1)

# 敌人类
class Enemy:
    def __init__(self, enemy_type):
        self.type = enemy_type
        self.setup_enemy()
        
    def setup_enemy(self):
        if self.type == "basic":
            self.width = 30
            self.height = 30
            self.health = 20
            self.speed = 2
            self.score_value = 10
            self.color = RED
            self.shoot_chance = 0.005
            
        elif self.type == "fast":
            self.width = 25
            self.height = 25
            self.health = 15
            self.speed = 4
            self.score_value = 15
            self.color = ORANGE
            self.shoot_chance = 0.003
            
        elif self.type == "tank":
            self.width = 50
            self.height = 50
            self.health = 100
            self.speed = 1
            self.score_value = 50
            self.color = PURPLE
            self.shoot_chance = 0.01
            
        elif self.type == "boss":
            self.width = 80
            self.height = 80
            self.health = 500
            self.speed = 1
            self.score_value = 500
            self.color = (150, 0, 150)
            self.shoot_chance = 0.02
            self.move_pattern = "zigzag"
            self.move_timer = 0
            
        self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.y = -self.height
        self.shoot_timer = 0
        
    def update(self):
        self.y += self.speed
        
        # Boss特殊移动模式
        if self.type == "boss":
            self.move_timer += 1
            if self.move_pattern == "zigzag":
                self.x += math.sin(self.move_timer * 0.1) * 3
                
        self.shoot_timer += 1
        
    def can_shoot(self):
        if self.shoot_timer > 60:  # 每秒最多射击一次
            self.shoot_timer = 0
            return random.random() < self.shoot_chance
        return False
    
    def get_bullets(self):
        bullets = []
        center_x = self.x + self.width // 2
        center_y = self.y + self.height
        
        if self.type == "boss":
            # Boss发射多发子弹
            for angle in [-30, -15, 0, 15, 30]:
                rad = math.radians(angle)
                bullets.append(EnemyBullet(
                    center_x, center_y,
                    math.sin(rad) * 3,
                    math.cos(rad) * 3,
                    PURPLE
                ))
        else:
            bullets.append(EnemyBullet(center_x, center_y, 0, 3, self.color))
            
        return bullets
    
    def draw(self, screen):
        # 绘制敌人主体
        pygame.draw.rect(screen, self.color, 
                        (self.x, self.y, self.width, self.height))
        
        # 绘制敌人细节
        if self.type == "basic":
            pygame.draw.polygon(screen, BLACK, [
                (self.x + self.width//2, self.y + 5),
                (self.x + 5, self.y + self.height - 5),
                (self.x + self.width - 5, self.y + self.height - 5)
            ])
            
        elif self.type == "tank":
            # 坦克履带
            pygame.draw.rect(screen, BLACK, 
                           (self.x - 3, self.y + 10, 6, self.height - 20))
            pygame.draw.rect(screen, BLACK, 
                           (self.x + self.width - 3, self.y + 10, 6, self.height - 20))
                           
        elif self.type == "boss":
            # Boss的眼睛
            eye_size = 8
            pygame.draw.circle(screen, RED, 
                             (int(self.x + self.width//3), int(self.y + self.height//3)), 
                             eye_size)
            pygame.draw.circle(screen, RED, 
                             (int(self.x + 2*self.width//3), int(self.y + self.height//3)), 
                             eye_size)
            
    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT

# 敌人子弹类
class EnemyBullet:
    def __init__(self, x, y, vx, vy, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.radius = 4
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        
    def is_off_screen(self):
        return (self.x < 0 or self.x > SCREEN_WIDTH or 
                self.y < 0 or self.y > SCREEN_HEIGHT)
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), self.radius - 1)

# 道具类
class PowerUp:
    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.type = power_type
        self.width = 20
        self.height = 20
        self.speed = 2
        self.timer = 0
        
        if self.type == "health":
            self.color = GREEN
        elif self.type == "shield":
            self.color = BLUE
        elif self.type == "weapon":
            self.color = YELLOW
        elif self.type == "speed":
            self.color = ORANGE
            
    def update(self):
        self.y += self.speed
        self.timer += 1
        
    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT
    
    def draw(self, screen):
        # 绘制道具图标
        pygame.draw.rect(screen, self.color, 
                        (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, WHITE, 
                        (self.x, self.y, self.width, self.height), 2)
        
        # 绘制道具符号
        if self.type == "health":
            pygame.draw.polygon(screen, WHITE, [
                (self.x + self.width//2, self.y + 5),
                (self.x + 5, self.y + self.height - 5),
                (self.x + self.width - 5, self.y + self.height - 5)
            ])
        elif self.type == "shield":
            pygame.draw.circle(screen, WHITE, 
                             (self.x + self.width//2, self.y + self.height//2), 
                             6)
        elif self.type == "weapon":
            pygame.draw.line(screen, WHITE, 
                           (self.x + 5, self.y + self.height//2),
                           (self.x + self.width - 5, self.y + self.height//2), 3)
            pygame.draw.line(screen, WHITE,
                           (self.x + self.width//2, self.y + 5),
                           (self.x + self.width//2, self.y + self.height - 5), 3)
        elif self.type == "speed":
            pygame.draw.polygon(screen, WHITE, [
                (self.x + self.width//2, self.y + 5),
                (self.x + 5, self.y + self.height - 5),
                (self.x + self.width//2, self.y + self.height - 10),
                (self.x + self.width - 5, self.y + self.height - 5)
            ])

# 游戏主类
class SpaceShooterGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("太空射击战")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('simhei', 24)
        self.big_font = pygame.font.SysFont('simhei', 48)
        
        # 游戏状态
        self.state = GameState.MENU
        self.score = 0
        self.high_score = self.load_high_score()
        self.level = 1
        self.enemies_killed = 0
        self.coins = 100
        
        # 游戏对象
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.enemies = []
        self.player_bullets = []
        self.enemy_bullets = []
        self.explosions = []
        self.powerups = []
        self.star_field = StarField(200)
        
        # 敌人生成计时器
        self.enemy_spawn_timer = 0
        self.enemy_spawn_delay = 60
        
        # 道具生成计时器
        self.powerup_spawn_timer = 0
        self.powerup_spawn_delay = 300
        
        # 按键重复延迟
        self.key_delays = {}
        
    def load_high_score(self):
        try:
            with open("highscore.json", "r") as f:
                data = json.load(f)
                return data.get("high_score", 0)
        except:
            return 0
    
    def save_high_score(self):
        try:
            with open("highscore.json", "w") as f:
                json.dump({"high_score": self.high_score}, f)
        except:
            pass
    
    def spawn_enemy(self):
        enemy_types = ["basic"] * 70 + ["fast"] * 20 + ["tank"] * 10
        
        # 每10级出现一次Boss
        if self.level % 10 == 0 and random.random() < 0.1:
            enemy_types.append("boss")
            
        enemy_type = random.choice(enemy_types)
        self.enemies.append(Enemy(enemy_type))
    
    def spawn_powerup(self, x, y):
        power_types = ["health", "shield", "weapon", "speed"]
        power_type = random.choice(power_types)
        self.powerups.append(PowerUp(x, y, power_type))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == GameState.PLAYING:
                        self.state = GameState.PAUSED
                    elif self.state == GameState.PAUSED:
                        self.state = GameState.PLAYING
                        
                elif event.key == pygame.K_SPACE:
                    if self.state == GameState.MENU:
                        self.state = GameState.PLAYING
                    elif self.state == GameState.GAME_OVER:
                        self.restart_game()
                    elif self.state == GameState.SHOP:
                        self.state = GameState.PLAYING
                        
                elif event.key == pygame.K_TAB and self.state == GameState.PLAYING:
                    self.state = GameState.SHOP
                    
        return True
    
    def update(self):
        if self.state != GameState.PLAYING:
            return
            
        # 更新星空
        self.star_field.update()
        
        # 更新玩家
        self.player.update()
        
        # 生成敌人
        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer >= self.enemy_spawn_delay:
            self.spawn_enemy()
            self.enemy_spawn_timer = 0
            # 随着等级提高，敌人生成速度加快
            self.enemy_spawn_delay = max(20, 60 - self.level * 2)
        
        # 生成道具
        self.powerup_spawn_timer += 1
        if self.powerup_spawn_timer >= self.powerup_spawn_delay:
            if random.random() < 0.3:  # 30%几率生成道具
                self.powerups.append(PowerUp(
                    random.randint(0, SCREEN_WIDTH - 20),
                    -20,
                    random.choice(["health", "shield", "weapon", "speed"])
                ))
            self.powerup_spawn_timer = 0
        
        # 更新敌人
        for enemy in self.enemies[:]:
            enemy.update()
            
            # 敌人射击
            if enemy.can_shoot():
                self.enemy_bullets.extend(enemy.get_bullets())
                
            # 移除超出屏幕的敌人
            if enemy.is_off_screen():
                self.enemies.remove(enemy)
        
        # 更新子弹
        for bullet in self.player_bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                self.player_bullets.remove(bullet)
                
        for bullet in self.enemy_bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                self.enemy_bullets.remove(bullet)
        
        # 更新道具
        for powerup in self.powerups[:]:
            powerup.update()
            if powerup.is_off_screen():
                self.powerups.remove(powerup)
        
        # 更新爆炸效果
        for explosion in self.explosions[:]:
            explosion.update()
            if explosion.is_finished():
                self.explosions.remove(explosion)
        
        # 碰撞检测：玩家子弹 vs 敌人
        for bullet in self.player_bullets[:]:
            for enemy in self.enemies[:]:
                if (bullet.x > enemy.x and bullet.x < enemy.x + enemy.width and
                    bullet.y > enemy.y and bullet.y < enemy.y + enemy.height):
                    
                    enemy.health -= bullet.damage
                    if bullet in self.player_bullets:
                        self.player_bullets.remove(bullet)
                    
                    if enemy.health <= 0:
                        self.enemies.remove(enemy)
                        self.enemies_killed += 1
                        self.score += enemy.score_value
                        
                        # 生成爆炸效果
                        self.explosions.append(Explosion(
                            enemy.x + enemy.width//2,
                            enemy.y + enemy.height//2,
                            min(50, enemy.width)
                        ))
                        
                        # 随机掉落道具
                        if random.random() < 0.2:  # 20%几率掉落道具
                            self.spawn_powerup(enemy.x + enemy.width//2, enemy.y + enemy.height//2)
                        
                        # 升级检查
                        if self.enemies_killed >= self.level * 10:
                            self.level += 1
                    
                    break
        
        # 碰撞检测：敌人子弹 vs 玩家
        for bullet in self.enemy_bullets[:]:
            if (bullet.x > self.player.x and bullet.x < self.player.x + self.player.width and
                bullet.y > self.player.y and bullet.y < self.player.y + self.player.height):
                
                self.enemy_bullets.remove(bullet)
                self.player.take_damage(10)
                
                # 生成爆炸效果
                self.explosions.append(Explosion(bullet.x, bullet.y, 20))
        
        # 碰撞检测：敌人 vs 玩家
        for enemy in self.enemies[:]:
            if (enemy.x < self.player.x + self.player.width and
                enemy.x + enemy.width > self.player.x and
                enemy.y < self.player.y + self.player.height and
                enemy.y + enemy.height > self.player.y):
                
                self.enemies.remove(enemy)
                self.player.take_damage(20)
                
                # 生成爆炸效果
                self.explosions.append(Explosion(
                    enemy.x + enemy.width//2,
                    enemy.y + enemy.height//2,
                    min(50, enemy.width)
                ))
        
        # 碰撞检测：道具 vs 玩家
        for powerup in self.powerups[:]:
            if (powerup.x < self.player.x + self.player.width and
                powerup.x + powerup.width > self.player.x and
                powerup.y < self.player.y + self.player.height and
                powerup.y + powerup.height > self.player.y):
                
                if powerup.type == "health":
                    self.player.heal(30)
                elif powerup.type == "shield":
                    self.player.add_shield(50)
                elif powerup.type == "weapon":
                    self.player.upgrade_weapon()
                elif powerup.type == "speed":
                    self.player.speed = min(8, self.player.speed + 1)
                
                self.powerups.remove(powerup)
        
        # 检查游戏结束
        if self.player.health <= 0:
            self.state = GameState.GAME_OVER
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()
    
    def draw(self):
        # 清屏
        self.screen.fill(BLACK)
        
        # 绘制星空
        self.star_field.draw(self.screen)
        
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.PLAYING:
            self.draw_game()
        elif self.state == GameState.PAUSED:
            self.draw_game()
            self.draw_pause()
        elif self.state == GameState.GAME_OVER:
            self.draw_game()
            self.draw_game_over()
        elif self.state == GameState.SHOP:
            self.draw_shop()
    
    def draw_menu(self):
        # 标题
        title = self.big_font.render("太空射击战", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100))
        self.screen.blit(title, title_rect)
        
        # 开始提示
        start_text = self.font.render("按空格键开始游戏", True, GREEN)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(start_text, start_rect)
        
        # 控制说明
        controls = [
            "方向键：移动",
            "空格键：开始/继续",
            "TAB键：商店",
            "ESC键：暂停"
        ]
        
        for i, control in enumerate(controls):
            text = self.font.render(control, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50 + i*30))
            self.screen.blit(text, text_rect)
        
        # 最高分
        high_score_text = self.font.render(f"最高分: {self.high_score}", True, YELLOW)
        high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 50))
        self.screen.blit(high_score_text, high_score_rect)
    
    def draw_game(self):
        # 绘制所有游戏对象
        self.player.draw(self.screen)
        
        for enemy in self.enemies:
            enemy.draw(self.screen)
            
        for bullet in self.player_bullets:
            bullet.draw(self.screen)
            
        for bullet in self.enemy_bullets:
            bullet.draw(self.screen)
            
        for powerup in self.powerups:
            powerup.draw(self.screen)
            
        for explosion in self.explosions:
            explosion.draw(self.screen)
        
        # 绘制UI
        self.draw_ui()
    
    def draw_ui(self):
        # 分数
        score_text = self.font.render(f"分数: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # 最高分
        high_score_text = self.font.render(f"最高分: {self.high_score}", True, YELLOW)
        self.screen.blit(high_score_text, (10, 40))
        
        # 等级
        level_text = self.font.render(f"等级: {self.level}", True, GREEN)
        self.screen.blit(level_text, (10, 70))
        
        # 击杀数
        kills_text = self.font.render(f"击杀: {self.enemies_killed}", True, ORANGE)
        self.screen.blit(kills_text, (10, 100))
        
        # 武器信息
        weapon_names = {
            WeaponType.SINGLE: "单发",
            WeaponType.DOUBLE: "双发",
            WeaponType.TRIPLE: "三发",
            WeaponType.SPREAD: "散射",
            WeaponType.LASER: "激光"
        }
        
        weapon_text = self.font.render(f"武器: {weapon_names[self.player.weapon_type]}", True, CYAN)
        self.screen.blit(weapon_text, (SCREEN_WIDTH - 150, 10))
        
        # 金币
        coins_text = self.font.render(f"金币: {self.coins}", True, YELLOW)
        self.screen.blit(coins_text, (SCREEN_WIDTH - 150, 40))
        
        # 商店提示
        shop_text = self.font.render("按TAB打开商店", True, WHITE)
        self.screen.blit(shop_text, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 30))
    
    def draw_pause(self):
        # 半透明遮罩
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        # 暂停文字
        pause_text = self.big_font.render("游戏暂停", True, WHITE)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(pause_text, pause_rect)
        
        # 继续提示
        continue_text = self.font.render("按ESC继续游戏", True, GREEN)
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        self.screen.blit(continue_text, continue_rect)
    
    def draw_game_over(self):
        # 半透明遮罩
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        # 游戏结束文字
        game_over_text = self.big_font.render("游戏结束", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(game_over_text, game_over_rect)
        
        # 最终分数
        final_score_text = self.font.render(f"最终分数: {self.score}", True, WHITE)
        final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(final_score_text, final_score_rect)
        
        # 重新开始提示
        restart_text = self.font.render("按空格键重新开始", True, GREEN)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        self.screen.blit(restart_text, restart_rect)
    
    def draw_shop(self):
        # 半透明遮罩
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        # 商店标题
        shop_title = self.big_font.render("武器商店", True, YELLOW)
        shop_title_rect = shop_title.get_rect(center=(SCREEN_WIDTH//2, 100))
        self.screen.blit(shop_title, shop_title_rect)
        
        # 武器列表
        weapons = [
            ("单发枪", 0, "基础武器"),
            ("双发枪", 100, "同时发射两颗子弹"),
            ("三发枪", 300, "同时发射三颗子弹"),
            ("散射枪", 500, "发射扇形子弹"),
            ("激光枪", 1000, "强力穿透激光")
        ]
        
        current_weapon = self.player.weapon_type.value
        
        for i, (name, cost, desc) in enumerate(weapons):
            y_pos = 200 + i * 80
            
            # 武器名称
            weapon_name = self.font.render(f"{i+1}. {name}", True, WHITE)
            self.screen.blit(weapon_name, (200, y_pos))
            
            # 价格
            cost_text = self.font.render(f"价格: {cost} 金币", True, YELLOW)
            self.screen.blit(cost_text, (200, y_pos + 25))
            
            # 描述
            desc_text = self.font.render(desc, True, CYAN)
            self.screen.blit(desc_text, (200, y_pos + 50))
            
            # 当前装备标识
            if i + 1 == current_weapon:
                equipped_text = self.font.render("已装备", True, GREEN)
                self.screen.blit(equipped_text, (500, y_pos))
            else:
                # 购买按钮
                button_color = GREEN if self.coins >= cost else RED
                pygame.draw.rect(self.screen, button_color, (500, y_pos, 100, 30))
                buy_text = self.font.render("购买", True, WHITE)
                self.screen.blit(buy_text, (520, y_pos + 5))
        
        # 返回提示
        back_text = self.font.render("按空格键返回游戏", True, WHITE)
        back_rect = back_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 50))
        self.screen.blit(back_text, back_rect)
    
    def restart_game(self):
        self.state = GameState.PLAYING
        self.score = 0
        self.level = 1
        self.enemies_killed = 0
        self.coins = 100
        
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.enemies = []
        self.player_bullets = []
        self.enemy_bullets = []
        self.explosions = []
        self.powerups = []
        
        self.enemy_spawn_timer = 0
        self.enemy_spawn_delay = 60
        self.powerup_spawn_timer = 0
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            
            # 处理玩家射击
            keys = pygame.key.get_pressed()
            if self.state == GameState.PLAYING and keys[pygame.K_SPACE]:
                self.player_bullets.extend(self.player.get_bullets())
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()

# 运行游戏
if __name__ == "__main__":
    game = SpaceShooterGame()
    game.run()
    