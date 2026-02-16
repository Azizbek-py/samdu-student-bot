from telegram import Update, Bot, InlineKeyboardMarkup, ReplyKeyboardMarkup, InputMediaDocument
from telegram.constants import ParseMode
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes
)
from settings import *
from details.database.db import *
from .messages import *
from .buttons import *
from parsing.parser import get_token, get_user_info, get_subjects, get_student_dars, get_student_attendance
from pprint import pprint
from datetime import datetime, timezone, timedelta

UZ_TZ = timezone(timedelta(hours=5))
bot = Bot(token=BOT_TOKEN)

async def log_deleter(user_id, type, context):
    messages = context.user_data.get(type, [])
    for msg_id in messages:
        try:
            await bot.delete_message(chat_id=user_id, message_id=msg_id)
        except:
            pass
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name
    user = get(table="users", user_id=user_id)

    if user_id == ADMIN_ID:
        if not user:
            insert(
                    user_id=user_id,
                    table="users",
                    data={
                    "first_name": first_name,
                    "role": "admin",
                    "stage": "start",
                    "index": 0,
                    "logged_in": True
                    }
                )
        else:
            upd(table="users", data={"role":"admin", "logged_in": True, "stage": "start"}, user_id=user_id)
        
        await update.message.reply_text(
                    text=ADMIN_welcome_mes,
                    reply_markup=ReplyKeyboardMarkup(
                        ADMIN_start_but,
                        resize_keyboard=True)
                        )
        return
    
    if user:

        if user["role"] == "teacher":
            msg = await update.message.reply_text(
                    text=teacher_start_mes.format(
                        user["full_name"],
                        user_id,
                        user["subject_name"]
                    ),
                    parse_mode=ParseMode.HTML,
                    reply_markup=ReplyKeyboardMarkup(
                        TEACHER_start_but,
                        resize_keyboard=True)
                        )
            upd(table="users", data={"stage":"start",
                                     "course_number":"0",
                                     "index":0,
                                     "group_data": "",
                                     "uploads_index": 0,
                                     "rate_group": "",
                                     "upload_id": "",
                                     "message_id": ""
                                     }, user_id=user_id)
            
            messages = context.user_data.get("start_messages", [])
            messages+= context.user_data.get("messages", [])
            for msg_id in messages:
                try:
                    await bot.delete_message(chat_id=user_id, message_id=msg_id)
                except:
                    pass
            context.user_data.setdefault("start_messages", []).append(msg.message_id)
            context.user_data.setdefault("start_messages", []).append(update.message.message_id)
            return
        
        else:
            
            if user["logged_in"]:
                msg = await update.message.reply_text(
                        text=USER_welcome_mes.format(first_name=user["full_data"]["first_name"]),
                        parse_mode=ParseMode.HTML,
                        reply_markup=ReplyKeyboardMarkup(
                            USER_start_but,
                            resize_keyboard=True)
                            )
                insert(table="users", user_id=user_id, data={
                    "stage": "start",
                    "index": 0
                })
            else:
                insert(
                    user_id=user_id,
                    table="users",
                    data={
                    "first_name": first_name,
                    "role": "user",
                    "stage": "get_login",
                    "index": 0,
                    "logged_in": False
                    }
                )
                msg = await update.message.reply_text(
                    text=GET_login_mes,
                    parse_mode=ParseMode.HTML
                    )

                messages = context.user_data.get("start_messages", [])
                messages+= context.user_data.get("messages", [])
                for msg_id in messages:
                    try:
                        await bot.delete_message(chat_id=user_id, message_id=msg_id)
                    except:
                        pass
    
    else:
        insert(
                user_id=user_id,
                table="users",
                data={
                "first_name": first_name,
                "role": "user",
                "stage": "start",
                "index": 0,
                "logged_in": False,
                "stage": "get_login",
                "role": "user",
                }
            )
        msg = await update.message.reply_text(
            text=GET_login_mes,
            parse_mode=ParseMode.HTML)

    messages = context.user_data.get("start_messages", [])
    messages+= context.user_data.get("messages", [])
    for msg_id in messages:
        try:
            await bot.delete_message(chat_id=user_id, message_id=msg_id)
        except:
            pass
    context.user_data["start_messages"] = []
    context.user_data.setdefault("start_messages").append(msg.message_id)
    context.user_data.setdefault("start_messages").append(update.message.message_id)

