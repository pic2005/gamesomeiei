from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout


class CharacterSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_character = None
        self.character_thumbnail = None

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

        self.add_widget(main_layout)

    def show_character_info(self, character):
        """แสดงข้อมูลตัวละครเมื่อกดปุ่ม"""
        self.name_label.text = f"Name: {character['name']}"
        self.info_label.text = f"Info: {character['info']}"
        self.bonus_label.text = f"Bonus: {character['bonus']}"

        self.selected_character = character

        # เพิ่ม Thumbnail ที่เลื่อนตามเมาส์
        if not self.character_thumbnail:
            self.character_thumbnail = Image(
                source=character["image"],
                size_hint=(None, None),
                size=(100, 100),
                allow_stretch=True,
            )
            self.add_widget(self.character_thumbnail)

    def on_touch_move(self, touch):
        """อัปเดตตำแหน่งตัวละครตามเมาส์"""
        if self.character_thumbnail:
            self.character_thumbnail.pos = (touch.x - 50, touch.y - 50)


class MyGameApp(App):
    def build(self):
        sm = ScreenManager()

        # เพิ่มหน้าจอ
        sm.add_widget(CharacterSelectionScreen(name="character_selection"))

        return sm


if __name__ == "__main__":
    MyGameApp().run()
