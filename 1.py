from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label


# หน้าจอหลัก
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # เพิ่มพื้นหลัง
        background = Image(
            source=r"C:\Users\Acer\OneDrive\Pictures\Screenshots\พื้นหลังไทย.png"
        )  # เปลี่ยนเป็น path ของพื้นหลัง
        layout.add_widget(background)

        # สร้างปุ่ม Start
        start_button = Button(
            text="Start",
            font_size=24,
            size_hint=(None, None),
            size=(200, 100),
            pos_hint={"center_x": 0.5, "center_y": 0.3},
            background_normal="",
            background_color=(1, 0.84, 0, 1),  # สีทอง
            border=(20, 20, 20, 20),  # ทำให้ขอบมน
            color=(0, 0, 0, 1),  # สีข้อความดำ
        )

        # กำหนดฟังก์ชันเมื่อคลิกปุ่ม Start
        start_button.bind(on_press=self.start_game)

        # เพิ่มปุ่มลงใน layout
        layout.add_widget(start_button)

        self.add_widget(layout)

    def start_game(self, instance):
        # เปลี่ยนไปยังหน้าจอเลือกตัวละคร
        self.manager.current = "character_screen"


# หน้าจอเลือกตัวละคร
class CharacterSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # เพิ่มพื้นหลัง
        background = Image(
            source=r"C:\Users\Acer\OneDrive\Pictures\Screenshots\พื้นหลังเลือกตัวละคร.png",  # เปลี่ยน path ของพื้นหลัง
            size_hint=(1, 1),  # ครอบคลุมพื้นที่ทั้งหมด
            allow_stretch=True,  # ทำให้ภาพยืดหยุ่นตามขนาดหน้าจอ
        )
        layout.add_widget(background)

        # เพิ่มตัวละครตัวเดียว (ขนาดใหญ่ขึ้น)
        character1 = Image(
            source=r"C:\Users\Acer\Downloads\ช้าง.png",  # เปลี่ยน path ของรูปตัวละคร
            size_hint=(None, None),
            size=(1000, 1000),  # ขนาดใหญ่ขึ้น
            pos_hint={"center_x": 0.5, "center_y": 0.6},
        )
        layout.add_widget(character1)

        # เพิ่มคำอธิบายเกม
        game_description = Label(
            text="Hello, my name is Khud Kat.\nMy name comes from mangosteen.\nPlease help me collect a lot of fallen mangosteen,\nand I will be able to go home.",
            font_size=20,
            color=(0, 0, 0, 1),  # ข้อความสีดำ
            size_hint=(None, None),
            size=(600, 200),  # ขยายขนาดให้พอดีกับข้อความ
            pos_hint={"center_x": 0.5, "center_y": 0.3},
            halign="center",  # จัดข้อความให้กึ่งกลาง
            valign="middle",  # จัดข้อความให้กึ่งกลาง
        )

        layout.add_widget(game_description)

        # เพิ่มปุ่มเลือกตัวละคร
        select_button = Button(
            text="START",
            font_size=24,
            size_hint=(None, None),
            size=(200, 100),
            pos_hint={"center_x": 0.5, "center_y": 0.1},
            background_color=(0.4, 0.8, 0.4, 1),
        )
        select_button.bind(on_press=self.select_character)

        layout.add_widget(select_button)
        self.add_widget(layout)

    def select_character(self, instance):
        print("เลือกตัวละครแล้ว!")
        # คุณสามารถดำเนินการต่อไป เช่น เริ่มเกมหรือทำอะไรก็ได้ที่ต้องการ


