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

        # Grid Layout สำหรับแสดงตัวละคร
        grid = GridLayout(cols=3, spacing=10, padding=10)

        # รูปตัวละคร (ระบุไฟล์รูป) พร้อมข้อมูลเกี่ยวกับสิ่งที่ทำให้ได้คะแนนบวก
        self.characters = [
            {
                "image": r"c:\Users\Acer\Downloads\\chinj.png",
                "name": "Shinchan",
                "info": "A 5-year-old boy who is naughty, likes to prank others, likes to dance butt cheek poses.",
                "bonus": "Choco Bee, Chewing Gum, Action Kamen.",
            },
            {
                "image": r"C:\Users\Acer\Downloads\\kasaj.png",
                "name": "Kasama",
                "info": "AShin-chan's best friend who is smart and often acts like an adult.",
                "bonus": "Books, Fancy Eateries and Good Looking.",
            },
            {
                "image": r"C:\Users\Acer\Downloads\\nenej.png",
                "name": "Nene",
                "info": "A girl who looks neat but actually secretly has a deep malice.",
                "bonus": "Cakes, tea, stuffed rabbits",
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

        for char in self.characters:
            char_button = Button(
                background_normal=char["image"],
                background_down=char["image"],
                size_hint=(1, 1),
            )
            char_button.bind(on_press=lambda instance, c=char: self.select_character(c))
            grid.add_widget(char_button)

        # เพิ่ม GridLayout ที่แสดงตัวละคร
        self.add_widget(grid)

    def select_character(self, character):
        # ส่งข้อมูลตัวละครไปยังหน้าจอถัดไป
        self.manager.current = "character_details"
        self.manager.get_screen("character_details").show_character_details(character)


class CharacterDetailsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", spacing=20, padding=20)

        # รูปภาพตัวละคร
        self.image = Image(size_hint=(1, 0.6))  # ปรับให้รูปภาพใหญ่ขึ้น
        self.layout.add_widget(self.image)

        # ชื่อ
        self.name_label = Label(
            text="Name: ",
            font_size=18,
            size_hint=(1, None),
            height=40,
            halign="left",
            valign="middle",
            text_size=(None, None),
        )
        self.layout.add_widget(self.name_label)

        # ข้อมูล
        self.info_label = Label(
            text="Info: ",
            font_size=16,
            size_hint=(1, None),
            height=40,
            halign="left",
            valign="middle",
            text_size=(None, None),
        )
        self.layout.add_widget(self.info_label)

        # โบนัส
        self.bonus_label = Label(
            text="Bonus: ",
            font_size=14,
            size_hint=(1, None),
            height=40,
            halign="left",
            valign="middle",
            text_size=(None, None),
        )
        self.layout.add_widget(self.bonus_label)

        self.add_widget(self.layout)

    def show_character_details(self, character):
        # แสดงข้อมูลของตัวละคร
        self.image.source = character["image"]
        self.name_label.text = f"Name: {character['name']}"
        self.info_label.text = f"Info: {character['info']}"
        self.bonus_label.text = f"Bonus: {character['bonus']}"


class MyGameApp(App):
    def build(self):
        # ScreenManager สำหรับจัดการหน้าจอ
        sm = ScreenManager()

        # เพิ่มหน้าต่างต่าง ๆ
        sm.add_widget(MainMenuScreen(name="menu"))
        sm.add_widget(CharacterSelectionScreen(name="character_selection"))
        sm.add_widget(CharacterDetailsScreen(name="character_details"))

        return sm


if __name__ == "__main__":
    MyGameApp().run()
