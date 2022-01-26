import pygame

class Sound():
    def __init__(self, mixer):
        self.mixer = mixer
        self.BGM = pygame.mixer.Sound('../audios/BGM_gameEasy_Pioneer.mp3')
        self.NORMAL_HIT_SOUND = pygame.mixer.Sound('../audios/normal_hit.wav')
        self.HARD_HIT_SOUND = pygame.mixer.Sound('../audios/powerful_hit.wav')
        self.RANDOM_ANGLE_SOUND = pygame.mixer.Sound('../audios/powerful_hit.wav')
        self.COLLISION_BALL_WALL = pygame.mixer.Sound('../audios/splash.wav')
        # self.COLLISION_BALL_BALL = pygame.mixer.Sound()

    def random_angle(self):
        self.mixer.Sound.play(self.RANDOM_ANGLE_SOUND)

    def bgm(self):
        self.mixer.Sound.play(self.BGM)

    def normal_hit(self):
        self.mixer.Sound.play(self.NORMAL_HIT_SOUND)

    def hard_hit(self):
        self.mixer.Sound.play(self.HARD_HIT_SOUND)

    def collision_ball_wall(self):
        self.mixer.Sound.play(self.COLLISION_BALL_WALL)

    def collision_ball_ball(self):
        self.mixer.Sound.play(self.COLLISION_BALL_BALL)
