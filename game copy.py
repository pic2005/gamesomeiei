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

        # รูปตัวละคร (ระบุไฟล์รูป) พร้อมข้อมูลเกี่ยวกับสิ่งที่ทำให้ได้คะแนนบวก
        self.characters = [
            {
                "image": r"c:\Users\Acer\Downloads\\chinj.png",
                "name": "Shinchan",
                "info": "A brave warrior.",
                "bonus": "Increased defense for bravery in battle.",
            },
            {
                "image": r"C:\Users\Acer\Downloads\\kasaj.png",
                "name": "Kasama",
                "info": "A stealthy assassin.",
                "bonus": "High attack power due to stealth tactics.",
            },
            {
                "image": r"C:\Users\Acer\Downloads\\nenej.png",
                "name": "Nene",
                "info": "A skilled mage.",
                "bonus": "Increased magic damage from intense training.",
            },
            {
                "image": r"C:\Users\Acer\Downloads\\bowwj.png",
                "name": "Bow jang",
                "info": "An archer with great aim.",
                "bonus": "Bonus damage for precise shots.",
            },
            {
                "image": r"C:\Users\Acer\Downloads\\masaj.png",
                "name": "Masao",
                "info": "A master of swords.",
                "bonus": "Bonus defense and attack when using a sword.",
            },
            {
                "image": r"c:\Users\Acer\Downloads\\ij.png",
                "name": "I jang",
                "info": "A swift and cunning rogue.",
                "bonus": "High evasion rate and critical hit chance.",
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
        self.image = Image()
        self.name_label = Button(size_hint=(None, None), size=(300, 50), font_size=24)
        self.info_label = Button(size_hint=(None, None), size=(300, 50), font_size=18)
        self.bonus_label = Button(size_hint=(None, None), size=(300, 50), font_size=16)

        self.layout.add_widget(self.image)
        self.layout.add_widget(self.name_label)
        self.layout.add_widget(self.info_label)
        self.layout.add_widget(self.bonus_label)

        self.add_widget(self.layout)

    def show_character_details(self, character):
        # แสดงข้อมูลของตัวละคร
        self.image.source = character["image"]
        self.name_label.text = f"Name: {character['name']}"
        self.info_label.text = f"Info: {character['info']}"
        self.bonus_label.text = f"Bonus: {character['bonus']}"  # แสดงข้อมูลโบนัส


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