# แอปหลัก
class GameApp(App):
    def build(self):
        # สร้าง ScreenManager
        sm = ScreenManager()

        # สร้างหน้าจอหลัก (หน้าแรก)
        main_screen = MainScreen(name="main_screen")
        sm.add_widget(main_screen)

        # สร้างหน้าจอเลือกตัวละคร
        character_screen = CharacterSelectionScreen(name="character_screen")
        sm.add_widget(character_screen)

        class CountdownScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=20, spacing=20)
        self.countdown_label = Label(text="5", font_size=150)
        layout.add_widget(self.countdown_label)
        self.count = 5
        self.add_widget(layout)

    def on_enter(self):
        self.count = 5
        Clock.schedule_interval(self.update_countdown, 1)

    def update_countdown(self, dt):
        self.count -= 1
        self.countdown_label.text = str(self.count)
        if self.count <= 0:
            Clock.unschedule(self.update_countdown)
            self.manager.current = "game_screen"
            return False
        return True


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=20)

        self.info_bar = BoxLayout(orientation="horizontal", size_hint=(1, 0.1))
        self.time_left = 30
        self.timer_label = Label(
            text=f"Time: {self.time_left}", size_hint=(0.5, 1), font_size=24
        )
        self.score = 0
        self.score_label = Label(
            text=f"Score: {self.score}", size_hint=(0.5, 1), font_size=24
        )

        self.info_bar.add_widget(self.timer_label)
        self.info_bar.add_widget(self.score_label)
        self.layout.add_widget(self.info_bar)

        self.game_area = Widget(size_hint=(1, 0.8))
        self.layout.add_widget(self.game_area)

        self.player = None
        self.bonus_objects = []
        self.game_active = False

        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)

        self.movement = 0
        self.add_widget(self.layout)

    def start_game(self):
        self.game_active = True
        self.time_left = 30
        self.score = 0
        self.score_label.text = f"Score: {self.score}"
        Clock.schedule_interval(self.update_timer, 1)
        Clock.schedule_interval(self.create_falling_bonus, 2)
        Clock.schedule_interval(self.update, 1 / 60)

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard.unbind(on_key_up=self._on_key_up)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == "left":
            self.movement = -1
        elif keycode[1] == "right":
            self.movement = 1
        return True

    def _on_key_up(self, keyboard, keycode):
        if keycode[1] in ("left", "right"):
            self.movement = 0
        return True

    def update_timer(self, dt):
        if not self.game_active:
            return False
        self.time_left -= 1
        self.timer_label.text = f"Time: {self.time_left}"
        if self.time_left <= 0:
            self.end_game()
            return False
        return True

    def create_falling_bonus(self, dt):
        if not self.game_active:
            return False
        bonus = FallingBonus()
        bonus.reset_position(self.game_area.width)
        self.game_area.add_widget(bonus)
        anim = Animation(y=0, duration=4)
        anim.bind(on_complete=self.remove_bonus)
        anim.start(bonus)
        self.bonus_objects.append(bonus)

    def remove_bonus(self, animation, bonus):
        if bonus in self.bonus_objects:
            self.bonus_objects.remove(bonus)
            self.game_area.remove_widget(bonus)

    def update(self, dt):
        if not self.game_active:
            return False
        if self.player:
            self.player.move(self.movement, dt)
            for bonus in self.bonus_objects[:]:
                if self.check_collision(self.player, bonus):
                    self.collect_bonus(bonus)

    def check_collision(self, player, bonus):
        return (
            player.x < bonus.x + bonus.width
            and player.x + player.width > bonus.x
            and player.y < bonus.y + bonus.height
            and player.y + player.height > bonus.y
        )

    def collect_bonus(self, bonus):
        self.score += bonus.points
        self.score_label.text = f"Score: {self.score}"
        if bonus in self.bonus_objects:
            self.bonus_objects.remove(bonus)
            self.game_area.remove_widget(bonus)

    def end_game(self):
        self.game_active = False
        Clock.unschedule(self.update_timer)
        Clock.unschedule(self.create_falling_bonus)
        Clock.unschedule(self.update)
        for bonus in self.bonus_objects[:]:
            self.game_area.remove_widget(bonus)
        self.bonus_objects.clear()
        self.show_game_over()

    def show_game_over(self):
        game_over_layout = BoxLayout(orientation="vertical", padding=20)
        game_over_label = Label(
            text=f"Game Over!\nFinal Score: {self.score}", font_size=36
        )
        game_over_layout.add_widget(game_over_label)

        restart_button = Button(
            text="Play Again",
            size_hint=(None, None),
            size=(200, 80),
            pos_hint={"center_x": 0.5},
            on_press=self.restart_game,
        )
        game_over_layout.add_widget(restart_button)

        menu_button = Button(
            text="Main Menu",
            size_hint=(None, None),
            size=(200, 80),
            pos_hint={"center_x": 0.5},
            on_press=self.go_to_menu,
        )
        game_over_layout.add_widget(menu_button)

        popup = Popup(
            title="Game Over",
            content=game_over_layout,
            size_hint=(0.8, 0.8),
            auto_dismiss=False,
        )
        popup.open()

    def restart_game(self, instance):
        self.manager.current = "countdown"

    def go_to_menu(self, instance):
        self.manager.current = "menu"

    def on_enter(self):
        if (
            hasattr(self.manager, "selected_character")
            and self.manager.selected_character
        ):
            if not self.player:
                self.player = Player(source=self.manager.selected_character["image"])
                self.game_area.add_widget(self.player)
            self.start_game()


class MyGameApp(App):
    def build(self):
        Window.size = (800, 600)
        sm = ScreenManager()
        sm.selected_character = None
        sm.add_widget(MainMenuScreen(name="menu"))
        sm.add_widget(CharacterSelectionScreen(name="character_selection"))
        sm.add_widget(CountdownScreen(name="countdown"))
        sm.add_widget(GameScreen(name="game_screen"))
        return sm



        return sm


# เริ่มแอป
if __name__ == "__main__":
    GameApp().run()
