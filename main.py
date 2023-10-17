import random
import pygame
import time

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)


class Pacman(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.8)
        img = pygame.image.load("walk.png").convert()
        self.move_right_animation = Animation(img, 32, 32)
        self.move_left_animation = Animation(
            pygame.transform.flip(img, True, False), 32, 32)
        self.move_up_animation = Animation(
            pygame.transform.rotate(img, 90), 32, 32)
        self.move_down_animation = Animation(
            pygame.transform.rotate(img, 270), 32, 32)
        self.player_image = pygame.image.load(filename).convert()
        self.player_image.set_colorkey(BLACK)
        self.change_x = 0
        self.change_y = 0

    def update(self, horizontal_blocks, vertical_blocks):
        if self.rect.left < 0:
            self.rect.left = 0
            self.change_x = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.change_x = 0
        if self.rect.top < 0:
            self.rect.top = 0
            self.change_y = 0
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.change_y = 0

        self.rect.x += self.change_x
        self.rect.y += self.change_y

        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH
        elif self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = SCREEN_HEIGHT
        elif self.rect.top > SCREEN_HEIGHT:
            self.rect.bottom = 0
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        for block in pygame.sprite.spritecollide(self, horizontal_blocks, False):
            self.rect.centery = block.rect.centery
            self.change_y = 0
        for block in pygame.sprite.spritecollide(self, vertical_blocks, False):
            self.rect.centerx = block.rect.centerx
            self.change_x = 0
        if self.change_x > 0:
            self.move_right_animation.update(10)
            self.image = self.move_right_animation.get_current_image()
        elif self.change_x < 0:
            self.move_left_animation.update(10)
            self.image = self.move_left_animation.get_current_image()
        if self.change_y > 0:
            self.move_down_animation.update(10)
            self.image = self.move_down_animation.get_current_image()
        elif self.change_y < 0:
            self.move_up_animation.update(10)
            self.image = self.move_up_animation.get_current_image()

    def move_right(self):
        self.change_x = 3

    def move_left(self):
        self.change_x = -3

    def move_up(self):
        self.change_y = -3

    def move_down(self):
        self.change_y = 3

    def stop_move_right(self):
        if self.change_x != 0:
            self.image = self.player_image
        self.change_x = 0

    def stop_move_left(self):
        if self.change_x != 0:
            self.image = pygame.transform.flip(self.player_image, True, False)
        self.change_x = 0

    def stop_move_up(self):
        if self.change_y != 0:
            self.image = pygame.transform.rotate(self.player_image, 90)
        self.change_y = 0

    def stop_move_down(self):
        if self.change_y != 0:
            self.image = pygame.transform.rotate(self.player_image, 270)
        self.change_y = 0


