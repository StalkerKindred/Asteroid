#Imports
import pygame
from constants import *
from player import Player,Shot
from asteroid import Asteroid
from asteroidfield import AsteroidField
import highscore
#activating virtual: source venv/bin/activate
pygame.init()
#Game Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def main():
    #Console
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    #Position for player
    p_x = SCREEN_WIDTH / 2
    p_y = SCREEN_HEIGHT / 2
    #Fps #Currently only 60
    clock = pygame.time.Clock()
    dt = 0
    #Drawing text on screen
    def draw_text(text, font, text_col, x, y, centered=True):
        img = font.render(text, True, text_col)
        if centered:
            text_rect = img.get_rect()
            text_rect.center = (x, y)
            screen.blit(img, text_rect)
        else:
            screen.blit(img, (x, y))
    text_font = pygame.font.SysFont(None, 30)
    #Score
    score = 0
    current_high_score = highscore.load_high_score()
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
    player = Player(p_x,p_y)
    asteroidfield = AsteroidField()
    #Start menu
    start = 1
    #Status
    game_state = "START"
    previous_game_state = game_state
    #Timer
    Countdown = 0
    Timer = 0
    Minuter = 00
    #Keys
    keys = pygame.key.get_pressed()
    #Game Loop
    while True:
        #dt
        dt = clock.tick(60) / 1000
        #Timer
        #Exiting and logic switching
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            #KeyDown logic
            elif event.type == pygame.KEYDOWN:
                #Tutorial
                if event.key == pygame.K_t:
                    if game_state == "TUTORIAL":
                        game_state = previous_game_state
                    else:
                        previous_game_state = game_state
                        game_state = "TUTORIAL"
                #Start
                elif game_state == "START":
                    game_state = "PLAYING"
                    previous_game_state = game_state
                #Deadscreen
                elif game_state == "DEATHSCREEN":
                    if event.key == pygame.K_r:
                        main()
                    elif event.key == pygame.K_ESCAPE:
                        exit()
                #Pause
                elif game_state == "PLAYING" and (event.key == pygame.K_ESCAPE or event.key == pygame.K_TAB):
                    game_state = "PAUSE"
                elif game_state == "PAUSE" and (event.key == pygame.K_ESCAPE or event.key == pygame.K_TAB):
                    game_state = "PLAYING"
        #Screen
        pygame.Surface.fill(screen, (0,0,0))
        #Version
        draw_text(f"Version: {GAME_VERSION}", text_font, (255,255,255), 3, SCREEN_HEIGHT - 20, centered=False)
        #Gamestate Logic
            #Start
        if game_state == "START":
            draw_text(f"Asteroids", text_font, (255,255,255), SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.30, centered=True)
            draw_text("Press any keys to continue", text_font, (255,255,255), SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, centered=True)
            draw_text("Press T for tutorial", text_font, (255,255,255), SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 20 , centered=True)
            #Tutorial Drawing
        elif game_state == "TUTORIAL":
            draw_text("Welcome to the tutorial screen:", text_font, (255,255,255), SCREEN_WIDTH * 0.10, SCREEN_HEIGHT * 0.10, centered=False)
            draw_text("Press W to move forward and S to move backwards", text_font, (255,255,255), SCREEN_WIDTH * 0.10, SCREEN_HEIGHT * 0.20, centered=False)
            draw_text("Press A to rotate left and D to rotate right", text_font, (255,255,255), SCREEN_WIDTH * 0.10, SCREEN_HEIGHT * 0.30, centered=False)
            draw_text("Press Space to shoot bullets", text_font, (255,255,255), SCREEN_WIDTH * 0.10, SCREEN_HEIGHT * 0.40, centered=False)
            draw_text("Shoot bullets at asteroids to increase your score", text_font, (255,255,255), SCREEN_WIDTH * 0.10, SCREEN_HEIGHT * 0.50, centered=False)
            #Game
        elif game_state == "DEATHSCREEN":
            draw_text(f"Your High Score:{current_high_score}", text_font, (255,255,255), 20, 45, centered=False)
            draw_text(f"Your Score: {score}", text_font, (255,255,255), 20, 20, centered=False)
            draw_text("Press R to restart", text_font, (255,255,255), SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2), centered=True)
            draw_text("Or ESC to quit", text_font, (255,255,255), SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) + 20, centered=True)
        elif game_state == "PLAYING" or game_state == "PAUSE":
            if game_state == "PAUSE":
                draw_text("Game is paused", text_font, (255,255,255), SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, centered=True)
            elif game_state == "PLAYING":
                #Timer logic
                Timer += dt
                if Timer >= 60:
                    Timer -= 60
                    Minuter += 1
                #Update
                for updating in updatable:
                    if updating == player:
                        updating.cooldown -= dt
                    updating.update(dt)
                #Collision check
                for steroid in asteroids:
                    if True == steroid.collision_check(player):
                        if score > current_high_score:
                            highscore.save_high_score(score)
                            if game_state == "DEATHSCREEN":
                                draw_text(f"Congratulations you managed to beat you highest score of {current_high_score}!!!", text_font, (255,255,255), SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 40, centered=True)
                            current_high_score = score
                        game_state = "DEATHSCREEN"
                    for bullet in shots:
                        if True == steroid.collision_check(bullet):
                            if steroid.radius == ASTEROID_MIN_RADIUS:  # Small asteroid
                                if "big" in steroid.origin_chain:  # From big to medium to small
                                    score += 30
                                elif "medium" in steroid.origin_chain:  # From medium to small
                                    score += 25
                                else:  # Base small asteroid
                                    score += 20
                            elif steroid.radius == ASTEROID_MAX_RADIUS - ASTEROID_MIN_RADIUS:  # Medium asteroid
                                if "big" in steroid.origin_chain:  # From big to medium
                                    score += 20
                                else:  # Base medium asteroid
                                    score += 15
                            elif steroid.radius == ASTEROID_MAX_RADIUS:  # Big asteroid
                                score += 10
                            steroid.split()
                            pygame.sprite.Sprite.kill(bullet)
            #Drawing
            for drawing in drawable:
                drawing.draw(screen)
            #Score
            draw_text(f"Score: {score}", text_font, (255,255,255), 20, 20, centered=False)
            draw_text(f"High Score:{current_high_score}", text_font, (255,255,255), 20, 45, centered=False)
            #Timer
            draw_text(f"Timer: {Minuter}:{Timer}", text_font, (255,255,255), SCREEN_WIDTH - 170, 20 , centered=False)
        #Flip       
        pygame.display.flip()


if __name__ == "__main__":
    main()

