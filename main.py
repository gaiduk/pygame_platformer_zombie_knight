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
    def __init__(self, player, zombie_group, platform_group, portal_group, bullet_group, ruby_group):
        # Set constant variables
        self.STARING_ROUND_TIME = 30
        self.STARING_ZOMBIE_CREATION_TIME = 3

        # SET game values
        self.score = 0
        self.round_number = 1
        self.frame_count = 0
        self.round_time = self.STARING_ROUND_TIME
        self.zombie_creation_time = self.STARING_ZOMBIE_CREATION_TIME

        self.title_font = pygame.font.Font("fonts/Poultrygeist.ttf", 48)
        self.HUD_font = pygame.font.Font("fonts/Pixel.ttf", 25)

        self.lost_ruby_sound = pygame.mixer.Sound("sounds/lost_ruby.wav")
        self.ruby_pickup_sound = pygame.mixer.Sound("sounds/ruby_pickup.wav")
        pygame.mixer.music.load("sounds/level_music.wav")


        self.player = player
        self.zombie_group = zombie_group
        self.platform_group = platform_group
        self.portal_group = portal_group
        self.bullet_group = bullet_group
        self.ruby_group = ruby_group

    def update(self):
        self.frame_count += 1
        if self.frame_count % FPS == 0:
            self.round_time -= 1
            self.frame_count = 0

        self.check_collisions()

        self.add_zombie()
        self.check_round_complition()
        self.check_game_over()

    def draw(self):
        WHITE = (255, 255, 255)
        GREEN = (27, 201, 27)

        score_text = self.HUD_font.render("Score: " + str(self.score), True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.topleft = (10, WINDOW_HEIGHT - 51)

        health_text = self.HUD_font.render("Health: " + str(self.player.health), True, WHITE)
        health_rect = health_text.get_rect()
        health_rect.topleft = (10, WINDOW_HEIGHT - 26)

        title_text = self.title_font.render("Knight vs Zombies", True, GREEN)
        title_rect = title_text.get_rect()
        title_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 26)

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
        if self.frame_count % FPS == 0:
            if self.round_time % self.zombie_creation_time == 0:
                zombie = Zombie(my_platform_group, my_portal_group, self.round_number, 4 + self.round_number)
                my_zombie_group.add(zombie)


    def check_collisions(self):
        collision_dict = pygame.sprite.groupcollide(self.bullet_group, self.zombie_group, True, False)
        if collision_dict:
            for zombies in collision_dict.values():
                for zombie in zombies:
                    if zombie.is_dead == False:
                        ruby = Ruby(self.platform_group, self.portal_group)
                        self.ruby_group.add(ruby)

                    zombie.hit_sound.play()
                    zombie.is_dead = True
                    zombie.animate_death = True


        collision_list = pygame.sprite.spritecollide(self.player, self.zombie_group, False)
        if collision_list:
            for zombie in collision_list:
                if zombie.is_dead:
                    zombie.kick_sound.play()
                    zombie.kill()
                    self.score += 1

                else:
                    self.player.health -= 20
                    self.player.hit_sound.play()
                    zombie.is_dead = True
                    self.player.position.y -= 20
                    self.player.rect.bottomleft = self.player.position

        if pygame.sprite.spritecollide(self.player, self.ruby_group, True):
            self.ruby_pickup_sound.play()
            self.score += 5

        for zombie in self.zombie_group:
            if zombie.is_dead == False:
                if pygame.sprite.spritecollide(zombie, self.ruby_group, True):
                    self.lost_ruby_sound.play()
                    zombie = Zombie(self.platform_group, self.portal_group, self.round_number, 4 + self.round_number)

                    self.zombie_group.add(zombie)

    def check_round_complition(self):
        if self.round_time == 0:
            self.start_new_round()

    def check_game_over(self):
        if self.player.health <= 0:
            pygame.mixer.music.stop()
            self.pause_game("GAME OVER! Score: " + str(self.score), "Press 'ENTER' to try again... ")

    def start_new_round(self):
        self.round_number += 1

        self.round_time = self.STARING_ROUND_TIME + self.round_number + 2
        self.zombie_group.empty()
        self.ruby_group.empty()
        self.bullet_group.empty()
        self.player.reset()

        self.pause_game("You survived the night! Score: " + str(self.score), "Press 'ENTER' to continue... ")
        self.reset_game()


    def pause_game(self, main_text, sub_text):
        global running

        pygame.mixer.music.pause()

        WHITE = (255, 255, 255)
        GREEN = (27, 201, 27)
        BLACK = (0, 0, 0)

        if self.player.health <= 0:
            main_text = self.title_font.render(main_text, True, (233, 0, 0))
            main_text_rect = main_text.get_rect()
            main_text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        else:
            main_text = self.title_font.render(main_text, True, GREEN)
            main_text_rect = main_text.get_rect()
            main_text_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

        sub_text = self.title_font.render(sub_text, True, WHITE)
        sub_text_rect = sub_text.get_rect()
        sub_text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 67)

        display_surface.fill(BLACK)
        display_surface.blit(main_text, main_text_rect)
        display_surface.blit(sub_text, sub_text_rect)
        pygame.display.update()

        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        is_paused = False
                        pygame.mixer.music.unpause()
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False
                    pygame.mixer.music.stop()

    def reset_game(self):
        self.score = 0
        self.round_time = self.STARING_ROUND_TIME
        self.round_time = 1

        self.zombie_creation_time = self.STARING_ZOMBIE_CREATION_TIME

        self.player.health = self.player.STARTING_HEALTH
        self.player.reset()

        self.zombie_group.empty()
        self.ruby_group.empty()
        self.bullet_group.empty()

        pygame.mixer.music.play(-1, 0.0)


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

        # Create a mask for better collision
        self.mask = pygame.mask.from_surface(self.image)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, platform_group, portal_group, bullet_group):
        super().__init__()

        self.HORIZONTAL_ACCELERATION = 2
        self.VERTICAL_ACCELERATION = 0.8  # Gravity
        self.HORIZONTAL_FRICTION = 0.15
        self.VERTICAL_JUMP_SPEED = 18
        self.STARTING_HEALTH = 100

        # Animations frames
        self.move_right_sprites = []
        self.move_left_sprites = []

        self.idle_right_sprites = []
        self.idle_left_sprites = []

        self.jump_right_sprites = []
        self.jump_left_sprites = []

        self.attack_right_sprites = []
        self.attack_left_sprites = []

        # Moving
        self.move_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/run/Run (1).png"), (64, 64)))
        self.move_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/run/Run (2).png"), (64, 64)))
        self.move_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/run/Run (3).png"), (64, 64)))
        self.move_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/run/Run (4).png"), (64, 64)))
        self.move_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/run/Run (5).png"), (64, 64)))
        self.move_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/run/Run (6).png"), (64, 64)))
        self.move_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/run/Run (7).png"), (64, 64)))
        self.move_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/run/Run (8).png"), (64, 64)))
        self.move_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/run/Run (9).png"), (64, 64)))
        self.move_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/run/Run (10).png"), (64, 64)))

        # change direction to the left side
        for sprite in self.move_right_sprites:
            self.move_left_sprites.append(pygame.transform.flip(sprite, True, False))

        # Idle
        self.idle_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/idle/Idle (1).png"), (64, 64)))
        self.idle_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/idle/Idle (2).png"), (64, 64)))
        self.idle_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/idle/Idle (3).png"), (64, 64)))
        self.idle_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/idle/Idle (4).png"), (64, 64)))
        self.idle_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/idle/Idle (5).png"), (64, 64)))
        self.idle_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/idle/Idle (6).png"), (64, 64)))
        self.idle_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/idle/Idle (7).png"), (64, 64)))
        self.idle_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/idle/Idle (8).png"), (64, 64)))
        self.idle_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/idle/Idle (9).png"), (64, 64)))
        self.idle_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/idle/Idle (10).png"), (64, 64)))

        # change direction to the left side
        for sprite in self.idle_right_sprites:
            self.idle_left_sprites.append(pygame.transform.flip(sprite, True, False))

        # Jump
        self.jump_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/jump/Jump (1).png"), (64, 64)))
        self.jump_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/jump/Jump (2).png"), (64, 64)))
        self.jump_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/jump/Jump (3).png"), (64, 64)))
        self.jump_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/jump/Jump (4).png"), (64, 64)))
        self.jump_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/jump/Jump (5).png"), (64, 64)))
        self.jump_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/jump/Jump (6).png"), (64, 64)))
        self.jump_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/jump/Jump (7).png"), (64, 64)))
        self.jump_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/jump/Jump (8).png"), (64, 64)))
        self.jump_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/jump/Jump (9).png"), (64, 64)))
        self.jump_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/jump/Jump (10).png"), (64, 64)))

        # change direction to the left side
        for sprite in self.jump_right_sprites:
            self.jump_left_sprites.append(pygame.transform.flip(sprite, True, False))

        # Attack
        self.attack_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/attack/Attack (1).png"), (64, 64)))
        self.attack_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/attack/Attack (2).png"), (64, 64)))
        self.attack_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/attack/Attack (3).png"), (64, 64)))
        self.attack_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/attack/Attack (4).png"), (64, 64)))
        self.attack_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/attack/Attack (5).png"), (64, 64)))
        self.attack_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/attack/Attack (6).png"), (64, 64)))
        self.attack_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/attack/Attack (7).png"), (64, 64)))
        self.attack_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/attack/Attack (8).png"), (64, 64)))
        self.attack_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/attack/Attack (9).png"), (64, 64)))
        self.attack_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/attack/Attack (10).png"), (64, 64)))

        # change direction to the left side
        for sprite in self.attack_right_sprites:
            self.attack_left_sprites.append(pygame.transform.flip(sprite, True, False))

        # Load img and get rect
        self.current_sprite = 0
        self.image = self.idle_right_sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

        self.platform_group = platform_group
        self.portal_group = portal_group
        self.bullet_group = bullet_group

        # Animation booleans
        self.animate_jump = False
        self.animate_fire = False

        # Sounds
        self.jump_sound = pygame.mixer.Sound("sounds/jump_sound.wav")
        self.slash_sound = pygame.mixer.Sound("sounds/slash_sound.wav")
        self.portal_sound = pygame.mixer.Sound("sounds/portal_sound.wav")
        self.hit_sound = pygame.mixer.Sound("sounds/player_hit.wav")

        # kinematics vectors
        self.position = vector(x, y)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, self.VERTICAL_ACCELERATION)

        # Set initial player variables
        self.health = self.STARTING_HEALTH
        self.starting_x = x
        self.starting_y = y

    def update(self):
        self.move()
        self.check_collisions()
        self.check_animations()

        #Update player mask for better collision
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        # Set acceleration vector
        self.acceleration = vector(0, self.VERTICAL_ACCELERATION)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acceleration.x = -1 * self.HORIZONTAL_ACCELERATION
            self.animate(self.move_left_sprites, 0.5)
        elif keys[pygame.K_RIGHT]:
            self.acceleration.x = self.HORIZONTAL_ACCELERATION
            self.animate(self.move_right_sprites, 0.5)
        else:
            if self.velocity.x > 0:
                self.animate(self.idle_right_sprites, 0.5)
            else:
                self.animate(self.idle_left_sprites, 0.5)

        # Calculate new kinematics values
        self.acceleration.x -= self.velocity.x * self.HORIZONTAL_FRICTION
        self.velocity += self.acceleration

        self.position += self.velocity + 0.5 * self.acceleration

        # Update rect
        if self.position.x < 0:
            self.position.x = WINDOW_WIDTH
        elif self.position.x > WINDOW_WIDTH:
            self.position.x = 0

        self.rect.bottomleft = self.position

    def check_collisions(self):
        if self.velocity.y > 0:
            collided_platforms = pygame.sprite.spritecollide(self, self.platform_group, False, pygame.sprite.collide_mask)
            if collided_platforms:
                self.position.y = collided_platforms[0].rect.top + 5
                self.velocity.y = 0

        # Collision when jumping up
        if self.velocity.y < 0:
            collided_platforms = pygame.sprite.spritecollide(self, self.platform_group, False, pygame.sprite.collide_mask)
            if collided_platforms:
                self.velocity.y = 0
                while pygame.sprite.spritecollide(self, self.platform_group, False):
                    self.position.y += 1
                    self.rect.bottomleft = self.position

        # Collision for portals
        if pygame.sprite.spritecollide(self, self.portal_group, False):
            self.portal_sound.play()

            if self.position.x > WINDOW_WIDTH // 2:
                self.position.x = 86
            else:
                self.position.x = WINDOW_WIDTH - 150

            if self.position.y > WINDOW_HEIGHT // 2:
                self.position.y = 64
            else:
                self.position.y = WINDOW_HEIGHT - 132

            self.rect.bottomleft = self.position

    def check_animations(self):
        if self.animate_jump:
            if self.velocity.x > 0:
                self.animate(self.jump_right_sprites, 0.1)
            else:
                self.animate(self.jump_left_sprites, 0.1)

        if self.animate_fire:
            if self.velocity.x > 0:
                self.animate(self.attack_right_sprites, 0.26)
            else:
                self.animate(self.attack_left_sprites, 0.26)

    def jump(self):
        if pygame.sprite.spritecollide(self, self.platform_group, False):
            self.jump_sound.play()
            self.velocity.y = -1 * self.VERTICAL_JUMP_SPEED
            self.animate_jump = True

    def fire(self):
        self.slash_sound.play()
        Bullet(self.rect.centerx, self.rect.centery, self.bullet_group, self)
        self.animate_fire = True

    def reset(self):
        self.velocity = (0, 0)
        self.position = vector(self.starting_x, self.starting_y)
        self.rect.bottomleft = self.position

    def animate(self, sprite_list, speed):
        if self.current_sprite < len(sprite_list) - 1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0
            # End jump and attack anim
            if self.animate_jump:
                self.animate_jump = False
            if self.animate_fire:
                self.animate_fire = False

        self.image = sprite_list[int(self.current_sprite)]


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_group, player):
        super().__init__()

        self.VELOCITY = 20
        self.RANGE = 500

        if player.velocity.x > 0:
            self.image = pygame.transform.scale(pygame.image.load("images/player/slash.png"), (32, 32))
        else:
            self.image = pygame.transform.scale(pygame.transform.flip(pygame.image.load("images/player/slash.png"),
                                                                      True, False), (32, 32))
            self.VELOCITY = -1 * self.VELOCITY

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.starting_x = x

        bullet_group.add(self)

    def update(self):
        self.rect.x += self.VELOCITY

        if abs(self.rect.x - self.starting_x) > self.RANGE:
            self.kill()


