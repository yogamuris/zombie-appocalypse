class Settings():
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (240, 240, 240)

        self.fighter_limit = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 0, 0)
        self.bullets_allowed = 10

        self.fighter_drop_speed = 10
        self.speedup_scale = 1.1
        self.fighter_direction = 1

        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.fighter_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.zombie_speed_factor = 1

        self.fighter_direction = 1
        self.zombie_points = 50

    def increase_speed(self):
        self.fighter_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.zombie_speed_factor *= self.speedup_scale

        self.zombie_points = int(self.zombie_points * self.score_scale)
        print(self.zombie_points)