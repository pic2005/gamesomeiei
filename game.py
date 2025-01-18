from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


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

        # ปุ่ม Start
        self.start_button = Button(
            text="Start",
            size_hint=(None, None),
            size=(200, 80),
            pos_hint={"center_x": 0.5, "y": 0},  # ตั้งตำแหน่งที่กลางล่าง
            font_size=24,
            background_color=(0.2, 0.8, 0.2, 1),  # สีเขียว
        )
        self.start_button.bind(on_press=self.go_to_game_screen)

        # เพิ่ม Layout เข้ากับหน้าจอหลัก
        main_layout.add_widget(grid)
        main_layout.add_widget(self.info_layout)
        main_layout.add_widget(self.start_button)

        self.add_widget(main_layout)

    def show_character_info(self, character):
        """แสดงข้อมูลตัวละครเมื่อกดปุ่ม"""
        self.name_label.text = f"Name: {character['name']}"
        self.info_label.text = f"Info: {character['info']}"
        self.bonus_label.text = f"Bonus: {character['bonus']}"

    def go_to_game_screen(self, instance):
        """ไปที่หน้าจอเกม"""
        self.manager.current = "game_screen"


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", spacing=10, padding=20)

        # ข้อความแสดงการเริ่มเกม
        self.game_label = Label(
            text="Game Started!",
            font_size=32,
            size_hint=(1, None),
            height=100,
            halign="center",
        )
        layout.add_widget(self.game_label)

        # ปุ่มกลับไปที่เมนูหลัก
        back_button = Button(
            text="Back to Main Menu",
            size_hint=(None, None),
            size=(200, 80),
            pos_hint={"center_x": 0.5, "y": 0},
            font_size=24,
            background_color=(0.8, 0.2, 0.2, 1),
        )
        back_button.bind(on_press=self.go_to_main_menu)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def go_to_main_menu(self, instance):
        """กลับไปที่หน้าจอเมนูหลัก"""
        self.manager.current = "menu"


class MyGameApp(App):
    def build(self):
        sm = ScreenManager()

        # เพิ่มหน้าจอ
        sm.add_widget(MainMenuScreen(name="menu"))
        sm.add_widget(CharacterSelectionScreen(name="character_selection"))
        sm.add_widget(GameScreen(name="game_screen"))

        return sm


if __name__ == "__main__":
    MyGameApp().run()
