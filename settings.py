import os
import dotenv

dotenv.load_dotenv("settings.env")
DB_URL = os.environ["DB_URL"]
CH_URL = os.environ["CH_URL"]
