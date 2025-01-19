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
import random


class FallingBonus(Image):
    """วัตถุที่ตกลงมาจากด้านบน"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (50, 50)  # ขนาดโบนัส

    def reset_position(self, screen_width):
        """กำหนดตำแหน่งเริ่มต้นใหม่ด้านบน"""
        self.x = random.randint(0, screen_width - self.width)
        self.y = screen_width  # เริ่มจากด้านบนสุด


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

        # เพิ่มปุ่ม Play ตรงกลางล่าง
        play_button = Button(
            text="Play",
            size_hint=(None, None),
            size=(200, 80),
            pos_hint={"center_x": 0.5, "y": 0},  # ตั้งตำแหน่งที่กลางล่าง
            font_size=24,
            background_color=(0.2, 0.6, 1, 1),  # สีน้ำเงิน
        )
        play_button.bind(on_press=self.go_to_character_selection)
        layout.add_widget(play_button)

        # เพิ่ม Layout ที่มีพื้นหลัง
        self.add_widget(layout)

    def go_to_character_selection(self, instance):
        self.manager.current = "character_selection"  # ไปหน้าที่สอง


class CharacterSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Layout หลัก
        main_layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        # Grid Layout สำหรับแสดงตัวละคร
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

        # เพิ่มปุ่มตัวละครใน GridLayout
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

        # Layout สำหรับแสดงข้อมูลตัวละครด้านล่าง
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

        # เพิ่ม Layout เข้ากับหน้าจอหลัก
        main_layout.add_widget(grid)
        main_layout.add_widget(self.info_layout)

        # เพิ่มปุ่ม start
        start_button = Button(
            text="Start",
            size_hint=(None, None),
            size=(200, 80),
            pos_hint={"center_x": 0.5, "y": 0},  # ตั้งตำแหน่งที่กลางล่าง
            font_size=24,
            background_color=(0.2, 0.6, 1, 1),  # สีน้ำเงิน
        )
        start_button.bind(on_press=self.start_countdown)
        main_layout.add_widget(start_button)

        self.add_widget(main_layout)

    def show_character_info(self, character):
        """แสดงข้อมูลตัวละครเมื่อกดปุ่ม"""
        self.name_label.text = f"Name: {character['name']}"
        self.info_label.text = f"Info: {character['info']}"
        self.bonus_label.text = f"Bonus: {character['bonus']}"
        self.manager.selected_character = character  # เก็บตัวละครที่เลือกใน ScreenManager

    def start_countdown(self, instance):
        """ไปหน้าจอนับถอยหลัง"""
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

        # Layout สำหรับการนับถอยหลัง
        layout = BoxLayout(orientation="vertical", padding=20, spacing=20)
        self.countdown_label = Label(
            text="5", font_size=150, size_hint=(1, 1), halign="center", valign="middle"
        )
        layout.add_widget(self.countdown_label)

        # เริ่มนับถอยหลังจาก 5
        self.count = 7
        Clock.schedule_interval(self.update_countdown, 1)

        self.add_widget(layout)

    def update_countdown(self, dt):
        """อัปเดตการนับถอยหลัง"""
        self.count -= 1
        self.countdown_label.text = str(self.count)
        if self.count == 0:
            Clock.unschedule(self.update_countdown)
            self.manager.current = "game_screen"  # เปลี่ยนไปหน้าจอเกม


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Layout หลัก
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=20)

        # พื้นที่เกมหลัก
        self.game_area = Widget(size_hint=(1, 0.8))
        self.layout.add_widget(self.game_area)

        # แทบด้านล่างสำหรับตัวละครที่เลือก
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

        # ตัวแปรสำหรับโบนัส
        self.bonus_objects = []
        Clock.schedule_interval(self.create_falling_bonus, 2)  # สร้างโบนัสทุก 2 วินาที

        self.add_widget(self.layout)

    def on_enter(self):
        """แสดงข้อมูลตัวละครที่เลือกเมื่อเข้าสู่หน้าจอนี้"""
        if (
            hasattr(self.manager, "selected_character")
            and self.manager.selected_character
        ):
            selected_character = self.manager.selected_character
            self.character_image.source = selected_character["image"]
            self.character_info.text = (
                f"Name: {selected_character['name']}\n"
                f"Info: {selected_character['info']}\n"
                f"Bonus: {selected_character['bonus']}"
            )

    def create_falling_bonus(self, dt):
        """สร้างโบนัสใหม่ที่ตกลงจากด้านบน"""
        screen_width = self.game_area.width
        bonus = FallingBonus(source="path/to/bonus_image.png")
        bonus.reset_position(screen_width)
        self.game_area.add_widget(bonus)

        # สร้างอนิเมชั่นให้โบนัสตกลง
        anim = Animation(y=0, duration=4)  # ระยะเวลาตก 4 วินาที
        anim.start(bonus)
        self.bonus_objects.append(bonus)


class MyGameApp(App):
    def build(self):
        sm = ScreenManager()

        # เพิ่มตัวเก็บข้อมูลตัวละครที่เลือก
        sm.selected_character = None

        # เพิ่มหน้าจอ
        sm.add_widget(MainMenuScreen(name="menu"))
        sm.add_widget(CharacterSelectionScreen(name="character_selection"))
        sm.add_widget(CountdownScreen(name="countdown"))
        sm.add_widget(GameScreen(name="game_screen"))

        return sm


if __name__ == "__main__":
    MyGameApp().run()
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
import random


class FallingBonus(Image):
    """วัตถุที่ตกลงมาจากด้านบน"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (50, 50)  # ขนาดโบนัส

    def reset_position(self, screen_width):
        """กำหนดตำแหน่งเริ่มต้นใหม่ด้านบน"""
        self.x = random.randint(0, screen_width - self.width)
        self.y = screen_width  # เริ่มจากด้านบนสุด


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

        # เพิ่มปุ่ม Play ตรงกลางล่าง
        play_button = Button(
            text="Play",
            size_hint=(None, None),
            size=(200, 80),
            pos_hint={"center_x": 0.5, "y": 0},  # ตั้งตำแหน่งที่กลางล่าง
            font_size=24,
            background_color=(0.2, 0.6, 1, 1),  # สีน้ำเงิน
        )
        play_button.bind(on_press=self.go_to_character_selection)
        layout.add_widget(play_button)

        # เพิ่ม Layout ที่มีพื้นหลัง
        self.add_widget(layout)

    def go_to_character_selection(self, instance):
        self.manager.current = "character_selection"  # ไปหน้าที่สอง


class CharacterSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Layout หลัก
        main_layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        # Grid Layout สำหรับแสดงตัวละคร
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

        # เพิ่มปุ่มตัวละครใน GridLayout
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

        # Layout สำหรับแสดงข้อมูลตัวละครด้านล่าง
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

        # เพิ่ม Layout เข้ากับหน้าจอหลัก
        main_layout.add_widget(grid)
        main_layout.add_widget(self.info_layout)

        # เพิ่มปุ่ม start
        start_button = Button(
            text="Start",
            size_hint=(None, None),
            size=(200, 80),
            pos_hint={"center_x": 0.5, "y": 0},  # ตั้งตำแหน่งที่กลางล่าง
            font_size=24,
            background_color=(0.2, 0.6, 1, 1),  # สีน้ำเงิน
        )
        start_button.bind(on_press=self.start_countdown)
        main_layout.add_widget(start_button)

        self.add_widget(main_layout)

    def show_character_info(self, character):
        """แสดงข้อมูลตัวละครเมื่อกดปุ่ม"""
        self.name_label.text = f"Name: {character['name']}"
        self.info_label.text = f"Info: {character['info']}"
        self.bonus_label.text = f"Bonus: {character['bonus']}"
        self.manager.selected_character = character  # เก็บตัวละครที่เลือกใน ScreenManager

    def start_countdown(self, instance):
        """ไปหน้าจอนับถอยหลัง"""
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

        # Layout สำหรับการนับถอยหลัง
        layout = BoxLayout(orientation="vertical", padding=20, spacing=20)
        self.countdown_label = Label(
            text="5", font_size=150, size_hint=(1, 1), halign="center", valign="middle"
        )
        layout.add_widget(self.countdown_label)

        # เริ่มนับถอยหลังจาก 5
        self.count = 7
        Clock.schedule_interval(self.update_countdown, 1)

        self.add_widget(layout)

    def update_countdown(self, dt):
        """อัปเดตการนับถอยหลัง"""
        self.count -= 1
        self.countdown_label.text = str(self.count)
        if self.count == 0:
            Clock.unschedule(self.update_countdown)
            self.manager.current = "game_screen"  # เปลี่ยนไปหน้าจอเกม


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Layout หลัก
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=20)

        # พื้นที่เกมหลัก
        self.game_area = Widget(size_hint=(1, 0.8))
        self.layout.add_widget(self.game_area)

        # แทบด้านล่างสำหรับตัวละครที่เลือก
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

        # ตัวแปรสำหรับโบนัส
        self.bonus_objects = []
        Clock.schedule_interval(self.create_falling_bonus, 2)  # สร้างโบนัสทุก 2 วินาที

        self.add_widget(self.layout)

    def on_enter(self):
        """แสดงข้อมูลตัวละครที่เลือกเมื่อเข้าสู่หน้าจอนี้"""
        if (
            hasattr(self.manager, "selected_character")
            and self.manager.selected_character
        ):
            selected_character = self.manager.selected_character
            self.character_image.source = selected_character["image"]
            self.character_info.text = (
                f"Name: {selected_character['name']}\n"
                f"Info: {selected_character['info']}\n"
                f"Bonus: {selected_character['bonus']}"
            )

    def create_falling_bonus(self, dt):
        """สร้างโบนัสใหม่ที่ตกลงจากด้านบน"""
        screen_width = self.game_area.width
        bonus = FallingBonus(source="path/to/bonus_image.png")
        bonus.reset_position(screen_width)
        self.game_area.add_widget(bonus)

        # สร้างอนิเมชั่นให้โบนัสตกลง
        anim = Animation(y=0, duration=4)  # ระยะเวลาตก 4 วินาที
        anim.start(bonus)
        self.bonus_objects.append(bonus)


class MyGameApp(App):
    def build(self):
        sm = ScreenManager()

        # เพิ่มตัวเก็บข้อมูลตัวละครที่เลือก
        sm.selected_character = None

        # เพิ่มหน้าจอ
        sm.add_widget(MainMenuScreen(name="menu"))
        sm.add_widget(CharacterSelectionScreen(name="character_selection"))
        sm.add_widget(CountdownScreen(name="countdown"))
        sm.add_widget(GameScreen(name="game_screen"))

        return sm


if __name__ == "__main__":
    MyGameApp().run()