class Animation(object):
    def __init__(self, img, width, height):
        self.sprite_sheet = img
        self.image_list = []
        self.load_images(width, height)
        self.index = 0
        self.clock = 1

    def load_images(self, width, height):
        for y in range(0, self.sprite_sheet.get_height(), height):
            for x in range(0, self.sprite_sheet.get_width(), width):
                img = self.get_image(x, y, width, height)
                self.image_list.append(img)

    def get_image(self, x, y, width, height):
        image = pygame.Surface([width, height]).convert()
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey((0, 0, 0))
        return image

    def get_current_image(self):
        return self.image_list[self.index]

    def get_length(self):
        return len(self.image_list)

    def update(self, fps=30):
        step = 30 // fps
        self.clock = (self.clock + 1) % 30
        if self.clock % step == 0:
            self.index = (self.index + 1) % len(self.image_list)


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, color, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Ellipse(pygame.sprite.Sprite):
    def __init__(self, x, y, color, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Enemies(pygame.sprite.Sprite):
    def __init__(self, x, y, change_x, change_y):
        pygame.sprite.Sprite.__init__(self)
        self.change_x = change_x
        self.change_y = change_y
        self.image = pygame.image.load("enemy.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.intersection_positions = self.get_intersection_position()
        self.direction_change_timer = time.time() + 5

    def update(self, horizontal_blocks, vertical_blocks):
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH
        elif self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = SCREEN_HEIGHT
        elif self.rect.top > SCREEN_HEIGHT:
            self.rect.bottom = 0
        if self.rect.topleft in self.intersection_positions:
            current_time = time.time()
            if current_time >= self.direction_change_timer:
                self.change_direction()
                self.direction_change_timer = current_time + 5

    def change_direction(self):
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        current_direction = (self.change_x, self.change_y)
        available_directions = [
            direction for direction in directions if direction != current_direction]
        new_direction = random.choice(available_directions)
        self.change_x, self.change_y = new_direction

    def get_intersection_position(self):
        items = []
        for i, row in enumerate(enviroment()):
            for j, item in enumerate(row):
                if item == 3:
                    items.append((j * 32, i * 32))
        return items


def enviroment():
    grid = ((0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0,
             0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1,
             1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0,
             0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0,
             0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0,
             0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1,
             1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0,
             0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0,
             0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0,
             0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1,
             1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0,
             0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0,
             0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0,
             0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1,
             1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0,
             0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0), (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0))

    return grid


def draw_enviroment(screen):
    environment = enviroment()
    for i, row in enumerate(environment):
        for j, item in enumerate(row):
            if item == 1:
                pygame.draw.line(
                    screen, BLUE, [j * 32, i * 32], [j * 32 + 32, i * 32], 3)
                pygame.draw.line(
                    screen, BLUE, [j * 32, i * 32 + 32], [j * 32 + 32, i * 32 + 32], 3)
            elif item == 2:
                pygame.draw.line(
                    screen, BLUE, [j * 32, i * 32], [j * 32, i * 32 + 32], 3)
                pygame.draw.line(
                    screen, BLUE, [j * 32 + 32, i * 32], [j * 32 + 32, i * 32 + 32], 3)


class Game(object):
    def __init__(self):
        self.player = Pacman(32, 128, "pacman.png")
        self.horizontal_blocks = pygame.sprite.Group()
        self.vertical_blocks = pygame.sprite.Group()
        self.dots_group = pygame.sprite.Group()
        for i, row in enumerate(enviroment()):
            for j, item in enumerate(row):
                if item == 1:
                    self.horizontal_blocks.add(
                        Block(j * 32 + 8, i * 32 + 8, BLACK, 16, 16))
                elif item == 2:
                    self.vertical_blocks.add(
                        Block(j * 32 + 8, i * 32 + 8, BLACK, 16, 16))
        self.enemies = pygame.sprite.Group()
        self.enemies.add(Enemies(288, 96, 0, 2))
        self.enemies.add(Enemies(288, 320, 0, -2))
        self.enemies.add(Enemies(544, 128, 0, 2))
        self.enemies.add(Enemies(32, 224, 0, 2))

        for i, row in enumerate(enviroment()):
            for j, item in enumerate(row):
                if item != 0:
                    self.dots_group.add(
                        Ellipse(j * 32 + 12, i * 32 + 12, WHITE, 8, 8))

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.player.move_right()
                elif event.key == pygame.K_LEFT:
                    self.player.move_left()
                elif event.key == pygame.K_UP:
                    self.player.move_up()
                elif event.key == pygame.K_DOWN:
                    self.player.move_down()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.player.stop_move_right()
                elif event.key == pygame.K_LEFT:
                    self.player.stop_move_left()
                elif event.key == pygame.K_UP:
                    self.player.stop_move_up()
                elif event.key == pygame.K_DOWN:
                    self.player.stop_move_down()

    def run_logic(self):
        self.player.update(self.horizontal_blocks, self.vertical_blocks)
        collided_dots = pygame.sprite.spritecollide(
            self.player, self.dots_group, True)
        collided_enemies = pygame.sprite.spritecollide(
            self.player, self.enemies, True)
        self.enemies.update(self.horizontal_blocks, self.vertical_blocks)

        if len(self.enemies) == 0:
            self.enemies.add(Enemies(288, 96, 0, 2))
            self.enemies.add(Enemies(288, 320, 0, -2))
            self.enemies.add(Enemies(544, 128, 0, 2))
            self.enemies.add(Enemies(32, 224, 0, 2))

    def display_frame(self, screen):
        screen.fill(BLACK)
        self.horizontal_blocks.draw(screen)
        self.vertical_blocks.draw(screen)
        draw_enviroment(screen)
        self.dots_group.draw(screen)
        self.enemies.draw(screen)
        screen.blit(self.player.image, self.player.rect)
        pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    game = Game()
    done = False
    while not done:
        done = game.process_events()
        game.run_logic()
        game.display_frame(screen)
        clock.tick(30)


if __name__ == '__main__':
    main()