class Zombie(pygame.sprite.Sprite):
    def __init__(self, platform_group, portal_group, min_speed, max_speed):
        super().__init__()
        self.VERTICAL_ACCELERATION = 3
        self.RISE_TIME = 2

        # Animation frames
        self.walk_right_sprites = []
        self.walk_left_sprites = []

        self.die_right_sprites = []
        self.die_left_sprites = []

        self.rise_right_sprites = []
        self.rise_left_sprites = []

        gender = random.randint(0, 1)
        if gender == 0:
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/walk/Walk (1).png"), (64, 64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/walk/Walk (2).png"), (64, 64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/walk/Walk (3).png"), (64, 64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/walk/Walk (4).png"), (64, 64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/walk/Walk (5).png"), (64, 64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/walk/Walk (6).png"), (64, 64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/walk/Walk (7).png"), (64, 64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/walk/Walk (8).png"), (64, 64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/walk/Walk (9).png"), (64, 64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/walk/Walk (10).png"), (64, 64)))

            for sprite in self.walk_right_sprites:
                self.walk_left_sprites.append(pygame.transform.flip(sprite, True, False))

            self.die_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (1).png"), (64, 64)))
            self.die_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (2).png"), (64, 64)))
            self.die_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (3).png"), (64, 64)))
            self.die_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (4).png"), (64, 64)))
            self.die_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (5).png"), (64, 64)))
            self.die_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (6).png"), (64, 64)))
            self.die_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (7).png"), (64, 64)))
            self.die_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (8).png"), (64, 64)))
            self.die_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (9).png"), (64, 64)))
            self.die_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (10).png"), (64, 64)))

            for sprite in self.die_right_sprites:
                self.die_left_sprites.append(pygame.transform.flip(sprite, True, False))

            self.rise_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (10).png"), (64, 64)))
            self.rise_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (9).png"), (64, 64)))
            self.rise_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (8).png"), (64, 64)))
            self.rise_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (7).png"), (64, 64)))
            self.rise_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (6).png"), (64, 64)))
            self.rise_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (5).png"), (64, 64)))
            self.rise_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (4).png"), (64, 64)))
            self.rise_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (3).png"), (64, 64)))
            self.rise_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (2).png"), (64, 64)))
            self.rise_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (1).png"), (64, 64)))

            for sprite in self.rise_right_sprites:
                self.rise_left_sprites.append(pygame.transform.flip(sprite, True, False))
        else:
            self.walk_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/walk/Walk (1).png"), (64, 64)))
            self.walk_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/walk/Walk (2).png"), (64, 64)))
            self.walk_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/walk/Walk (3).png"), (64, 64)))
            self.walk_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/walk/Walk (4).png"), (64, 64)))
            self.walk_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/walk/Walk (5).png"), (64, 64)))
            self.walk_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/walk/Walk (6).png"), (64, 64)))
            self.walk_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/walk/Walk (7).png"), (64, 64)))
            self.walk_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/walk/Walk (8).png"), (64, 64)))
            self.walk_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/walk/Walk (9).png"), (64, 64)))
            self.walk_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/walk/Walk (10).png"), (64, 64)))

            for sprite in self.walk_right_sprites:
                self.walk_left_sprites.append(pygame.transform.flip(sprite, True, False))

            self.die_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (1).png"), (64, 64)))
            self.die_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (2).png"), (64, 64)))
            self.die_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (3).png"), (64, 64)))
            self.die_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (4).png"), (64, 64)))
            self.die_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (5).png"), (64, 64)))
            self.die_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (6).png"), (64, 64)))
            self.die_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (7).png"), (64, 64)))
            self.die_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (8).png"), (64, 64)))
            self.die_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (9).png"), (64, 64)))
            self.die_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (10).png"), (64, 64)))

            for sprite in self.die_right_sprites:
                self.die_left_sprites.append(pygame.transform.flip(sprite, True, False))

            self.rise_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (10).png"), (64, 64)))
            self.rise_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (9).png"), (64, 64)))
            self.rise_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (8).png"), (64, 64)))
            self.rise_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (7).png"), (64, 64)))
            self.rise_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (6).png"), (64, 64)))
            self.rise_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (5).png"), (64, 64)))
            self.rise_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (4).png"), (64, 64)))
            self.rise_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (3).png"), (64, 64)))
            self.rise_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (2).png"), (64, 64)))
            self.rise_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (1).png"), (64, 64)))

            for sprite in self.rise_right_sprites:
                self.rise_left_sprites.append(pygame.transform.flip(sprite, True, False))

        self.direction = random.choice([-1, 1])
        self.current_sprite = 0

        if self.direction == 1:
            self.image = self.walk_right_sprites[self.current_sprite]
        else:
            self.image = self.walk_left_sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.bottomleft = (random.randint(100, WINDOW_WIDTH - 100), -100)

        self.platform_group = platform_group
        self.portal_group = portal_group

        self.animate_death = False
        self.animate_rise = False

        self.hit_sound = pygame.mixer.Sound("sounds/zombie_hit.wav")
        self.kick_sound = pygame.mixer.Sound("sounds/zombie_kick.wav")
        self.portal_sound = pygame.mixer.Sound("sounds/portal_sound.wav")

        self.position = vector(self.rect.x, self.rect.y)
        self.velocity = vector(self.direction * random.randint(min_speed, max_speed), 0)
        self.acceleration = vector(0, self.VERTICAL_ACCELERATION)

        self.is_dead = False
        self.round_time = 0
        self.frame_count = 0

    def update(self):
        self.move()
        self.check_collisions()
        self.check_animations()

        if self.is_dead:
            self.frame_count += 1
            if self.frame_count % FPS == 0:
                self.round_time += 1
                if self.round_time == self.RISE_TIME:
                    self.animate_rise = True

                    self.current_sprite = 0

    def move(self):
        if not self.is_dead:
            if self.direction == -1:
                self.animate(self.walk_left_sprites, 0.5)
            else:
                self.animate(self.walk_right_sprites, 0.5)

            self.velocity += self.acceleration
            self.position += self.velocity + 0.5 * self.acceleration

            # Update rect
            if self.position.x < 0:
                self.position.x = WINDOW_WIDTH
            elif self.position.x > WINDOW_WIDTH:
                self.position.x = 0

            self.rect.bottomleft = self.position

    def check_collisions(self):
        collided_platforms = pygame.sprite.spritecollide(self, self.platform_group, False)
        if collided_platforms:
            self.position.y = collided_platforms[0].rect.top + 1
            self.velocity.y = 0

        # Collision for portals
        if pygame.sprite.spritecollide(self, self.portal_group, False):
            self.portal_sound.play()

            if self.position.x > WINDOW_WIDTH // 2:
                self.position.x = 86
            else:
                self.position.x = WINDOW_WIDTH - 150

            if self.position.y > WINDOW_HEIGHT // 2:
                self.position.y = 64
            else:
                self.position.y = WINDOW_HEIGHT - 132

            self.rect.bottomleft = self.position

    def check_animations(self):
        if self.animate_death:
            if self.direction == 1:
                self.animate(self.die_right_sprites, 0.9)
            else:
                self.animate(self.die_left_sprites, 0.9)

        if self.animate_rise:
            if self.direction == 1:
                self.animate(self.rise_right_sprites, 0.9)
            else:
                self.animate(self.rise_left_sprites, 0.9)

    def animate(self, sprite_list, speed):
        if self.current_sprite < len(sprite_list) - 1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0

            if self.animate_death:
                self.current_sprite = len(sprite_list) - 1
                self.animate_death = False

            if self.animate_rise:
                self.animate_rise = False
                self.is_dead = False
                self.frame_count = 0
                self.round_time = 0

        self.image = sprite_list[int(self.current_sprite)]


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
    def __init__(self, platform_group, portal_group):
        super().__init__()

        self.VERTICAL_VELOCITY = 3
        self.HORIZONTAL_VELOCITY = 5

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
        self.rect.bottomleft = (WINDOW_WIDTH//2, 100)

        self.platform_group = platform_group
        self.portal_group = portal_group

        self.portal_sound = pygame.mixer.Sound("sounds/portal_sound.wav")

        self.position = vector(self.rect.x, self.rect.y)
        self.velocity = vector(random.choice([-1*self.HORIZONTAL_VELOCITY, self.HORIZONTAL_VELOCITY]), 0)
        self.acceleration = vector(0, self.VERTICAL_VELOCITY)


    def update(self):
        self.animate(self.ruby_sprites, 0.25)
        self.move()
        self.check_collisions()

    def move(self):
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration

        # Update rect
        if self.position.x < 0:
            self.position.x = WINDOW_WIDTH
        elif self.position.x > WINDOW_WIDTH:
            self.position.x = 0

        self.rect.bottomleft = self.position

    def check_collisions(self):
        collided_platforms = pygame.sprite.spritecollide(self, self.platform_group, False)
        if collided_platforms:
            self.position.y = collided_platforms[0].rect.top + 1
            self.velocity.y = 0

        # Collision for portals
        if pygame.sprite.spritecollide(self, self.portal_group, False):
            self.portal_sound.play()

            if self.position.x > WINDOW_WIDTH // 2:
                self.position.x = 86
            else:
                self.position.x = WINDOW_WIDTH - 150

            if self.position.y > WINDOW_HEIGHT // 2:
                self.position.y = 64
            else:
                self.position.y = WINDOW_HEIGHT - 132

            self.rect.bottomleft = self.position

    def animate(self, sprite_list, speed):
        if self.current_sprite < len(sprite_list) - 1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0

        self.image = sprite_list[int(self.current_sprite)]


class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, colour, portal_group):
        super().__init__()

        # Animations list
        self.portal_sprites = []

        # Portal animations
        if colour == "green":
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile000.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile001.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile002.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile003.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile004.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile005.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile006.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile007.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile008.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile009.png"), (72, 72)))
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
# 0 -> no tile, 1 -> dirt, 2-5 -> platforms, 6 -> ruby maker, 7-8 -> portals, 9 -> player
# 23 rows and 40 columns
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
            my_player = Player(j * 32 - 32, i * 32 + 32, my_platform_group, my_portal_group, my_bullet_group)
            my_player_group.add(my_player)

