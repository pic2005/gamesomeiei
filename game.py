from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image


class StartGameApp(App):
    def build(self):

        layout = BoxLayout(orientation="vertical", spacing=10, padding=20)

        background = Image(source="Backgeam.jpg", allow_stretch=True, keep_ratio=False)
        layout.add_widget(background)

        play_button = Button(
            text="Play",
            size_hint=(None, None),
            size=(200, 80),
            pos_hint={"center_x": 0.5},
        )
        play_button.bind(on_press=self.start_game)
        layout.add_widget(play_button)

        return layout

    def start_game(self, instance):
        print("Game Started!")


if __name__ == "__main__":
    StartGameApp().run()
