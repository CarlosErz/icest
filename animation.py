import pygame
import math
import random
import sys  # Para salir del juego
from const import window_height, window_width, title
pygame.init()
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption(title)

bg_images = []
scroll = 0
for i in range(1, 5):
    bg_image = pygame.image.load(f"sprite/bg_{i}.png").convert_alpha()
    bg_images.append(bg_image)


def show_score_animation(x):
    # Dibujar el signo +
    font = pygame.font.SysFont('Comic Sans MS', 40)
    plus_image = font.render("+3", True, (0, 255, 0))
    plus_rect = plus_image.get_rect()
    plus_rect.center = (x, window_height // 2)
    window.blit(plus_image, plus_rect)

    # Obtener la posición del número de puntuación
    score_rect = font.render("3", True, (0, 255, 0)).get_rect()
    score_rect.center = (x + plus_rect.width / 2, window_height // 2)


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
    # Aumentar el tamaño del suelo
    floor_surface = pygame.transform.scale2x(floor_surface)

    # Calcular el número de veces que la textura del suelo debe ser repetida
    num_tiles = window.get_width() // floor_surface.get_width() + 1

    # Crear una superficie vacía del tamaño de la ventana
    floor_width = num_tiles * floor_surface.get_width()
    floor_height = floor_surface.get_height()
    floor_surface_full = pygame.Surface((floor_width, floor_height))

    # Repetir la textura del suelo en la superficie completa
    for i in range(num_tiles):
        floor_surface_full.blit(
            floor_surface, (i * floor_surface.get_width(), 0))

    # Colocar la superficie completa en el fondo de la ventana
    floor_rect = floor_surface_full.get_rect(bottom=window.get_height())
    window.blit(floor_surface_full, floor_rect)

    return floor_surface_full, floor_rect


def show_running_animation(window, run_frames, jump_frames, x, y):
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
    sprite_speed = 5
    frame_speed = sprite_speed
    scroll_speed = 5
    scroll = 0
    score = 0
    rect_x = window_width
    rect_y = 200
    rect_width = 50
    rect_height = 50
    rect_speed = -5
    score_text = None
    score_rect = None
    object_speed = 5
    last_spike_time = 0
    spike_interval = 2500
    jumps_taken = 0
    # Aparecerá un nuevo rectángulo de picos cada 2.5 milisegudos
    active_spikes = []
    double_jump_available = True
    rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)

    # Definir el tiempo de inicio
    start_time = pygame.time.get_ticks()

    # Configurar la fuente y el tamaño del texto
    font = pygame.font.SysFont('Comic Sans MS', 30)

    # Obtener el rectángulo del texto
    score_text = font.render(f"Puntos: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect()

    # Establecer la posición del rectángulo del texto en la parte superior central de la ventana
    score_rect.centerx = window.get_rect().centerx
    score_rect.top = 10

    # Llamar a la función floor() para obtener el piso
    floor_surface, floor_rect = floor(window, 'sprite/floor25.png')
    casco = pygame.image.load('sprite/cascopts.png')
    object_image = pygame.image.load('sprite/picos.png')
    object_rect = object_image.get_rect()
    object_rect.bottom = floor_rect.bottom - 60
    object_rect.left = window_width
    character_rect = pygame.Rect(
        x, y, run_frames[0].get_width(), run_frames[0].get_height())
    # la parte inferior del personaje está en línea con la parte inferior del piso
    character_rect.bottom = floor_rect.bottom

    # Establecer la posición del rectángulo del texto en el centro de la ventana
    text_rect = pygame.Rect(0, 0, 400, 200)
    text_rect.center = window.get_rect().center
    # Creamos una pantalla de inicio con un mensaje y una imagen de fondo
    start_font = pygame.font.Font('freesansbold.ttf', 32)
    start_text = start_font.render(
        'Presiona Enter para jugar', True, (255, 255, 255))
    start_text_rect = start_text.get_rect()
    start_text_rect.center = (window_width // 2, window_height // 2)
    
    # Crear una superficie para el contorno negro
    outline_surface = pygame.Surface(
        (start_text_rect.width + 10, start_text_rect.height + 10))
    outline_surface.fill((0, 0, 0))

    # Obtener el rectángulo que contiene el contorno
    outline_rect = outline_surface.get_rect()
    outline_rect.center = start_text_rect.center

    # Dibujar el contorno negro
    window.blit(outline_surface, outline_rect)


    running = False

    # Mostrar la pantalla de inicio hasta que se presione Enter
    while True:
        window.blit(start_text, start_text_rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = True
                    break
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if running:
            break

    # Mostrar la animación hasta que se cierre la ventana
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Actualizar el puntaje
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        object_rect.left -= object_speed

        # Detectar si se presiona la tecla
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not is_jumping and not is_falling:
            is_jumping = True
            jump_count = 0
            jump_speed = 10
            jumps_taken += 1
            if jumps_taken == 2:
                double_jump_available = False
        elif jumps_taken == 1 and not is_jumping and not is_falling and score % 10 == 0 and double_jump_available:
            is_jumping = True
            jump_count = 0
            jump_speed = 10
            jumps_taken += 1
            double_jump_available = False

        scroll += scroll_speed

        if pygame.time.get_ticks() - last_spike_time > spike_interval:
            # Genera un nuevo rectángulo de picos
            new_spike_rect = object_rect.copy()
            new_spike_rect.bottom = floor_rect.bottom - 60
            new_spike_rect.left = window_width
            active_spikes.append(new_spike_rect)
            last_spike_time = pygame.time.get_ticks()
        # Mostrar el fondo
        draw_bg(window, scroll)

        elapsed_time = pygame.time.get_ticks() - start_time
        # Detectar si ha pasado el tiempo suficiente para aumentar el contador
        # Detectar colisiones con el suelo
        if character_rect.bottom > floor_rect.bottom:
            character_rect.bottom = floor_rect.bottom

        if elapsed_time > 1000:
            score += 1
            start_time = pygame.time.get_ticks()
            # Actualizar la variable de tiempo inicial

            # si toca los picos pierde  condicionalidad de game over
        for spike_rect in active_spikes:
            if character_rect.colliderect(spike_rect):
                print("Game Over")
                return
        if character_rect.colliderect(rect):
            show_score_animation(x)
            score += 3
            rect_x = window_width
            rect_y = random.randint(100, 200)

        # Mover y mostrar el rectángulo
        rect_x = (rect_x + rect_speed) % window_width
        rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
        window.blit(casco, rect)

        # Mostrar la animación de correr
        if is_jumping:
            if is_jumping and y <= jump_height:
                is_jumping = False
                is_falling = True
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

        for spike_rect in active_spikes:
            spike_rect.left -= object_speed
            # Actualizar el piso en la ventana
            window.blit(object_image, spike_rect)
        window.blit(floor_surface, floor_rect)

        score_text = font.render(f"Puntos: {score}", True, (255, 255, 255))
        # Actualizar la posición del rectángulo del puntaje
        score_rect.centerx = window.get_rect().centerx
        window.blit(score_text, score_rect)
        if score >= 10 and score < 20:
            scroll_speed = 6
            sprite_speed = 2.5
            spike_interval = 2500
            rect_speed = -6

        if score >= 20 and score < 30:
            scroll_speed = 8
            sprite_speed = 2
            spike_interval = 2000
            rect_speed = -8

        if score >= 30 and score < 50:
            scroll_speed = 12
            sprite_speed = 1.5
            spike_interval = 2500
            rect_speed = -12

        if score >= 50 and score < 80:
            scroll_speed = 16
            sprite_speed = 1
            spike_interval = 2000
            rect_speed = -16

        if score >= 80:
            scroll_speed = 20
            sprite_speed = 0.5
            spike_interval = 1500
            rect_speed = -20

        if score % 10 == 0:
            double_jump_available = True

        # Actualizar la pantalla
        pygame.display.update()
        pygame.display.flip()
