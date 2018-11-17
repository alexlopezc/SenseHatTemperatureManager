from sense_hat import SenseHat, ACTION_RELEASED
import time
from Ball import Ball
from random import getrandbits
import sys

ORIENTATION_REFRESH = 0.05
class Game():

    def __init__(self):
        self.sense = SenseHat()
        self.configure_stick()
        self.last_orientation = self.sense.get_orientation_degrees()
        while True:
            for i in range(5):
                self.sense.load_image("img/heart8.png")
                time.sleep(0.5)
                self.sense.clear()
                time.sleep(0.5)
            self.sense.show_message("TE QUIERO")
            time.sleep(1)
        self.running = False
        # event = self.sense.stick.wait_for_event()
    
    def run(self):
        #self.init_message()
        self.start_game()

    def configure_stick(self,):
        self.sense.stick.direction_any = self.launch_game

    def init_message(self):
        self.sense.show_message("Ready", scroll_speed = 0.05)
        self.sense.show_message("Set", scroll_speed = 0.05)
        self.sense.show_message("Go!!", scroll_speed = 0.05)

    def start_game(self):
        ball = Ball(x=4, y=4, sense=self.sense)
        self.running = True
        
        while self.running:
            dx, dy = self.next_move()
            game_over = self.is_game_over(ball, dx, dy)
            print("Game over = {}".format(game_over))
            if game_over:
                self.running = False
                print("Game over")
                self.sense.show_letter("X", text_colour=[255,255,0])
                time.sleep(3)
                self.show_message("Game over")
            else:
                ball.move(dx, dy)
                time.sleep(ORIENTATION_REFRESH)

    def launch_game(self, event):
        if event.action != ACTION_RELEASED:
            self.run()



    def is_game_over(self, ball, dx, dy):
        died = False
        new_x = ball.x + dx
        new_y = ball.y + dy
        if new_x <= 7 and new_x >= 0 and new_y <= 7 and new_y >= 0:
            died =  False
        else: 
            died = True
        print("Died = {}".format(died))
        return died

    def next_move(self, min_value=0, max_value=7):
        # x = getrandbits(1) * 2 - 1 
        # y = getrandbits(1) * 2 - 1
        
        orientation = self.sense.get_orientation_degrees()
        difference= {
            'd_pitch': orientation['pitch'] - self.last_orientation['pitch'],
            'd_roll': orientation['roll'] - self.last_orientation['roll'], 
            'd_yaw': orientation['yaw'] - self.last_orientation['yaw']
        }
        # sys.stdout.write("p: {pitch:.2f}, r: {roll:.2f}, y: {yaw:.2f}".format(**orientation))
        if difference['d_pitch'] / 0.5 > 1:
            x = -1
        elif difference['d_pitch'] / 0.5 < -1:
            x = 1
        else:
            x = 0

        if difference['d_roll'] / 0.5 > 1:
            y = 1
        elif difference['d_roll'] / 0.5 < -1:
            y = -1
        else:
            y = 0


        sys.stdout.write("droll: {:.2f}, dpitch: {:.2f} - X: {:.2f},Y: {:.2f}\n".format(difference['d_roll'], difference['d_pitch'], x, y))
        self.last_orientation = orientation
        return x, y
    

game = Game()
