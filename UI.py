import pygame
from math import inf

aqua = (26, 195, 166)
green = (52, 207, 122)
blue = (65, 161, 225)
dark_blue = (46, 0, 249)
purple = (154, 82, 183)
yellow = (246, 167, 26)
orange = (237, 139, 29)
peach = (235, 93, 73)
gray = (71, 91, 111)
light_gray = (159, 174, 175)
white = (236, 240, 241)
black = (5, 5, 5)
dark_gray = (34, 34, 34)
light_green = (92, 242, 96)


class Cell:
    def __init__(self, x, y, width, height, color, text=None, text_size=15, value=0, is_wall=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = None
        if text is not None:
            font = pygame.font.SysFont('arial', text_size, bold=True)
            rendered_font = font.render(text, True, black)
            self.text = rendered_font
        self.value = value
        self.is_wall = is_wall

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        if self.text:
            r = int(min(self.width, self.height) / 2)
            pygame.draw.circle(screen, light_gray, (self.x + self.width // 2, self.y + self.height // 2), r)
            text_rect = self.text.get_rect()
            text_len = text_rect.width
            text_height = text_rect.height
            tx = self.x + (self.width - text_len) // 2
            ty = self.y + (self.width - text_height) // 2
            screen.blit(self.text, (tx, ty))

    def set_color(self, color):
        self.color = color

    def get_pos(self, grid):
        for row, line in enumerate(grid.get_table()):
            for col, cell in enumerate(line):
                if cell == self:
                    return row, col

    def get_rect(self):
        return self.x, self.y, self.width, self.height

    def set_text(self, text, text_size=15):
        if not text:
            self.text = None
            return
        font = pygame.font.SysFont('arial', text_size, bold=True)
        rendered_font = font.render(text, True, black)
        self.text = rendered_font

    def set_wall(self, make_wall=True):
        self.is_wall = make_wall

    def set_value(self, val):
        self.value = val

    def get_value(self):
        return self.value

    def get_mouseover(self, mouse_x, mouse_y):
        return mouse_x in range(self.x, self.x + self.width + 1) and mouse_y in range(self.y, self.y + self.height + 1)


class Grid:
    def __init__(self, width, height, x, y, rows, cols):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.rows = rows
        self.cols = cols
        self.row_size = height // rows
        self.col_size = width // cols
        self.table = [[None for i in range(cols)] for j in range(rows)]

    def draw_grid(self, surface, width=2, color=gray):
        for y in range(self.y, self.y + self.row_size * self.rows + width, self.row_size):
            pygame.draw.line(surface, color, (self.x, y), (self.x + self.col_size * self.cols, y), width)

        for x in range(self.x, self.x + self.col_size * self.cols + width, self.col_size):
            pygame.draw.line(surface, color, (x, self.y), (x, self.y + self.row_size * self.rows), width)

    def draw(self, surface, grid_col=gray, grid_w=2):
        self.draw_grid(surface, grid_w, grid_col)
        for line in self.table:
            for el in line:
                if el:
                    el.draw(surface)

    def get_mouseover(self, mouse_x, mouse_y):
        return mouse_x in range(self.x, self.x + self.width + 1) and mouse_y in range(self.y, self.y + self.height + 1)


class Field(Grid):
    def __init__(self, width, height, x, y, rows, cols, wall_color, bg_color):
        super().__init__(width, height, x, y, rows, cols)
        self.wall_color = wall_color
        self.bg_color = bg_color
        self.start_point = None
        self.end_point = None
        for i in range(rows):
            for j in range(cols):
                cell_x = self.x + self.col_size * j + 3
                cell_y = self.y + self.row_size * i + 3
                cell_is_wall = i == 0 or j == 0 or i == self.rows - 1 or j == self.cols - 1
                cell_color = wall_color if cell_is_wall else bg_color
                vl = inf
                self.table[i][j] = Cell(cell_x, cell_y, self.col_size - 4,
                                        self.row_size - 4, color=cell_color, value=vl, is_wall=cell_is_wall)

    def set_start_point(self, s_p):
        if self.start_point:
            self.set_color(*self.start_point, self.bg_color)
            self.set_text(*self.start_point, None)
        self.start_point = s_p
        self.set_color(*s_p, blue)
        self.set_text(*s_p, "Start", text_size=min(self.row_size, self.col_size) // 2)

    def set_end_point(self, e_p):
        if self.end_point:
            self.set_color(*self.end_point, self.bg_color)
            self.set_text(*self.end_point, None)
        self.end_point = e_p
        self.set_color(*e_p, green)
        self.set_text(*e_p, "End", text_size=min(self.row_size, self.col_size) // 2)

    def set_wall(self, row, col, is_wall=True):
        self.table[row][col].set_wall(is_wall)
        if is_wall:
            self.table[row][col].set_color(self.wall_color)
        else:
            self.table[row][col].set_color(self.bg_color)

    def set_color(self, row, col, color):
        self.table[row][col].set_color(color)

    def set_value(self, row, col, value):
        self.table[row][col].set_value(value)

    def set_text(self, row, col, text, text_size=-1):
        if text_size == -1:
            text_size = int(min(self.row_size, self.col_size) / 2.3)
        self.table[row][col].set_text(text, text_size)

    def get_value(self, row, col):
        return self.table[row][col].get_value()

    def get_table(self):
        return self.table

    def get_cell(self, row, col):
        return self.table[row][col]

    def draw_at(self, row, col, screen):
        cell = self.table[row][col]
        cell.draw(screen)
        pygame.display.update(cell.get_rect())

    def get_rows(self):
        return self.rows

    def get_cols(self):
        return self.cols

    def get_neighbors(self, row, col, straight=True, diag=True):
        if row not in range(0, self.rows) or col not in range(0, self.cols):
            return []
        out = []
        if row != 0:
            if straight:
                out.append((row - 1, col))
            if col != 0 and diag:
                out.append((row - 1, col - 1))
            if col != self.cols - 1 and diag:
                out.append((row - 1, col + 1))
        if col != 0 and straight:
            out.append((row, col - 1))
        if col != self.cols - 1 and straight:
            out.append((row, col + 1))
        if row != self.rows - 1:
            if straight:
                out.append((row + 1, col))
            if col != 0 and diag:
                out.append((row + 1, col - 1))
            if col != self.cols - 1 and diag:
                out.append((row + 1, col + 1))
        return out


def generate_title(sel_algorythm, font='arial', size=20, color=black):
    font = pygame.font.SysFont(font, size, bold=True)
    out = []
    title_text = ["Pathfinding visualisation by @PaperPlane0",
                  "Left click to add walls, right click to remove walls",
                  "S + LMB - set start point, E + LMB - set end point",
                  f"Selected algorithm: {sel_algorythm}"]
    for i, txt in enumerate(title_text):
        cl = dark_blue if not i else color
        render = font.render(txt, True, cl)
        out.append(render)
    return out


def make_button(screen, x, y, width, height, image):
    img = pygame.transform.smoothscale(image, (width, height))
    return img, Cell(x, y, width, height, white)


def get_color_difference(col1, col2):
    out = []
    for c1, c2 in zip(col1, col2):
        out.append(c2 - c1)
    return tuple(out)


def mix_color(c1, difference, coeff):
    out = [col + int(coeff * dif) for col, dif in zip(c1, difference)]
    for col in out:
        if col < 0:
            col = 0
        if col > 255:
            col = 255
    return tuple(out)


def get_gradient(start_color, end_color, steps):
    difference = get_color_difference(start_color, end_color)
    s_c = start_color[:]
    out = []
    for i in range(steps):
        out.append(mix_color(s_c, difference, 1 / steps))
        s_c = mix_color(s_c, difference, 1 / steps)
    return out