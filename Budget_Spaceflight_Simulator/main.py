"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import os
import random
import sys
import threading

import pygame

sys.setrecursionlimit(10**7)
threading.stack_size(2**27)

pygame.init()
pygame.font.init()

# set the screen and caption
WIDTH, HEIGHT = 700, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Budget_Spaceflight_Simulator")
FPS = 60

# Set the Spaceship
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 29.6, 68.5
SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'rocket.png'))
SPACESHIP = pygame.transform.scale(SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

SPACESHIP2_IMAGE = pygame.image.load(os.path.join('Assets', 'rocket2.png'))
SPACESHIP2 = pygame.transform.scale(SPACESHIP2_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

SPACESHIP3_IMAGE = pygame.image.load(os.path.join('Assets', 'rocket3.png'))
SPACESHIP3 = pygame.transform.scale(SPACESHIP3_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

# Set the different fonts to be used
small_font = pygame.font.SysFont('courier', 20)
middle_font = pygame.font.SysFont('courier', 25)
large_font = pygame.font.SysFont('courier', 30)

# Set the colours used
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Set the background images to be used
BACKGROUND_IMAGE = pygame.image.load(os.path.join('Assets', "Background.png"))
BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))


class Player:
    def __init__(self, x, y, y_speed, ship_rotation):
        self.image = SPACESHIP
        self.x = x
        self.y = y
        self.y_speed = y_speed
        self.angle = 0
        self.rotate = ship_rotation
        self.rect = self.image.get_rect()

    # Change the x and y values of the object
    def move(self):
        self.y += self.y_speed
        self.angle += self.rotate

    def display(self, fuel_value):
        self.image = pygame.transform.rotate(SPACESHIP, self.angle)

        # change to thrusting ship if a key is pressed
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_UP]:
            self.image = pygame.transform.rotate(SPACESHIP3, self.angle)
        if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_UP]:
            self.image = pygame.transform.rotate(SPACESHIP2, self.angle)
        if fuel_value <= 0:
            self.image = pygame.transform.rotate(SPACESHIP, self.angle)

    def collided_with(self, other):
        return self.rect.colliderect(other.rect)


def draw_menu():
    """
    controls start-menu look
    """
    welcome_text = middle_font.render("Welcome to the budget-spaceflight-simulator", True, WHITE)
    start_text = middle_font.render("press ENTER to start", True, WHITE)

    WIN.fill(BLACK)
    WIN.blit(welcome_text, (WIDTH / 2 - int(welcome_text.get_width() / 2), HEIGHT / 2 - 40))
    WIN.blit(start_text, (WIDTH / 2 - int(start_text.get_width() / 2), HEIGHT / 2 + 40))

    pygame.display.update()


def draw_window(ship, fuel_value):
    """
    controls game-design
    """
    WIN.blit(BACKGROUND, (0, 0))
    WIN.blit(ship.image, (ship.x - int(ship.image.get_width() / 2) + 5, ship.y - int(ship.image.get_height() / 2)))

    altitude_text = small_font.render("Altitude: " + str(int(HEIGHT - ship.y)) + "km", True, WHITE)
    speed_text = small_font.render("Speed: " + str(round(ship.y_speed, 1)) + "km/s", True, GREEN)
    angle_text = small_font.render("Rotation: " + str(int(ship.angle)) + "°", True, GREEN)
    fuel_value_text = small_font.render("Fuel: " + str(int(fuel_value)) + "%", True, GREEN)

    # make sure the angle-stat stays between -180° and 180°
    if int(ship.angle) > 180:
        ship.angle = -180
    if int(ship.angle) < -180:
        ship.angle = 180

    # Update speed-stat-colour
    if ship.y_speed >= 0.5:
        speed_text = small_font.render("Speed: " + str(round(ship.y_speed, 1)) + "km/s", True, YELLOW)
    if ship.y_speed >= 1.5:
        speed_text = small_font.render("Speed: " + str(round(ship.y_speed, 1)) + "km/s", True, RED)

    # Update angle-stat-colour
    if ship.angle >= 5:
        angle_text = small_font.render("Rotation: " + str(int(ship.angle)) + "°", True, YELLOW)
    if ship.angle <= -5:
        angle_text = small_font.render("Rotation: " + str(int(ship.angle)) + "°", True, YELLOW)
    if ship.angle >= 30:
        angle_text = small_font.render("Rotation: " + str(int(ship.angle)) + "°", True, RED)
    if ship.angle <= -30:
        angle_text = small_font.render("Rotation: " + str(int(ship.angle)) + "°", True, RED)

    # Update fuel-stat-colour
    if fuel_value <= 30:
        fuel_value_text = small_font.render("Fuel: " + str(int(fuel_value)) + "%", True, YELLOW)
    if fuel_value <= 10:
        fuel_value_text = small_font.render("Fuel: " + str(int(fuel_value)) + "%", True, RED)
    if fuel_value <= 0:
        fuel_value_text = small_font.render("Fuel: 0%", True, RED)  # make sure fuel display stops at 0

    # Display the stats
    WIN.blit(altitude_text, (10, 5))
    WIN.blit(speed_text, (10, 30))
    WIN.blit(angle_text, (10, 55))
    WIN.blit(fuel_value_text, (10, 80))

    pygame.display.update()


