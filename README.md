โปรแกรมเกมส์เก็บผลไม้ "Khud Kat" เป็นเกมส์ที่ผู้เล่นต้องช่วยตัวละครหลัก Khud Kat เก็บผลไม้ที่หล่นจากฟ้าให้ได้มากที่สุดภายในเวลาที่กำหนด โดยต้องหลบเลี่ยงผลไม้ที่ไม่ดีที่ทำให้คะแนนลดลง เกมนี้พัฒนาด้วยภาษา Python และใช้เฟรมเวิร์ก Kivy สำหรับสร้าง GUI
โปรแกรมประกอบด้วยหน้าจอหลัก 4 หน้าจอ:
1.หน้าจอหลัก (Main Screen): แสดงชื่อเกมส์, ปุ่มเริ่มเกมส์, และตัวละครหลัก
2.หน้าจอเลือกตัวละคร (Character Selection Screen): แสดงข้อมูลตัวละครและปุ่มเริ่มเกมส์
3.หน้าจออธิบายเกมส์ (Game Explanation Screen): แสดงกฎกติกาและวิธีการเล่น
4.หน้าจอเกมส์ (Game Screen): หน้าจอหลักสำหรับเล่นเกมส์

การทำงานของโปรแกรม
1. หน้าจอหลัก (Main Screen)
แสดงชื่อเกมส์ "Khud Kat Game" และปุ่ม "START"
มีภาพพื้นหลังและตัวละครหลัก (ช้าง)
เมื่อกดปุ่ม "START" จะเข้าสู่หน้าจอเลือกตัวละคร

2. หน้าจอเลือกตัวละคร (Character Selection Screen)
แสดงข้อมูลตัวละครและปุ่ม "GO" เพื่อเริ่มเกมส์
มีปุ่ม "Back" เพื่อกลับไปที่หน้าจอหลัก
เมื่อกดปุ่ม "GO" จะเข้าสู่หน้าจออธิบายเกมส์

3. หน้าจออธิบายเกมส์ (Game Explanation Screen)
แสดงกฎกติกาและวิธีการเล่น
มีปุ่ม "Next" เพื่อเริ่มเกมส์ และปุ่ม "Back" เพื่อกลับไปที่หน้าจอเลือกตัวละคร
เมื่อกดปุ่ม "Next" จะเริ่มนับถอยหลังและเข้าสู่หน้าจอเกมส์

4. หน้าจอเกมส์ (Game Screen)
ผู้เล่นควบคุมตัวละครด้วยปุ่ม "A" (ซ้าย) และ "D" (ขวา)

ผลไม้และวัตถุต่าง ๆ จะหล่นจากฟ้า ผู้เล่นต้องเก็บผลไม้ที่ดี  มังคุด (เพิ่มคะแนน) และหลบผลไม้ที่ไม่ดี ผลไม้ที่ไม่ใช้มังคุด (ลดคะแนน)
มีการแสดงคะแนนและเวลาที่เหลือบนหน้าจอ
เมื่อเวลาเหลือ 0 เกมส์จะจบและแสดงผลลัพธ์