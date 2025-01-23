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

    def move(self, direction, dt):
        new_x = self.x + (direction * self.speed * dt)
        if 0 <= new_x <= Window.width - self.width:
            self.x = new_x


class FallingObject(Image):
    """Base class for falling objects (both bonuses and obstacles)"""

    points = NumericProperty(0)
    object_type = "neutral"  # can be "bonus", "obstacle", or "neutral"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (50, 50)

    def reset_position(self, screen_width):
        self.x = random.randint(0, screen_width - self.width)
        self.y = screen_width


class BonusObject(FallingObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object_type = "bonus"

        # สุ่มประเภทโบนัสและคะแนน
        bonus_types = ["normal", "special", "rare"]
        self.bonus_type = random.choice(bonus_types)
        if self.bonus_type == "normal":
            self.points = 10
            self.source = "path/to/normal_bonus.png"
        elif self.bonus_type == "special":
            self.points = 20
            self.source = "path/to/special_bonus.png"
        else:
            self.points = 50
            self.source = "path/to/rare_bonus.png"


class ObstacleObject(FallingObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object_type = "obstacle"

        # สุ่มประเภทอุปสรรค
        obstacle_types = ["rock", "cloud", "trap"]
        self.obstacle_type = random.choice(obstacle_types)
        if self.obstacle_type == "rock":
            self.points = -15
            self.source = "path/to/rock_obstacle.png"
        elif self.obstacle_type == "cloud":
            self.points = -10
            self.source = "path/to/cloud_obstacle.png"
        else:
            self.points = -20
            self.source = "path/to/trap_obstacle.png"


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # [เก็บโค้ดเดิมของ __init__]

        # เพิ่มรายการสำหรับอุปสรรค
        self.obstacle_objects = []

    def create_falling_objects(self, dt):
        """สร้างออบเจ็กต์ที่ตกลงมา (ทั้งโบนัสและอุปสรรค)"""
        if not self.game_active:
            return False

        # สุ่มว่าจะสร้างอะไร
        object_type = random.choices(
            ["bonus", "obstacle"], weights=[0.7, 0.3]  # 70% โบนัส, 30% อุปสรรค
        )[0]

        if object_type == "bonus":
            falling_object = BonusObject()
        else:
            falling_object = ObstacleObject()

        falling_object.reset_position(self.game_area.width)
        self.game_area.add_widget(falling_object)

        # อนิเมชั่นตกลง
        anim = Animation(y=0, duration=4)
        anim.bind(on_complete=self.remove_falling_object)
        anim.start(falling_object)

        # เก็บในรายการที่เหมาะสม
        if object_type == "bonus":
            self.bonus_objects.append(falling_object)
        else:
            self.obstacle_objects.append(falling_object)

    def remove_falling_object(self, animation, falling_object):
        """ลบออบเจ็กต์ที่ตกถึงพื้น"""
        if falling_object in self.bonus_objects:
            self.bonus_objects.remove(falling_object)
        if falling_object in self.obstacle_objects:
            self.obstacle_objects.remove(falling_object)
        self.game_area.remove_widget(falling_object)

    def start_game(self):
        """เริ่มเกมและตั้งค่าต่างๆ"""
        super().start_game()

        # ยกเลิก scheduler เดิม
        Clock.unschedule(self.create_falling_bonus)

        # เพิ่ม scheduler ใหม่สำหรับออบเจ็กต์ทั่วไป
        Clock.schedule_interval(self.create_falling_objects, 2)

    def collect_object(self, falling_object):
        """เก็บออบเจ็กต์และอัพเดทคะแนน"""
        if falling_object.object_type == "bonus":
            self.score += falling_object.points
            # เสียงหรือเอฟเฟกต์เมื่อเก็บโบนัส
        else:
            # หักคะแนนสำหรับอุปสรรค
            self.score += falling_object.points
            # เสียงหรือเอฟเฟกต์เมื่อชนอุปสรรค

        # อัพเดทข้อความคะแนน
        self.score_label.text = f"Score: {self.score}"
        self.character_info.text = (
            f"Name: {self.manager.selected_character['name']}\n"
            f"Score: {self.score}\n"
            f"Bonus: {self.manager.selected_character['bonus']}"
        )

        # ลบออบเจ็กต์
        if falling_object in self.bonus_objects:
            self.bonus_objects.remove(falling_object)
        if falling_object in self.obstacle_objects:
            self.obstacle_objects.remove(falling_object)
        self.game_area.remove_widget(falling_object)

    def update(self, dt):
        """อัพเดทเกม"""
        if not self.game_active:
            return False

        # เคลื่อนที่ตัวละคร
        if self.player:
            self.player.move(self.movement, dt)

            # ตรวจสอบการชนกับโบนัสและอุปสรรค
            for bonus in self.bonus_objects[:]:
                if self.check_collision(self.player, bonus):
                    self.collect_object(bonus)

            for obstacle in self.obstacle_objects[:]:
                if self.check_collision(self.player, obstacle):
                    self.collect_object(obstacle)


# [ส่วนที่เหลือของโค้ดคงเดิม]


class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", spacing=10, padding=20)
        try:
            self.background = Image(
                source=r"C:\Users\Acer\Downloads\Backgeam.jpg", allow_stretch=True
            )
        except:
            self.background = Widget()
        self.add_widget(self.background)

        play_button = Button(
            text="Play",
            size_hint=(None, None),
            size=(200, 80),
            pos_hint={"center_x": 0.5},
            font_size=24,
            background_color=(0.2, 0.6, 1, 1),
        )
        play_button.bind(on_press=self.go_to_character_selection)
        layout.add_widget(play_button)
        self.add_widget(layout)

    def go_to_character_selection(self, instance):
        self.manager.current = "character_selection"


class CharacterSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.characters = [
            {
                "image": "chinj.png",
                "name": "Shinchan",
                "info": "A 5-year-old boy who is naughty",
                "bonus": "Choco Bee",
            },
            {
                "image": "kasaj.png",
                "name": "Kasama",
                "info": "Shin-chan's best friend",
                "bonus": "Books",
            },
            {
                "image": "nenej.png",
                "name": "Nene",
                "info": "A neat girl",
                "bonus": "Tea",
            },
            {
                "image": "bowwj.png",
                "name": "Bow jang",
                "info": "The laconic boy",
                "bonus": "Bread",
            },
            {
                "image": "masaj.png",
                "name": "Masao",
                "info": "A shy boy",
                "bonus": "Drawing",
            },
            {
                "image": "ij.png",
                "name": "I jang",
                "info": "A rich girl",
                "bonus": "Cake",
            },
        ]

        main_layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        grid = GridLayout(cols=3, spacing=10, padding=10, size_hint=(1, 0.8))

        for char in self.characters:
            char_button = Button(size_hint=(1, 1))
            try:
                char_button.background_normal = char["image"]
                char_button.background_down = char["image"]
            except:
                pass
            char_button.bind(
                on_press=lambda instance, c=char: self.show_character_info(c)
            )
            grid.add_widget(char_button)

        self.info_layout = BoxLayout(orientation="vertical", size_hint=(1, 0.2))
        self.name_label = Label(text="", font_size=24, size_hint=(1, None), height=40)
        self.info_label = Label(text="", font_size=18, size_hint=(1, None), height=80)
        self.bonus_label = Label(text="", font_size=18, size_hint=(1, None), height=40)

        self.info_layout.add_widget(self.name_label)
        self.info_layout.add_widget(self.info_label)
        self.info_layout.add_widget(self.bonus_label)

        main_layout.add_widget(grid)
        main_layout.add_widget(self.info_layout)

        start_button = Button(
            text="Start",
            size_hint=(None, None),
            size=(200, 80),
            pos_hint={"center_x": 0.5},
            font_size=24,
            background_color=(0.2, 0.6, 1, 1),
        )
        start_button.bind(on_press=self.start_countdown)
        main_layout.add_widget(start_button)
        self.add_widget(main_layout)

    def show_character_info(self, character):
        self.name_label.text = f"Name: {character['name']}"
        self.info_label.text = f"Info: {character['info']}"
        self.bonus_label.text = f"Bonus: {character['bonus']}"
        self.manager.selected_character = character

    def start_countdown(self, instance):
        if (
            not hasattr(self.manager, "selected_character")
            or not self.manager.selected_character
        ):
            self.name_label.text = "Please select a character!"
        else:
            self.manager.current = "countdown"


class CountdownScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=20, spacing=20)
        self.countdown_label = Label(text="5", font_size=150)
        layout.add_widget(self.countdown_label)
        self.count = 5
        self.add_widget(layout)

    def on_enter(self):
        self.count = 5
        Clock.schedule_interval(self.update_countdown, 1)

    def update_countdown(self, dt):
        self.count -= 1
        self.countdown_label.text = str(self.count)
        if self.count <= 0:
            Clock.unschedule(self.update_countdown)
            self.manager.current = "game_screen"
            return False
        return True


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
        self.bonus_objects = []
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
        Clock.schedule_interval(self.create_falling_bonus, 2)
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

    def create_falling_bonus(self, dt):
        if not self.game_active:
            return False
        bonus = FallingBonus()
        bonus.reset_position(self.game_area.width)
        self.game_area.add_widget(bonus)
        anim = Animation(y=0, duration=4)
        anim.bind(on_complete=self.remove_bonus)
        anim.start(bonus)
        self.bonus_objects.append(bonus)

    def remove_bonus(self, animation, bonus):
        if bonus in self.bonus_objects:
            self.bonus_objects.remove(bonus)
            self.game_area.remove_widget(bonus)

    def update(self, dt):
        if not self.game_active:
            return False
        if self.player:
            self.player.move(self.movement, dt)
            for bonus in self.bonus_objects[:]:
                if self.check_collision(self.player, bonus):
                    self.collect_bonus(bonus)

    def check_collision(self, player, bonus):
        return (
            player.x < bonus.x + bonus.width
            and player.x + player.width > bonus.x
            and player.y < bonus.y + bonus.height
            and player.y + player.height > bonus.y
        )

    def collect_bonus(self, bonus):
        self.score += bonus.points
        self.score_label.text = f"Score: {self.score}"
        if bonus in self.bonus_objects:
            self.bonus_objects.remove(bonus)
            self.game_area.remove_widget(bonus)

    def end_game(self):
        self.game_active = False
        Clock.unschedule(self.update_timer)
        Clock.unschedule(self.create_falling_bonus)
        Clock.unschedule(self.update)
        for bonus in self.bonus_objects[:]:
            self.game_area.remove_widget(bonus)
        self.bonus_objects.clear()
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
        sm.add_widget(MainMenuScreen(name="menu"))
        sm.add_widget(CharacterSelectionScreen(name="character_selection"))
        sm.add_widget(CountdownScreen(name="countdown"))
        sm.add_widget(GameScreen(name="game_screen"))
        return sm


if __name__ == "__main__":
    MyGameApp().run()
