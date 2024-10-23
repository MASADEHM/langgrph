import getpass
import os


OPENAI_API_KEY1 = os.getenv('OPENAI_API_KEY')
print (OPENAI_API_KEY1)
#print(os.environ)
print(os.environ['COMPUTERNAME'])
home_dir = os.getenv('OPENAI_API_KEY')
print(home_dir)
# def _set_env(var: str):
#     if not os.environ.get(var):
#         os.environ[var] = getpass.getpass(f"{var}: ")
    

# _set_env("OPENAI_API_KEY")

