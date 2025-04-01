from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.label import Label
import random

# Constants
WIDTH, HEIGHT = 600, 480
CELL_SIZE = 20
SNAKE_COLOR = (0, 1, 0, 1)  # RGBA (green)
FOOD_COLOR = (1, 0, 0, 1)  # RGBA (red)
BACKGROUND_COLOR = (0, 0, 0, 1)  # RGBA (black)
TEXT_COLOR = (1, 1, 1, 1)  # RGBA (white)
SNAKE_SPEED = 1 / 5  # Seconds per frame (5 FPS)
BUTTON_WIDTH = 120
BUTTON_HEIGHT = 50
BUTTON_COLOR = (0.2, 0.2, 0.2, 1)
BUTTON_TEXT_COLOR = (1, 1, 1, 1)

class SnakeGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.snake = [(WIDTH // 2, HEIGHT // 2)]
        self.snake_direction = (1, 0)
        self.food = self.generate_food()
        self.game_over = False

        # Create control buttons
        self.create_control_buttons()

        # Game over message
        self.game_over_label = Label(
            text="Вы проиграли! Нажмите на экран для рестарта",
            font_size=30, color=TEXT_COLOR,
            pos=(WIDTH // 2, HEIGHT // 2), opacity=0
        )
        self.add_widget(self.game_over_label)

        # Bind keyboard
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        # Start game loop
        Clock.schedule_interval(self.update, SNAKE_SPEED)

    def create_control_buttons(self):
        # Create buttons for touch control
        self.up_button = Button(
            text="Вверх", size=(BUTTON_WIDTH, BUTTON_HEIGHT),
            pos=(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT - BUTTON_HEIGHT * 2 - 10),
            background_color=BUTTON_COLOR, color=BUTTON_TEXT_COLOR
        )
        self.down_button = Button(
            text="Вниз", size=(BUTTON_WIDTH, BUTTON_HEIGHT),
            pos=(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT - BUTTON_HEIGHT - 5),
            background_color=BUTTON_COLOR, color=BUTTON_TEXT_COLOR
        )
        self.left_button = Button(
            text="Влево", size=(BUTTON_WIDTH, BUTTON_HEIGHT),
            pos=(50, HEIGHT - BUTTON_HEIGHT - 5),
            background_color=BUTTON_COLOR, color=BUTTON_TEXT_COLOR
        )
        self.right_button = Button(
            text="Вправо", size=(BUTTON_WIDTH, BUTTON_HEIGHT),
            pos=(WIDTH - BUTTON_WIDTH - 50, HEIGHT - BUTTON_HEIGHT - 5),
            background_color=BUTTON_COLOR, color=BUTTON_TEXT_COLOR
        )

        # Bind button events
        self.up_button.bind(on_press=lambda x: self.change_direction(0, 1))  # Up
        self.down_button.bind(on_press=lambda x: self.change_direction(0, -1))  # Down
        self.left_button.bind(on_press=lambda x: self.change_direction(-1, 0))
        self.right_button.bind(on_press=lambda x: self.change_direction(1, 0))

        # Add buttons to widget
        self.add_widget(self.up_button)
        self.add_widget(self.down_button)
        self.add_widget(self.left_button)
        self.add_widget(self.right_button)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if self.game_over:
            if keycode[1] == 'spacebar':
                self.restart_game()
            return True
        key = keycode[1]
        # Arrow key controls
        if key == 'up' and self.snake_direction != (0, -1):
            self.change_direction(0, 1)  # Move up
        elif key == 'down' and self.snake_direction != (0, 1):
            self.change_direction(0, -1)  # Move down
        elif key == 'left' and self.snake_direction != (1, 0):
            self.change_direction(-1, 0)
        elif key == 'right' and self.snake_direction != (-1, 0):
            self.change_direction(1, 0)
        return True

    def generate_food(self):
        while True:
            food = (
                random.randrange(0, WIDTH // CELL_SIZE) * CELL_SIZE,
                random.randrange(0, HEIGHT // CELL_SIZE) * CELL_SIZE
            )
            if food not in self.snake:
                return food

    def change_direction(self, dx, dy):
        # Only change direction if not reversing
        if (dx, dy) != (-self.snake_direction[0], -self.snake_direction[1]):
            self.snake_direction = (dx, dy)

    def update(self, dt):
        if self.game_over:
            return

        # Move snake
        new_head = (
            self.snake[0][0] + self.snake_direction[0] * CELL_SIZE,
            self.snake[0][1] + self.snake_direction[1] * CELL_SIZE
        )

        # Check for collisions with walls
        if (
            new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT
        ):
            self.game_over = True
            self.show_game_over()
            return

        # Check for self-collision
        if new_head in self.snake:
            self.game_over = True
            self.show_game_over()
            return

        self.snake.insert(0, new_head)

        # Check for food collision
        if new_head == self.food:
            self.food = self.generate_food()
        else:
            self.snake.pop()

        self.draw()

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            # Draw background
            Color(*BACKGROUND_COLOR)
            Rectangle(pos=(0, 0), size=(WIDTH, HEIGHT))
            # Draw snake
            Color(*SNAKE_COLOR)
            for segment in self.snake:
                Rectangle(pos=segment, size=(CELL_SIZE, CELL_SIZE))
            # Draw food
            Color(*FOOD_COLOR)
            Rectangle(pos=self.food, size=(CELL_SIZE, CELL_SIZE))

    def show_game_over(self):
        self.game_over_label.opacity = 1

    def restart_game(self):
        self.snake = [(WIDTH // 2, HEIGHT // 2)]
        self.snake_direction = (1, 0)
        self.food = self.generate_food()
        self.game_over = False
        self.game_over_label.opacity = 0
        self.draw()

    def on_touch_down(self, touch):
        if self.game_over:
            self.restart_game()
        return super().on_touch_down(touch)

class SnakeApp(App):
    def build(self):
        game = SnakeGame()
        Window.size = (WIDTH, HEIGHT)
        return game

if __name__ == "__main__":
    SnakeApp().run()