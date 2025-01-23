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


class FallingBonus(Image):
    points = NumericProperty(10)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (50, 50)

        bonus_types = ["normal", "special", "rare"]
        self.bonus_type = random.choice(bonus_types)
        if self.bonus_type == "normal":
            self.points = 10
        elif self.bonus_type == "special":
            self.points = 20
        else:
            self.points = 50

    def reset_position(self, screen_width):
        self.x = random.randint(0, screen_width - self.width)
        self.y = screen_width


class FallingObstacle(Image):
    points = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (50, 50)

        obstacle_types = [
            {"type": "rock", "points": -15},
            {"type": "cloud", "points": -10},
            {"type": "trap", "points": -20},
        ]

        obstacle = random.choice(obstacle_types)
        self.points = obstacle["points"]
        self.obstacle_type = obstacle["type"]

    def reset_position(self, screen_width):
        self.x = random.randint(0, screen_width - self.width)
        self.y = screen_width


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Layout หลัก
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=20)

        # Timer and score layout
        self.info_bar = BoxLayout(orientation="horizontal", size_hint=(1, 0.1))

        # Timer label
        self.time_left = 30  # 30 seconds
        self.timer_label = Label(
            text=f"Time: {self.time_left}", size_hint=(0.5, 1), font_size=24
        )

        # Score label
        self.score = 0
        self.score_label = Label(
            text=f"Score: {self.score}", size_hint=(0.5, 1), font_size=24
        )

        self.info_bar.add_widget(self.timer_label)
        self.info_bar.add_widget(self.score_label)

        self.layout.add_widget(self.info_bar)

        # พื้นที่เกมหลัก
        self.game_area = Widget(size_hint=(1, 0.8))
        self.layout.add_widget(self.game_area)

        # ตัวละครผู้เล่น
        self.player = None  # จะถูกสร้างใน on_enter

        # แถบข้อมูลตัวละคร
        self.character_bar = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.2), spacing=10, padding=10
        )
        self.character_image = Image(size_hint=(0.3, 1))
        self.character_info = Label(
            size_hint=(0.7, 1), text="", font_size=18, halign="left", valign="middle"
        )
        self.character_info.bind(size=self.character_info.setter("text_size"))

        self.character_bar.add_widget(self.character_image)
        self.character_bar.add_widget(self.character_info)
        self.layout.add_widget(self.character_bar)

        # โบนัสและอุปสรรค
        self.bonus_objects = []
        self.obstacle_objects = []
        self.game_active = False  # Flag to track if game is active

        self.add_widget(self.layout)

        # การรับค่าคีย์บอร์ด
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)

        self.movement = 0  # -1: ซ้าย, 0: หยุด, 1: ขวา

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

    def start_game(self):
        """เริ่มเกมและตั้งค่าต่างๆ"""
        self.game_active = True
        self.time_left = 30
        self.score = 0
        self.score_label.text = f"Score: {self.score}"

        # เริ่ม schedulers
        Clock.schedule_interval(self.update_timer, 1)  # Timer update every second
        Clock.schedule_interval(
            self.create_falling_objects, 2
        )  # Create objects every 2 seconds
        Clock.schedule_interval(self.update, 1 / 60)  # Game update at 60 FPS

    def create_falling_objects(self, dt):
        """สร้างโบนัสและอุปสรรคที่ตกลงมา"""
        if not self.game_active:
            return False

        # สุ่มว่าจะสร้างอะไร (70% โบนัส, 30% อุปสรรค)
        object_type = random.choices(["bonus", "obstacle"], weights=[0.7, 0.3])[0]

        if object_type == "bonus":
            falling_object = FallingBonus(source="path/to/bonus_image.png")
            falling_object.reset_position(self.game_area.width)
            self.game_area.add_widget(falling_object)
            self.bonus_objects.append(falling_object)
        else:
            falling_object = FallingObstacle(source="path/to/obstacle_image.png")
            falling_object.reset_position(self.game_area.width)
            self.game_area.add_widget(falling_object)
            self.obstacle_objects.append(falling_object)

        # อนิเมชั่นตกลง
        anim = Animation(y=0, duration=4)
        anim.bind(on_complete=self.remove_falling_object)
        anim.start(falling_object)

    def remove_falling_object(self, animation, falling_object):
        """ลบโบนัสหรืออุปสรรคที่ตกถึงพื้น"""
        if falling_object in self.bonus_objects:
            self.bonus_objects.remove(falling_object)
        if falling_object in self.obstacle_objects:
            self.obstacle_objects.remove(falling_object)
        self.game_area.remove_widget(falling_object)

    def update_timer(self, dt):
        """อัพเดทเวลา"""
        if not self.game_active:
            return False

        self.time_left -= 1
        self.timer_label.text = f"Time: {self.time_left}"

        if self.time_left <= 0:
            self.end_game()
            return False
        return True

    def end_game(self):
        """จบเกม"""
        self.game_active = False

        # ยกเลิก schedulers ทั้งหมด
        Clock.unschedule(self.update_timer)
        Clock.unschedule(self.create_falling_objects)
        Clock.unschedule(self.update)

        # ลบโบนัสและอุปสรรคทั้งหมด
        for bonus in self.bonus_objects[:]:
            self.game_area.remove_widget(bonus)
        self.bonus_objects.clear()

        for obstacle in self.obstacle_objects[:]:
            self.game_area.remove_widget(obstacle)
        self.obstacle_objects.clear()

        # แสดงคะแนนสุดท้าย
        self.show_game_over()

    def show_game_over(self):
        """แสดงหน้าจอจบเกม"""
        game_over_layout = BoxLayout(orientation="vertical", padding=20)
        game_over_label = Label(
            text=f"Game Over!\nFinal Score: {self.score}", font_size=36, halign="center"
        )
        game_over_layout.add_widget(game_over_label)

        # ปุ่มเล่นใหม่
        restart_button = Button(
            text="Play Again",
            size_hint=(None, None),
            size=(200, 80),
            pos_hint={"center_x": 0.5},
            on_press=self.restart_game,
        )
        game_over_layout.add_widget(restart_button)

        # ปุ่มกลับเมนูหลัก
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
        """เริ่มเกมใหม่"""
        self.manager.current = "countdown"

    def go_to_menu(self, instance):
        """กลับไปยังเมนูหลัก"""
        self.manager.current = "menu"

    def on_enter(self):
        """เมื่อเข้าสู่หน้าจอเกม"""
        if (
            hasattr(self.manager, "selected_character")
            and self.manager.selected_character
        ):
            selected_character = self.manager.selected_character
            self.character_image.source = selected_character["image"]
            self.character_info.text = (
                f"Name: {selected_character['name']}\n"
                f"Score: {self.score}\n"
                f"Bonus: {selected_character['bonus']}"
            )

            # สร้างตัวละครผู้เล่น
            if not self.player:
                self.player = Player(source=selected_character["image"])
                self.game_area.add_widget(self.player)

            # เริ่มเกมใหม่
            self.start_game()

    def update(self, dt):
        """อัพเดทเกม"""
        if not self.game_active:
            return False

        # เคลื่อนที่ตัวละคร
        if self.player:
            self.player.move(self.movement, dt)

            # ตรวจสอบการชนกับโบนัส
            for bonus in self.bonus_objects[:]:
                if self.check_collision(self.player, bonus):
                    self.collect_bonus(bonus)

            # ตรวจสอบการชนกับอุปสรรค
            for obstacle in self.obstacle_objects[:]:
                if self.check_collision(self.player, obstacle):
                    self.collect_obstacle(obstacle)

    def check_collision(self, player, obj):
        """ตรวจสอบการชนกันระหว่างตัวละครและวัตถุ"""
        return (
            player.x < obj.x + obj.width
            and player.x + player.width > obj.x
            and player.y < obj.y + obj.height
            and player.y + player.height > obj.y
        )

    def collect_bonus(self, bonus):
        """เก็บโบนัสและเพิ่มคะแนน"""
        self.score += bonus.points
        self.score_label.text = f"Score: {self.score}"
        self.character_info.text = (
            f"Name: {self.manager.selected_character['name']}\n"
            f"Score: {self.score}\n"
            f"Bonus: {self.manager.selected_character['bonus']}"
        )
        # ลบโบนัส
        if bonus in self.bonus_objects:
            self.bonus_objects.remove(bonus)
            self.game_area.remove_widget(bonus)

    def collect_obstacle(self, obstacle):
        """เก็บอุปสรรคและลดคะแนน"""
        self.score += obstacle.points  # จะเป็นค่าติดลบ
        self.score_label.text = f"Score: {self.score}"
        self.character_info.text = (
            f"Name: {self.manager.selected_character['name']}\n"
            f"Score: {self.score}\n"
            f"Bonus: {self.manager.selected_character['bonus']}"
        )
        # ลบอุปสรรค
        if obstacle in self.obstacle_objects:
            self.obstacle_objects.remove(obstacle)
            self.game_area.remove_widget(obstacle)


# [ส่วนที่เหลือของโค้ดคงเดิม - MainMenuScreen, CharacterSelectionScreen, CountdownScreen, MyGameApp]
# (ให้เพ
