import os
import dotenv

env_file = ".env"

env = os.path.join(os.getcwd(), env_file)
if os.path.exists(env):
    dotenv.read_dotenv(override=True)
