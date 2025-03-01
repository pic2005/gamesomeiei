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


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # Background image with stretching and keeping ratio
        background = Image(
            source=r"C:\Users\Acer\Downloads\ฟ้า.jpg",
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

        # เพิ่มชื่อเกม
        game_title = Label(
            text="Khud Kat Game",  # ชื่อเกม
            font_size=48,  # ขนาดฟอนต์
            color=(1, 1, 1, 1),  # สีขาว
            size_hint=(None, None),
            size=(400, 100),  # ขนาด Label
            pos_hint={"center_x": 0.5, "top": 0.95},  # ตำแหน่งด้านบนกลาง
            bold=True,  # ตัวหนา
        )
        layout.add_widget(game_title)

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

        # ตัวแปรสำหรับเก็บของที่หล่นลงมา
        self.falling_objects = []

        # สร้างของที่หล่นลงมาเป็นระยะ
        Clock.schedule_interval(self.spawn_falling_object, 1)

        # อัพเดทของที่หล่นลงมาทุกเฟรม
        Clock.schedule_interval(self.update_falling_objects, 1.0 / 60.0)

        # เพิ่มข้อความที่ปรากฏและหายไป
        self.floating_labels = []
        self.add_floating_labels(layout)

        self.add_widget(layout)

    def add_floating_labels(self, layout):
        # ข้อความที่ต้องการแสดง
        messages = [
            "Welcome!",
            "Help Khud Kat!",
            "Hungry!",
        ]

        # สร้าง Label สำหรับข้อความแต่ละอัน
        for i, message in enumerate(messages):
            label = Label(
                text=message,
                font_size=24,
                color=(0, 0, 0, 1),  # สีขาว
                size_hint=(None, None),
                size=(300, 50),
                pos_hint={
                    "center_x": random.uniform(0.2, 0.8),
                    "center_y": random.uniform(0.3, 0.8),
                },
                opacity=0,  # เริ่มต้นด้วยการซ่อนข้อความ
            )
            layout.add_widget(label)
            self.floating_labels.append(label)

        # เริ่มแอนิเมชันข้อความ
        Clock.schedule_interval(self.update_floating_labels, 2.0 / 60.0)

    def update_floating_labels(self, dt):
        # อัพเดทข้อความที่ปรากฏและหายไป
        for label in self.floating_labels:
            # สุ่มตำแหน่งใหม่
            if random.random() < 0.01:  # ความน่าจะเป็นที่ข้อความจะเคลื่อนที่
                label.pos_hint = {
                    "center_x": random.uniform(0.2, 0.8),
                    "center_y": random.uniform(0.3, 0.8),
                }

            # สุ่มความโปร่งใส (opacity)
            if random.random() < 0.02:  # ความน่าจะเป็นที่ข้อความจะปรากฏหรือหายไป
                label.opacity = 1 if label.opacity == 0 else 0

    def spawn_falling_object(self, dt):
        # สุ่มตำแหน่งเริ่มต้นบนแกน X
        x = random.randint(0, int(Window.width - 50))
        y = Window.height  # เริ่มจากด้านบนของหน้าจอ

        # สุ่มเลือกรูปภาพของที่หล่นลงมา
        source = random.choice(
            [
                "images/มังคุด3.png",
                "images/ก้อนเมฆ.png",
            ]
        )

        # สร้างของที่หล่นลงมา
        obj = FallingObject(
            pos=(x, y),
            size=(70, 70),  # ขนาดของของที่หล่นลงมา
            source=source,
            score_change=0,  # ไม่นับคะแนน
        )

        # วาดของที่หล่นลงมาด้วย canvas
        with self.canvas:
            obj.rect = Rectangle(source=obj.source, pos=obj.pos, size=obj.size)

        # เพิ่มของที่หล่นลงมาเข้าไปในลิสต์
        self.falling_objects.append(obj)

    def update_falling_objects(self, dt):
        for obj in self.falling_objects[:]:  # ใช้ [:] เพื่อป้องกันปัญหาในการลบของจากลิสต์
            # เคลื่อนที่ของที่หล่นลงมา
            obj.pos = (obj.pos[0], obj.pos[1] - obj.speed * dt)
            obj.rect.pos = obj.pos

            # ลบของที่หล่นลงมาหากตกออกจากหน้าจอ
            if obj.pos[1] + obj.size[1] < 0:
                self.canvas.remove(obj.rect)
                self.falling_objects.remove(obj)

    def start_game(self, instance):
        # ไปที่หน้าแนะนำตัวละคร
        self.manager.current = "character_screen"


class CharacterSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # Background image with stretching and keeping ratio
        background = Image(
            source=r"C:\Users\Acer\Downloads\ฟ้า.jpg",
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

        # Game description label with a border
        game_description = Label(
            text="Hello, my name is Khud Kat.\nMy name comes from mangosteen.\nPlease help me collect a lot of fallen mangosteen,\nand I will be able to go home.",
            font_size=20,
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            size=(500, 100),
            pos_hint={"center_x": 0.5, "center_y": 0.3},
            halign="center",
            valign="middle",
        )

        # Create a canvas to draw a border around the label
        with game_description.canvas.before:
            self.border = Rectangle(
                pos=game_description.pos,
                size=game_description.size,
            )

        # Bind the border to the label's position and size
        game_description.bind(pos=self.update_border, size=self.update_border)

        layout.add_widget(game_description)

        # GO button
        go_button = Button(
            text="GO",
            font_size=24,
            size_hint=(None, None),
            size=(200, 100),
            pos_hint={"center_x": 0.5, "center_y": 0.1},
            background_color=(0.8, 0.4, 0.4, 1),
        )
        go_button.bind(on_press=self.go_to_game)
        layout.add_widget(go_button)

        # Back to main screen button
        back_to_main_button = Button(
            text="Back",
            font_size=20,
            size_hint=(None, None),
            size=(100, 50),
            pos_hint={"x": 0.02, "top": 0.1},
            background_color=(0.5, 0.5, 0.5, 1),
        )
        back_to_main_button.bind(on_press=self.back_to_main)
        layout.add_widget(back_to_main_button)

        # ตัวแปรสำหรับเก็บของที่หล่นลงมา
        self.falling_objects = []

        # สร้างของที่หล่นลงมาเป็นระยะ
        Clock.schedule_interval(self.spawn_falling_object, 1)

        # อัพเดทของที่หล่นลงมาทุกเฟรม
        Clock.schedule_interval(self.update_falling_objects, 1.0 / 60.0)

        # เพิ่มข้อความที่ปรากฏและหายไป
        self.floating_labels = []
        self.add_floating_labels(layout)

        self.add_widget(layout)

    def update_border(self, instance, value):
        # Update the border's position and size when the label moves or resizes
        self.border.pos = instance.pos
        self.border.size = instance.size

    def add_floating_labels(self, layout):
        # ข้อความที่ต้องการแสดง
        messages = [
            "GO",
            "Help Khud Kat!",
            "Hungry!",
        ]

        # สร้าง Label สำหรับข้อความแต่ละอัน
        for i, message in enumerate(messages):
            label = Label(
                text=message,
                font_size=24,
                color=(0, 0, 0, 1),  # สีขาว
                size_hint=(None, None),
                size=(300, 50),
                pos_hint={
                    "center_x": random.uniform(0.2, 0.8),
                    "center_y": random.uniform(0.3, 0.8),
                },
                opacity=0,  # เริ่มต้นด้วยการซ่อนข้อความ
            )
            layout.add_widget(label)
            self.floating_labels.append(label)

        # เริ่มแอนิเมชันข้อความ
        Clock.schedule_interval(self.update_floating_labels, 2.0 / 60.0)

    def update_floating_labels(self, dt):
        # อัพเดทข้อความที่ปรากฏและหายไป
        for label in self.floating_labels:
            # สุ่มตำแหน่งใหม่
            if random.random() < 0.01:  # ความน่าจะเป็นที่ข้อความจะเคลื่อนที่
                label.pos_hint = {
                    "center_x": random.uniform(0.2, 0.8),
                    "center_y": random.uniform(0.3, 0.8),
                }

            # สุ่มความโปร่งใส (opacity)
            if random.random() < 0.02:  # ความน่าจะเป็นที่ข้อความจะปรากฏหรือหายไป
                label.opacity = 1 if label.opacity == 0 else 0

    def spawn_falling_object(self, dt):
        # สุ่มตำแหน่งเริ่มต้นบนแกน X
        x = random.randint(0, int(Window.width - 50))
        y = Window.height  # เริ่มจากด้านบนของหน้าจอ

        # สุ่มเลือกรูปภาพของที่หล่นลงมา
        source = random.choice(
            [
                "images/มังคุด3.png",
                "images/ก้อนเมฆ.png",
            ]
        )

        # สร้างของที่หล่นลงมา
        obj = FallingObject(
            pos=(x, y),
            size=(70, 70),  # ขนาดของของที่หล่นลงมา
            source=source,
            score_change=0,  # ไม่นับคะแนน
        )

        # วาดของที่หล่นลงมาด้วย canvas
        with self.canvas:
            obj.rect = Rectangle(source=obj.source, pos=obj.pos, size=obj.size)

        # เพิ่มของที่หล่นลงมาเข้าไปในลิสต์
        self.falling_objects.append(obj)

    def update_falling_objects(self, dt):
        for obj in self.falling_objects[:]:  # ใช้ [:] เพื่อป้องกันปัญหาในการลบของจากลิสต์
            # เคลื่อนที่ของที่หล่นลงมา
            obj.pos = (obj.pos[0], obj.pos[1] - obj.speed * dt)
            obj.rect.pos = obj.pos

            # ลบของที่หล่นลงมาหากตกออกจากหน้าจอ
            if obj.pos[1] + obj.size[1] < 0:
                self.canvas.remove(obj.rect)
                self.falling_objects.remove(obj)

    def go_to_game(self, instance):
        # ไปที่หน้าอธิบายเกม (Game Explanation Screen)
        self.manager.current = "game_explanation_screen"

    def back_to_main(self, instance):
        # กลับไปที่หน้าแรก
        self.manager.current = "main_screen"


class GameExplanationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # Background image
        background = Image(
            source=r"C:\Users\Acer\Downloads\ฟ้า.jpg",  # เปลี่ยนเป็น path ของภาพพื้นหลัง
            size_hint=(1, 1),
            allow_stretch=True,
            keep_ratio=False,
        )
        layout.add_widget(background)

        # Game explanation label
        explanation_label = Label(
            text="Game Rules:\n\n"
            "1. Help Khud Kat collect as many mangosteens as possible.\n"
            "2. Avoid bad fruits like lychee and rambutan.\n"
            "3. You have 30 seconds to collect as many points as you can.\n"
            "4. Use the 'A' and 'D' keys to move left and right.\n"
            "5. Good luck!",
            font_size=20,
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            size=(600, 300),
            pos_hint={"center_x": 0.5, "center_y": 0.6},
            halign="center",
            valign="middle",
        )
        layout.add_widget(explanation_label)

        # Next button (to go to the game screen)
        next_button = Button(
            text="Next",
            font_size=24,
            size_hint=(None, None),
            size=(200, 100),
            pos_hint={"center_x": 0.5, "center_y": 0.2},
            background_color=(0.8, 0.4, 0.4, 1),
        )
        next_button.bind(on_press=self.go_to_game)
        layout.add_widget(next_button)

        # Back button (to return to the character selection screen)
        back_button = Button(
            text="Back",
            font_size=20,
            size_hint=(None, None),
            size=(100, 50),
            pos_hint={"x": 0.02, "top": 0.1},
            background_color=(0.5, 0.5, 0.5, 1),
        )
        back_button.bind(on_press=self.back_to_character)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def go_to_game(self, instance):
        # ไปที่หน้าเกม (Game Screen)
        self.manager.current = "game_screen"

    def back_to_character(self, instance):
        # กลับไปที่หน้าอธิบายตัวละคร (Character Selection Screen)
        self.manager.current = "character_screen"


class GameExplanationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # Background image
        background = Image(
            source=r"C:\Users\Acer\Downloads\ฟ้า.jpg",  # เปลี่ยนเป็น path ของภาพพื้นหลัง
            size_hint=(1, 1),
            allow_stretch=True,
            keep_ratio=False,
        )
        layout.add_widget(background)

        # Game explanation label
        self.explanation_label = Label(
            text="Game Rules:\n\n"
            "1. Help Khud Kat collect as many mangosteens as possible.\n"
            "2. Avoid bad fruits like lychee and rambutan.\n"
            "3. You have 30 seconds to collect as many points as you can.\n"
            "4. Use the 'A' and 'D' keys to move left and right.\n"
            "5. Good luck!",
            font_size=20,
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            size=(600, 300),
            pos_hint={"center_x": 0.5, "center_y": 0.6},
            halign="center",
            valign="middle",
        )
        layout.add_widget(self.explanation_label)

        # Countdown label (ซ่อนไว้ในตอนแรก)
        self.countdown_label = Label(
            text="",
            font_size=100,
            color=(1, 0, 0, 1),  # สีแดง
            size_hint=(None, None),
            size=(200, 200),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            opacity=0,  # ซ่อนไว้ในตอนแรก
        )
        layout.add_widget(self.countdown_label)

        # Next button (to go to the game screen)
        self.next_button = Button(
            text="Next",
            font_size=24,
            size_hint=(None, None),
            size=(200, 100),
            pos_hint={"center_x": 0.5, "center_y": 0.2},
            background_color=(0.8, 0.4, 0.4, 1),
        )
        self.next_button.bind(on_press=self.start_countdown)  # เปลี่ยนเป็นเริ่มนับถอยหลัง
        layout.add_widget(self.next_button)

        # Back button (to return to the character selection screen)
        back_button = Button(
            text="Back",
            font_size=20,
            size_hint=(None, None),
            size=(100, 50),
            pos_hint={"x": 0.02, "top": 0.1},
            background_color=(0.5, 0.5, 0.5, 1),
        )
        back_button.bind(on_press=self.back_to_character)
        layout.add_widget(back_button)

        self.add_widget(layout)

        # ตัวแปรสำหรับนับถอยหลัง
        self.countdown_value = 3  # เริ่มนับจาก 3
        self.countdown_active = False  # สถานะการนับถอยหลัง

    def start_countdown(self, instance):
        # ซ่อนปุ่ม Next และข้อความอธิบายเกม
        self.next_button.opacity = 0
        self.explanation_label.opacity = 0

        # แสดง Label นับถอยหลัง
        self.countdown_label.opacity = 1
        self.countdown_label.text = str(self.countdown_value)

        # เริ่มนับถอยหลัง
        self.countdown_active = True
        Clock.schedule_interval(self.update_countdown, 0.5)  # อัพเดททุก 1 วินาที

    def update_countdown(self, dt):
        # อัพเดทการนับถอยหลัง
        if self.countdown_value > 0:
            self.countdown_label.text = str(self.countdown_value)
            self.countdown_value -= 1
        else:
            # เมื่อนับถอยหลังเสร็จสิ้น
            self.countdown_label.text = "GO!"
            Clock.schedule_once(self.go_to_game, 1)  # รอ 1 วินาทีแล้วเริ่มเกม

    def go_to_game(self, dt):
        # หยุดการนับถอยหลัง
        self.countdown_active = False
        Clock.unschedule(self.update_countdown)

        # ไปที่หน้าเกม (Game Screen)
        self.manager.current = "game_screen"

    def back_to_character(self, instance):
        # กลับไปที่หน้าอธิบายตัวละคร (Character Selection Screen)
        self.manager.current = "character_screen"


class FallingObject:
    def __init__(self, pos, size, source, score_change):
        self.pos = pos
        self.size = size
        self.source = source
        self.speed = random.randint(100, 300)  # ความเร็วในการตก
        self.score_change = score_change  # ผลต่อคะแนน (+10, -10, หรือ -20)


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
        self.hero_size = (200, 150)

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
        self.is_paused = False  # สถานะหยุดเกมหรือไม่

        # สร้างของที่หล่นลงมาเป็นระยะ
        Clock.schedule_interval(self.spawn_falling_object, 1)

        # อัพเดทของที่หล่นลงมาทุกเฟรม
        Clock.schedule_interval(self.update_falling_objects, 1.0 / 60.0)

        # อัพเดทเวลา
        Clock.schedule_interval(self.update_time, 1)

        # Back to character selection screen button
        back_to_character_button = Button(
            text="Back",
            font_size=20,
            size_hint=(None, None),
            size=(100, 50),
            pos_hint={"x": 0.02, "top": 0.1},
            background_color=(0.5, 0.5, 0.5, 1),
        )
        back_to_character_button.bind(on_press=self.back_to_character)
        self.layout.add_widget(back_to_character_button)

        # Pause/Resume button (อยู่ด้านขวา)
        self.pause_button = Button(
            text="Pause",
            font_size=20,
            size_hint=(None, None),
            size=(100, 50),
            pos_hint={"right": 0.98, "top": 0.1},  # ปรับตำแหน่งไปด้านขวา
            background_color=(0.5, 0.5, 0.5, 1),
        )
        self.pause_button.bind(on_press=self.toggle_pause)
        self.layout.add_widget(self.pause_button)

        # Game Over label
        self.game_over_label = Label(
            text="",
            font_size=40,
            color=(1, 0, 0, 1),
            size_hint=(None, None),
            size=(600, 200),
            pos_hint={"center_x": 0.5, "center_y": 0.7},
            halign="center",
            valign="middle",
            opacity=0,  # ซ่อนไว้ในตอนแรก
        )
        self.layout.add_widget(self.game_over_label)

        # Play Again button
        self.play_again_button = Button(
            text="Play Again",
            font_size=24,
            size_hint=(None, None),
            size=(200, 100),
            pos_hint={"center_x": 0.5, "center_y": 0.4},
            background_color=(0.5, 0.5, 0.5, 1),
            opacity=0,  # ซ่อนไว้ในตอนแรก
        )
        self.play_again_button.bind(on_press=self.play_again)
        self.layout.add_widget(self.play_again_button)

        # Back to Main button
        self.back_to_main_button = Button(
            text="Back to Main",
            font_size=24,
            size_hint=(None, None),
            size=(200, 100),
            pos_hint={"center_x": 0.5, "center_y": 0.2},
            background_color=(0.5, 0.5, 0.5, 1),
            opacity=0,  # ซ่อนไว้ในตอนแรก
        )
        self.back_to_main_button.bind(on_press=self.back_to_main)
        self.layout.add_widget(self.back_to_main_button)

    def toggle_pause(self, instance):
        # สลับสถานะหยุดเกม
        self.is_paused = not self.is_paused

        if self.is_paused:
            self.pause_button.text = "Resume"  # เปลี่ยนข้อความปุ่มเป็น "Resume"
            self.pause_game()  # หยุดเกม
        else:
            self.pause_button.text = "Pause"  # เปลี่ยนข้อความปุ่มเป็น "Pause"
            self.resume_game()  # เล่นต่อ

    def pause_game(self):
        # หยุดเวลาและหยุดการเคลื่อนที่ของวัตถุ
        self.game_over = True  # หยุดเกมชั่วคราว

    def resume_game(self):
        # เล่นต่อเวลาและการเคลื่อนที่ของวัตถุ
        self.game_over = False  # เล่นต่อเกม

    def back_to_character(self, instance):
        # กลับไปที่หน้าเลือกตัวละคร
        self.manager.current = "character_screen"

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard.unbind(on_key_up=self._on_key_up)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        if not self.is_paused:  # ตรวจสอบว่าเกมไม่หยุด
            self.pressed_keys.add(text)

    def _on_key_up(self, keyboard, keycode):
        text = keycode[1]
        if text in self.pressed_keys:
            self.pressed_keys.remove(text)

    def move_step(self, dt):
        if self.game_over or self.is_paused:
            return  # หยุดเคลื่อนที่หากเกมจบหรือหยุดชั่วคราว

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
        if self.game_over or self.is_paused:
            return  # หยุดสร้างของที่หล่นลงมาหากเกมจบหรือหยุดชั่วคราว

        # สุ่มตำแหน่งเริ่มต้นบนแกน X
        x = random.randint(0, int(Window.width - 50))
        y = Window.height  # เริ่มจากด้านบนของหน้าจอ

        random_value = random.random()
        if random_value < 0.4:  # 40% โอกาสเป็นโบนัส (มังคุด)
            # สุ่มเลือกรูปโบนัส (มังคุด1, มังคุด2, มังคุด3)
            bonus_type = random.choice(["มังคุด1", "มังคุด2", "มังคุด3"])
            if bonus_type == "มังคุด1":
                source = "images/มังคุด1.png"
                score_change = 10  # เพิ่มคะแนน
            elif bonus_type == "มังคุด2":
                source = "images/มังคุด2.png"
                score_change = 15  # เพิ่มคะแนน
            elif bonus_type == "มังคุด3":
                source = "images/มังคุด3.png"
                score_change = 20  # เพิ่มคะแนน
        elif random_value < 0.6:  # 20% โอกาสเป็นของที่ไม่ดี (ลำไย)
            source = "images/ลำไย.png"
            score_change = -10  # ลดคะแนน
        elif random_value < 0.7:  # 10% โอกาสเป็นของที่ไม่ดี (เงาะ)
            source = "images/เงาะ.png"
            score_change = -15  # ลดคะแนน
        elif random_value < 0.8:  # 10% โอกาสเป็นของที่ไม่ดี (มะม่วง)
            source = "images/สัปปะรด.png"
            score_change = -20  # ลดคะแนน
        else:  # 20% โอกาสเป็นของที่ไม่ดีอีกชนิด (มะม่วง2)
            source = "images/มะม่วง.png"  # เพิ่มของลบคะแนนใหม่
            score_change = -25  # ลดคะแนนเพิ่มเติม

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
        if self.game_over or self.is_paused:
            return  # หยุดอัพเดทของที่หล่นลงมาหากเกมจบหรือหยุดชั่วคราว

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
        if self.game_over or self.is_paused:
            return  # หยุดนับเวลาหากเกมจบหรือหยุดชั่วคราว

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
        self.game_over_label.text = f"Game Over!\nYour Score: {self.score}"
        self.game_over_label.opacity = 1  # แสดงข้อความ Game Over

        # แสดงปุ่ม Play Again และ Back to Main
        self.play_again_button.opacity = 1
        self.back_to_main_button.opacity = 1

    def play_again(self, instance):
        # รีเซ็ตเกมและเริ่มเล่นใหม่
        self.game_over = False
        self.time_elapsed = 0
        self.score = 0
        self.score_label.text = f"Score: {self.score}"
        self.time_label.text = "Time: 30:00"
        self.game_over_label.opacity = 0
        self.play_again_button.opacity = 0
        self.back_to_main_button.opacity = 0

        # ลบของที่หล่นลงมาทั้งหมด
        for obj in self.falling_objects:
            self.layout.canvas.remove(obj.rect)
        self.falling_objects.clear()

        # เริ่มเวลาใหม่
        Clock.schedule_interval(self.spawn_falling_object, 1)
        Clock.schedule_interval(self.update_falling_objects, 1.0 / 60.0)
        Clock.schedule_interval(self.update_time, 1)

    def back_to_main(self, instance):
        # กลับไปที่หน้าหลัก
        self.manager.current = "main_screen"


class GameApp(App):
    def build(self):
        # ตั้งค่าขนาดหน้าจอเริ่มต้น
        Window.size = (800, 600)

        sm = ScreenManager()

        # เพิ่มหน้าจอต่าง ๆ
        main_screen = MainScreen(name="main_screen")
        sm.add_widget(main_screen)

        character_screen = CharacterSelectionScreen(name="character_screen")
        sm.add_widget(character_screen)

        game_explanation_screen = GameExplanationScreen(name="game_explanation_screen")
        sm.add_widget(game_explanation_screen)

        game_screen = GameScreen(name="game_screen")
        sm.add_widget(game_screen)

        # เริ่มต้นที่หน้าแรก
        sm.current = "main_screen"

        return sm


if __name__ == "__main__":
    GameApp().run()
