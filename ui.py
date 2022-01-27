from flaskwebgui import FlaskUI
from main import app

FlaskUI(app,start_server='fastapi',width=350,height=600).run()