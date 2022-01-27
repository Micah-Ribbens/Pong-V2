from base_pong.events import Event
from base_pong.utility_classes import HistoryKeeper
from base_pong.engines import CollisionsFinder
from base_pong.ball import Ball
from base_pong.velocity_calculator import VelocityCalculator
from pong_types.pong_type import PongType
from pong_types.normal_pong import NormalPong
from base_pong.score_keeper import ScoreKeeper
from base_pong.important_variables import *
from base_pong.colors import red, white
from copy import deepcopy


class SplitPong(PongType):
    """Pong where the balls size increases until it doubles in size and after that it splits"""
    balls = []
    base_ball_length = 0
    normal_pong = None

    def __init__(self, player1, player2, ball):
        """ summary: Initializes with the PongType with the needed objects to run its methods

            params:
                player1: Paddle; the player on the leftmost side on the screen
                player2: Paddle; the player on the rightmost side on the screen
                ball: Ball; the ball that the players hit

            returns: None
        """

        super().__init__(player1, player2, ball)
        self.normal_pong = NormalPong(player1, player2, ball)
        
        self.balls.append(ball)
        ball.color = red
        
    def increase_ball_size(self, ball):
        """ summary: increases the ball's size

            params:
                ball: Ball; the ball which size should increase

            returns: None
        """

        ball.length += (self.base_ball_length * .2)
        ball.height += (self.base_ball_length * .2)

    def ball_is_ready_to_split(self, ball):
        """ summary: finds out if the ball's size is double the size of its base length

            params:
                ball: Ball; the ball that this function is testing if it is ready to split

            returns: boolean; if the ball is ready to split
        """

        return ball.length >= self.base_ball_length * 2

    def split(self, ball: Ball, new_balls, ball_has_collided_with_player1):
        """ summary: splits the ball

            params:
                ball: Ball; the ball that should be split
                new_balls: List of Ball; the new_balls that were created from splitting this cycle
                ball_has_collided_with_player1: boolean; the ball has collided with the first player

            returns: None
        """

        ball.reset()
        new_ball: Ball = deepcopy(ball)
        new_ball.color = white
        new_ball.is_moving_down = not ball.is_moving_down
        new_ball.forwards_velocity *= 1.1
        distance_change = new_ball.forwards_velocity * .1

        new_ball.is_moving_right = True if ball_has_collided_with_player1 else False

        new_ball.x_coordinate += distance_change if ball_has_collided_with_player1 else -distance_change
        new_balls.append(new_ball)

    def ball_collisions(self):
        """ summary: does all the collisions with the paddles for the ball
            params: None
            returns: None
        """

        new_balls = []
        for ball in self.balls:
            self.normal_pong._ball_collisions(ball, self.player1, self.player2)
            ball_has_collided_with_paddle1 = CollisionsFinder.is_collision(
                ball, self.player1)

            ball.render()

            # Makes sure that the ball doesn't collide into the same paddle mulitple times
            if not HistoryKeeper.get_last(f"ball_has_collided{id(ball)}") and self.ball_has_collided(ball):
                self.increase_ball_size(ball)

            if self.ball_is_ready_to_split(ball):
                self.split(ball, new_balls, ball_has_collided_with_paddle1)

        for new_ball in new_balls:
            self.balls.append(new_ball)

    def ball_has_collided(self, ball):
        """ summary: calls CollisionsFinder.is_collision() for player1 and player2

            params:
                ball
        """
        return CollisionsFinder.is_collision(ball, self.player1) or CollisionsFinder.is_collision(ball, self.player2)

    def run(self):
        self.add_needed_objects()
        for ball in self.balls:
            self.normal_pong._ball_movement(ball)

        self.ball_collisions()

    def reset(self):
        """ summary: resets everything necessary after each time someone scores
            params: None
            returns: None
        """

        # Meaning the base_pong self.ball length has not been assigned yet
        if self.base_ball_length == 0:
            self.base_ball_length = self.ball.length

        self.balls = [self.ball]
        self.ball.length = self.base_ball_length
        self.ball.height = self.base_ball_length
        self.ball.forwards_velocity = self.ball.base_forwards_velocity

    def draw_game_objects(self):
        """ summary: draws all the game objects (paddles and ball) onto the screen
            params: None
            returns: None
        """

        self.player1.render()
        self.player2.render()
        for ball in self.balls:
            ball.render()
    
    def player1_has_scored(self):
        """ summary: finds out if a ball has gone beyond the screens left boundary
            params: None
            returns: boolean; if player2 has scored
        """
        return self.player_has_scored(self.player1)
    
    def player2_has_scored(self):
        """ summary: finds out if a ball has gone beyond the screens right boundary
            params: None
            returns: boolean; if player2 has scored
        """

        return self.player_has_scored(self.player2)
    
    def player_has_scored(self, player_is_leftside):
        """ summary: iterates over every ball in balls and calls ScoreKeeper.player_has_scored()

            params:
                player_is_leftside: boolean; the player is on the left side of the screen

            returns: None
        """

        has_scored = False
        for ball in self.balls:
            if ScoreKeeper.player_has_scored(ball, player_is_leftside):
                has_scored = True
        return has_scored
    
    def add_needed_objects(self):
        """ summary: adds all the games objects (paddle and ball) onto the screen
            params: None
            returns: None
        """

        super().add_needed_objects()
        for ball in self.balls:
            HistoryKeeper.add(self.ball_has_collided(ball),f"ball_has_collided{id(ball)}", False)
