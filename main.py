#Imports
import pygame
from constants import *
from player import Player,Shot
from asteroid import Asteroid
from asteroidfield import AsteroidField

pygame.init()

screen = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h))

def main():
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2
    clock = pygame.time.Clock()
    dt = 0
    #Groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    #Containers
    Asteroid.containers = (asteroids, updatable, drawable)
    Player.containers = (updatable, drawable)
    Shot.containers = (updatable, drawable, shots)
    AsteroidField.containers = updatable
    #Objects
    player = Player(x,y)
    asteroidfield = AsteroidField()
    #Game Loop
    while True:
        #dt
        dt = clock.tick(60) / 1000
        #Exiting
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        #Update
        for updating in updatable:
            if updating == player:
                updating.cooldown -= dt
            updating.update(dt)

        #Drawing
        pygame.Surface.fill(screen, (0,0,0))
        for drawing in drawable:
            drawing.draw(screen)
        #Collision check
        for steroid in asteroids:
            if True == steroid.collision_check(player):
                print("Game over!")
                exit()
            for bullet in shots:
                if True == steroid.collision_check(bullet):
                    steroid.split()
                    pygame.sprite.Sprite.kill(bullet)
        #Flip       
        pygame.display.flip()


if __name__ == "__main__":
    main()

