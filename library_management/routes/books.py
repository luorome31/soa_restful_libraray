from flask import Blueprint, request, jsonify, abort, Response
from models import Book, Category
from extensions import db

books_bp = Blueprint('books', __name__)

# 获取所有图书
@books_bp.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([{
        "bookId": book.bookId,
        "title": book.title,
        "author": book.author,
        "isbn": book.isbn,
        "category": book.category.name
    } for book in books]), 200

# 获取特定图书信息
@books_bp.route('/books/<int:bookId>', methods=['GET'])
def get_book(bookId):
    book = Book.query.get(bookId)
    if book is None:
        abort(404, description="Book not found")
    return jsonify({
        "bookId": book.bookId,
        "title": book.title,
        "author": book.author,
        "isbn": book.isbn,
        "category": book.category.name
    }), 200

# 添加新图书
@books_bp.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    if not data or not data.get('title') or not data.get('author') or not data.get('categoryId') or not data.get('isbn'):
        abort(400, description="Title, author, categoryId, and isbn are required")
    
    category = Category.query.get(data["categoryId"])
    if category is None:
        abort(400, description="Category not found")
    
    new_book = Book(
        title=data["title"],
        author=data["author"],
        isbn=data["isbn"],
        categoryId=data["categoryId"]
    )
    db.session.add(new_book)
    db.session.commit()
    
    return jsonify({
        "bookId": new_book.bookId,
        "title": new_book.title,
        "author": new_book.author,
        "isbn": new_book.isbn,
        "category": category.name
    }), 201

# 更新图书信息
@books_bp.route('/books/<int:bookId>', methods=['PUT'])
def update_book(bookId):
    book = Book.query.get(bookId)
    if book is None:
        abort(404, description="Book not found")
    
    data = request.get_json()
    if not data or not data.get('title'):
        abort(400, description="Title is required")
    
    book.title = data["title"]
    db.session.commit()
    
    return jsonify({
        "bookId": book.bookId,
        "title": book.title,
        "author": book.author,
        "isbn": book.isbn,
        "category": book.category.name
    }), 200

# 删除图书
@books_bp.route('/books/<int:bookId>', methods=['DELETE'])
def delete_book(bookId):
    book = Book.query.get(bookId)
    if book is None:
        abort(404, description="Book not found")
    
    db.session.delete(book)
    db.session.commit()
    
    return Response(status=204)
