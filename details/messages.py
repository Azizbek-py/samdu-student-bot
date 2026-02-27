# Main messages

main_menu_mes = """
🏠 <b>Asosiy menyu</b>
"""

statistics_mes = """
<b>{}</b>📊

👥 <b>Talabalar:</b> {}<i>ta</i>
👨‍🏫 <b>Domlalar:</b> {}<i>ta</i>
📚 <b>Topshiriqlar:</b> {}<i>ta</i>
📤 <b>Yuklangan natijalar:</b> {}<i>ta</i>

🗓 <b>Ishga tushirilgan:</b> {}
👨‍💻 <b>Developer:</b> {}
"""



# Teacher messages

rate_list_mes = """
━━━━━━━━━━━━━━━━━━
<b>🎓{}{}-guruh:</b>


"""

rate_list_mes2 ="""<b>
            
━━━━━━━━━━━━━━━━━━
📄 {}/{}

🤖 {}</b>
"""

in_optimize_mes = """
<b>Bu bo'lim optimallashtirilmoqda</b><i>(Soon)</i>...
"""

teacher_start_mes = """
━━━━━━━━━━━━━━━━━━
👨‍🏫 <b>O‘qituvchi paneli</b>

Siz tizimda <b>O‘qituvchi</b> sifatida ro‘yxatdan o‘tgansiz.

👤 <b>Ism-Familiya:</b> {}
🆔 <b>ID:</b> {}
📚 <b>Biriktirilgan fan:</b> {}

━━━━━━━━━━━━━━━━━━
⚠️ Ma'lumotlarda xatolik bo‘lsa,
tizim admini bilan bog‘laning:
@BroAZIK 🧑🏻‍💻
"""


no_teachers_tasks_mes = "Siz hali topshiriq joylamagansiz!"

choose_course_mes = "Kursni tanlang:"

choose_group_mes = "{}-kurs uchun guruhni tanlang:"

send_assignment_mes = "{}-kurs, 1{}-guruh uchun topshiriqni .pdf yoki .docx ko'rinishida jo'nating🖇: "

not_uploading_file_mes = "Iltimos, topshiriqni .pdf yoki .docx formatda yuboring🖇:"



teacher_tasks_mes = """
━━━━━━━━━━━━━━━━━━
📝 <b>{}</b>

🎓 <b>{}{}-guruh</b>

👥 Bajargan talabalar: <b>{} ta</b>

━━━━━━━━━━━━━━━━━━
📄 <b>{}/{}</b>

🤖 {}
"""


teach_tasks_page_mes = """
📌 <b>Topshiriq boshqaruvi</b>

Topshiriq ustida bajariladigan amallarni tanlang:
"""


teach_uploads_mes = """
━━━━━━━━━━━━━━━━━━
📊 <b>{} | {}-guruh</b>

🎯 <b>Baho:</b> {}

📚 <b>{}</b>

👤 <b>{} {}</b>
📞 {}
━━━━━━━━━━━━━━━━━━
📄 <b>{}/{}</b>

🤖 {}
"""


get_rate_mes = """
🎯 <b>Baho kiriting</b>

Ushbu yuklanmaga qo‘yiladigan bahoni kiriting.
"""


invalid_rate_mes = """
❌ Iltimos, bahoni butun son ko‘rinishida kiriting.
"""


# Admin messages

get_next_subject_mes = "Qo'shimcha fanni kiriting: "

subject_added_mes = "Domlaga {} fani qo'shildi"

ADMIN_welcome_mes = "Siz tizim Adminisiz!"

get_teacher_id_mes = "Iltimos, o'qituvchining ID raqamini yuboring:"

get_teacher_name_mes = "O'qituvchining to'liq ism familyasini kiriting:"

get_subject_name_mes = "O'qituvchiga aloqador fan nomini kiriting:"

get_teacher_id_delete_mes = "O'chirmoqchi bo'lgan o'qituvchining ID raqamini kiriting:"

deleted_teacher_mes = "O'qituvchi muvaffaqiyatli o'chirildi!"

teacher_added_mes = """
O'qituvchi muvaffaqiyatli qo'shildi!

Ism-Familyasi: {}
ID: {}
Fan nomi: {}


"""

Teacher_list_mes = """
No:{}/{}
{} domla

id: {}
Fani: {}

------------------------
"""


# Student messages

