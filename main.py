import pygame, random

vector = pygame.math.Vector2

pygame.init()

# tile size is 32 x 32.  1280/32 = 40 tiles, 736/32 = 23 tiles
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 736

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Knight vs zombie")

# Set FPS andd clock
FPS = 60
clock = pygame.time.Clock()


# define classes
class Game():
    def __init__(self):
        # Set constant variables
        self.STARING_ROUND_TIME = 30

        # SET game values
        self.score = 0
        self.round_number = 1
        self.frame_count = 0
        self.round_time = self.STARING_ROUND_TIME

        self.title_font = pygame.font.Font("fonts/Poultrygeist.ttf", 48)
        self.HUD_font = pygame.font.Font("fonts/Pixel.ttf", 25)


    def update(self):
        self.frame_count += 1
        if self.frame_count % FPS == 0:
            self.round_time -= 1
            self.frame_count = 0


    def draw(self):
        WHITE = (255, 255, 255)
        GREEN = (27, 201, 27)

        score_text = self.HUD_font.render("Score: " + str(self.score), True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.topleft = (10, WINDOW_HEIGHT - 51)

        health_text = self.HUD_font.render("Health: " + str(100), True, WHITE)
        health_rect = health_text.get_rect()
        health_rect.topleft = (10, WINDOW_HEIGHT - 26)

        title_text = self.title_font.render("Knight vs Zombies", True, GREEN)
        title_rect = title_text.get_rect()
        title_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT - 26)

        round_text = self.HUD_font.render("Round: " + str(self.round_number), True, GREEN)
        round_rect = round_text.get_rect()
        round_rect.topright = (WINDOW_WIDTH - 11, WINDOW_HEIGHT - 51)

        time_text = self.HUD_font.render("Sunrise in: " + str(self.round_time), True, GREEN)
        time_rect = time_text.get_rect()
        time_rect.topright = (WINDOW_WIDTH - 11, WINDOW_HEIGHT - 26)

        # Draw HUD
        display_surface.blit(score_text, score_rect)
        display_surface.blit(health_text, health_rect)
        display_surface.blit(title_text, title_rect)
        display_surface.blit(round_text, round_rect)
        display_surface.blit(time_text, time_rect)

    def add_zombie(self):
        pass

    def check_collisions(self):
        pass

    def check_round_complition(self):
        pass

    def check_game_over(self):
        pass

    def start_new_round(self):
        pass

    def pause_game(self):
        pass

    def reset_game(self):
        pass


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, image_int, main_group, sub_group=""):
        super().__init__()
        if image_int == 1:
            self.image = pygame.transform.scale(pygame.image.load("images/tiles/Tile (1).png"), (32, 32))
        elif image_int == 2:
            self.image = pygame.transform.scale(pygame.image.load("images/tiles/Tile (2).png"), (32, 32))
            sub_group.add(self)
        elif image_int == 3:
            self.image = pygame.transform.scale(pygame.image.load("images/tiles/Tile (3).png"), (32, 32))
            sub_group.add(self)
        elif image_int == 4:
            self.image = pygame.transform.scale(pygame.image.load("images/tiles/Tile (4).png"), (32, 32))
            sub_group.add(self)
        elif image_int == 5:
            self.image = pygame.transform.scale(pygame.image.load("images/tiles/Tile (5).png"), (32, 32))
            sub_group.add(self)

        main_group.add(self)

        # Get rect and position in grid
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)



class Player(pygame.sprite.Sprite):
    def __init__(self):
        pass

    def update(self):
        pass

    def move(self):
        pass

    def check_collisions(self):
        pass

    def check_animations(self):
        pass

    def jump(self):
        pass

    def fire(self):
        pass

    def reset(self):
        pass

    def animate(self):
        pass


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pass

    def update(self):
        pass


class Zombie(pygame.sprite.Sprite):
    def __init__(self):
        pass

    def update(self):
        pass

    def move(self):
        pass

    def check_collisions(self):
        pass

    def check_animations(self):
        pass

    def animate(self):
        pass


