import pygame
from const import window_height, window_width, title
from animation import load_animation, show_running_animation, floor
pygame.init()

clock = pygame.time.Clock()
FPS = 60

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption(title)
scroll = 0 
bg_images = []
for i in range(1, 5):
    bg_image = pygame.image.load(f"sprite/bg_{i}.png").convert_alpha()
    bg_images.append(bg_image)



def draw_bg():
    for x in range(5):
        for i in bg_images:
            new_width = window.get_width()
            new_height = window.get_height()
            scaled_image = pygame.transform.scale(i, (new_width, new_height))
            window.blit(scaled_image, ((x* new_width) -scroll, 0))
run = True
while run:

    clock.tick(FPS)
    draw_bg()

    key=pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        scroll -=5
    if key[pygame.K_RIGHT]:
        scroll +=5 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
pygame.quit()
