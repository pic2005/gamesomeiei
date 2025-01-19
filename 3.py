from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock


class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical", spacing=10, padding=20)

        self.background = Image(
            source="D:\\game\\Backgeam.jpg", allow_stretch=True, keep_ratio=False
        )
        self.add_widget(self.background)

        play_button = Button(
            text="Play",
            size_hint=(None, None),
            size=(200, 80),
            pos_hint={"center_x": 0.5, "y": 0},
            font_size=24,
            background_color=(0.2, 0.6, 1, 1),
        )
        play_button.bind(on_press=self.go_to_character_selection)
        layout.add_widget(play_button)

        character_tab_button = Button(
            text="Character Tab",
            size_hint=(None, None),
            size=(200, 80),
            pos_hint={"center_x": 0.5, "y": 0},
            font_size=24,
            background_color=(0.8, 0.4, 0.2, 1),
        )
        character_tab_button.bind(on_press=self.go_to_character_tab)
        layout.add_widget(character_tab_button)

        self.add_widget(layout)

    def go_to_character_selection(self, instance):
        self.manager.current = "character_selection"

    def go_to_character_tab(self, instance):
        self.manager.current = "character_tab"


class CharacterSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_characters = []

        main_layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        grid = GridLayout(cols=3, spacing=10, padding=10, size_hint=(1, 0.8))

        self.characters = [
            {
                "image": r"c:\\Users\\Acer\\Downloads\\chinj.png",
                "name": "Shinchan",
                "info": "A 5-year-old boy who is naughty, likes to prank others, likes to dance butt cheek poses.",
                "bonus": "Choco Bee, Action Kamen.",
            },
            {
                "image": r"C:\\Users\\Acer\\Downloads\\kasaj.png",
                "name": "Kasama",
                "info": "Shin-chan's best friend who is smart and often acts like an adult.",
                "bonus": "Books, Fancy Eateries and Good Looking.",
            },
            {
                "image": r"C:\\Users\\Acer\\Downloads\\nenej.png",
                "name": "Nene",
                "info": "A girl who looks neat but actually secretly has a deep malice.",
                "bonus": "Tea, stuffed rabbits",
            },
            {
                "image": r"C:\\Users\\Acer\\Downloads\\bowwj.png",
                "name": "Bow jang",
                "info": "The boy is laconic and cute, and unique in that he always has a runny nose.",
                "bonus": "Butter bread, stones.",
            },
            {
                "image": r"C:\\Users\\Acer\\Downloads\\masaj.png",
                "name": "Masao",
                "info": "A shy boy who is often bullied.",
                "bonus": "Drawing, Snack",
            },
            {
                "image": r"c:\\Users\\Acer\\Downloads\\ij.png",
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

        main_layout.add_widget(grid)
        main_layout.add_widget(self.info_layout)

        start_button = Button(
            text="Start",
            size_hint=(None, None),
            size=(200, 80),
            pos_hint={"center_x": 0.5, "y": 0},
            font_size=24,
            background_color=(0.2, 0.6, 1, 1),
        )
        start_button.bind(on_press=self.start_game)
        main_layout.add_widget(start_button)

        self.add_widget(main_layout)

    def select_character(self, character):
        self.name_label.text = f"Name: {character['name']}"
        self.info_label.text = f"Info: {character['info']}"
        self.bonus_label.text = f"Bonus: {character['bonus']}"

        if character not in self.selected_characters:
            self.selected_characters.append(character)

    def start_game(self, instance):
        self.manager.current = "countdown"  # ไปหน้าจอนับถอยหลัง
        self.manager.get_screen("game_screen").update_selected_characters(
            self.selected_characters
        )
        self.manager.get_screen("character_tab").update_selected_characters(
            self.selected_characters
        )


class CountdownScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Layout สำหรับการนับถอยหลัง
        layout = BoxLayout(orientation="vertical", padding=20, spacing=20)

        # ป้ายข้อความสำหรับนับถอยหลัง
        self.countdown_label = Label(
            text="5", font_size=150, size_hint=(1, 1), halign="center", valign="middle"
        )
        layout.add_widget(self.countdown_label)

        # เริ่มนับถอยหลังจาก 5
        self.count = 5
        Clock.schedule_interval(self.update_countdown, 1)

        self.add_widget(layout)

    def update_countdown(self, dt):
        """อัปเดตการนับถอยหลัง"""
        self.count -= 1
        self.countdown_label.text = str(self.count)
        if self.count == 0:
            Clock.unschedule(self.update_countdown)
            self.manager.current = "game_screen"  # เปลี่ยนไปหน้าจอเกม


class CharacterTabScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.main_layout = BoxLayout(orientation="vertical", spacing=10, padding=20)

        self.label = Label(text="Character Tab", font_size=50, size_hint=(1, 0.1))
        self.main_layout.add_widget(self.label)

        self.scroll_view = ScrollView(size_hint=(1, 0.9))
        self.character_layout = BoxLayout(size_hint_y=None, height=150, spacing=10)
        self.scroll_view.add_widget(self.character_layout)
        self.main_layout.add_widget(self.scroll_view)

        self.add_widget(self.main_layout)

    def update_selected_characters(self, selected_characters):
        self.character_layout.clear_widgets()

        for char in selected_characters:
            char_image = Button(
                background_normal=char["image"],
                size_hint=(None, None),
                size=(150, 150),
            )
            self.character_layout.add_widget(char_image)


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_layout = BoxLayout(orientation="vertical", spacing=10, padding=20)

        self.label = Label(text="Game Started", font_size=50, size_hint=(1, 0.2))
        self.main_layout.add_widget(self.label)

        self.scroll_view = ScrollView(size_hint=(1, 0.2))
        self.character_layout = BoxLayout(size_hint_y=None, height=150, spacing=10)
        self.scroll_view.add_widget(self.character_layout)
        self.main_layout.add_widget(self.scroll_view)

        self.add_widget(self.main_layout)

    def update_selected_characters(self, selected_characters):
        self.character_layout.clear_widgets()

        for char in selected_characters:
            char_image = Button(
                background_normal=char["image"],
                size_hint=(None, None),
                size=(150, 150),
            )
            self.character_layout.add_widget(char_image)


class MyGameApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenuScreen(name="menu"))
        sm.add_widget(CharacterSelectionScreen(name="character_selection"))
        sm.add_widget(CountdownScreen(name="countdown"))  # เพิ่มหน้าจอนับถอยหลัง
        sm.add_widget(CharacterTabScreen(name="character_tab"))  # เพิ่มหน้าจอแทบตัวละคร
        sm.add_widget(GameScreen(name="game_screen"))
        return sm


if __name__ == "__main__":
    MyGameApp().run()
