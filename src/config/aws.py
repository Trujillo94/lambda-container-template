from src.utils.toolbox import load_env_var

SECRET_ACCESS_KEY = load_env_var("AWS_SECRET_ACCESS_KEY")
ACCESS_KEY_ID = load_env_var("AWS_ACCESS_KEY_ID")
DEFAULT_REGION = load_env_var("AWS_DEFAULT_REGION")
SESSION_TOKEN = load_env_var("AWS_SESSION_TOKEN")
