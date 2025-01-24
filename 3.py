from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.uix.popup import Popup
import random


class Player(Image):
    speed = NumericProperty(300)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (80, 80)
        self.pos_hint = {"x": 0.5, "bottom": 0.1}
        self.source = kwargs.get("source", "default.png")

    def move(self, direction, dt):
        new_x = self.x + (direction * self.speed * dt)
        if 0 <= new_x <= Window.width - self.width:
            self.x = new_x


class FallingObject(Image):
    points = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (50, 50)
        self.source = kwargs.get("source", "object.png")

    def reset_position(self, screen_width):
        self.x = random.randint(0, screen_width - self.width)
        self.y = screen_width


class FallingBonus(FallingObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = kwargs.get("source", "bonus.png")
        bonus_types = ["normal", "special", "rare"]
        self.bonus_type = random.choice(bonus_types)
        self.points = {"normal": 10, "special": 20, "rare": 50}[self.bonus_type]


class FallingObstacle(FallingObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = kwargs.get("source", "obstacle.png")
        self.points = -15


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=20)

        self.info_bar = BoxLayout(orientation="horizontal", size_hint=(1, 0.1))
        self.time_left = 30
        self.timer_label = Label(
            text=f"Time: {self.time_left}", size_hint=(0.5, 1), font_size=24
        )
        self.score = 0
        self.score_label = Label(
            text=f"Score: {self.score}", size_hint=(0.5, 1), font_size=24
        )

        self.info_bar.add_widget(self.timer_label)
        self.info_bar.add_widget(self.score_label)
        self.layout.add_widget(self.info_bar)

        self.game_area = Widget(size_hint=(1, 0.8))
        self.layout.add_widget(self.game_area)

        self.player = None
        self.objects = []
        self.game_active = False

        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)

        self.movement = 0
        self.add_widget(self.layout)

    def start_game(self):
        self.game_active = True
        self.time_left = 30
        self.score = 0
        self.score_label.text = f"Score: {self.score}"
        Clock.schedule_interval(self.update_timer, 1)
        Clock.schedule_interval(self.create_falling_objects, 2)
        Clock.schedule_interval(self.update, 1 / 60)

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard.unbind(on_key_up=self._on_key_up)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == "left":
            self.movement = -1
        elif keycode[1] == "right":
            self.movement = 1
        return True

    def _on_key_up(self, keyboard, keycode):
        if keycode[1] in ("left", "right"):
            self.movement = 0
        return True

    def update_timer(self, dt):
        if not self.game_active:
            return False
        self.time_left -= 1
        self.timer_label.text = f"Time: {self.time_left}"
        if self.time_left <= 0:
            self.end_game()
            return False
        return True

    def create_falling_objects(self, dt):
        if not self.game_active:
            return False

        if random.random() < 0.7:
            obj = FallingBonus()
        else:
            obj = FallingObstacle()

        obj.reset_position(self.game_area.width)
        self.game_area.add_widget(obj)
        anim = Animation(y=0, duration=4)
        anim.bind(on_complete=self.remove_object)
        anim.start(obj)
        self.objects.append(obj)

    def remove_object(self, animation, obj):
        if obj in self.objects:
            self.objects.remove(obj)
            self.game_area.remove_widget(obj)

    def update(self, dt):
        if not self.game_active:
            return False
        if self.player:
            self.player.move(self.movement, dt)
            for obj in self.objects[:]:
                if self.check_collision(self.player, obj):
                    self.handle_collision(obj)

    def check_collision(self, player, obj):
        return (
            player.x < obj.x + obj.width
            and player.x + player.width > obj.x
            and player.y < obj.y + obj.height
            and player.y + player.height > obj.y
        )

    def handle_collision(self, obj):
        self.score += obj.points
        self.score_label.text = f"Score: {self.score}"
        if obj in self.objects:
            self.objects.remove(obj)
            self.game_area.remove_widget(obj)

    def end_game(self):
        self.game_active = False
        Clock.unschedule(self.update_timer)
        Clock.unschedule(self.create_falling_objects)
        Clock.unschedule(self.update)
        for obj in self.objects[:]:
            self.game_area.remove_widget(obj)
        self.objects.clear()
        self.show_game_over()

    def show_game_over(self):
        game_over_layout = BoxLayout(orientation="vertical", padding=20)
        game_over_label = Label(
            text=f"Game Over!\nFinal Score: {self.score}", font_size=36
        )
        game_over_layout.add_widget(game_over_label)

        restart_button = Button(
            text="Play Again",
            size_hint=(None, None),
            size=(200, 80),
            pos_hint={"center_x": 0.5},
            on_press=self.restart_game,
        )
        game_over_layout.add_widget(restart_button)

        menu_button = Button(
            text="Main Menu",
            size_hint=(None, None),
            size=(200, 80),
            pos_hint={"center_x": 0.5},
            on_press=self.go_to_menu,
        )
        game_over_layout.add_widget(menu_button)

        popup = Popup(
            title="Game Over",
            content=game_over_layout,
            size_hint=(0.8, 0.8),
            auto_dismiss=False,
        )
        popup.open()

    def restart_game(self, instance):
        self.manager.current = "countdown"

    def go_to_menu(self, instance):
        self.manager.current = "menu"

    def on_enter(self):
        if (
            hasattr(self.manager, "selected_character")
            and self.manager.selected_character
        ):
            if not self.player:
                self.player = Player(source=self.manager.selected_character["image"])
                self.game_area.add_widget(self.player)
            self.start_game()


class MyGameApp(App):
    def build(self):
        Window.size = (800, 600)
        sm = ScreenManager()
        sm.selected_character = None
        sm.add_widget(GameScreen(name="game_screen"))
        return sm


if __name__ == "__main__":
    MyGameApp().run()
