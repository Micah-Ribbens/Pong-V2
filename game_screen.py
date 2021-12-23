import pygame
from base_pong.engines import CollisionsEngine
from base_pong.utility_classes import HistoryKeeper
from base_pong.score_keeper import ScoreKeeper
from base_pong.players import Player
from base_pong.ball import Ball
from base_pong.HUD import HUD
from base_pong.important_variables import *
from base_pong.velocity_calculator import VelocityCalculator
import time
from game_modes.portal_pong import PortalPong
from base_pong.colors import *
from game_modes.game_mode_selector import GameModeSelector
from GUI.screen import Screen

nameOfGame = "robowars"
pygame.display.set_caption(f'{nameOfGame}')

# Game Screen as in where the game is actually played not selection screens and the sort


class GameScreen(Screen):
    game_mode = None
    pause_is_held_down = False
    game_paused = False
    ball = Ball()
    player1 = Player()
    player2 = Player()
    player1_score = 0
    player2_score = 0

    def set_up():
        GameScreen.game_mode = GameModeSelector.get_pong_type()
        GameScreen.ball.reset()
        GameScreen.game_mode.reset(GameScreen.ball, GameScreen.player1,
                                   GameScreen.player2)
        GameScreen.ball.name = "ball"
        GameScreen.player2.color, GameScreen.player2.outline_color = white, blue
        GameScreen.player1.name = "player1"
        GameScreen.player2.name = "player2"
        GameScreen.player1.up_key = pygame.K_w
        GameScreen.player1.down_key = pygame.K_s
        GameScreen.player1.right_key = pygame.K_d
        GameScreen.player1.left_key = pygame.K_a
        GameScreen.player2.x_coordinate = screen_length - GameScreen.player2.length

    def reset_after_scoring():
        HistoryKeeper.reset()
        GameScreen.ball.reset()
        GameScreen.game_mode.reset(GameScreen.ball, GameScreen.player1,
                                   GameScreen.player2)

    def run():
        GameScreen.game_mode.add_needed_objects(
            GameScreen.ball, GameScreen.player1, GameScreen.player2)

        ScoreKeeper.show_score(GameScreen.player1_score,
                               GameScreen.player2_score)

        GameScreen.game_mode.draw_game_objects(
            GameScreen.ball, GameScreen.player1, GameScreen.player2)

        GameScreen.game_mode.ball_collisions(
            GameScreen.ball, GameScreen.player1, GameScreen.player2)

        GameScreen.player1.movement()
        GameScreen.player2.movement()
        CollisionsEngine.paddle_movements(GameScreen.player1)
        CollisionsEngine.paddle_movements(GameScreen.player2)
        GameScreen.game_mode.run(GameScreen.ball, GameScreen.player1,
                                 GameScreen.player2)

        if GameScreen.game_mode.player2_has_scored(GameScreen.ball, GameScreen.player2):
            GameScreen.player2_score += 1
            GameScreen.reset_after_scoring()

        if GameScreen.game_mode.player1_has_scored(GameScreen.ball, GameScreen.player1):
            GameScreen.player1_score += 1
            GameScreen.reset_after_scoring()
