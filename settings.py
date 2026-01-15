import os
import dotenv

dotenv.load_dotenv("settings.env")
DB_URL = os.getenv("DB_URL")
