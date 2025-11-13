# commander.py
from modules.teach_reply import register as teach_register
from modules.help import register as help_register

def register_commands(app):
    # سجل كل أوامر الموديولات هنا
    teach_register(app)
    help_register(app)
