from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.core.window import Window


class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Layout หลัก
        layout = BoxLayout(orientation="vertical", padding=20, spacing=20)

        # หัวข้อหลัก
        title = Label(text="เลือกตัวละคร", font_size=32, size_hint=(1, 0.2))
        layout.add_widget(title)

        # ตัวเลือกตัวละคร
        character_layout = BoxLayout(spacing=20, size_hint=(1, 0.5))

        # ตัวละครตัวอย่าง
        characters = [
            {"name": "ตัวละคร A", "image": "character_a.png"},
            {"name": "ตัวละคร B", "image": "character_b.png"},
        ]

        for character in characters:
            button = Button(
                background_normal=character["image"],
                background_down=character["image"],
                size_hint=(None, None),
                size=(100, 100),
            )
            button.bind(
                on_release=lambda btn, char=character: self.select_character(char)
            )
            character_layout.add_widget(button)

        layout.add_widget(character_layout)

        # ปุ่มเริ่มเกม
        start_button = Button(text="เริ่มเกม", size_hint=(1, 0.2))
        start_button.bind(on_release=self.start_game)
        layout.add_widget(start_button)

        self.add_widget(layout)

    def select_character(self, character):
        """บันทึกตัวละครที่เลือกใน ScreenManager"""
        self.manager.selected_character = character

    def start_game(self, instance):
        """เปลี่ยนไปยังหน้าจอเกม"""
        self.manager.current = "game_screen"


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Layout หลัก
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=20)

        # พื้นที่เกมหลัก
        self.game_area = Widget(size_hint=(1, 0.8))
        self.layout.add_widget(self.game_area)

        # ตัวละครที่เลื่อนตามเมาส์
        self.character_image = Image(size_hint=(None, None), size=(80, 80))
        self.layout.add_widget(self.character_image)

        # กำหนดการจับตำแหน่งเมาส์
        Window.bind(mouse_pos=self.on_mouse_move)

        # เพิ่ม Layout เข้ากับหน้าจอ
        self.add_widget(self.layout)

    def on_enter(self):
        """แสดงข้อมูลตัวละครที่เลือกเมื่อเข้าสู่หน้าจอนี้"""
        if (
            hasattr(self.manager, "selected_character")
            and self.manager.selected_character
        ):
            selected_character = self.manager.selected_character
            self.character_image.source = selected_character["image"]

    def on_mouse_move(self, window, pos):
        """อัปเดตตำแหน่งตัวละครตามเมาส์"""
        x, y = pos
        self.character_image.center_x = x
        self.character_image.center_y = y


class CharacterGameApp(App):
    def build(self):
        # สร้าง ScreenManager
        sm = ScreenManager()
        sm.selected_character = None

        # เพิ่มหน้าจอเข้าไปใน ScreenManager
        sm.add_widget(MainMenuScreen(name="main_menu"))
        sm.add_widget(GameScreen(name="game_screen"))

        return sm


# เรียกใช้งานแอปพลิเคชัน
if __name__ == "__main__":
    CharacterGameApp().run()
