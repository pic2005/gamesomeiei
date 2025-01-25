from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.animation import Animation
import random


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # Background image with stretching and keeping ratio
        background = Image(
            source=r"C:\Users\Acer\Downloads\พล.jpg",
            size_hint=(1, 1),  # ขยายให้เต็มหน้าจอ
            allow_stretch=True,  # อนุญาตให้ขยายภาพ
            keep_ratio=True,  # รักษาสัดส่วนภาพ
        )
        layout.add_widget(background)

        # Start button
        start_button = Button(
            text="START",
            font_size=24,
            size_hint=(None, None),
            size=(200, 100),
            pos_hint={"center_x": 0.5, "center_y": 0.2},
            background_normal="",
            background_color=(1, 0.84, 0, 1),
            border=(20, 20, 20, 20),
            color=(0, 0, 0, 1),
        )
        start_button.bind(on_press=self.start_game)
        layout.add_widget(start_button)

        self.add_widget(layout)

    def start_game(self, instance):
        # ไปที่หน้าแนะนำตัวละคร
        self.manager.current = "character_screen"


class CharacterSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # Background image with stretching and keeping ratio
        background = Image(
            source=r"C:\Users\Acer\Downloads\พื้นหลัง23.jpg",
            size_hint=(1, 1),  # ขยายให้เต็มหน้าจอ
            allow_stretch=True,  # อนุญาตให้ขยายภาพ
            keep_ratio=True,  # รักษาสัดส่วนภาพ
        )
        layout.add_widget(background)

        # Character image
        self.character = Image(
            source=r"C:\Users\Acer\Downloads\ช้าง.png",
            size_hint=(None, None),
            size=(1000, 1000),
            pos_hint={"center_x": 0.5, "center_y": 0.6},
        )
        layout.add_widget(self.character)

        # Game description label
        game_description = Label(
            text="Hello, my name is Khud Kat.\nMy name comes from mangosteen.\nPlease help me collect a lot of fallen mangosteen,\nand I will be able to go home.",
            font_size=20,
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            size=(600, 200),
            pos_hint={"center_x": 0.5, "center_y": 0.3},
            halign="center",
            valign="middle",
        )
        layout.add_widget(game_description)

        # Start game button
        start_game_button = Button(
            text="PLAY",
            font_size=24,
            size_hint=(None, None),
            size=(200, 100),
            pos_hint={"center_x": 0.5, "center_y": 0.1},
            background_color=(0.4, 0.8, 0.4, 1),
        )
        start_game_button.bind(on_press=self.start_game)
        layout.add_widget(start_game_button)

        self.add_widget(layout)

    def start_game(self, instance):
        # ไปที่หน้าเกม
        self.manager.current = "game_screen"


