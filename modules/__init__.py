from .teach_reply import register as register_teach_reply
from .start import register as register_start
from .help import register as register_help

def register_modules(app, ADMIN_ID):
    register_teach_reply(app, ADMIN_ID)
    register_start(app, ADMIN_ID)
    register_help(app, ADMIN_ID)
