import math
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse, Line, Rectangle

class HillClimbGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Car Physics Variables
        self.car_x = 100
        self.car_y = 200
        self.velocity_x = 0
        self.velocity_y = 0
        self.angle = 0
        self.angular_velocity = 0
        
        # Controls
        self.gas_pressed = False
        self.brake_pressed = False
        
        # UI Buttons Setup
        Clock.schedule_once(self.setup_ui, 0)
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def setup_ui(self, dt):
        # Gas Button
        gas_btn = Button(text="GAS", size=(120, 80), pos=(self.width - 140, 20))
        gas_btn.bind(on_press=self.on_gas_down, on_release=self.on_gas_up)
        self.add_widget(gas_btn)

        # Brake Button
        brake_btn = Button(text="BRAKE", size=(120, 80), pos=(20, 20))
        brake_btn.bind(on_press=self.on_brake_down, on_release=self.on_brake_up)
        self.add_widget(brake_btn)

    def get_ground_y(self, x):
        # Pahad ki uunchai (Hills topography calculation)
        return 150 + math.sin(x * 0.008) * 80 + math.cos(x * 0.003) * 40

    def on_gas_down(self, instance): self.gas_pressed = True
    def on_gas_up(self, instance): self.gas_pressed = False
    def on_brake_down(self, instance): self.brake_pressed = True
    def on_brake_up(self, instance): self.brake_pressed = False

    def update(self, dt):
        # Ground height at current position
        ground_y = self.get_ground_y(self.car_x)
        ground_slope = (self.get_ground_y(self.car_x + 5) - self.get_ground_y(self.car_x - 5)) / 10.0

        # Acceleration & Friction logic
        if self.gas_pressed:
            self.velocity_x += 0.15
        elif self.brake_pressed:
            self.velocity_x -= 0.15
        else:
            self.velocity_x *= 0.98  # Friction

        # Apply Gravity
        self.velocity_y -= 0.25

        # Move Car
        self.car_x += self.velocity_x
        self.car_y += self.velocity_y

        # Collision with Ground
        target_angle = math.degrees(math.atan(ground_slope))
        if self.car_y <= ground_y + 25:
            self.car_y = ground_y + 25
            self.velocity_y = 0
            # Snap angle to ground slope
            self.angle = target_angle
        else:
            # Air rotation physics
            if self.gas_pressed: self.angle -= 1.5
            if self.brake_pressed: self.angle += 1.5

        # Draw Graphics Frame
        self.canvas.clear()
        with self.canvas:
            # Draw Sky
            Color(0.5, 0.8, 1, 1)
            Rectangle(pos=(0, 0), size=self.size)

            # Draw Hills Ground
            Color(0.2, 0.7, 0.2, 1)
            points = []
            start_x = int(self.car_x - self.width / 2)
            for screen_x in range(0, int(self.width) + 20, 20):
                world_x = start_x + screen_x
                world_y = self.get_ground_y(world_x)
                points.extend([screen_x, world_y])
            
            if len(points) >= 4:
                Line(points=points, width=4)

            # Draw Car Body & Wheels
            screen_car_x = self.width / 2
            screen_car_y = self.car_y

            # Car Body
            Color(0.9, 0.1, 0.1, 1)
            Rectangle(pos=(screen_car_x - 30, screen_car_y), size=(60, 25))

            # Wheels
            Color(0.1, 0.1, 0.1, 1)
            Ellipse(pos=(screen_car_x - 25, screen_car_y - 12), size=(20, 20))
            Ellipse(pos=(screen_car_x + 5, screen_car_y - 12), size=(20, 20))

class HillClimbApp(App):
    def build(self):
        return HillClimbGame()

if __name__ == '__main__':
    HillClimbApp().run()
      
