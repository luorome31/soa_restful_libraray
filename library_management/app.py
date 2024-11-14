from flask import Flask
from config import Config
from extensions import db
from routes.books import books_bp
import models

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化扩展
    db.init_app(app)

    # 注册蓝图
    app.register_blueprint(books_bp)

    return app
