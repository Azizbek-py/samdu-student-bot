from telegram import InlineKeyboardButton


def teach_upload_but(user_id):
    teach_rate_but = [
            [InlineKeyboardButton("Baholash📝", callback_data="rate_student_upload")],
        [InlineKeyboardButton("⬅️", callback_data="previous"),InlineKeyboardButton("Talaba👁‍🗨", url = f"tg://user?id={user_id}"), InlineKeyboardButton("➡️", callback_data="next")],
            [InlineKeyboardButton("Ortga🔙", callback_data="back_tasks")]
        ]
    
    return teach_rate_but

def teach_list_but(user_id):
    but = [
            [InlineKeyboardButton("Domla👁‍🗨", url = f"tg://user?id={user_id}")],
        [InlineKeyboardButton("⬅️", callback_data="prev_teach"), InlineKeyboardButton("➡️", callback_data="next_teach")]]
    
    return but


weekday_but = [
    [InlineKeyboardButton("⬅️", callback_data="prev_week"), InlineKeyboardButton("➡️", callback_data="next_week")],
    [InlineKeyboardButton("Ortga🔙", callback_data="back")]
]

attend_but = [
    [InlineKeyboardButton("⬅️", callback_data="prev_attend"), InlineKeyboardButton("➡️", callback_data="next_attend")],
    [InlineKeyboardButton("Ortga🔙", callback_data="back")]
]

ADMIN_start_but = [["Teachers list"], ["Add Teacher", "Remove Teacher"], ["Get bases"]]

USER_start_but = [["Fanlar📚"],["Dars jadvali🗓", "Davomat📝"], ["Profilim👤", "Statistika📊"]]

TEACHER_start_but = [["Topshiriqlar🗂"], 
                     ["Natijalar📥", "Baholar jadvali📄"],
                     ["Profilim👤","Statistika📊"]
                    ]

teach_task_page_but = [
    ["Joylash➕", "Boshqarish✏️"],
    ["Ortga🔙"]
]

all_coureses_but = [
    [InlineKeyboardButton("1-kurs", callback_data="1_kurs")],
    [InlineKeyboardButton("2-kurs", callback_data="2_kurs")],
    [InlineKeyboardButton("3-kurs", callback_data="3_kurs")],
    [InlineKeyboardButton("Ortga🔙", callback_data="back")]]

groups_but1 = [
    [InlineKeyboardButton("101-Axborot xavfsizligi", callback_data="IT_2025_AX_01_uz"),InlineKeyboardButton("102-Axborot xavfsizligi", callback_data="IT_2025_AX_02_uz")],
    [InlineKeyboardButton("103-Sun'iy intellekt", callback_data="IT_2025_SI_03_uz"),InlineKeyboardButton("104-Sun'iy intellekt", callback_data="IT_2025_SI_04_uz")],
    [InlineKeyboardButton("105-Axborot tizimlari", callback_data="IT_2025_ATT_05_uz"),InlineKeyboardButton("106-Axborot tizimlari", callback_data="IT_2025_ATT_06_uz")],
    [InlineKeyboardButton("107-Axborot tizimlari", callback_data="IT_2025_ATT_07_uz"),InlineKeyboardButton("108-Axborot tizimlari", callback_data="IT_2025_ATT_08_ru")],
    [InlineKeyboardButton("109-Dasturiy injenering", callback_data="IT_2025_DI_09_uz"),InlineKeyboardButton("110-Dasturiy injenering", callback_data="IT_2025_DI_10_uz")],
    [InlineKeyboardButton("114-Axborot tizimlari", callback_data="IT_2025_ATT_14_uz"),InlineKeyboardButton("115-Axborot tizimlari", callback_data="IT_2025_ATT_15_uz")],
    [InlineKeyboardButton("Ortga🔙", callback_data="back_courses")]
]

groups_but2 = [
    [InlineKeyboardButton("201-Axborot xavfsizligi", callback_data="IT_2024_AX_01-guruh")],
    
    [InlineKeyboardButton("208-Dasturiy inejenering", callback_data="IT_2024_DI_08-guruh"),
     InlineKeyboardButton("209-Dasturiy inejenering", callback_data="IT_2024_DI_09-guruh")],
    
    [InlineKeyboardButton("202-Sun'iy intellekt", callback_data="IT_2024_SI_02-guruh"),
     InlineKeyboardButton("203-Sun'iy intellekt", callback_data="IT_2024_SI_03-guruh")],
    
    [InlineKeyboardButton("205-Axborot tizimlari", callback_data="IT_2024_ATT_05-guruh"),
     InlineKeyboardButton("206-Axborot tizimlari", callback_data="IT_2024_ATT_06-guruh")],
    [InlineKeyboardButton("Ortga🔙", callback_data="back_courses")]
]

groups_but3 = [
    [InlineKeyboardButton("302-KIDT", callback_data="IT_2023_KIDT_02-guruh"),
     InlineKeyboardButton("304-Dasturiy injenering", callback_data="IT_2023_DI_04-guruh")],

    [InlineKeyboardButton("306-Amaliy matematika", callback_data="AmaliyMat_2023_06-guruh"),
     InlineKeyboardButton("307-Amaliy matematika", callback_data="AmaliyMat_2023_07-guruh")],

    [InlineKeyboardButton("308-Amaliy matematika(rus)", callback_data="AmaliyMat_2023_08-guruh(rus)")],
    [InlineKeyboardButton("Ortga🔙", callback_data="back_courses")]
]


back_but = [
    ["Ortga🔙"]
]

back_inline_but = [
    [InlineKeyboardButton("Ortga🔙", callback_data="back")
    ]]

teach_tasks1_but = [
    [InlineKeyboardButton("⬅️", callback_data="previous"),InlineKeyboardButton("O'chirish", callback_data="delete"), InlineKeyboardButton("➡️", callback_data="next")],
    [InlineKeyboardButton("Joylaganlar📊", callback_data="student_results"), InlineKeyboardButton("Ortga🔙", callback_data="back")]
]

teach_tasks2_but = [
    [InlineKeyboardButton("⬅️", callback_data="previous"),InlineKeyboardButton("O'chirish", callback_data="delete"), InlineKeyboardButton("➡️", callback_data="next")],
    [InlineKeyboardButton("Ortga🔙", callback_data="back")]
]


logout_inline_button = [
    [InlineKeyboardButton('Logout❌', callback_data="logout"), InlineKeyboardButton("Ortga🔙", callback_data="profile_back")]
]

student_tasks_but = [
    [InlineKeyboardButton("⬅️", callback_data="previous"), InlineKeyboardButton("➡️", callback_data="next")],
    [InlineKeyboardButton("Joylash📤", callback_data="send_result")],
    [InlineKeyboardButton("Ortga🔙", callback_data="back")]]

student_tasks_but2 = [
    [InlineKeyboardButton("⬅️", callback_data="previous"), InlineKeyboardButton("➡️", callback_data="next")],
    [InlineKeyboardButton("Natijamni ko'rish👁", callback_data="send_result")],
    [InlineKeyboardButton("Ortga🔙", callback_data="back")]]

student_uploads_but = [
    [InlineKeyboardButton("O'chirish🗑",callback_data="delete_upload")],
    [InlineKeyboardButton("Ortga🔙", callback_data="back_tasks")]
]