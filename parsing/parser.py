import requests
from datetime import datetime, timezone, timedelta

UZ_TZ = timezone(timedelta(hours=5))

WEEKDAY_UZ = {
    0: "Dushanba",
    1: "Seshanba",
    2: "Chorshanba",
    3: "Payshanba",
    4: "Juma",
    5: "Shanba",
    6: "Yakshanba",
}

from datetime import datetime, timezone, timedelta

UZ_TZ = timezone(timedelta(hours=5))

WEEKDAY_UZ = {
    0: "Dushanba",
    1: "Seshanba",
    2: "Chorshanba",
    3: "Payshanba",
    4: "Juma",
    5: "Shanba",
    6: "Yakshanba",
}

def _norm(s: str) -> str:
    return " ".join((s or "").replace("’", "'").replace("‘", "'").split()).strip()

def convert_schedule_weeklist_dedup_per_day(api_json: dict | list) -> dict:
    if isinstance(api_json, dict):
        lessons = api_json.get("data") or api_json.get("items") or []
    else:
        lessons = api_json

    weeklist = {day: {"weekname": day, "lessons": []} for day in WEEKDAY_UZ.values()}

    # ✅ har bir kun uchun alohida seen
    seen_by_day = {day: set() for day in WEEKDAY_UZ.values()}

    for lesson in lessons:
        ts = lesson.get("lesson_date")
        if not isinstance(ts, (int, float)):
            continue

        day = WEEKDAY_UZ[datetime.fromtimestamp(int(ts), tz=UZ_TZ).weekday()]

        lp = lesson.get("lessonPair") or {}
        start = _norm(lp.get("start_time", ""))
        end = _norm(lp.get("end_time", ""))

        teacher = _norm((lesson.get("employee") or {}).get("name", "—"))
        subject = _norm((lesson.get("subject") or {}).get("name", "—"))
        room = _norm((lesson.get("auditorium") or {}).get("name", "—"))

        # ✅ shu kunda darsni noyob qiladigan kalit
        key = (start, end, teacher, subject, room)

        # ✅ agar shu kunda oldin qo‘shilgan bo‘lsa -> skip
        if key in seen_by_day[day]:
            continue

        seen_by_day[day].add(key)

        weeklist[day]["lessons"].append({
            "teacher": teacher,
            "subject": subject,
            "room": room,
            "time": f"{start} -> {end}",
        })

    # sort
    for day in weeklist:
        weeklist[day]["lessons"].sort(key=lambda x: x["time"][:5] if x["time"] else "")

    return weeklist

def get_student_dars(token):
    response = requests.get(
        "https://student.samdu.uz/rest/v1/education/schedule?week=2937&semester=12",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    if response.status_code != 200:
        return {}

    # 🔥 JSON ni o'zgaruvchiga olamiz
    api_json = response.json()

    return convert_schedule_weeklist_dedup_per_day(api_json)

def convert_attendance(api_json: dict) -> dict:
    """
    API dan kelgan attendance JSON ni
    kerakli formatga o‘tkazadi.
    """

    lessons = api_json.get("data", [])

    davomat_list = []

    for item in lessons:
        subject_name = (item.get("subject") or {}).get("name", "—").strip()
        lesson_type = (item.get("trainingType") or {}).get("name", "—").strip()
        teacher = (item.get("employee") or {}).get("name", "—").strip()

        # Davomat soni (absent_off ni oldim, kerak bo‘lsa o‘zgartiramiz)
        count = item.get("absent_off", 0)

        # Sana formatlash
        timestamp = item.get("lesson_date")
        if isinstance(timestamp, (int, float)):
            date_str = datetime.fromtimestamp(timestamp, tz=UZ_TZ).strftime("%d.%m.%Y")
        else:
            date_str = "—"

        # Vaqt
        lesson_pair = item.get("lessonPair") or {}
        start = lesson_pair.get("start_time", "")
        end = lesson_pair.get("end_time", "")
        time_str = f"{start} -> {end}" if start and end else "—"

        davomat_list.append({
            "subject_name": subject_name,
            "type": lesson_type,
            "teacher": teacher,
            "count": str(count),
            "date": date_str,
            "time": time_str
        })

    return {"davomat": davomat_list}

def get_student_attendance(token):
    response = requests.get(
        "https://student.samdu.uz/rest/v1/education/attendance?semester=12",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    if response.status_code != 200:
        return {}

    api_json = response.json()  
    return convert_attendance(api_json)

def get_token(login: int, password: str) -> str:
    response = requests.post("https://student.samdu.uz/rest/v1/auth/login", json={
        "login": login,
        "password": password})
    if response.status_code != 200:
        return {}
    return response.json()

def get_user_info(token: str) -> dict:
    response = requests.get("https://student.samdu.uz/rest/v1/account/me", headers={
        "Authorization": f"Bearer {token}"
    })
    if response.status_code != 200:
        return {}
    return response.json()

def get_subjects(token: str, semester: int) -> dict:
    response = requests.get("https://student.samdu.uz/rest/v1/education/subject-list?semester=12", headers={
        "Authorization": f"Bearer {token}"
    })
    if response.status_code != 200:
        return {}
    return response.json()