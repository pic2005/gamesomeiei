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
            pos_hint={"center_x": 0.5, "center_y": 0.1},
            font_size=24,
            background_color=(0.2, 0.6, 1, 1),
        )
        play_button.bind(on_press=self.go_to_character_selection)
        layout.add_widget(play_button)

        # เพิ่ม Layout บนพื้นหลัง
        self.add_widget(layout)

    def go_to_character_selection(self, instance):
        self.manager.current = "character_selection"


class CharacterSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Grid Layout สำหรับแสดงตัวละคร
        grid = GridLayout(cols=3, spacing=10, padding=10)

        # รูปตัวละคร พร้อมข้อมูล
        self.characters = [
            {
                "image": r"c:\Users\Acer\Downloads\chinj.png",
                "name": "Shinchan",
                "info": "A 5-year-old boy who is naughty, likes to prank others, likes to dance butt cheek poses.",
                "bonus": "Choco Bee, Chewing Gum, Action Kamen.",
            },
            # เพิ่มตัวละครอื่น ๆ ตามต้องการ
        ]

        for char in self.characters:
            char_button = Button(
                background_normal=char["image"],
                background_down=char["image"],
                size_hint=(1, 1),
            )
            char_button.bind(on_press=lambda instance, c=char: self.select_character(c))
            grid.add_widget(char_button)

        self.add_widget(grid)

    def select_character(self, character):
        self.manager.current = "character_details"
        self.manager.get_screen("character_details").show_character_details(character)


class CharacterDetailsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", spacing=20, padding=20)
        self.image = Image(size_hint=(1, 0.6))
        self.name_label = Label(font_size=24, size_hint=(1, None), height=50)
        self.info_label = Label(font_size=18, size_hint=(1, None), height=100)
        self.bonus_label = Label(font_size=16, size_hint=(1, None), height=50)

        layout.add_widget(self.image)
        layout.add_widget(self.name_label)
        layout.add_widget(self.info_label)
        layout.add_widget(self.bonus_label)
        self.add_widget(layout)

    def show_character_details(self, character):
        self.image.source = character["image"]
        self.name_label.text = f"Name: {character['name']}"
        self.info_label.text = f"Info: {character['info']}"
        self.bonus_label.text = f"Bonus: {character['bonus']}"


class MyGameApp(App):
   