def draw_end_succ():
    """
    end-screen if successful
    """
    succ_text = large_font.render("Well done!! Dare to try again?", True, WHITE)
    start_text = large_font.render("press ENTER to start", True, WHITE)

    WIN.blit(succ_text, (WIDTH / 2 - int(succ_text.get_width() / 2), HEIGHT / 2 - 40))
    WIN.blit(start_text, (WIDTH / 2 - int(start_text.get_width() / 2), HEIGHT / 2 + 40))

    pygame.display.update()


def draw_end_failed():
    """
    end-screen if failed
    """
    fail_text = large_font.render("Too bad!! Better luck next time", True, WHITE)
    start_text = large_font.render("press ENTER to start", True, WHITE)

    WIN.blit(fail_text, (WIDTH / 2 - int(fail_text.get_width() / 2), HEIGHT / 2 - 40))
    WIN.blit(start_text, (WIDTH / 2 - int(start_text.get_width() / 2), HEIGHT / 2 + 40))

    pygame.display.update()


def ship_movement(keys_pressed, ship_y_acceleration, ship, fuel_value, ship_rotation):
    """
    controls ship movement
    """
    if keys_pressed[pygame.K_LEFT] and fuel_value > 0:
        ship_rotation += -0.001
    if keys_pressed[pygame.K_RIGHT] and fuel_value > 0:
        ship_rotation += 0.001
    if keys_pressed[pygame.K_UP] and fuel_value > 0:
        ship_y_acceleration = -0.005

    ship.y_speed += ship_y_acceleration
    ship.rotate += ship_rotation
    ship.move()


def main():
    ship = Player(WIDTH / 2, 20, 0, 0)

    # Player-stats at the beginning
    ship_y_acceleration = 0.005
    fuel_value = 100
    ship.angle = random.randint(-100, 100)
    ship_rotation = 0

    clock = pygame.time.Clock()
    run = False
    menu = True
    while menu:
        """
        start-menu loop
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    run = True
        draw_menu()

        while run:
            """
            Main game loop
            """
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            # handle fuel usage
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_UP]:
                fuel_value -= 0.2
                if fuel_value <= 0:
                    ship_y_acceleration = 0.005

            # initialize the end of the game
            if ship.y >= HEIGHT - (120 + SPACESHIP_HEIGHT / 2):

                # check win-conditions
                if 3 >= ship_rotation >= -3 and ship.y_speed <= 0.5:
                    draw_end_succ()
                    run = False
                    end = True

                else:
                    draw_end_failed()
                    run = False
                    end = True
                # make the return to start-menu possible
                while end:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                end = False
                                run = False
                                menu = True
            ship.display(fuel_value)
            keys_pressed = pygame.key.get_pressed()
            ship_movement(keys_pressed, ship_y_acceleration, ship, fuel_value, ship_rotation)
            draw_window(ship, fuel_value)

        main()


if __name__ == "__main__":
    main()
