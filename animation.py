import pygame
import math
import random
from const import window_height, window_width, title

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption(title)
bg_images = []
scroll = 0
for i in range(1, 5):
    bg_image = pygame.image.load(f"sprite/bg_{i}.png").convert_alpha()
    bg_images.append(bg_image)


def draw_bg(window, scroll):
    new_width = window.get_width()
    new_height = window.get_height()
    scaled_images = [pygame.transform.scale(
        i, (new_width, new_height)) for i in bg_images]

    for x in range(5):
        for i, scaled_image in enumerate(scaled_images):
            # calcular la posición horizontal de la imagen de fondo
            pos_x = x * new_width - (scroll % new_width)

            window.blit(scaled_image, (pos_x, 0))


def load_animation(image_path, sprite_width, sprite_height, num_frames):
    # Cargar la imagen del sprite
    sprite_image = pygame.image.load(image_path)
    # Crear una lista con los diferentes frames de la animación
    frames = []
    for i in range(num_frames):
        frame = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
        frame.blit(sprite_image, (0, 0), (i * sprite_width,
                   0, sprite_width, sprite_height))
        frames.append(frame)
    return frames


def floor(window, floor_image_path):
    # Configurar el suelo
    floor_surface = pygame.image.load(floor_image_path)

    # Duplicar la imagen del suelo por todo el largo de la ventana
    num_copies = math.ceil(window.get_width() / floor_surface.get_width())
    floor_surface = pygame.transform.scale2x(floor_surface)
    floor_surface = pygame.transform.scale(
        floor_surface, (num_copies * floor_surface.get_width(), floor_surface.get_height()))
    floor_rect = floor_surface.get_rect(bottom=window.get_height())
    return floor_surface, floor_rect


def show_running_animation(window, run_frames, jump_frames, sprite_speed, x, y):
    # Configurar la animación
    clock = pygame.time.Clock()
    run_frame_index = 0
    jump_frame_index = 0
    frame_count = 0
    is_jumping = False
    jump_count = 0
    jump_height = 30
    jump_speed = 7
    is_falling = False
    fall_count = 0
    fall_height = 70
    frame_speed = sprite_speed
    scroll_speed = 5
    scroll = 0
    score = 0
    rect_x = window_width
    rect_y = 300
    rect_width = 50
    rect_height = 50
    rect_speed = -5
    score_text = None
    score_rect = None
    rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)

    # Definir el tiempo de inicio
    start_time = pygame.time.get_ticks()

    # Configurar la fuente y el tamaño del texto
    font = pygame.font.SysFont('Comic Sans MS', 30)
    
    # Obtener el rectángulo del texto
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect()

    # Establecer la posición del rectángulo del texto en la parte superior central de la ventana
    score_rect.centerx = window.get_rect().centerx
    score_rect.top = 10
    
    # Llamar a la función floor() para obtener el piso
    floor_surface, floor_rect = floor(window, 'sprite/floor25.png')
    casco = pygame.image.load('sprite/cascopts.png')
    character_rect = pygame.Rect(
        x, y, run_frames[0].get_width(), run_frames[0].get_height())

    # Mostrar la animación hasta que se cierre la ventana
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Actualizar el puntaje
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        
        # Detectar si se presiona la tecla
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not is_jumping and not is_falling:
            is_jumping = True
            jump_count = 0
            jump_speed = 10
        scroll += scroll_speed

        # Mostrar el fondo
        draw_bg(window, scroll)

        elapsed_time = pygame.time.get_ticks() - start_time
        # Detectar si ha pasado el tiempo suficiente para aumentar el contador

        if elapsed_time > 1000:
            score += 1
            start_time = pygame.time.get_ticks()
            # Actualizar la variable de tiempo inicial

        if character_rect.colliderect(rect):
            score += 3
            rect_x = window_width
            rect_y = random.randint(100, 400)
        # Mover y mostrar el rectángulo
        rect_x = (rect_x + rect_speed) % window_width
        casco_rect = casco.get_rect()
        rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
        window.blit(casco, rect)

        # Mostrar la animación de correr
        if is_jumping:
            if jump_count < jump_height:
                y -= int(jump_speed)
                jump_count += 1
                if frame_count % frame_speed == 0:
                    jump_frame_index = (
                        jump_frame_index + 1) % len(jump_frames)
                window.blit(run_frames[run_frame_index], (x, y))
            else:
                is_jumping = False
                is_falling = True
                fall_count = 0
        elif is_falling:
            if fall_count < fall_height:
                y += int(math.sin(math.radians(fall_count)) * jump_speed)
                fall_count += 1
                if frame_count % frame_speed == 0:
                    jump_frame_index = (
                        jump_frame_index + 1) % len(jump_frames)
                window.blit(jump_frames[jump_frame_index], (x, y))
            else:
                is_falling = False
                jump_frame_index = 0
                y = floor_rect.top - 120
        else:
            frame_count += 1
            if frame_count % frame_speed == 0:
                run_frame_index = (run_frame_index + 1) % len(run_frames)
                frame_count = 0
            window.blit(run_frames[run_frame_index], (x, y))

         # Actualizar el rectángulo del personaje
        character_rect.x = x
        character_rect.y = y

        # Dibujar el rectángulo del personaje (solo para fines de depuración)
        # pygame.draw.rect(window, (255, 0, 0), character_rect, 2)

        # Actualizar el piso en la ventana
        window.blit(floor_surface, floor_rect)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        # Actualizar la posición del rectángulo del puntaje
        score_rect.centerx = window.get_rect().centerx
        window.blit(score_text, score_rect)

        # Actualizar la pantalla
        pygame.display.update()
        pygame.display.flip()
