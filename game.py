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
from kivy.uix.popup import Popup  # เพิ่ม import สำหรับ popup
import random


class Player(Image):
    """ตัวละครที่ผู้เล่นควบคุม"""

    speed = NumericProperty(300)  # ความเร็วการเคลื่อนที่ (pixels per second)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (80, 80)  # ขนาดตัวละคร
        self.pos_hint = {"x": 0.5, "bottom": 0.1}  # ตำแหน่งเริ่มต้น

    def move(self, direction, dt):
        """เคลื่อนที่ตัวละครซ้าย-ขวา"""
        new_x = self.x + (direction * self.speed * dt)
        # ตรวจสอบขอบเขตหน้าจอ
        if 0 <= new_x <= Window.width - self.width:
            self.x = new_x


class FallingBonus(Image):
    """วัตถุที่ตกลงมาจากด้านบน"""

    points = NumericProperty(10)  # คะแนนเมื่อรับได้

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (50, 50)
        # สุ่มประเภทโบนัสและคะแนน
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

        # โบนัส
        self.bonus_objects = []
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
            self.create_falling_bonus, 2
        )  # Create bonus every 2 seconds
        Clock.schedule_interval(self.update, 1 / 60)  # Game update at 60 FPS

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
        Clock.unschedule(self.create_falling_bonus)
        Clock.unschedule(self.update)

        # ลบโบนัสทั้งหมด
        for bonus in self.bonus_objects[:]:
            self.game_area.remove_widget(bonus)
        self.bonus_objects.clear()

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

    def create_falling_bonus(self, dt):
        """สร้างโบนัสใหม่"""
        if not self.game_active:
            return False

        bonus = FallingBonus(source="path/to/bonus_image.png")
        bonus.reset_position(self.game_area.width)
        self.game_area.add_widget(bonus)

        # อนิเมชั่นตกลง
        anim = Animation(y=0, duration=4)
        anim.bind(on_complete=self.remove_bonus)
        anim.start(bonus)
        self.bonus_objects.append(bonus)

    def remove_bonus(self, animation, bonus):
        """ลบโบนัสที่ตกถึงพื้น"""
        if bonus in self.bonus_objects:
            self.bonus_objects.remove(bonus)
            self.game_area.remove_widget(bonus)

    def update(self, dt):
        """อัพเดทเกม"""
        if not self.game_active:
            return False

        # เคลื่อนที่ตัวละคร
        if self.player:
            self.player.move(self.movement, dt)

            # ตรวจสอบการชนกับโบนัส
            for bonus in self.bonus_objects[:]:  # ใช้สำเนาเพื่อป้องกันการเปลี่ยนแปลงระหว่างวนลูป
                if self.check_collision(self.player, bonus):
                    self.collect_bonus(bonus)

    def check_collision(self, player, bonus):
        """ตรวจสอบการชนกันระหว่างตัวละครและโบนัส"""
        return (
            player.x < bonus.x + bonus.width
            and player.x + player.width > bonus.x
            and player.y < bonus.y + bonus.height
            and player.y + player.height > bonus.y
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


# [ส่วนของ MainMenuScreen, CharacterSelectionScreen, CountdownScreen คงเดิม]


class MyGameApp(App):
    def build(self):
        # ตั้งค่าขนาดหน้าต่างเกม
        Window.size = (800, 600)

        # สร้าง ScreenManager
        sm = ScreenManager()
        sm.selected_character = None

        # เพิ่มหน้าจอทั้งหมด
        sm.add_widget(MainMenuScreen(name="menu"))
        sm.add_widget(CharacterSelectionScreen(name="character_selection"))
        sm.add_widget(CountdownScreen(name="countdown"))
        sm.add_widget(GameScreen(name="game_screen"))

        return sm


if __name__ == "__main__":
    MyGameApp().run()

# ส่วนที่เหลือของโค้ดยังคงเหมือนเดิม (MainMenuScreen, CharacterSelectionScreen, CountdownScreen, MyGameApp)
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
import random

# [Previous Player and FallingBonus classes remain the same]


class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Layout หลัก
        layout = BoxLayout(orientation="vertical", spacing=10, padding=20)

        # ใส่พื้นหลัง
        self.background = Image(
            source="D:\\game\\Backgeam.jpg", allow_stretch=True, keep_ratio=False
        )
        self.add_widget(self.background)

        # เพิ่มปุ่ม Play
        play_button = Button(
            text="Play",
            size_hint=(None, None),
            size=(200, 80),
            pos_hint={"center_x": 0.5, "y": 0},
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

        main_layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        # Grid Layout สำหรับตัวละคร
        grid = GridLayout(cols=3, spacing=10, padding=10, size_hint=(1, 0.8))

        # รายละเอียดตัวละคร
        self.characters = [
            {
                "image": r"c:\Users\Acer\Downloads\\chinj.png",
                "name": "Shinchan",
                "info": "A 5-year-old boy who is naughty, likes to prank others, likes to dance butt cheek poses.",
                "bonus": "Choco Bee, Action Kamen.",
            },
            {
                "image": r"C:\Users\Acer\Downloads\\kasaj.png",
                "name": "Kasama",
                "info": "Shin-chan's best friend who is smart and often acts like an adult.",
                "bonus": "Books, Fancy Eateries and Good Looking.",
            },
            {
                "image": r"C:\Users\Acer\Downloads\\nenej.png",
                "name": "Nene",
                "info": "A girl who looks neat but actually secretly has a deep malice.",
                "bonus": "Tea, stuffed rabbits",
            },
            {
                "image": r"C:\Users\Acer\Downloads\\bowwj.png",
                "name": "Bow jang",
                "info": "The boy is laconic and cute, and unique in that he always has a runny nose.",
                "bonus": "Butter bread, stones.",
            },
            {
                "image": r"C:\Users\Acer\Downloads\\masaj.png",
                "name": "Masao",
                "info": "A shy boy who is often bullied.",
                "bonus": "Drawing, Snack",
            },
            {
                "image": r"c:\Users\Acer\Downloads\\ij.png",
                "name": "I jang",
                "info": "A rich girl who likes Shin-chan.",
                "bonus": "Cake, Princess",
            },
        ]

        # เพิ่มปุ่มตัวละคร
        for char in self.characters:
            char_button = Button(
                background_normal=char["image"],
                background_down=char["image"],
                size_hint=(1, 1),
            )
            char_button.bind(
                on_press=lambda instance, c=char: self.show_character_info(c)
            )
            grid.add_widget(char_button)

        # Layout แสดงข้อมูลตัวละคร
        self.info_layout = BoxLayout(orientation="vertical", size_hint=(1, 0.2))

        self.name_label = Label(text="", font_size=24, size_hint=(1, None), height=40)
        self.info_label = Label(
            text="",
            font_size=18,
            size_hint=(1, None),
            height=80,
            halign="center",
            valign="middle",
        )
        self.info_label.bind(size=self.info_label.setter("text_size"))
        self.bonus_label = Label(text="", font_size=18, size_hint=(1, None), height=40)

        self.info_layout.add_widget(self.name_label)
        self.info_layout.add_widget(self.info_label)
        self.info_layout.add_widget(self.bonus_label)

        main_layout.add_widget(grid)
        main_layout.add_widget(self.info_layout)

        # ปุ่ม Start
        start_button = Button(
            text="Start",
            size_hint=(None, None),
            size=(200, 80),
            pos_hint={"center_x": 0.5, "y": 0},
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

        # Layout สำหรับนับถอยหลัง
        layout = BoxLayout(orientation="vertical", padding=20, spacing=20)
        self.countdown_label = Label(
            text="5", font_size=150, size_hint=(1, 1), halign="center", valign="middle"
        )
        layout.add_widget(self.countdown_label)

        self.count = 7
        Clock.schedule_interval(self.update_countdown, 1)

        self.add_widget(layout)

    def update_countdown(self, dt):
        self.count -= 1
        self.countdown_label.text = str(self.count)
        if self.count == 0:
            Clock.unschedule(self.update_countdown)
            self.manager.current = "game_screen"


# [Previous GameScreen class implementation remains the same]


class MyGameApp(App):
    def build(self):
        # ตั้งค่าขนาดหน้าต่างเกม
        Window.size = (800, 600)

        # สร้าง ScreenManager
        sm = ScreenManager()
        sm.selected_character = None

        # เพิ่มหน้าจอทั้งหมด
        sm.add_widget(MainMenuScreen(name="menu"))
        sm.add_widget(CharacterSelectionScreen(name="character_selection"))
        sm.add_widget(CountdownScreen(name="countdown"))
        sm.add_widget(GameScreen(name="game_screen"))

        return sm


if __name__ == "__main__":
    MyGameApp().run()
