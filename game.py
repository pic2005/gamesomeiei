from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout


class MainMenuApp(App):
    def build(self):
        # Layout หลัก
        layout = BoxLayout(orientation="vertical", spacing=10, padding=20)

        # ใส่พื้นหลัง
        self.background = Image(
            source="D:\game\Backgeam.jpg", allow_stretch=True, keep_ratio=False
        )
        layout.add_widget(self.background)

        # ปุ่ม Play
        play_button = Button(
            text="Play",
            size_hint=(None, None),
            size=(200, 80),
            pos_hint={"center_x": 0.5},
            font_size=24,
            background_color=(0.2, 0.6, 1, 1),  # สีน้ำเงิน
        )
        play_button.bind(on_press=self.on_play_button_pressed)
        layout.add_widget(play_button)

        return layout

    def on_play_button_pressed(self, instance):
        print("Play button pressed!")  # แสดงข้อความเมื่อกดปุ่ม


if __name__ == "__main__":
    MainMenuApp().run()
