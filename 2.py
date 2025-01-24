from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.graphics import Rectangle
from kivy.uix.image import Image


# สร้างหน้าจอเริ่มต้น (หน้าแรก)
class StartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # เพิ่มพื้นหลัง (ใช้สีหรือภาพ)
        with self.canvas.before:
            # สามารถใช้สีพื้นหลังได้
            self.rect = Rectangle(source="background.jpg", pos=self.pos, size=self.size)

        # ให้เรามีการอัพเดทขนาดเมื่อหน้าจอมีการเปลี่ยนแปลง
        self.bind(size=self._update_rect, pos=self._update_rect)

        self.layout = BoxLayout(orientation="vertical", padding=50, spacing=20)

        # ป้ายข้อความบนหน้าจอ
        self.title_label = Label(text="ยินดีต้อนรับสู่เกม!", font_size=40)
        self.layout.add_widget(self.title_label)

        # ปุ่มเริ่มเกม
        self.start_button = Button(
            text="Start Game",
            font_size=40,
            size_hint=(None, None),
            size=(400, 100),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        self.start_button.bind(on_press=self.start_game)  # กดแล้วเริ่มเกม
        self.layout.add_widget(self.start_button)

        self.add_widget(self.layout)

    def _update_rect(self, instance, value):
        # อัพเดทตำแหน่งและขนาดของพื้นหลัง
        self.rect.pos = self.pos
        self.rect.size = self.size

    def start_game(self, instance):
        # เมื่อกดปุ่มจะเปลี่ยนไปที่หน้าจอเกม
        self.manager.current = "game_screen"


# สร้างหน้าจอเกม
class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=50)

        # ใส่ข้อความว่า "เล่นเกมอยู่"
        self.game_label = Label(text="เล่นเกมอยู่!", font_size=40)
        self.layout.add_widget(self.game_label)

        self.add_widget(self.layout)


# สร้าง ScreenManager สำหรับการจัดการหลายๆ หน้าจอ
class MyGameApp(App):
    def build(self):
        # สร้าง ScreenManager
        sm = ScreenManager()

        # เพิ่มหน้าจอทั้งสอง (หน้าแรกและหน้าจอเกม)
        sm.add_widget(StartScreen(name="start_screen"))
        sm.add_widget(GameScreen(name="game_screen"))

        # ตั้งค่าเริ่มต้นที่หน้าจอเริ่มต้น
        sm.current = "start_screen"

        # กำหนดขนาดหน้าต่าง
        Window.size = (800, 600)

        return sm


if __name__ == "__main__":
    MyGameApp().run()