class FallingObject(Image):
    def __init__(self, is_bonus=True, **kwargs):
        image_choices_bonus = [
            r"C:\Users\Acer\Downloads\มังคุด1.jpg",
            r"C:\Users\Acer\Downloads\มังคุด2.jpg",
        ]
        image_choices_obstacle = [
            r"C:\Users\Acer\Downloads\ลำไย.jpg",
            r"C:\Users\Acer\Downloads\เงาะ.jpg",
        ]

        if is_bonus:
            chosen_image = random.choice(image_choices_bonus)
            self.points = random.randint(1, 5)
        else:
            chosen_image = random.choice(image_choices_obstacle)
            self.points = -random.randint(1, 5)

        super().__init__(
            source=chosen_image,
            size_hint=(None, None),
            size=(50, 50),  # ขนาดของวัตถุที่ตก
        )

    def reset_position(self, screen_width):
        self.x = random.randint(0, screen_width - self.width)
        self.y = Window.height  # เริ่มตกจากด้านบน


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()

        # Background image with stretching and keeping ratio
        background = Image(
            source=r"C:\Users\Acer\Downloads\พื้นหลัง2.jpg",
            size_hint=(1, 1),  # ขยายให้เต็มหน้าจอ
            allow_stretch=True,  # อนุญาตให้ขยายภาพ
            keep_ratio=True,  # รักษาสัดส่วนภาพ
        )
        self.layout.add_widget(background)

        # Player character (แทบด้านล่าง)
        self.player = Image(
            source=r"C:\Users\Acer\Downloads\ช้าง.png",
            size_hint=(None, None),
            size=(150, 50),  # ขนาดของแทบตัวละคร
            pos_hint={"center_x": 0.5, "y": 0.05},
        )
        self.layout.add_widget(self.player)

        # Score label
        self.score_label = Label(
            text="Score: 0",
            font_size=24,
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={"x": 0.1, "top": 0.95},
        )
        self.layout.add_widget(self.score_label)

        # Time label
        self.time_label = Label(
            text="Time: 30",
            font_size=24,
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={"right": 0.9, "top": 0.95},
        )
        self.layout.add_widget(self.time_label)

        self.add_widget(self.layout)

        # Game variables
        self.score = 0
        self.time_left = 30
        self.falling_objects = []
        self.move_speed = 10  # ความเร็วการเคลื่อนที่ของแทบตัวละคร
        self.is_paused = False

        # Keyboard handling
        Window.bind(on_key_down=self._on_keyboard_down)
        Window.bind(on_key_up=self._on_keyboard_up)

        # Movement variables
        self.movement_x = 0

        # Start game timers
        Clock.schedule_interval(self.update_timer, 1)
        Clock.schedule_interval(self.create_falling_objects, 1)  # สร้างวัตถุทุก 1 วินาที
        Clock.schedule_interval(self.update, 1 / 60)  # อัพเดทเกมทุกเฟรม

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if self.is_paused:
            return False

        if keycode == 37:  # Left arrow
            self.movement_x = -self.move_speed
        elif keycode == 39:  # Right arrow
            self.movement_x = self.move_speed
        return True

    def _on_keyboard_up(self, instance, keyboard, keycode, text, modifiers):
        if keycode in [37, 39]:  # Left or Right arrow
            self.movement_x = 0
        return True

    def update(self, dt):
        if self.is_paused:
            return

        # Move player
        x, y = self.player.pos
        new_x = x + self.movement_x
        new_x = max(0, min(new_x, Window.width - self.player.width))  # จำกัดขอบเขต
        self.player.pos = (new_x, y)

        # Check collisions
        for obj in self.falling_objects[:]:
            if self.check_collision(self.player, obj):
                self.score += obj.points
                self.score_label.text = f"Score: {self.score}"
                self.layout.remove_widget(obj)
                self.falling_objects.remove(obj)

    def check_collision(self, player, obj):
        return (
            player.x < obj.x + obj.width
            and player.x + player.width > obj.x
            and player.y < obj.y + obj.height
            and player.y + player.height > obj.y
        )

    def update_timer(self, dt):
        if self.is_paused:
            return

        self.time_left -= 1
        self.time_label.text = f"Time: {self.time_left}"
        if self.time_left <= 0:
            self.end_game()

    def create_falling_objects(self, dt):
        if self.is_paused:
            return

        is_bonus = random.choice([True, False])
        obj = FallingObject(is_bonus=is_bonus)
        obj.reset_position(Window.width)
        self.layout.add_widget(obj)

        # Animate falling
        anim = Animation(y=0, duration=random.uniform(2, 5))  # ความเร็วการตกสุ่ม
        anim.bind(on_complete=self.remove_fallen_object)
        anim.start(obj)

        self.falling_objects.append(obj)

    def remove_fallen_object(self, animation, obj):
        if obj in self.falling_objects:
            self.layout.remove_widget(obj)
            self.falling_objects.remove(obj)

    def end_game(self):
        Clock.unschedule(self.update_timer)
        Clock.unschedule(self.create_falling_objects)
        Clock.unschedule(self.update)

        # Game over layout
        game_over_layout = FloatLayout()

        game_over_label = Label(
            text=f"Game Over!\nScore: {self.score}",
            font_size=36,
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            size=(500, 200),
            pos_hint={"center_x": 0.5, "center_y": 0.6},
        )

        restart_button = Button(
            text="Restart",
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={"center_x": 0.5, "center_y": 0.4},
        )
        restart_button.bind(on_press=self.restart_game)

        game_over_layout.add_widget(game_over_label)
        game_over_layout.add_widget(restart_button)

        self.add_widget(game_over_layout)

    def restart_game(self, instance):
        self.score = 0
        self.time_left = 30
        self.falling_objects.clear()
        self.layout.clear_widgets()

        # Re-add all initial widgets
        background = Image(
            source=r"C:\Users\Acer\Downloads\พื้นหลัง2.jpg",
            size_hint=(1, 1),
            allow_stretch=True,
            keep_ratio=True,
        )
        self.layout.add_widget(background)

        self.player = Image(
            source=r"C:\Users\Acer\Downloads\ช้าง.png",
            size_hint=(None, None),
            size=(150, 50),
            pos_hint={"center_x": 0.5, "y": 0.05},
        )
        self.layout.add_widget(self.player)

        self.score_label = Label(
            text="Score: 0",
            font_size=24,
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={"x": 0.1, "top": 0.95},
        )
        self.layout.add_widget(self.score_label)

        self.time_label = Label(
            text="Time: 30",
            font_size=24,
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={"right": 0.9, "top": 0.95},
        )
        self.layout.add_widget(self.time_label)

        # Restart game timers
        Clock.schedule_interval(self.update_timer, 1)
        Clock.schedule_interval(self.create_falling_objects, 1)
        Clock.schedule_interval(self.update, 1 / 60)

        self.manager.current = "game_screen"


class GameApp(App):
    def build(self):
        # ตั้งค่าขนาดหน้าจอเริ่มต้น
        Window.size = (800, 600)  # ตัวอย่างขนาด 800x600 พิกเซล

        sm = ScreenManager()

        # เพิ่มหน้าแรก, หน้าแนะนำตัวละคร, และหน้าเกม
        main_screen = MainScreen(name="main_screen")
        sm.add_widget(main_screen)

        character_screen = CharacterSelectionScreen(name="character_screen")
        sm.add_widget(character_screen)

        game_screen = GameScreen(name="game_screen")
        sm.add_widget(game_screen)

        # เริ่มต้นที่หน้าแรก
        sm.current = "main_screen"

        return sm


if __name__ == "__main__":
    GameApp().run()
