import pygame
from const import window_height, window_width, title
from animation import load_animation, show_running_animation, floor, draw_bg
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption(title)
pygame.init()

clock = pygame.time.Clock()
FPS = 80

run_frames = load_animation('sprite/Tibu_run.png', 120, 120, 7)
jump_frames = load_animation('sprite/Tibu_jump.png', 120, 120, 1)
floor_surface, floor_rect = floor(window, 'sprite/floor25.png')
sprite_speed = 7
x, y = 50, floor_rect.top - 120
window = pygame.display.set_mode((window_width, window_height))

while True:
    clock.tick(FPS)
    draw_bg(window)
    show_running_animation(window, run_frames, jump_frames, sprite_speed, x, y)
pygame.display.update()
