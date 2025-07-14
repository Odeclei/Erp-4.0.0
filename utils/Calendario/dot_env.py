import os

from dotenv import load_dotenv

load_dotenv()

# pprint.pp(os.environ)
print(os.getenv('BD_PASSWORD'))
