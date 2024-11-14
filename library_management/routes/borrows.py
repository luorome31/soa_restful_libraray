from flask import Blueprint, request, jsonify, abort
from datetime import datetime
from models import BorrowRecord, User, Book
from extensions import db

# 创建蓝图
borrows_bp = Blueprint('borrows', __name__)


# 获取所有借用记录
@borrows_bp.route('/borrows', methods=['GET'])
def get_borrows():
    borrow_records = BorrowRecord.query.all()
    results = []
    for record in borrow_records:
        results.append({
            "recordId": record.recordId,
            "userId": record.userId,
            "bookId": record.bookId,
            "borrowDate": record.borrowDate.strftime("%Y-%m-%d %H:%M:%S") if record.borrowDate else None,
            "returnDate": record.returnDate.strftime("%Y-%m-%d %H:%M:%S") if record.returnDate else None,
            "status": record.status
        })
    return jsonify(results), 200


# 创建新的借用记录
@borrows_bp.route('/borrows', methods=['POST'])
def create_borrow():
    data = request.get_json()

    if not data or not data.get('userId') or not data.get('bookId'):
        abort(400, description="userId and bookId are required")

    # 检查用户是否存在
    user = User.query.get(data['userId'])
    if user is None:
        abort(400, description="User not found")

    # 检查图书是否存在
    book = Book.query.get(data['bookId'])
    if book is None:
        abort(400, description="Book not found")

    # 创建新的借用记录
    new_borrow = BorrowRecord(
        userId=data['userId'],
        bookId=data['bookId'],
        borrowDate=datetime.now(),
        status="借出"
    )
    db.session.add(new_borrow)
    db.session.commit()

    return jsonify({
        "recordId": new_borrow.recordId,
        "userId": new_borrow.userId,
        "bookId": new_borrow.bookId,
        "borrowDate": new_borrow.borrowDate.strftime("%Y-%m-%d %H:%M:%S"),
        "status": new_borrow.status
    }), 201


# 更新借用记录状态为归还
@borrows_bp.route('/borrows/<int:record_id>/return', methods=['PUT'])
def return_borrow(record_id):
    borrow_record = BorrowRecord.query.get(record_id)

    if borrow_record is None:
        abort(404, description="Borrow record not found")

    if borrow_record.status == "已归还":
        abort(400, description="The book is already returned")

    # 更新借用记录状态
    borrow_record.status = "已归还"
    borrow_record.returnDate = datetime.now()
    db.session.commit()

    return jsonify({
        "recordId": borrow_record.recordId,
        "userId": borrow_record.userId,
        "bookId": borrow_record.bookId,
        "borrowDate": borrow_record.borrowDate.strftime("%Y-%m-%d %H:%M:%S"),
        "returnDate": borrow_record.returnDate.strftime("%Y-%m-%d %H:%M:%S"),
        "status": borrow_record.status
    }), 200
