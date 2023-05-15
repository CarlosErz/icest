import pygame
from const import window_height, window_width, title
from animation import load_animation, show_running_animation, floor
pygame.init()

clock = pygame.time.Clock()
FPS = 60

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption(title)
scroll = 0
scroll_speed = 5  # velocidad de desplazamiento del fondo
bg_images = []
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

            # dibujar la imagen de fondo en la posición calculada
            window.blit(scaled_image, (pos_x, 0))


run = True
while run:
    clock.tick(FPS)

    # Actualizar la variable 'scroll' para mover el fondo
    scroll += scroll_speed

    draw_bg(window, scroll)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
pygame.quit()
