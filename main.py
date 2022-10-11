import pygame
from logic import Gaming

y_tuple = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j')
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

block_size = 50
left_margin = 200
upper_margin = 30

size = (left_margin + 30 * block_size, upper_margin + 15 * block_size)

pygame.init()

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Sea Battle")

font_size = int(block_size / 1.5)

font = pygame.font.SysFont('notosans', font_size)


def draw_grid():
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    for i in range(11):
        # Hor grid1
        pygame.draw.line(screen, BLACK, (left_margin, upper_margin + i * block_size),
                         (left_margin + 10 * block_size, upper_margin + i * block_size), 1)
        # Vert grid1
        pygame.draw.line(screen, BLACK, (left_margin + i * block_size, upper_margin),
                         (left_margin + i * block_size, upper_margin + 10 * block_size), 1)
        # Hor grid2
        pygame.draw.line(screen, BLACK, (left_margin + 15 * block_size, upper_margin +
                                         i * block_size),
                         (left_margin + 25 * block_size, upper_margin + i * block_size), 1)
        # Vert grid2
        pygame.draw.line(screen, BLACK, (left_margin + (i + 15) * block_size, upper_margin),
                         (left_margin + (i + 15) * block_size, upper_margin + 10 * block_size), 1)

        if i < 10:
            num_ver = font.render(str(i + 1), True, BLACK)
            letters_hor = font.render(letters[i], True, BLACK)

            num_ver_width = num_ver.get_width()
            num_ver_height = num_ver.get_height()
            letters_hor_width = letters_hor.get_width()

            # Ver num grid1
            screen.blit(letters_hor, (left_margin - (block_size // 2 + num_ver_width // 2),
                                      upper_margin + i * block_size + (block_size // 2 - num_ver_height // 2)))
            # Hor letters grid1
            screen.blit(num_ver, (left_margin + i * block_size + (block_size //
                                                                  2 - letters_hor_width // 2),
                                  upper_margin + 10 * block_size))
            # Ver num grid2
            screen.blit(letters_hor, (left_margin - (block_size // 2 + num_ver_width // 2) + 15 *
                                      block_size,
                                      upper_margin + i * block_size + (block_size // 2 - num_ver_height // 2)))
            # Hor letters grid2
            screen.blit(num_ver, (left_margin + i * block_size + (block_size // 2 -
                                                                  letters_hor_width // 2) + 15 * block_size,
                                  upper_margin + 10 * block_size))


def draw_boats_right(field_dict):
    for x, y_set in field_dict.items():
        for y in y_set:
            if field_dict[x][y] == 'boat':
                pygame.draw.rect(
                    screen, BLACK, ((block_size * (x + 14) + left_margin, block_size * y_tuple.index(y) + upper_margin),
                                    (block_size, block_size)), width=block_size // 10)


def draw_one_boat(boat_coordinate):
    for x, y_set in boat_coordinate.items():
        for y in y_set:
            pygame.draw.rect(
                screen, BLACK, ((block_size * (x - 1) + left_margin, block_size * y_tuple.index(y) + upper_margin),
                                (block_size, block_size)), width=block_size // 10)
    pygame.display.update()


def draw_point(field_dict, x, y):
    o = font.render(str("O"), True, BLACK)
    crestik = font.render(str("X"), True, BLACK)
    width = o.get_width()
    if field_dict[x][y] == 'burned/boat':
        screen.blit(crestik, (left_margin + (x - 1) * block_size + width,
                              upper_margin + y_tuple.index(y) * block_size + width))
    elif field_dict[x][y] == 'burned/empty':
        screen.blit(o, (left_margin + (x - 1) * block_size + width,
                        upper_margin + y_tuple.index(y) * block_size + width))
    pygame.display.update()


def draw_point_right(field_dict, x, y):
    o = font.render(str("O"), True, BLACK)
    crestik = font.render(str("X"), True, BLACK)
    width = o.get_width()
    if field_dict[x][y] == 'burned/boat':
        screen.blit(crestik, (left_margin + (x + 14) * block_size + width,
                              upper_margin + y_tuple.index(y) * block_size + width))
    elif field_dict[x][y] == 'burned/empty':
        screen.blit(o, (left_margin + (x + 14) * block_size + width,
                        upper_margin + y_tuple.index(y) * block_size + width))
    pygame.display.update()


def draw_points_around_boat(near_dict, field_dict):
    o = font.render(str("O"), True, BLACK)
    width = o.get_width()
    for x, y_list_near in near_dict.items():
        for y in y_list_near:
            if field_dict[x][y] == 'empty':
                screen.blit(o, (left_margin + (x - 1) * block_size + width,
                                upper_margin + y_tuple.index(y) * block_size + width))
    pygame.display.update()


def main():
    game_over = False
    screen.fill(WHITE)
    draw_grid()
    computer = Gaming()
    computer.set_dict()
    computer.random_boats()
    human = Gaming()
    human.set_dict()
    human.random_boats()
    field_dict_human = human.get_field_dict()
    draw_boats_right(field_dict_human)
    pygame.display.update()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if (left_margin <= x <= left_margin + 10 * block_size) and (
                        upper_margin <= y <= upper_margin + 10 * block_size):
                    x = (x - left_margin) // block_size + 1
                    y = y_tuple[(y - upper_margin) // block_size]
                    field_dict = computer.gaming(x, y)
                    if field_dict[x][y] == 'burned/boat':
                        boat_coordinate = computer.find_full_boat(x, y)
                        if boat_coordinate:
                            draw_one_boat(boat_coordinate)
                            near_dict_final = computer.create_near_dict(boat_coordinate)
                            draw_points_around_boat(near_dict_final, field_dict)
                    draw_point(field_dict, x, y)
                    pygame.time.delay(800)
                    x, y = human.random_x_y()
                    field_dict_human = human.gaming(x, y)
                    draw_point_right(field_dict_human, x, y)


if __name__ == "__main__":
    main()
    pygame.quit()