async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    user_id = update.effective_user.id
    user = get(table="users", user_id=user_id)
    stage = user["stage"]

    if message == "Ortga🔙":
        
        if user["role"] == "admin":
            teacher_id = user.get("teacher_id", 0)
            await update.message.reply_text(
                text=ADMIN_welcome_mes,
                reply_markup=ReplyKeyboardMarkup(ADMIN_start_but, resize_keyboard=True)
                )
            if teacher_id != 0:
                delete(table="users", user_id=teacher_id)
                upd(
                    table="users",
                    data={
                        "teacher_id": 0
                    },
                    user_id=user_id
                )
        
        if user['role'] == 'user':

            context.user_data.setdefault("messages", []).append(update.message.message_id)
            messages = context.user_data.get("messages", [])
            messages += context.user_data.get("upload_msg_id", [])

            msg = await update.message.reply_text(
                            text=main_menu_mes,
                            parse_mode=ParseMode.HTML,
                            reply_markup=ReplyKeyboardMarkup(USER_start_but, resize_keyboard=True)
                            )
            for msg_id in messages:
                try:
                    await bot.delete_message(chat_id=user_id, message_id=msg_id)
                except:
                    pass
            context.user_data["messages"] = []

            
            context.user_data.setdefault("messages", []).append(msg.message_id)
        
        if user['role'] == "teacher":
            context.user_data.setdefault("messages", []).append(update.message.message_id)
            messages = context.user_data.get("messages", [])

            msg = await update.message.reply_text(
                text=main_menu_mes,
                parse_mode=ParseMode.HTML,
                reply_markup=ReplyKeyboardMarkup(TEACHER_start_but, resize_keyboard=True)
            )
            for msg_id in messages:
                try:
                    await bot.delete_message(chat_id=user_id, message_id=msg_id)
                except:
                    pass
            context.user_data["messages"] = []

            
            context.user_data.setdefault("messages", []).append(msg.message_id)

        upd(table="users", user_id=user_id, data={"stage": "start"})
        return
    
    if message == "Statistika📊":
        students_len = len(get(table="users"))
        teachers = []
        for i in get(table="users"):
            if i['role'] == "teacher":
                teachers.append(i)
        teachers_len = len(teachers)       
        tasks_len = len(get(table="tasks"))
        uploads_len = len(get_student_uploads())

        msg = await update.message.reply_text(
            text=statistics_mes.format(
                BOT_USERNAME,
                students_len,
                teachers_len,
                tasks_len,
                uploads_len,
                START_DATE,
                DEVELOPER
            ),
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(back_inline_but)
        )
        messages = context.user_data.get("messages", [])
        for msg_id in messages:
                try:
                    await bot.delete_message(chat_id=user_id, message_id=msg_id)
                except:
                    pass
        context.user_data["messages"] = []
        context.user_data.setdefault("messages", []).append(update.message.message_id)
        context.user_data.setdefault("messages", []).append(msg.message_id)
    

    if user_id == ADMIN_ID:

        if message == "Get bases":

            files = [
                "details/database/base.json",
                "details/database/student_uploads.json",
                "details/database/tasks.json"
            ]

            for file_name in files:
                if os.path.exists(file_name):
                    with open(file_name, "rb") as f:
                        await update.message.reply_document(document=f)
                else:
                    await update.message.reply_text(f"{file_name} topilmadi ❌")

        if message == "Add Teacher":
            upd(table="users", data={"stage":"add_teacher"}, user_id=user_id)

            msg = await update.message.reply_text(
                text=get_teacher_id_mes,
                reply_markup=ReplyKeyboardMarkup(back_but, resize_keyboard=True)
            )

        if stage == "add_teacher":
            teacher_id = int(message)

            upd(table="users", data={"teacher_id": teacher_id, "stage": "get_teacher_name"}, user_id=user_id)
            insert(table="users", data={"id": teacher_id, "role": "teacher", "logged_in": True}, user_id=teacher_id)

            msg = await update.message.reply_text(
                text=get_teacher_name_mes,
                reply_markup=ReplyKeyboardMarkup(
                    back_but,
                    resize_keyboard=True
                )
            )
        
        if stage == "get_teacher_name":
            teacher_name = message
            teacher_id = user["teacher_id"]
            upd(table="users", data={"full_name": teacher_name}, user_id=teacher_id)
            upd(table="users", data={"stage":"get_subject_name"}, user_id=user_id)

            msg = await update.message.reply_text(
                text=get_subject_name_mes,
                reply_markup=ReplyKeyboardMarkup(
                    back_but,
                    resize_keyboard=True
                ))
            
        if stage == "get_subject_name":
            subject_name = message
            teacher_id = user["teacher_id"]

            upd(
                table="users",
                data={
                    "subject_name": subject_name
                },
                user_id=teacher_id
            )
            

            msg = await update.message.reply_text(
                text=teacher_added_mes.format(
                    get(table="users", user_id=teacher_id)["full_name"],
                    teacher_id,
                    subject_name
                ))
            
            upd(table="users", data={"stage":"start", "teacher_id": 0}, user_id=user_id)
            return

        if message == "Teachers list":
            teachers = []
            for user in get(table="users"):
                if user["role"] == "teacher":
                    teachers.append(user)

            index = user.get("index", 0)
            try:
                teacher = teachers[index]
            except:
                await update.message.reply_text("Hali teacher yo'q")
                return
            
            await update.message.reply_text(
                text=Teacher_list_mes.format(
                    index+1,
                    len(teachers),
                    teacher.get("full_name", ""),
                    teacher.get("id", 0),
                    teacher.get("subject_name", "")
                ),
                reply_markup=InlineKeyboardMarkup(teach_list_but(teacher.get("id")))
            )
            return

        if message ==  "Remove Teacher":
            upd(table="users", data={"stage":"remove_teacher"}, user_id=user_id)

            msg = await update.message.reply_text(
                text=get_teacher_id_delete_mes,
                reply_markup=ReplyKeyboardMarkup(
                    back_but,
                    resize_keyboard=True
                )
            )

        if stage == "remove_teacher":
            teacher_id = int(message)
            delete(table="users", user_id=teacher_id)

            msg = await update.message.reply_text(
                text=deleted_teacher_mes,
                reply_markup=ReplyKeyboardMarkup(ADMIN_start_but, resize_keyboard=True)
            )
            upd(table="users", data={"stage":"start"}, user_id=user_id)
            return
        
    if user['role'] == 'user':

        if message == "Davomat📝":
            davomat = get_student_attendance(user.get("token"))
            upd(table="users", user_id=user_id, data={"attend_index": 0,"davomat": davomat.get("davomat",[])})
            items = davomat.get("davomat", [])

            if not items:
                msg = await update.message.reply_text(no_attendance_mes, parse_mode="HTML")
                return
            first_page = items[:ATTEND_LIMIT]
            total_pages = (len(items) + ATTEND_LIMIT - 1) // ATTEND_LIMIT

            text = f"📊 <b>Davomat ma'lumotlari:\nJami: {len(items)}ta - {len(items)*2}soat</b>\n\n"

            for item in first_page:
                text += attendance_item_mes.format(
                    subject=item["subject_name"],
                    type=item["type"],
                    teacher=item["teacher"],
                    date=item["date"],
                    time=item["time"],
                    count=item["count"]
                )
            text+=f"\n<b>Sahifa:</b> 1/{total_pages}"
            msg = await update.message.reply_text(
                text=text,
                reply_markup=InlineKeyboardMarkup(attend_but),
                parse_mode=ParseMode.HTML
            )
            messages = context.user_data.get("messages", [])
            for msg_id in messages:
                try:
                    await bot.delete_message(chat_id=user_id, message_id=msg_id)
                except:
                    pass
            context.user_data["messages"] = []
            context.user_data.setdefault("messages", []).append(update.message.message_id)
            context.user_data.setdefault("messages", []).append(msg.message_id)

        if message == "Dars jadvali🗓":
            weekday = user.get("weekday", "")

            days = get_student_dars(token=user.get("token"))

            date = datetime.now(UZ_TZ).weekday()
            day = list(days.values())[date]
            upd(table="users", user_id=user_id, data={"day_index": date,"weekday": days})
                
            today_lessons = day['lessons']
            if not today_lessons:
                msg = await update.message.reply_text(
                    f"📅 <b>{day['weekname']}</b>\n\nBugun dars yo‘q 🎉",
                    parse_mode=ParseMode.HTML,
                    reply_markup=InlineKeyboardMarkup(weekday_but)
                )
                context.user_data.setdefault("weekday", []).append(msg.message_id)
                context.user_data.setdefault("weekday", []).append(update.message.message_id)
            else:
                text = f"📅 <b>{day['weekname']} — Darslar:</b>\n\n"

                for i, lesson in enumerate(today_lessons, start=1):
                    text += (
                            f"{i}. 📚 <b>{lesson['subject']}</b>\n"
                            f"   ⏰ {lesson['time']}\n"
                            f"   👨‍🏫 {lesson['teacher']}\n"
                            f"   🏫 {lesson['room']}\n\n"
                        )

                msg = await update.message.reply_text(text,reply_markup=InlineKeyboardMarkup(weekday_but), parse_mode=ParseMode.HTML)
            
            messages = context.user_data.get("messages", [])
            for msg_id in messages:
                try:
                    await bot.delete_message(chat_id=user_id, message_id=msg_id)
                except:
                    pass
            context.user_data["messages"] = []
            context.user_data.setdefault("messages", []).append(update.message.message_id)
            context.user_data.setdefault("messages", []).append(msg.message_id)
            return
                
        if user["stage"] == "get_login":
            login = message
            upd(table="users", data={"stage":"get_password", "login": login}, user_id=user_id)
            msg = await update.message.reply_text(GET_password_mes, parse_mode=ParseMode.HTML)
            await bot.delete_message(chat_id=user_id, message_id=update.message.message_id)
            context.user_data.setdefault("messages", []).append(msg.message_id)
            context.user_data.setdefault("messages", []).append(update.message.message_id)

        elif user["stage"] == "get_password":
            password = message
            login = user["login"]
            token = get_token(login=login, password=password)
            await bot.delete_message(chat_id=user_id, message_id=update.message.message_id)

            if token != {}:
                token = token["data"]["token"]
                user_info = get_user_info(token=token)
                upd(
                    table="users",
                    data={
                        "full_data": user_info["data"],
                        "password": password,
                        "logged_in": True,
                        "token": token,
                        "stage": "start"
                    },
                    user_id=user_id
                )
                msg = await update.message.reply_text(
                    text=USER_welcome_mes.format(first_name=user_info["data"]["first_name"]),
                    reply_markup=ReplyKeyboardMarkup(
                        USER_start_but,
                        resize_keyboard=True)
                    )
                
                
            else:
                msg = await update.message.reply_text(
                    text=login_error_mes,
                    parse_mode=ParseMode.HTML
                )
                upd(table="users", data={"stage":"get_login", "logged_in": False}, user_id=user_id)
            context.user_data.setdefault("messages", []).append(update.message.message_id)
            
            messages = context.user_data.get("messages", [])
            messages+= context.user_data.get("start_messages", [])
            for msg_id in messages:
                try:
                    await bot.delete_message(chat_id=user_id, message_id=msg_id)
                except:
                    pass      
        
        if message == "Profilim👤":

            user_info = get(table="users", user_id=user_id)["full_data"]

            msg = await update.message.reply_photo(
                photo=user_info["image"],
                caption=student_profile_mes.format(
                    user_info["full_name"],
                    user_info["id"],
                    user_info["university"],
                    user_info["faculty"]["name"],
                    user_info["specialty"]["name"],
                    user_info["educationType"]["name"],
                    user_info["educationForm"]["name"],
                    user_info["paymentForm"]["name"],
                    user_info["group"]["name"],
                    user_info["level"]["name"],
                    user_info["semester"]["name"],
                    user_info["avg_gpa"],
                    user_info["studentStatus"]["name"],
                    user_info["province"]["name"],
                    user_info["district"]["name"],
                    user_info["address"],
                    user_info["phone"],
                    user_info["email"],
                    user_info["gender"]["name"]
                ),
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(logout_inline_button)
            )
            messages = context.user_data.get("messages", [])
            for msg_id in messages:
                try:
                    await bot.delete_message(chat_id=user_id, message_id=msg_id)
                except:
                    pass
            context.user_data["messages"] = []
            context.user_data.setdefault("messages", []).append(update.message.message_id)
            context.user_data.setdefault("messages", []).append(msg.message_id)

        if message == "Fanlar📚":
            user = get(table="users", user_id=user_id)
            token = user["token"]
            semester = user["full_data"]["semester"]["id"]
            subjects = get_subjects(token=token, semester=semester)
            
            subject_button = []
            row = []
            subjectss = ""
            for subject in subjects["data"]:
                if "Kurs ishi" not in subject['curriculumSubject']['subject']['name']:
                    row.append(subject['curriculumSubject']['subject']['name'])
                    subjectss += f"{subject['curriculumSubject']['subject']['name']}\n"
                    if len(row) == 2:
                        subject_button.append(row)
                        row = []
            if row:
                subject_button.append(row)
            subject_button.append(["Ortga🔙"])

            msg = await update.message.reply_text(
                text=f"<b>Fanni tanlang:</b>",
                parse_mode=ParseMode.HTML,
                reply_markup=ReplyKeyboardMarkup(subject_button, resize_keyboard=True)
            )
            upd(table="users", data={"stage":"subjects", "subjects": subject_button}, user_id=user_id)
            context.user_data.setdefault("messages", []).append(update.message.id)
            context.user_data.setdefault("messages", []).append(msg.message_id)

        if user['stage'] == "subjects" or user['stage'] == 'tasks':
            index = get(table="users", user_id=user_id).get("index", 0)
            group = get(table="users", user_id=user_id)["full_data"]["group"]["name"]
            rate = get(table="users", user_id=user_id).get("rate", 0)
            subject = message
            tasks = get_students_tasks(group=group, subject=subject)
            


            if len(tasks) == 0:
                msg = await update.message.reply_text(
                    text=no_students_tasks.format(subject)
                )
                        
            else:
                uniq_id = tasks[index]['uniq_id']  

                if get_student_uploads(user_id=user_id, uniq_id=uniq_id) == None:
                    reply_markup = InlineKeyboardMarkup(student_tasks_but)
                else:
                    reply_markup = InlineKeyboardMarkup(student_tasks_but2)
                task = tasks[index] 
                msg = await update.message.reply_document(
                    document=task["file_id"],
                    caption=Student_tasks_view_mes.format(
                        str(subject),
                        task.get('caption', " "),
                        task['from_teacher']['full_name'],
                        index + 1,
                        len(tasks),
                        BOT_USERNAME
                    ),
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup
                )
                upd(table="users", user_id=user_id, data={"subject": subject, "stage": "tasks"})
                
            if user['stage'] == "tasks":
                messages = context.user_data.get("tasks_message",[])
                for msg_id in messages:
                    try:
                        await bot.delete_message(chat_id=user_id, message_id=msg_id)
                    except:
                        pass
                
            context.user_data.setdefault("tasks_message", []).append(msg.message_id)
            context.user_data.setdefault("tasks_message", []).append(update.message.message_id)
            context.user_data.setdefault("messages", []).append(msg.message_id)

    if user['role'] == 'teacher':
        
        if stage == "rate_upload":
            upload_id = get(table="users", user_id=user_id)['upload_id']
            task = get_students_tasks(subject=user.get('subject_name'), group=user.get("rate_group"))[user.get("index")]
            uniq_id = task.get("uniq_id")
            uploads = get_student_uploads(uniq_id=uniq_id)
            upload = uploads[user.get("uploads_index")]
            context.user_data.setdefault("messages", []).append(update.message.message_id)

            
            try:
                rate = int(message)
            except:
                msg = await update.message.reply_text(
                    text=invalid_rate_mes
                )
                return
            update_student_uploads(id=int(upload_id), data={"rate": rate})
            context.user_data.setdefault("rate_log", []).append(update.message.message_id)
            
            await bot.send_message(chat_id=upload['from_user']['user_id'], text=you_have_rate_mes.format(user.get("subject_name"), rate), parse_mode=ParseMode.HTML)

            messages = context.user_data.get("rate_log", [])
            for message in messages:
                try:
                    await bot.delete_message(chat_id=user_id, message_id=message)
                except:
                    pass

            upd(table="users", user_id=user_id, data={"stage": "student_uploads", "message_id": 0, "upload_id": 0})
            msg = await bot.edit_message_caption(
                chat_id=user_id,
                message_id=user.get("message_id"),
                caption=teach_uploads_mes.format(
                    upload['from_user']['course'],
                    upload['from_user']['group'],
                    rate,
                    user.get("subject_name"),
                    upload['from_user']['second_name'],
                    upload['from_user']['first_name'],
                    upload['from_user']['phone'],
                    user.get("uploads_index")+1,
                    len(uploads),
                    BOT_USERNAME
                ),parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(teach_upload_but(upload['from_user']['user_id']))
            )
            
            return

        if message == "Topshiriqlar🗂":
            msg = await update.message.reply_text(
                text=teach_tasks_page_mes,
                reply_markup=ReplyKeyboardMarkup(teach_task_page_but, resize_keyboard=True),
                parse_mode=ParseMode.HTML
            )
            await log_deleter(user_id=user_id, type="messages", context=context)
            
        if message == "Natijalar📥":
            msg = await update.message.reply_text(
                text=choose_course_mes,
                reply_markup=InlineKeyboardMarkup(all_coureses_but)
            )
            await log_deleter(user_id=user_id, type="messages", context=context)
            upd(table="users", user_id=user_id, data={"stage": "rate"})

        if message == "Joylash➕":

            msg = await update.message.reply_text(
                text=choose_course_mes,
                reply_markup=InlineKeyboardMarkup(all_coureses_but)
            )
            upd(table="users", user_id=user_id, data={"stage": "upload_task"})

        if message == "Boshqarish✏️":
            index = get(table="users", user_id=user_id).get("index", 0)
            tasks_list = []
            for task in get(table="tasks", user_id=user_id):
                    tasks_list.append(task)
            if not tasks_list:
                msg = await update.message.reply_text(
                    text=no_teachers_tasks_mes,
                    reply_markup=ReplyKeyboardMarkup(TEACHER_start_but, resize_keyboard=True)
                )
                return
            uniq_id = tasks_list[index]["uniq_id"]
            uploads = get_student_uploads(uniq_id=uniq_id)
            if len(uploads) == 0:
                reply_markup = teach_tasks2_but
            else:
                reply_markup = teach_tasks2_but

            task = tasks_list[index]
            msg = await update.message.reply_document(
                document=task["file_id"],
                caption=teacher_tasks_mes.format(
                        task['caption'],
                        task['course_number'],
                        task["group_data"].split("_")[3],
                        task['from_teacher']['subject_name'],
                        len(uploads),
                        index+1,
                        len(tasks_list),
                        BOT_USERNAME
                ),
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(reply_markup)
            )
            upd(table="users", data={"stage":"manage_tasks"}, user_id=user_id)
        
        if message == "Profilim👤":
            msg = await update.message.reply_text(
                text=teacher_start_mes.format(
                    user.get("full_name", ""),
                    user.get("id", ""),
                    user.get("subject_name", "")
                ),
                reply_markup=ReplyKeyboardMarkup(TEACHER_start_but, resize_keyboard=True),
                parse_mode=ParseMode.HTML
            )
            await log_deleter(user_id=user_id, type="messages", context=context)
        
        if message == "Baholar jadvali📄":
            msg = await update.message.reply_text(
                text=in_optimize_mes,
                reply_markup=ReplyKeyboardMarkup(TEACHER_start_but, resize_keyboard=True),
                parse_mode=ParseMode.HTML
            )
            await log_deleter(user_id=user_id, type="messages", context=context)
        context.user_data.setdefault("messages", []).append(msg.message_id)             
    context.user_data.setdefault("messages", []).append(update.message.id)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = update.effective_user.id
    user = get(table="users", user_id=user_id)

    await query.answer()

    if user_id == ADMIN_ID:
        if query.data in ["prev_teach", "next_teach"]:
            index = user.get("index")
            teachers = []
            for user in get(table="users"):
                if user["role"] == "teacher":
                    teachers.append(user)

            if query.data == "prev_teach":
                if index > 0:
                    index -= 1
                else:
                    index = len(teachers)-1
            if query.data == "next_teach":
                if index < len(teachers)-1:
                    index += 1
                else:
                    index = 0

            teacher = teachers[index]

            await query.edit_message_text(
                text=Teacher_list_mes.format(
                    index+1,
                    len(teachers),
                    teacher.get("full_name", ""),
                    teacher.get("id", 0),
                    teacher.get("subject_name", "")
                ),
                reply_markup=InlineKeyboardMarkup(teach_list_but(teacher.get("id")))
            )
            return

    if user['role'] == 'teacher':
        messages = context.user_data.get("rate_log", [])
        for message in messages:
            try:
                await bot.delete_message(chat_id=user_id, message_id=message)
            except: 
                pass
        if messages:
            upd(table="users", user_id=user_id, data={"stage": "student_uploads"})
            
        user = get(table="users", user_id=user_id)
        stage = user["stage"]

        if query.data == "back" or query.data == "back_courses":
            await query.message.delete()

            msg = await query.message.reply_text(
                text=main_menu_mes,
                parse_mode=ParseMode.HTML,
                reply_markup=ReplyKeyboardMarkup(TEACHER_start_but, resize_keyboard=True)
            )

            messages = context.user_data.get("messages", [])
            for msg_id in messages:
                try:
                    await bot.delete_message(chat_id=user_id, message_id=msg_id)
                except:
                    pass
            context.user_data["messages"] = []
            context.user_data.setdefault("messages", []).append(msg.message_id)

            upd(table="users", data={"stage":"start"}, user_id=user_id)
            return  

        if query.data in ["1_kurs", "2_kurs", "3_kurs"]:
            print("a")
            if stage == "upload_task":
                if query.data == "1_kurs":
                    reply_markup=groups_but1
                if query.data == "2_kurs":
                    reply_markup=groups_but2
                if query.data == "3_kurs":
                    reply_markup=groups_but3

                course_number = query.data.split("_")[0]
                msg = await query.edit_message_text(
                    text=choose_group_mes.format(course_number),
                    reply_markup=InlineKeyboardMarkup(reply_markup)
                )
                upd(table="users", data={"stage":"choose_group", "course_number": course_number}, user_id=user_id)
                return
            
            if stage == "rate":
                course_number = query.data.split("_")[0]
                if query.data == "1_kurs":
                    reply_markup=groups_but1
                if query.data == "2_kurs":
                    reply_markup=groups_but2
                if query.data == "3_kurs":
                    reply_markup=groups_but3

                msg = await query.edit_message_text(
                    text=choose_group_mes.format(course_number),
                    reply_markup=InlineKeyboardMarkup(reply_markup)
                )
                upd(table="users", user_id=user_id, data={
                    "stage": "rate_group"
                })

        if query.data == "rate_student_upload":
            if stage == "student_uploads":
                task = get_students_tasks(subject=user.get('subject_name'), group=user.get("rate_group"))[user.get('index')]
                uniq_id = task.get("uniq_id")
                uploads = get_student_uploads(uniq_id=uniq_id)
                upload = uploads[user.get("uploads_index")]

                upl_id = f"{upload['from_user']['user_id']}{upload['uniq_id']}"
                upd(table="users", user_id=user_id, data={"stage": "rate_upload", "upload_id": upl_id, "message_id": query.message.message_id})

                msg = await query.message.reply_text(
                    text=get_rate_mes,
                    parse_mode=ParseMode.HTML
                )
                context.user_data.setdefault("rate_log", []).append(msg.message_id)
        
        if query.data == "back_tasks":
            group = user.get("rate_group")
            subject = user.get("subject_name")
            tasks = get_students_tasks(subject=subject, group=group)
            task = tasks[user.get("index")]
            uploads = get_student_uploads(uniq_id=task["uniq_id"])

            if len(uploads) == 0:
                reply_markup = teach_tasks2_but
            else:
                reply_markup = teach_tasks1_but

            msg = await query.edit_message_media(
                media=InputMediaDocument(
                    caption=teacher_tasks_mes.format(
                        task['caption'],
                        task['course_number'],
                        task["group_data"].split("_")[3],
                        subject,
                        len(uploads),
                        user.get("index") + 1,
                        len(tasks),
                        BOT_USERNAME
                    ),
                    parse_mode=ParseMode.HTML,
                    media=task['file_id']),
                    reply_markup=InlineKeyboardMarkup(reply_markup)
            )
            upd(table="users", user_id=user_id, data={"stage": "rate_gr"})
            return

        if stage == "rate_group":
            subject = get(table="users", user_id=user_id)["subject_name"]
            callback = query.data
            index = get(table="users", user_id=user_id)["index"]
            tasks = get_students_tasks(group=callback, subject=subject)
            try:
                task = tasks[index]
            except:
                msg = await query.message.reply_text(text="Bu guruh uchun hali topshiriq joylanmagan🚫 ")
                context.user_data.setdefault("not_log", []).append(msg.message_id)
                context.user_data.setdefault("messages", []).append(msg.message_id)
                return
            
            uniq_id = task["uniq_id"]
            uploads = get_student_uploads(uniq_id=uniq_id)
            upd(table="users", user_id=user_id, data={"rate_group": callback, "stage": "rate_gr"})
            
            if len(uploads) == 0:
                reply_markup = teach_tasks2_but
            else:
                reply_markup = teach_tasks1_but

            msg = await query.edit_message_media(
                media=InputMediaDocument(
                    caption=teacher_tasks_mes.format(
                        task['caption'],
                        task['course_number'],
                        task["group_data"].split("_")[3],
                        subject,
                        len(uploads),
                        index+1,
                        len(tasks),
                        BOT_USERNAME
                    ),
                    parse_mode=ParseMode.HTML,
                    media=task['file_id']),
                    reply_markup=InlineKeyboardMarkup(reply_markup)
            )
            messages = context.user_data.get("not_log",[])

            for msg_id in messages:
                try:
                    await bot.delete_message(chat_id =user_id, message_id=msg_id)
                except:
                    pass
            return

        if stage == "choose_group":
            group_data = query.data
            course_number = user["course_number"]

            msg = await query.edit_message_text(
                text=send_assignment_mes.format(course_number, group_data.split("_")[3]),
                reply_markup=InlineKeyboardMarkup(back_inline_but)
            )
            upd(table="users", data={"stage":"upload_assignment", "group_data": group_data}, user_id=user_id)
            return

        if stage == "student_uploads":
            group = user.get('rate_group')
            index = user.get("index") 
            uploads_index = user.get('uploads_index')
            task = get_students_tasks(subject=user.get('subject_name'), group=group)[index]
            uniq_id = task.get("uniq_id")

            uploads = get_student_uploads(uniq_id=uniq_id)


            if query.data == "previous":
                if uploads_index > 0:
                    uploads_index -= 1
                else:
                    uploads_index = len(uploads) - 1
            if query.data == "next":
                if uploads_index < len(uploads) - 1:
                    uploads_index += 1
                else:
                    uploads_index = 0
            upload = uploads[uploads_index]
            upd(table="users", user_id=user_id, data={"uploads_index": uploads_index})
            
            if len(uploads) != 1:
                await query.edit_message_media(
                    media=InputMediaDocument(
                        media=upload['file_id'],
                            filename=upload['file_name'],
                            caption=teach_uploads_mes.format(
                            upload['from_user']['course'],
                            upload['from_user']['group'],
                            upload['rate'],
                            user.get('subject_name'),
                            upload['from_user']['second_name'],                          
                            upload['from_user']['first_name'],
                            upload['from_user']['phone'],
                            uploads_index+1,
                            len(uploads),
                            BOT_USERNAME
                                        ),
                                        parse_mode=ParseMode.HTML),
                            reply_markup=InlineKeyboardMarkup(teach_upload_but(upload['from_user']['user_id'])))
            else:
                pass
            return
 
             
        if stage == "upload_assignment":
            await query.edit_message_text(
                text=not_uploading_file_mes
            )
            return

        if query.data in ["previous", "next", "delete"]:
            tasks_list = []
            index = get(table="users", user_id=user_id)["index"]
            
            if stage == "manage_tasks":
                for task in get(table="tasks", user_id=user_id):
                    tasks_list.append(task)

            if stage == "rate_gr":
                tasks_list=get_students_tasks(subject=user["subject_name"], group=user["rate_group"])

            if query.data == "delete":
                for task in tasks_list:
                    if task["uniq_id"] == get(table="tasks", user_id=user_id)[index]["uniq_id"]:
                        delete(table="tasks", user_id=task["uniq_id"])
                        tasks_list.remove(task)
                        break

                if index != 0:
                    index -= 1
                if not tasks_list:
                    await query.delete_message()
                    msg = await query.message.reply_text(
                        text=USER_welcome_mes.format(first_name=user['first_name']),
                        reply_markup=ReplyKeyboardMarkup(TEACHER_start_but, resize_keyboard=True)
                    )
                    upd(table="users", data={"stage":"start"}, user_id=user_id)
                    return
                uniq_id = tasks_list[index]["uniq_id"]
                uploads = get_student_uploads(uniq_id=uniq_id)
                if len(uploads) == 0:
                    reply_markup = teach_tasks2_but
                else:
                    reply_markup = teach_tasks1_but

                     
                msg = await query.edit_message_media(
                    media=InputMediaDocument(
                        media=tasks_list[index]["file_id"],
                        caption=teacher_tasks_mes.format(
                            tasks_list[index]["caption"],
                            tasks_list[index]["course_number"],
                            tasks_list[index]["group_data"].split("_")[3],
                            tasks_list[index]['from_teacher']['subject_name'],
                            len(uploads),
                            index + 1,
                            len(tasks_list),
                            BOT_USERNAME
                        ),
                        parse_mode=ParseMode.HTML,
                    ),
                    reply_markup=InlineKeyboardMarkup(reply_markup)
                )
                upd(table="users", data={"index": index}, user_id=user_id)
                return
            
            if query.data == "previous":
                if index > 0:
                    index -= 1
                else:
                    index = len(tasks_list) - 1
            if query.data == "next":
                if index < len(tasks_list) - 1:
                    index += 1
                else:
                    index = 0
            

            upd(table="users", data={"index": index}, user_id=user_id)
            uniq_id = tasks_list[index]["uniq_id"]
            uploads = get_student_uploads(uniq_id=uniq_id)
            task = tasks_list[index]

            if len(uploads) != 0 and stage == "rate_gr":
                reply_markup = teach_tasks1_but
            else:
                reply_markup = teach_tasks2_but
            msg = await query.edit_message_media(
                media=InputMediaDocument(
                    media=task["file_id"],
                    caption=teacher_tasks_mes.format(
                            tasks_list[index]["caption"],
                            tasks_list[index]["course_number"],
                            tasks_list[index]["group_data"].split("_")[3],
                            task['from_teacher']['subject_name'],
                            len(uploads),
                            index + 1,
                            len(tasks_list),
                            BOT_USERNAME
                        ),
                        parse_mode=ParseMode.HTML
                ),
                reply_markup=InlineKeyboardMarkup(reply_markup)
            )
            return

        if query.data == "student_results":
            index = get(table="users", user_id=user_id).get("index", 0)
            if stage == "rate_gr":
                await query.answer()
                try:
                    subject = get(table="users", user_id=user_id)["subject_name"]
                    uniq_id = get_students_tasks(subject=subject, group=user['rate_group'])[index]['uniq_id']
                    uploads_index = get(table="users", user_id=user_id).get("uploads_index", 0)
                    student_uploads = get_student_uploads(uniq_id=uniq_id)
                    upload = student_uploads[uploads_index]
                    msg = await query.edit_message_media(
                        media=InputMediaDocument(
                            media=upload['file_id'],
                            filename=f"{upload['file_name']} {BOT_USERNAME}",
                            caption=teach_uploads_mes.format(
                            upload['from_user']['course'],
                            upload['from_user']['group'],
                            upload['rate'],
                            upload['subject'],
                            upload['from_user']['second_name'],
                            upload['from_user']['first_name'],
                            upload['from_user']['phone'],
                            uploads_index+1,
                            len(student_uploads),
                            BOT_USERNAME
                        ),parse_mode=ParseMode.HTML),
                        reply_markup=InlineKeyboardMarkup(teach_upload_but(upload['from_user']['user_id']))
                    )
                    upd(table="users", user_id=user_id, data={"stage": "student_uploads"})
                except:
                    await query.answer("Hali natijalar yo'q!", show_alert=True)
            
    if user['role'] == "user":

        if "attend" in query.data:
            attend_index = user.get("attend_index", 0)
            attendance_list = user.get("davomat", [])
            total_items = len(attendance_list)
            total_pages = (total_items + ATTEND_LIMIT - 1) // ATTEND_LIMIT

            if total_pages == 0:
                return

            if query.data == "prev_attend":
                attend_index = (attend_index - 1) % total_pages
            if query.data == "next_attend":
                attend_index = (attend_index + 1) % total_pages
            
            upd(table="users", user_id=user_id, data={"attend_index": attend_index})

            start = attend_index * ATTEND_LIMIT
            end = start + ATTEND_LIMIT
            page_items = attendance_list[start:end]

            text = f"📊 <b>Davomat ma'lumotlari:\nJami: {len(attendance_list)}ta - {len(attendance_list)*2}soat</b>\n\n"

            for item in page_items:
                text += attendance_item_mes.format(
                    subject=item["subject_name"],
                    type=item["type"],
                    teacher=item["teacher"],
                    date=item["date"],
                    time=item["time"],
                    count=item["count"]
                )
            text+=f"\n<b>Sahifa:</b> {attend_index+1}/{total_pages}"
            await query.edit_message_text(
                text=text,
                reply_markup=InlineKeyboardMarkup(attend_but),
                parse_mode=ParseMode.HTML
            )

        if "week" in query.data:
            week_index = user.get("day_index")
            if query.data == "prev_week":
                if week_index > 0:
                    week_index-=1
                else:
                    week_index=5
            
            if query.data == "next_week":
                if week_index < 5:
                    week_index+=1
                else:
                    week_index=0

            day = list(user.get("weekday").values())[week_index]
            today_lessons = day["lessons"]
            text = f"📅 <b>{day['weekname']} — Darslar:</b>\n\n"

            for i, lesson in enumerate(today_lessons, start=1):
                text += (
                        f"{i}. 📚 <b>{lesson['subject']}</b>\n"
                        f"   ⏰ {lesson['time']}\n"
                        f"   👨‍🏫 {lesson['teacher']}\n"
                        f"   🏫 {lesson['room']}\n\n"
                    )

            msg = await query.edit_message_text(text,reply_markup=InlineKeyboardMarkup(weekday_but), parse_mode=ParseMode.HTML)
            context.user_data.setdefault("weekday", []).append(msg.message_id)
            upd(table="users", user_id=user_id, data={"day_index": week_index})
            return
        try:
            index = get(table="users", user_id=user_id)["index"]
            tasks = get_students_tasks(group=user["full_data"]["group"]["name"], subject=user["subject"])
            task = tasks[index]
            uniq_id = task['uniq_id']
            stage = user.get("stage", "")
        except:
            pass

        if query.data in ["previous", "next"]:


            if query.data  == "next":
                if index < len(tasks) - 1:
                    index += 1
                else:
                    index = 0
            if query.data == "previous":
                if index > 0:
                    index -= 1
                else:
                    index = len(tasks) - 1

            try:
                rate = user.get('rate', 0)[user['subject']]
            except:
                rate = 0
            
            upd(table="users", user_id=user_id, data={"index": index, "stage": "tasks"})
            uploads = get_student_uploads(user_id=user_id, uniq_id=tasks[index]['uniq_id'])
            
            if uploads == None:
                reply_markup = InlineKeyboardMarkup(student_tasks_but)
            else:
                reply_markup = InlineKeyboardMarkup(student_tasks_but2)
            task = tasks[index]
            msg = await query.edit_message_media(
                media=InputMediaDocument(
                    media=task['file_id'],
                    caption = Student_tasks_view_mes.format(
                        user['subject'],
                        task['caption'],
                        task['from_teacher']['full_name'],
                        index + 1,
                        len(tasks),
                        BOT_USERNAME
                ),parse_mode=ParseMode.HTML),
                reply_markup=reply_markup,
            )
            if stage == "uploading":
                for msg_id in context.user_data.get("upload_msg_id"):
                    
                    try:
                        await bot.delete_message(chat_id=user_id, message_id=msg_id)
                    except:
                        pass

        if query.data == "send_result":
            await query.answer()
            uploads = get_student_uploads(user_id=user_id, uniq_id=uniq_id)
            
            if stage != "uploading":
                upd(table="users", user_id=user_id, data={"applying_uniq_id": uniq_id})
                if uploads == None:
                    msg = await query.message.reply_text(
                        text=not_uploaded_mes,
                        parse_mode=ParseMode.HTML,
                        reply_markup=ReplyKeyboardMarkup(back_but, resize_keyboard=True)
                    )
                    upd(table="users", user_id=user_id, data={"stage": "uploading"})

                    context.user_data.setdefault("upload_msg_id", []).append(msg.message_id)
                else:
                    msg = await query.edit_message_media(
                        media=InputMediaDocument(
                            filename=uploads['file_name'],
                            media=uploads['file_id'],
                        caption=upload_view_mes.format(
                            uploads['subject'],
                            uploads['rate'],
                            BOT_USERNAME
                        ),
                        parse_mode=ParseMode.HTML),
                        reply_markup=InlineKeyboardMarkup(student_uploads_but)
                    )
            else:
                await query.answer("Fayl Jo'nating!")
        
        if query.data == "delete_upload":
            await query.answer()
            deleted = delete_student_uploads(uniq_id=uniq_id, user_id=user_id)
            
            if deleted == True:
                await query.edit_message_caption(
                    caption=succesfully_deleted_mes
                )
                upd(table="users", user_id=user_id, data={"stage": "subjects", "applying_uniq_id": 0})
            else:
                await query.answer("xabar uje yo'q")

        if query.data == "back_tasks":

            if get_student_uploads(user_id=user_id, uniq_id=tasks[index]['uniq_id']) == None:
                reply_markup = InlineKeyboardMarkup(student_tasks_but)
            else:
                reply_markup = InlineKeyboardMarkup(student_tasks_but2)

            msg = await query.edit_message_media(
                media=InputMediaDocument(
                    filename=task["file_name"],
                    media=task['file_id'],
                    caption=Student_tasks_view_mes.format(
                    user["subject"],
                    task['caption'],
                    task['from_teacher']["full_name"],
                    index+1,
                    len(tasks),
                    BOT_USERNAME
                ),
                parse_mode=ParseMode.HTML
                ),
                reply_markup=reply_markup
            )
            upd(table="users", user_id=user_id, data={"applying_uniq_id": 0})
            
        if query.data == "back" or query.data == "profile_back":
            context.user_data.setdefault("messages", []).append(query.message.message_id)
            messages = context.user_data.get("messages", [])
            messages += context.user_data.get("upload_msg_id", [])
            messages += context.user_data.get("weekday", [])

            msg = await query.message.reply_text(
                            text=main_menu_mes,
                            parse_mode=ParseMode.HTML,
                            reply_markup=ReplyKeyboardMarkup(USER_start_but, resize_keyboard=True)
                            )
            
            for msg_id in messages:
                try:
                    await bot.delete_message(chat_id=user_id, message_id=msg_id)
                except:
                    pass
            context.user_data["messages"] = []
            context.user_data["upload_msg_id"] = []
            context.user_data["weekday"] = []
            context.user_data.setdefault("messages", []).append(msg.message_id)
            upd(table="users", user_id=user_id, data={"stage": "start", "index": 0, "applying_uniq_id": 0, "subject": ""})

        if query.data == "logout":
            messages = context.user_data.get("profile_messages", [])
            messages+= context.user_data.get("messages", [])
            messages+= context.user_data.get("start_messages", [])
            
            upd(table="users", user_id=user_id, data={
                "stage": "get_login",
                "index": 0,
                "logged_in": False,
                "login": "",
                "full_data": {},
                "password": "",
                "token": "",
                "subjects": [],
            })

            msg = await query.message.reply_text(
                text=GET_login_mes,
                parse_mode=ParseMode.HTML
            )
            context.user_data.setdefault("start_messages", []).append(msg.message_id)
            for msg_id in messages:
                try:
                    await bot.delete_message(chat_id=user_id, message_id=msg_id)
                except:
                    pass
            
