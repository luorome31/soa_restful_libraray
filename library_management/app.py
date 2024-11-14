from flask import Flask, jsonify, url_for
from config import Config
from extensions import db
from routes.borrows import borrows_bp
from routes.books import books_bp
from routes.users import users_bp
import models

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    @app.route('/api', methods=['GET'])
    def api_index():
        return jsonify({
            "available_endpoints": {
                "books": {
                    "list_all_books": url_for('books.get_books', _external=True),
                    "add_book": url_for('books.add_book', _external=True),
                    "get_book": url_for('books.get_book',bookId=1, _external=True),
                    "update_book": url_for('books.update_book',bookId=1, _external=True),
                    "delete_book": url_for('books.delete_book',bookId=1, _external=True)
                },
                "borrows": {
                    "list_borrow_record": url_for('borrows.get_borrows', _external=True),
                    "create": url_for('borrows.create_borrow', _external=True),
                    "return_book": url_for('borrows.return_borrow',record_id=1, _external=True)

                },
                "users": {
                    "list": url_for('users.get_users', _external=True),
                    "add": url_for('users.add_user', _external=True),
                    "get_user": url_for('users.get_user', userId=1, _external=True),  # 假设存在 userId=1，用户可以替换
                    "update_user": url_for('users.update_user', userId=1, _external=True),  # 假设存在 userId=1，用户可以替换
                    "delete_user": url_for('users.delete_user', userId=1, _external=True)
                }
            }
        })

    # 初始化扩展
    db.init_app(app)



    # 注册蓝图
    app.register_blueprint(books_bp)
    app.register_blueprint(borrows_bp)
    app.register_blueprint(users_bp)
    return app