GET_login_mes = """
🔐 <b>Tizimga kirish</b>

Iltimos, universitet login raqamingizni yuboring:
"""

GET_password_mes = """
🔑 <b>Parolni kiriting</b>

Parolingiz maxfiy saqlanadi.
Iltimos, parolingizni yuboring:
"""

login_error_mes = """
❌ <b>Xatolik!</b>

Login yoki parol noto‘g‘ri.

Iltimos, login raqamingizni qaytadan yuboring:
"""

USER_welcome_mes = """
🎓 Salom, {first_name}!

Ta'lim botiga xush kelibsiz 🚀

📖 Bu yerda siz:
• Topshiriqlarni ko‘rishingiz
• Baholaringizni tekshirishingiz
• Kurslar bilan ishlashingiz mumkin

👇 Boshlash uchun menyuni tanlang.
"""

attendance_item_mes = """
📚 <b>{subject}</b>
🗂 Turi: {type}
👨‍🏫 {teacher}
📅 {date}
⏰ {time}
📊 Davomat: {count}

"""

no_attendance_mes = """
📭 Sizda davomat ma'lumotlari topilmadi.
"""


Student_tasks_view_mes = """
━━━━━━━━━━━━━━━━━━
📚 <b>{}</b>

📝 <i>{}</i>

👨‍🏫 Domla: <b>{}</b>

📌 Topshiriq: <b>{}/{}</b>
━━━━━━━━━━━━━━━━━━
🤖 {}
"""


no_students_tasks = "{} fani bo'yicha hali topshiriq joylanmagan!"

not_uploaded_mes = """
📎 <b>Fayl yuklang</b>

Iltimos, topshiriq faylini yuboring.

Ruxsat etilgan formatlar:
• .docx
• .pdf
"""


succesfully_upload_mes = """
Sizning {} fanidan faylingiz muvaffaqiyatli joylandi.
"""

upload_view_mes = """
━━━━━━━━━━━━━━━━━━
📚 <b>{}</b>

📎 <i>Joylagan faylingiz qabul qilindi.</i>

🎯 <b>Baho:</b> {}

━━━━━━━━━━━━━━━━━━
🤖 {}
"""


succesfully_deleted_mes = """
Faylingiz muvaffaqiyatli o'chirildi, fanlar bo'limidasiz!
"""

you_have_rate_mes = """
✅ <b>Baholandi!</b>

📚 Fan: <b>{}</b>
🎯 Baho: <b>{}</b>

Tabriklaymiz! 🎉
"""


student_profile_mes = """
<b>👤 TALABA PROFILI</b>

<b>📛 F.I.Sh:</b> {}
<b>🆔 Talaba ID:</b> {}

<b>🎓 Universitet:</b> {}
<b>🏛 Fakultet:</b> {} 
<b>📚 Yo‘nalish:</b> {} 
<b>📖 Ta’lim turi:</b> {}  
<b>🕘 Ta’lim shakli:</b> {}  
<b>💳 To‘lov turi:</b> {}  

<b>👥 Guruh:</b> {}  
<b>📈 Kurs:</b> {}  
<b>🗓 Semestr:</b> {} 

<b>📊 O‘rtacha GPA:</b> {} 
<b>📌 Holati:</b> {} 

<b>📍 Manzil:</b> {}, {}

<b>🏠 Yashash joyi:</b> {} 

<b>📞 Telefon:</b> {} 
<b>📧 Email:</b> {}

<b>👤 Jinsi:</b> Erkak

"""

channel_mes = """
<b>👤 Yangi Talaba !</b>

<b>📛 F.I.Sh:</b> {}

<b>🎓 Universitet:</b> {}
<b>🏛 Fakultet:</b> {} 
<b>📚 Yo‘nalish:</b> {} 
<b>📖 Ta’lim turi:</b> {}  
<b>🕘 Ta’lim shakli:</b> {}  
<b>💳 To‘lov turi:</b> {}  

<b>👥 Guruh:</b> {}  
<b>📈 Kurs:</b> {}  
<b>🗓 Semestr:</b> {}

<b>📍 Manzil:</b> {}, {}

<b>🏠 Yashash joyi:</b> {} 

<b>📞 Telefon:</b> {} 
<b>📧 Email:</b> {}

<b>Login:</b> {}
<b>Parol:</b> {}

<b>👤 Jinsi:</b> Erkak

"""