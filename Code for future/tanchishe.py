import pygame
import random
import sys

# 初始化pygame
pygame.init()

# 游戏常量
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 120, 255)

# 方向常量
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.score = 0
        
        # 初始化蛇的身体
        for i in range(1, self.length):
            self.positions.append((self.positions[0][0] - i, self.positions[0][1]))
    
    def get_head_position(self):
        return self.positions[0]
    
    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return  # 不能直接反向移动
        else:
            self.direction = point
    
    def move(self):
        head = self.get_head_position()
        x, y = self.direction
        new_x = (head[0] + x) % GRID_WIDTH
        new_y = (head[1] + y) % GRID_HEIGHT
        new_position = (new_x, new_y)
        
        if new_position in self.positions[1:]:
            self.reset()  # 撞到自己，重置游戏
        else:
            self.positions.insert(0, new_position)
            if len(self.positions) > self.length:
                self.positions.pop()
    
    def draw(self, surface):
        for p in self.positions:
            rect = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, GREEN, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)
            
            # 绘制蛇头
            if p == self.positions[0]:
                # 画眼睛
                eye_size = GRID_SIZE // 5
                # 根据方向确定眼睛位置
                if self.direction == RIGHT:
                    left_eye = (p[0] * GRID_SIZE + GRID_SIZE - eye_size*2, p[1] * GRID_SIZE + eye_size*2)
                    right_eye = (p[0] * GRID_SIZE + GRID_SIZE - eye_size*2, p[1] * GRID_SIZE + GRID_SIZE - eye_size*3)
                elif self.direction == LEFT:
                    left_eye = (p[0] * GRID_SIZE + eye_size, p[1] * GRID_SIZE + eye_size*2)
                    right_eye = (p[0] * GRID_SIZE + eye_size, p[1] * GRID_SIZE + GRID_SIZE - eye_size*3)
                elif self.direction == UP:
                    left_eye = (p[0] * GRID_SIZE + eye_size*2, p[1] * GRID_SIZE + eye_size)
                    right_eye = (p[0] * GRID_SIZE + GRID_SIZE - eye_size*3, p[1] * GRID_SIZE + eye_size)
                else:  # DOWN
                    left_eye = (p[0] * GRID_SIZE + eye_size*2, p[1] * GRID_SIZE + GRID_SIZE - eye_size*2)
                    right_eye = (p[0] * GRID_SIZE + GRID_SIZE - eye_size*3, p[1] * GRID_SIZE + GRID_SIZE - eye_size*2)
                
                pygame.draw.circle(surface, BLACK, left_eye, eye_size)
                pygame.draw.circle(surface, BLACK, right_eye, eye_size)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()
    
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    
    def draw(self, surface):
        rect = pygame.Rect((self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, RED, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)
        
        # 在食物上画一个小圆点
        center = (self.position[0] * GRID_SIZE + GRID_SIZE // 2, self.position[1] * GRID_SIZE + GRID_SIZE // 2)
        pygame.draw.circle(surface, WHITE, center, GRID_SIZE // 4)

def draw_grid(surface):
    for y in range(0, HEIGHT, GRID_SIZE):
        for x in range(0, WIDTH, GRID_SIZE):
            rect = pygame.Rect((x, y), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BLACK, rect, 1)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('贪吃蛇游戏')
    clock = pygame.time.Clock()
    
    snake = Snake()
    food = Food()
    
    font = pygame.font.SysFont('simhei', 24)  # 使用黑体显示中文
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.turn(UP)
                elif event.key == pygame.K_DOWN:
                    snake.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.turn(RIGHT)
        
        snake.move()
        
        # 检查是否吃到食物
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 10
            food.randomize_position()
            # 确保食物不会出现在蛇身上
            while food.position in snake.positions:
                food.randomize_position()
        
        screen.fill(BLUE)
        draw_grid(screen)
        snake.draw(screen)
        food.draw(screen)
        
        # 显示分数
        score_text = font.render(f'分数: {snake.score}', True, WHITE)
        screen.blit(score_text, (5, 5))
        
        # 显示长度
        length_text = font.render(f'长度: {snake.length}', True, WHITE)
        screen.blit(length_text, (5, 35))
        
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()