from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout


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

        # Grid Layout สำหรับแสดงตัวละคร
        grid = GridLayout(cols=3, spacing=10, padding=10)

        # รูปตัวละคร (ระบุไฟล์รูป)
        characters = [
            r"C:\Users\Acer\Downloadsฃฃ316e71bd-0f12-47d5-ad1f-6a11b0a4121f.jpg",
            r"C:\Users\Acer\Downloads\\kasama.png",
            r"C:\Users\Acer\Downloads\\nenej.png",
            r"C:\Users\Acer\Downloads\\bowwj.png",
            r"C:\Users\Acer\Downloads\\masaj.png",
            r"D:\\game\\char6.jpg",
        ]

        for char in characters:
            char_button = Button(
                background_normal=char,
                background_down=char,
                size_hint=(1, 1),
            )
            char_button.bind(on_press=lambda instance, c=char: self.select_character(c))
            grid.add_widget(char_button)

        # เพิ่ม GridLayout ที่แสดงตัวละคร
        self.add_widget(grid)

    def select_character(self, character):
        print(f"Selected character: {character}")  # แสดงตัวละครที่เลือก


class MyGameApp(App):
    def build(self):
        # ScreenManager สำหรับจัดการหน้าจอ
        sm = ScreenManager()

        # เพิ่มหน้าต่างต่าง ๆ
        sm.add_widget(MainMenuScreen(name="menu"))
        sm.add_widget(CharacterSelectionScreen(name="character_selection"))

        return sm


if __name__ == "__main__":
    MyGameApp().run()
