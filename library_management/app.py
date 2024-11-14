from flask import Flask
from config import Config
from extensions import db
from library_management.routes.borrows import borrows_bp
from routes.books import books_bp
import models

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化扩展
    db.init_app(app)

    # 注册蓝图
    app.register_blueprint(books_bp)
    app.register_blueprint(borrows_bp)
    return app
