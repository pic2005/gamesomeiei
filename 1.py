from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock
import random


# หน้าจอหลัก
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # เพิ่มพื้นหลัง
        background = Image(
            source=r"C:\Users\Acer\OneDrive\Pictures\Screenshots\พื้นหลังไทย.png"
        )
        layout.add_widget(background)

        # สร้างปุ่ม Start
        start_button = Button(
            text="Start",
            font_size=24,
            size_hint=(None, None),
            size=(200, 100),
            pos_hint={"center_x": 0.5, "center_y": 0.3},
            background_normal="",
            background_color=(1, 0.84, 0, 1),
            border=(20, 20, 20, 20),
            color=(0, 0, 0, 1),
        )

        start_button.bind(on_press=self.start_game)

        layout.add_widget(start_button)

        self.add_widget(layout)

    def start_game(self, instance):
        self.manager.current = "character_screen"


# หน้าจอเลือกตัวละคร
class CharacterSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()

        # เพิ่มพื้นหลัง
        background = Image(
            source=r"C:\Users\Acer\OneDrive\Pictures\Screenshots\พื้นหลังเลือกตัวละคร.png",
            size_hint=(1, 1),
            allow_stretch=True,
        )
        self.layout.add_widget(background)

        # เพิ่มตัวละคร (ให้เป็นขนาดเดิม)
        self.character = Image(
            source=r"C:\Users\Acer\Downloads\ช้าง.png",
            size_hint=(None, None),
            size=(1000, 1000),  # ขนาดตัวละครเดิม
            pos_hint={"center_x": 0.5, "center_y": 0.6},  # ปรับตำแหน่งตามเดิม
        )
        self.layout.add_widget(self.character)

        # เพิ่มคำอธิบายเกม
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
        self.layout.add_widget(game_description)

        # เพิ่มปุ่มเลือกตัวละคร
        select_button = Button(
            text="START",
            font_size=24,
            size_hint=(None, None),
            size=(200, 100),
            pos_hint={"center_x": 0.5, "center_y": 0.1},
            background_color=(0.4, 0.8, 0.4, 1),
        )
        select_button.bind(on_press=self.select_character)

        self.layout.add_widget(select_button)
        self.add_widget(self.layout)

        # ฟังก์ชันจับการกดแป้นพิมพ์
        Window.bind(on_key_down=self.on_key_down)

    def on_key_down(self, instance, keyboard, keycode, text, modifiers):
        step_size = 10  # ขนาดการเดินแต่ละครั้ง
        x, y = self.character.pos

        # ปรับการเคลื่อนที่เฉพาะแนวนอน (ด้านซ้ายและขวา)
        if keycode == 275:  # ปุ่มลูกศรขวา
            self.character.pos = (x + step_size, y)
        elif keycode == 276:  # ปุ่มลูกศรซ้าย
            self.character.pos = (x - step_size, y)

    def select_character(self, instance):
        print("เลือกตัวละครแล้ว!")
        self.manager.current = "game_screen"


# หน้าจอเกม
class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()

        # เพิ่มตัวละคร (ขนาดเล็กลงครึ่งหนึ่ง)
        self.character = Image(
            source=r"C:\Users\Acer\Downloads\ช้าง.png",
            size_hint=(None, None),
            size=(250, 250),  # ขนาดตัวละครเล็กลงครึ่งหนึ่ง
            pos_hint={"center_x": 0.5, "center_y": 0.1},  # อยู่แถบด้านล่าง
        )
        self.layout.add_widget(self.character)

        # ตัวแปรสำหรับคะแนน
        self.score = 0
        self.score_label = Label(
            text=f"Score: {self.score}",
            font_size=24,
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={"right": 1, "top": 1},
        )
        self.layout.add_widget(self.score_label)

        self.add_widget(self.layout)

        # สร้างโบนัสที่ตกลงมา
        self.bonus = Image(
            source=r"C:\Users\Acer\Downloads\โบนัส.png",  # ใช้ภาพโบนัสของคุณ
            size_hint=(None, None),
            size=(50, 50),  # ขนาดโบนัส
            pos_hint={"center_x": random.random(), "center_y": 1},  # เริ่มต้นที่ด้านบน
        )
        self.layout.add_widget(self.bonus)

        # เริ่มจับเวลาเพื่อให้โบนัสตกลงมา
        self.bonus_fall_event = Clock.schedule_interval(
            self.make_bonus_fall, 1.0 / 60.0
        )  # 60 FPS

        # ฟังก์ชันจับการกดแป้นพิมพ์
        Window.bind(on_key_down=self.on_key_down)

    def on_key_down(self, instance, keyboard, keycode, text, modifiers):
        step_size = 10  # ขนาดการเดินแต่ละครั้ง
        x, y = self.character.pos

        # ปรับการเคลื่อนที่เฉพาะแนวนอน (ด้านซ้ายและขวา)
        if keycode == 275:  # ปุ่มลูกศรขวา
            self.character.pos = (x + step_size, y)
        elif keycode == 276:  # ปุ่มลูกศรซ้าย
            self.character.pos = (x - step_size, y)

    def make_bonus_fall(self, dt):
        # ดึงตำแหน่งปัจจุบันของโบนัส
        x, y = self.bonus.pos

        # ทำให้โบนัสตกลง
        if y > 0:
            self.bonus.pos = (x, y - 5)  # ขนาดการตกลง
        else:
            # รีเซ็ตโบนัสเมื่อมันตกลงถึงพื้น
            self.bonus.pos = (random.random(), 1)  # เปลี่ยนตำแหน่งใหม่ที่ด้านบน

        # เช็คว่าโบนัสชนกับตัวละครหรือไม่
        if self.check_collision(self.character, self.bonus):
            self.score += 10  # เพิ่มคะแนน
            self.score_label.text = f"Score: {self.score}"
            self.bonus.pos = (random.random(), 1)  # รีเซ็ตโบนัส

    def check_collision(self, character, bonus):
        char_x, char_y = character.pos
        bonus_x, bonus_y = bonus.pos

        # เช็คว่าตัวละครและโบนัสอยู่ในตำแหน่งใกล้กันหรือไม่
        if (char_x - 250 < bonus_x < char_x + 250) and (
            char_y - 250 < bonus_y < char_y + 250
        ):
            return True
        return False


# แอปหลัก
class GameApp(App):
    def build(self):
        sm = ScreenManager()

        # หน้าจอหลัก
        main_screen = MainScreen(name="main_screen")
        sm.add_widget(main_screen)

        # หน้าจอเลือกตัวละคร
        character_screen = CharacterSelectionScreen(name="character_screen")
        sm.add_widget(character_screen)

        # หน้าจอเกม
        game_screen = GameScreen(name="game_screen")
        sm.add_widget(game_screen)

        return sm


if __name__ == "__main__":
    GameApp().run()
