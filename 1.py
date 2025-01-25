from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.vector import Vector


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

        # Back button
        back_button = Button(
            text="BACK",
            font_size=24,
            size_hint=(None, None),
            size=(200, 100),
            pos_hint={"center_x": 0.5, "center_y": 0.1},
            background_color=(0.8, 0.4, 0.4, 1),
        )
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def go_back(self, instance):
        # ไปที่หน้าควบคุมตัวละคร
        self.manager.current = "game_screen"


class GameScreen(Screen):
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
            size=(100, 100),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        layout.add_widget(self.character)

        # กำหนดความเร็วการเคลื่อนที่
        self.velocity_x = 0
        self.speed = 5  # ความเร็วในการเคลื่อนที่

        # ตรวจจับการกดปุ่มคีย์บอร์ด
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

        # อัพเดทตำแหน่งตัวละครทุกเฟรม
        Clock.schedule_interval(self.update, 1.0 / 60.0)

        self.add_widget(layout)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # ตรวจสอบปุ่มที่กด
        if keycode[1] == "a":  # ปุ่ม A
            self.velocity_x = -self.speed
        elif keycode[1] == "d":  # ปุ่ม D
            self.velocity_x = self.speed
        return True

    def _on_keyboard_up(self, keyboard, keycode):
        # หยุดเคลื่อนที่เมื่อปล่อยปุ่ม
        if keycode[1] in ("a", "d"):
            self.velocity_x = 0
        return True

    def update(self, dt):
        # อัพเดทตำแหน่งตัวละครตามความเร็ว
        self.character.x += self.velocity_x

        # จำกัดขอบเขตการเคลื่อนที่ของตัวละคร
        if self.character.x < 0:
            self.character.x = 0
        elif self.character.right > Window.width:
            self.character.right = Window.width


class GameApp(App):
    def build(self):
        # ตั้งค่าขนาดหน้าจอเริ่มต้น
        Window.size = (800, 600)  # ตัวอย่างขนาด 800x600 พิกเซล

        sm = ScreenManager()

        # เพิ่มหน้าแรก, หน้าแนะนำตัวละคร, และหน้าควบคุมตัวละคร
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