async def document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get(table="users", user_id=user_id)
    stage = user["stage"]

    if user['role'] == 'teacher':
        if stage == "upload_assignment":
            document = update.message.document
            file_id = document.file_id
            file_name = document.file_name
            uniq_id = update.message.message_id

            group_data = user["group_data"]
            course_number = user["course_number"]

            msg = await update.message.reply_text(
                text=f"Topshiriq muvaffaqiyatli {course_number}-kurs, {course_number}{group_data.split('_')[3]}-guruhga joylandi!",
                reply_markup=ReplyKeyboardMarkup(TEACHER_start_but, resize_keyboard=True)
            )
            caption = update.message.caption if update.message.caption is not None else ""
            insert(table="tasks", data={
                "file_id": file_id,
                "file_name": file_name,
                "course_number": course_number,
                "group_data": group_data,
                "caption": caption,
                "own_of_file": user_id,
                "uniq_id": uniq_id,
                "from_teacher": {
                    "id": user_id,
                    "full_name": user["full_name"],
                    "subject_name": user["subject_name"]
                }
            })

            upd(table="users", data={"stage":"start"}, user_id=user_id)
            context.user_data.setdefault("messages", []).append(update.message.message_id)
            messages = context.user_data.get("messages", [])
            context.user_data.setdefault("messages", []).append(msg.message_id)
            for msg_id in messages:
                try:
                    await bot.delete_message(chat_id=user_id, message_id=msg_id)
                except:
                    pass
            
            return
    
    if user['role'] == "user":
        if stage == "uploading":
            msg_id = update.message.message_id
            document = update.message.document
            file_id = document.file_id
            file_name = document.file_name
            file_name = f"{file_name} {BOT_USERNAME}"
            uniq_id = user['applying_uniq_id']
            course = user['full_data']["level"]["name"]
            group = user['full_data']['group']['name'].split("_")[3]
            group = int(f"{course[0]}{group}")
            
            ins = insert_student_uploads(user_id=user_id,uniq_id=uniq_id, data={
                "file_id": file_id,
                "file_name": file_name,
                "subject": user["subject"],
                "uniq_id": uniq_id,
                "rate": 0,
                "from_user":{
                    "course": course,
                    "group": group,
                    "first_name": user['full_data']['first_name'],
                    "second_name": user['full_data']['second_name'],
                    "phone": user['full_data']['phone'],
                    'user_id': user_id,
                    "image": user['full_data']['image'],
                    }
            })
            if ins:
                msg = await update.message.reply_text(
                        text=succesfully_upload_mes.format(user['subject']),
                            reply_markup=ReplyKeyboardMarkup(USER_start_but, resize_keyboard=True)
                        )
            else:
                pass

            context.user_data.setdefault("messages", []).append(update.message.message_id)

            messages = context.user_data.get("messages", [])
            messages += context.user_data.get("upload_msg_id", [])

            for msg_id in messages:
                try:
                    await bot.delete_message(chat_id=user_id, message_id=msg_id)
                except:
                    pass
            context.user_data["messages"] = []
            context.user_data.setdefault("messages", []).append(msg.message_id)