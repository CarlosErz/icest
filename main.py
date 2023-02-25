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
floor_surface, floor_rect  = floor(window, 'sprite/floor25.png')
scroll = 0
sprite_speed = 8
x, y = 50, floor_rect.top - 120

# Creamos una pantalla de inicio con un mensaje y una imagen de fondo
start_font = pygame.font.Font('freesansbold.ttf', 32)
start_text = start_font.render('Presiona Enter para jugar', True, (255, 255, 255))
start_text_rect = start_text.get_rect()
start_text_rect.center = (window_width // 2, window_height // 2)

# Agregamos un bucle while para esperar que el usuario presione Enter
while True:
    window.blit(start_text, start_text_rect)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # El usuario ha presionado Enter, rompemos el bucle y comenzamos el juego
                break
    else:
        continue
    break

# Bucle principal del juego
while True:
    clock.tick(FPS)
    draw_bg(window ,scroll)
    show_running_animation(window, run_frames, jump_frames, sprite_speed, x, y)
    pygame.display.update()

    # Chequeamos los eventos para salir del juego si el usuario lo desea
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x or event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()


