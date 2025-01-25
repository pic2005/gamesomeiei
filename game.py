from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Rectangle
import random


class FallingObject:
    def __init__(self, pos, size, source, score_change):
        self.pos = pos
        self.size = size
        self.source = source
        self.speed = random.randint(100, 300)  # ความเร็วในการตก
        self.score_change = score_change  # ผลต่อคะแนน (+10, -10, หรือ -20)


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # Background image with stretching and keeping ratio
        background = Image(
            source=r"C:\Users\Acer\Downloads\พล.jpg",
            size_hint=(1, 1),  # ขยายให้เต็มหน้าจอ
            allow_stretch=True,  # อนุญาตให้ขยายภาพ
            keep_ratio=False,  # ไม่รักษาสัดส่วนภาพ
        )
        layout.add_widget(background)

        # Start button
        start_button = Button(
            text="START",
            font_size=24,
            size_hint=(None, None),
            size=(200, 100),
            pos_hint={"center_x": 0.5, "center_y": 0.2},
            background_normal="",
            background_color=(1, 0.84, 0, 1),
            border=(20, 20, 20, 20),
            color=(0, 0, 0, 1),
        )
        start_button.bind(on_press=self.start_game)
        layout.add_widget(start_button)

        self.add_widget(layout)

    def start_game(self, instance):
        # ไปที่หน้าแนะนำตัวละคร
        self.manager.current = "character_screen"


class CharacterSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # Background image with stretching and keeping ratio
        background = Image(
            source=r"C:\Users\Acer\Downloads\พื้นหลัง23.jpg",
            size_hint=(1, 1),  # ขยายให้เต็มหน้าจอ
            allow_stretch=True,  # อนุญาตให้ขยายภาพ
            keep_ratio=False,  # ไม่รักษาสัดส่วนภาพ
        )
        layout.add_widget(background)

        # Character image
        self.character = Image(
            source=r"C:\Users\Acer\Downloads\ช้าง.png",
            size_hint=(None, None),
            size=(1000, 1000),
            pos_hint={"center_x": 0.5, "center_y": 0.6},
        )
        layout.add_widget(self.character)

        # Game description label
        game_description = Label(
            text="Hello, my name is Khud Kat.\nMy name comes from mangosteen.\nPlease help me collect a lot of fallen mangosteen,\nand I will be able to go home.",
            font_size=20,
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            size=(600, 200),
            pos_hint={"center_x": 0.5, "center_y": 0.3},
            halign="center",
            valign="middle",
        )
        layout.add_widget(game_description)

        # Back button
        back_button = Button(
            text="GO",
            font_size=24,
            size_hint=(None, None),
            size=(200, 100),
            pos_hint={"center_x": 0.5, "center_y": 0.1},
            background_color=(0.8, 0.4, 0.4, 1),
        )
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def go_back(self, instance):
        # ไปที่หน้าควบคุมตัวละคร
        self.manager.current = "game_screen"


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)
        self.pressed_keys = set()
        Clock.schedule_interval(self.move_step, 0)

        # กำหนดตำแหน่งเริ่มต้นที่ด้านล่างของหน้าจอ
        initial_x = 0
        initial_y = 0  # ด้านล่างของหน้าจอ
        self.layout = FloatLayout()
        self.add_widget(self.layout)  # เพิ่ม layout เข้าไปในหน้าจอ

        # Background image with stretching and keeping ratio
        background = Image(
            source=r"images\พื้นหลัง2.jpg",
            size_hint=(1, 1),  # ขยายให้เต็มหน้าจอ
            allow_stretch=True,  # อนุญาตให้ขยายภาพ
            keep_ratio=False,  # ไม่รักษาสัดส่วนภาพ
        )
        self.layout.add_widget(background)

        # กำหนดขนาดตัวละคร
        self.hero_size = (300, 250)

        # วาดตัวละครด้วย canvas ของ FloatLayout
        with self.layout.canvas:
            self.hero = Rectangle(
                source="images/ช้าง.png", pos=(initial_x, initial_y), size=self.hero_size
            )

        # ตัวแปรสำหรับเก็บของที่หล่นลงมา
        self.falling_objects = []
        self.score = 0

        # Label สำหรับแสดงคะแนน
        self.score_label = Label(
            text=f"Score: {self.score}",
            font_size=24,
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={"top": 1, "right": 1},
            color=(1, 1, 1, 1),
        )
        self.layout.add_widget(self.score_label)

        # Label สำหรับแสดงเวลา
        self.time_label = Label(
            text="Time: 30:00",
            font_size=24,
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={"top": 1, "left": 1},
            color=(1, 1, 1, 1),
        )
        self.layout.add_widget(self.time_label)

        # ตัวแปรสำหรับเวลา
        self.time_elapsed = 0  # เวลาที่ผ่านไป
        self.game_duration = 30  # ระยะเวลาเกม (วินาที)
        self.game_over = False  # สถานะเกมจบหรือไม่

        # สร้างของที่หล่นลงมาเป็นระยะ
        Clock.schedule_interval(self.spawn_falling_object, 1)

        # อัพเดทของที่หล่นลงมาทุกเฟรม
        Clock.schedule_interval(self.update_falling_objects, 1.0 / 60.0)

        # อัพเดทเวลา
        Clock.schedule_interval(self.update_time, 1)

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard.unbind(on_key_up=self._on_key_up)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        print("down", text)
        self.pressed_keys.add(text)

    def _on_key_up(self, keyboard, keycode):
        text = keycode[1]
        print("up", text)
        if text in self.pressed_keys:
            self.pressed_keys.remove(text)

    def move_step(self, dt):
        if self.game_over:
            return  # หยุดเคลื่อนที่หากเกมจบ

        cur_x = self.hero.pos[0]
        step = 300 * dt  # ความเร็วการเคลื่อนที่

        # เคลื่อนที่เฉพาะซ้ายและขวา
        if "a" in self.pressed_keys:
            cur_x -= step
        if "d" in self.pressed_keys:
            cur_x += step

        # จำกัดขอบเขตการเคลื่อนที่ของตัวละคร (ไม่ให้ออกนอกหน้าจอ)
        if cur_x < 0:
            cur_x = 0
        elif cur_x + self.hero_size[0] > Window.width:
            cur_x = Window.width - self.hero_size[0]

        # อัพเดทตำแหน่งตัวละคร
        self.hero.pos = (cur_x, self.hero.pos[1])

    def spawn_falling_object(self, dt):
        if self.game_over:
            return  # หยุดสร้างของที่หล่นลงมาหากเกมจบ

        # สุ่มตำแหน่งเริ่มต้นบนแกน X
        x = random.randint(0, int(Window.width - 50))
        y = Window.height  # เริ่มจากด้านบนของหน้าจอ

        # สุ่มเลือกประเภทของที่หล่นลงมา (โบนัสหรือของที่ไม่ดี)
        random_value = random.random()
        if random_value < 0.4:  # 40% โอกาสเป็นโบนัส
            if random.random() < 0.5:  # 50% โอกาสเลือกรูปภาพมังคุด1 หรือมังคุด2
                source = "images/มังคุด1.png"
                score_change = 10  # เพิ่มคะแนน
            else:
                source = "images/มังคุด2.png"
                score_change = 15  # เพิ่มคะแนน
        elif random_value < 0.7:  # 30% โอกาสเป็นของที่ไม่ดี (ลดคะแนน -10)
            source = "images/ลำไย.png"
            score_change = -10  # ลดคะแนน
        else:  # 30% โอกาสเป็นของที่ไม่ดีอีกชนิด (ลดคะแนน -20)
            source = "images/เงาะ.png"
            score_change = -20  # ลดคะแนนเพิ่มเติม

        # สร้างของที่หล่นลงมา
        obj = FallingObject(
            pos=(x, y),
            size=(70, 70),  # ขนาดของของที่หล่นลงมา
            source=source,
            score_change=score_change,
        )

        # วาดของที่หล่นลงมาด้วย canvas
        with self.layout.canvas:
            obj.rect = Rectangle(source=obj.source, pos=obj.pos, size=obj.size)

        # เพิ่มของที่หล่นลงมาเข้าไปในลิสต์
        self.falling_objects.append(obj)

    def update_falling_objects(self, dt):
        if self.game_over:
            return  # หยุดอัพเดทของที่หล่นลงมาหากเกมจบ

        for obj in self.falling_objects[:]:  # ใช้ [:] เพื่อป้องกันปัญหาในการลบของจากลิสต์
            # เคลื่อนที่ของที่หล่นลงมา
            obj.pos = (obj.pos[0], obj.pos[1] - obj.speed * dt)
            obj.rect.pos = obj.pos

            # ตรวจสอบการชนกันระหว่างตัวละครและของที่หล่นลงมา
            if self.check_collision(self.hero, obj):
                self.score += obj.score_change  # ปรับคะแนน
                self.score_label.text = f"Score: {self.score}"  # อัพเดทคะแนน
                self.layout.canvas.remove(obj.rect)  # ลบของที่หล่นลงมาออกจาก canvas
                self.falling_objects.remove(obj)  # ลบของที่หล่นลงมาออกจากลิสต์

            # ลบของที่หล่นลงมาหากตกออกจากหน้าจอ
            if obj.pos[1] + obj.size[1] < 0:
                self.layout.canvas.remove(obj.rect)
                self.falling_objects.remove(obj)

    def check_collision(self, hero, obj):
        # ตรวจสอบว่าตัวละครและของที่หล่นลงมาซ้อนทับกันหรือไม่
        hero_x, hero_y = hero.pos
        hero_width, hero_height = hero.size
        obj_x, obj_y = obj.pos
        obj_width, obj_height = obj.size

        if (
            hero_x < obj_x + obj_width
            and hero_x + hero_width > obj_x
            and hero_y < obj_y + obj_height
            and hero_y + hero_height > obj_y
        ):
            return True
        return False

    def update_time(self, dt):
        if self.game_over:
            return  # หยุดนับเวลาหากเกมจบ

        self.time_elapsed += dt  # เพิ่มเวลาที่ผ่านไป
        time_left = max(
            0, self.game_duration - int(self.time_elapsed)
        )  # คำนวณเวลาที่เหลือ
        minutes = time_left // 60  # คำนวณนาที
        seconds = time_left % 60  # คำนวณวินาที

        # แสดงเวลาที่เหลือในรูปแบบ MM:SS
        self.time_label.text = f"Time: {minutes:02}:{seconds:02}"

        if time_left <= 0:  # ตรวจสอบว่าเวลาเกิน 30 วินาทีหรือไม่
            self.game_over = True  # ตั้งค่าสถานะเกมจบ
            self.show_game_over()  # แสดงผลลัพธ์

    def show_game_over(self):
        # แสดงผลลัพธ์เมื่อเกมจบ
        game_over_label = Label(
            text=f"Game Over!\nYour Score: {self.score}",
            font_size=40,
            color=(1, 0, 0, 1),
            size_hint=(None, None),
            size=(600, 200),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            halign="center",
            valign="middle",
        )
        self.layout.add_widget(game_over_label)


class GameApp(App):
    def build(self):
        # ตั้งค่าขนาดหน้าจอเริ่มต้น
        Window.size = (800, 600)  # ตัวอย่างขนาด 800x600 พิกเซล

        sm = ScreenManager()

        # เพิ่มหน้าแรก, หน้าแนะนำตัวละคร, และหน้าควบคุมตัวละคร
        main_screen = MainScreen(name="main_screen")
        sm.add_widget(main_screen)

        character_screen = CharacterSelectionScreen(name="character_screen")
        sm.add_widget(character_screen)

        game_screen = GameScreen(name="game_screen")
        sm.add_widget(game_screen)

        # เริ่มต้นที่หน้าแรก
        sm.current = "main_screen"

        return sm


if __name__ == "__main__":
    GameApp().run()