class RubyMaker(pygame.sprite.Sprite):
    def __init__(self, x, y, main_group):
        super().__init__()

        # Animation frames
        self.ruby_sprites = []

        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile000.png"), (64, 64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile001.png"), (64, 64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile002.png"), (64, 64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile003.png"), (64, 64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile004.png"), (64, 64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile005.png"), (64, 64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile006.png"), (64, 64)))

        self.current_sprite = 0
        self.image = self.ruby_sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

        main_group.add(self)

    def update(self):
        self.animate(self.ruby_sprites, 0.25)

    def animate(self, sprite_list, speed):
        if self.current_sprite < len(sprite_list) - 1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0

        self.image = sprite_list[int(self.current_sprite)]


class Ruby(pygame.sprite.Sprite):
    def __init__(self):
        pass

    def update(self):
        pass

    def move(self):
        pass

    def check_collisions(self):
        pass

    def animate(self):
        pass


class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, colour, portal_group):
        super().__init__()

        # Animations list
        self.portal_sprites = []

        # Portal animations
        if colour == "green":
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/green/tile000.png"), (72, 72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/green/tile001.png"), (72, 72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/green/tile002.png"), (72, 72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/green/tile003.png"), (72, 72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/green/tile004.png"), (72, 72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/green/tile005.png"), (72, 72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/green/tile006.png"), (72, 72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/green/tile007.png"), (72, 72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/green/tile008.png"), (72, 72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/green/tile009.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile010.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile011.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile012.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile013.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile014.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile015.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile016.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile017.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile018.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile019.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile020.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile021.png"), (72, 72)))

        else:
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile000.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile001.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile002.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile003.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile004.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile005.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile006.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile007.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile008.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile009.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile010.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile011.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile012.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile013.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile014.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile015.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile016.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile017.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile018.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile019.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile020.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile021.png"), (72, 72)))

        self.current_sprite = random.randint(0, len(self.portal_sprites) - 1)
        self.image = self.portal_sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

        portal_group.add(self)

    def update(self):
        self.animate(self.portal_sprites, 0.2)

    def animate(self, sprite_list, speed):
        if self.current_sprite < len(sprite_list) - 1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0

        self.image = sprite_list[int(self.current_sprite)]


# Create sprite Group
my_main_tile_group = pygame.sprite.Group()
my_platform_group = pygame.sprite.Group()

my_player_group = pygame.sprite.Group()
my_bullet_group = pygame.sprite.Group()

my_zombie_group = pygame.sprite.Group()

my_portal_group = pygame.sprite.Group()
my_ruby_group = pygame.sprite.Group()

# Create a tile map
#0 -> no tile, 1 -> dirt, 2-5 -> platforms, 6 -> ruby maker, 7-8 -> portals, 9 -> player
#23 rows and 40 columns
tile_map = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0],
    [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     8, 0],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
     4, 4],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0],
    [4, 4, 4, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 4,
     4, 4],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
     4, 4],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0],
    [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     7, 0],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
     2, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 1]
]

# Generate tile obj from tile map
# Loop through 23 rows
for i in range(len(tile_map)):
    # loop through 40 columns
    for j in range(len(tile_map[i])):
        if tile_map[i][j] == 1:
            Tile(j * 32, i * 32, 1, my_main_tile_group)

        elif tile_map[i][j] == 2:
            Tile(j * 32, i * 32, 2, my_main_tile_group, my_platform_group)
        elif tile_map[i][j] == 3:
            Tile(j * 32, i * 32, 3, my_main_tile_group, my_platform_group)
        elif tile_map[i][j] == 4:
            Tile(j * 32, i * 32, 4, my_main_tile_group, my_platform_group)
        elif tile_map[i][j] == 5:
            Tile(j * 32, i * 32, 5, my_main_tile_group, my_platform_group)

        elif tile_map[i][j] == 6:
            RubyMaker(j * 32, i * 32, my_main_tile_group)
        elif tile_map[i][j] == 7:
            Portal(j * 32, i * 32, "green", my_portal_group)
        elif tile_map[i][j] == 8:
            Portal(j * 32, i * 32, "purple", my_portal_group)
        elif tile_map[i][j] == 9:
            pass

background_image = pygame.transform.scale(pygame.image.load("images/background.png"), (1280, 736))
background_rect = background_image.get_rect()
background_rect.topleft = (0, 0)

my_game = Game()

# Main loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # blit bg
    display_surface.blit(background_image, background_rect)

    # Draw tiles and update
    my_main_tile_group.update()
    my_main_tile_group.draw(display_surface)

    my_portal_group.update()
    my_portal_group.draw(display_surface)

    # Draw and update game
    my_game.update()
    my_game.draw()

    # Update display and tick clock
    pygame.display.update()
    clock.tick(FPS)


pygame.quit()
