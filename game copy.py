from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from random import randint


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

        self.add_widget(layout)

    def go_to_character_selection(self, instance):
        self.manager.current = "character_selection"


class CharacterSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        grid = GridLayout(cols=3, spacing=10, padding=10)

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
                "bonus": "tea, stuffed rabbits",
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

        self.add_widget(grid)

    def select_character(self, character):
        self.manager.current = "character_details"
        self.manager.get_screen("character_details").show_character_details(character)


class CharacterDetailsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation="vertical", spacing=20, padding=20)

        self.image = Image(size_hint=(1, 0.6))
        self.layout.add_widget(self.image)

        self.name_label = Label(
            text="Name: ",
            font_size=23,
            size_hint=(1, None),
            height=40,
            halign="left",
            valign="middle",
            text_size=(None, None),
        )
        self.layout.add_widget(self.name_label)

        self.info_label = Label(
            text="Info: ",
            font_size=23,
            size_hint=(1, None),
            height=40,
            halign="left",
            valign="middle",
            text_size=(None, None),
        )
        self.layout.add_widget(self.info_label)

        self.bonus_label = Label(
            text="Bonus: ",
            font_size=23,
            size_hint=(1, None),
            height=40,
            halign="center",
            valign="middle",
            text_size=(None, None),
        )
        self.layout.add_widget(self.bonus_label)

        start_button = Button(
            text="Start Game",
            size_hint=(None, None),
            size=(200, 80),
            pos_hint={"center_x": 0.5, "y": 0},
            font_size=24,
            background_color=(0.2, 0.6, 1, 1),
        )
        start_button.bind(on_press=self.start_game)
        self.layout.add_widget(start_button)

        self.add_widget(self.layout)

    def show_character_details(self, character):
        self.image.source = character["image"]
        self.name_label.text = f"Name: {character['name']}"
        self.info_label.text = f"Info: {character['info']}"
        self.bonus_label.text = f"Bonus: {character['bonus']}"

    def start_game(self, instance):
        self.manager.current = "game_screen"
        self.manager.get_screen("game_screen").start_game(
            self.manager.get_screen("character_details").name_label.text
        )


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.character = None
        self.score = 0
        self.bonus_objects = []
        self.non_bonus_objects = []
        self.character_bar = None
        self.game_area = None
        self.fall_speed = 3
        self.game_over_label = None

        Window.bind(mouse_pos=self.on_mouse_move)

    def start_game(self, character_name):
        self.character = character_name
        self.score = 0
        self.bonus_objects = []
        self.non_bonus_objects = []

        layout = BoxLayout(orientation="vertical", spacing=10)
        self.game_area = Widget(size_hint=(1, 0.9))

        self.character_bar = Image(
            source="c:\\Users\\Acer\\Downloads\\chinj.png",
            size_hint=(None, None),
            size=(100, 100),
            pos=(Window.width / 2 - 50, 10),
        )
        self.game_area.add_widget(self.character_bar)

        self.score_label = Label(
            text=f"Score: {self.score}", font_size=30, size_hint=(1, None), height=50
        )
        layout.add_widget(self.score_label)

        layout.add_widget(self.game_area)
        self.add_widget(layout)

        Clock.schedule_interval(self.falling_objects, 1 / 60)
        Clock.schedule_interval(self.update_score, 1)

    def on_mouse_move(self, window, pos):
        x, y = pos
        if self.character_bar:
            new_x = min(
                max(x - self.character_bar.width / 2, 0),
                Window.width - self.character_bar.width,
            )
            self.character_bar.x = new_x

    def falling_objects(self, dt):
        if randint(1, 100) > 90:
            x = randint(0, self.game_area.width - 50)
            obj = BonusObject(x, self.game_area.height, "bonus", self)
            self.bonus_objects.append(obj)
            self.game_area.add_widget(obj)

        if randint(1, 100) > 70:
            x = randint(0, self.game_area.width - 50)
            obj = BonusObject(x, self.game_area.height, "non_bonus", self)
            self.non_bonus_objects.append(obj)
            self.game_area.add_widget(obj)

        for obj in self.bonus_objects + self.non_bonus_objects:
            obj.update_position(dt)
            if obj.y < 0:
                self.game_area.remove_widget(obj)
                if obj.type == "bonus":
                    self.score -= 10
                else:
                    self.score += 10

        for obj in self.bonus_objects + self.non_bonus_objects:
            if self.character_bar.collide_widget(obj):
                if obj.type == "bonus":
                    self.score += 10
                else:
                    self.score -= 10

                self.game_area.remove_widget(obj)
                (
                    self.bonus_objects.remove(obj)
                    if obj.type == "bonus"
                    else self.non_bonus_objects.remove(obj)
                )

    def update_score(self, dt):
        self.score_label.text = f"Score: {self.score}"


class BonusObject(Widget):
    def __init__(self, x, y, type, game_screen, **kwargs):
        super().__init__(**kwargs)
        self.size = (50, 50)
        self.pos = (x, y)
        self.type = type
        self.game_screen = game_screen

        self.color = (1, 0, 0, 1) if type == "bonus" else (0, 1, 0, 1)

        with self.canvas:
            Color(*self.color)
            self.rect = Rectangle(size=self.size, pos=self.pos)

    def update_position(self, dt):
        self.y -= self.game_screen.fall_speed
        self.rect.pos = (self.x, self.y)


class MyGameApp(App):
    def build(self):
        sm = ScreenManager()

        sm.add_widget(MainMenuScreen(name="menu"))
        sm.add_widget(CharacterSelectionScreen(name="character_selection"))
        sm.add_widget(CharacterDetailsScreen(name="character_details"))
        sm.add_widget(GameScreen(name="game_screen"))

        return sm


if __name__ == "__main__":
    MyGameApp().run()
