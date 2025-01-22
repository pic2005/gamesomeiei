def on_enter(self):
        """เมื่อเข้าสู่หน้าจอเกม"""
        if hasattr(self.manager, "selected_character") and self.manager.selected_character:
            selected_character = self.manager.selected_character
            self.character_image.source = selected_character["image"]
            self.character_info.text = (
                f"Name: {selected_character['name']}\n"
                f"Bonus: {selected_character['bonus']}"
            )

            # สร้างตัวละครผู้เล่น
            if not self.player:
                self.player = Player(source=selected_character["image"])
                self.game_area.add_widget(self.player)

    def collect_bonus(self, bonus):
        """เก็บโบนัสและเพิ่มคะแนน"""
        self.score += bonus.points
        self.score_label.text = f"Score: {self.score}"
        # ลบโบนัส
        if bonus in self.bonus_objects:
            self.bonus_objects.remove(bonus)
            self.game_area.remove_widget(bonus)