background_image = pygame.transform.scale(pygame.image.load("images/background.png"), (1280, 736))
background_rect = background_image.get_rect()
background_rect.topleft = (0, 0)

my_game = Game(my_player, my_zombie_group, my_platform_group, my_portal_group, my_bullet_group, my_ruby_group)
my_game.pause_game("Knight VS Zombies", "Press 'ENTER' to begin")
pygame.mixer.music.play(-1, 0.0)

# Main loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                my_player.jump()

            if event.key == pygame.K_SPACE:
                my_player.fire()
            # Test zombie
            if event.key == pygame.K_z:
                zombie = Zombie(my_platform_group, my_portal_group, 3, 5)
                my_zombie_group.add(zombie)

    # blit bg
    display_surface.blit(background_image, background_rect)

    # Draw tiles and update
    my_main_tile_group.update()
    my_main_tile_group.draw(display_surface)

    my_portal_group.update()
    my_portal_group.draw(display_surface)

    my_player_group.update()
    my_player_group.draw(display_surface)

    my_bullet_group.update()
    my_bullet_group.draw(display_surface)

    my_zombie_group.update()
    my_zombie_group.draw(display_surface)

    my_ruby_group.update()
    my_ruby_group.draw(display_surface)

    # Draw and update game
    my_game.update()
    my_game.draw()

    # Update display and tick clock
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
