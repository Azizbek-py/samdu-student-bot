import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
BOT_USERNAME = os.getenv("BOT_USERNAME", "@SamDU_Talaba_Bot")
START_DATE = os.getenv("START_DATE", "15.02.2026")
DEVELOPER = os.getenv("DEVELOPER", "@BroAZIK")

ATTEND_LIMIT = int(os.getenv("ATTEND_LIMIT", "3"))

