from UI import *
from algorythms import algorythms
import pygame

pygame.init()
screen_size = screen_w, screen_h = (750, 750)
screen = pygame.display.set_mode(screen_size, 0, 16, pygame.HWACCEL)
clock = pygame.time.Clock()

selected_algorythm = "Djikstra's algorithm"
anim_speed = 60

field = Field(screen_w - 50, screen_h - 150, 25, 125, 24, 30, wall_color=dark_gray, bg_color=white)
title = generate_title(selected_algorythm)
run_button = make_button(screen, screen_w - 200, 5, 100, 100, pygame.image.load("run.jpg"))

s_down, e_down, flag = False, False, True


def draw_path(fld, args):
    pygame.event.clear()

    dist = int(((fld.start_point[0] - fld.end_point[0]) ** 2 +
                (fld.start_point[1] - fld.end_point[1]) ** 2) ** 0.5)

    gradient = get_gradient(green, yellow, dist // 2) + get_gradient(yellow, peach, dist // 2)

    if args[0] not in (field.start_point, field.end_point):

        fld.set_color(*args[0], gradient[min(len(gradient) - 1, int(fld.get_value(*args[0])))])

        value_text = str(fld.get_value(*args[0]))
        if '.' in value_text:
            value_text = value_text[:(min(value_text.find('.') + 2, len(value_text) - 1))].strip('.')
        fld.set_text(*args[0], value_text)
        fld.draw_at(*args[0], screen)


def draw_display(fld, *args):
    if args:
        draw_path(fld, args)
    else:
        for i, line in enumerate(title):
            h = line.get_rect().height
            screen.blit(line, (25, h * i + 5))
            fld.draw(screen, grid_col=black)
            screen.blit(run_button[0], (run_button[1].x, run_button[1].y))
        pygame.display.flip()


def visualise_algorythm(fld, *args):
    draw_display(fld, *args)
    clock.tick(anim_speed)


while flag:
    screen.fill(white)
    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                s_down = True
            if event.key == pygame.K_e:
                e_down = True
        if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
            m_b = pygame.mouse.get_pressed()
            if run_button[1].get_mouseover(mouse_x, mouse_y) and m_b[0]:
                flag = False
            if field.get_mouseover(mouse_x, mouse_y):
                row = (mouse_y - field.y) // field.row_size
                col = (mouse_x - field.x) // field.col_size
                if m_b[0]:
                    if s_down:
                        field.set_start_point([row, col])
                    elif e_down:
                        field.set_end_point([row, col])
                    else:
                        field.set_wall(row, col)
                elif m_b[2]:
                    field.set_wall(row, col, False)
        if event.type == pygame.KEYUP:
            s_down, e_down = False, False

    draw_display(field)

    pygame.display.flip()
    clock.tick(120)

path = algorythms[selected_algorythm](field, visualise_algorythm)
print(field.end_point)
for location in path:
    field.set_color(*location, dark_blue)
    if list(location) not in (field.start_point, field.end_point):
        field.set_text(*location, None)
visualise_algorythm(field)
while True:
    pass
