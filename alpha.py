import pygame
import random
import math
import speech_recognition as sr

# 初始化Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("语音识别粒子文字效果")
clock = pygame.time.Clock()

# 粒子类
class Particle:
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.size = random.uniform(2, 4)  # 粒子大小
        self.target_x = target_x
        self.target_y = target_y
        self.speed = random.uniform(2, 6)  # 初始速度
        self.angle = math.atan2(target_y - y, target_x - x)  # 飞行方向角度

    def move(self):
        distance = math.hypot(self.target_x - self.x, self.target_y - self.y)
        if distance > 1:  # 当粒子距离目标还有一定距离时继续移动
            self.x += self.speed * math.cos(self.angle)
            self.y += self.speed * math.sin(self.angle)
            self.speed *= 0.98  # 逐渐减速，模拟自然效果
        else:  # 如果已经接近目标点，则停留在目标位置
            self.x, self.y = self.target_x, self.target_y

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), int(self.size))

# 生成粒子函数
def create_particles_from_text(text, font, center_x, center_y):
    text_surface = font.render(text, True, (255, 255, 255))
    text_width, text_height = text_surface.get_size()
    text_x = center_x - text_width // 2
    text_y = center_y - text_height // 2

    particles = []
    for y in range(text_surface.get_height()):
        for x in range(text_surface.get_width()):
            if text_surface.get_at((x, y))[:3] == (255, 255, 255):  # 检测白色像素
                target_x = text_x + x
                target_y = text_y + y
                start_x = random.randint(0, WIDTH)
                start_y = random.randint(0, HEIGHT)
                particles.append(Particle(start_x, start_y, target_x, target_y))
    return particles

# 语音识别函数
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("请说话...")
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)  # 增加超时时间
            text = recognizer.recognize_google(audio, language="zh-CN")
            print(f"识别到的文字: {text}")
            return text
        except sr.UnknownValueError:
            print("无法识别，请再试一次")
            return "无法识别"
        except sr.RequestError as e:
            print(f"语音识别服务错误: {e}")
            return "服务错误"
        except Exception as e:
            print(f"错误: {e}")
            return "错误"

# 主程序
font = pygame.font.SysFont("arial", 48)  # 使用系统默认字体
particles = []
recognized_text = ""

running = True
while running:
    screen.fill((0, 0, 0))  # 黑色背景

    # 绘制粒子
    for particle in particles[:]:
        particle.move()
        particle.draw(screen)
        if particle.x == particle.target_x and particle.y == particle.target_y:
            particles.remove(particle)

    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # 按空格触发语音识别
            recognized_text = recognize_speech()
            if recognized_text:
                particles = create_particles_from_text(recognized_text, font, WIDTH // 2, HEIGHT // 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()