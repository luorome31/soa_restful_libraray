from flask import Blueprint, request, jsonify, abort
from models import User
from extensions import db

# 创建蓝图
users_bp = Blueprint('users', __name__)

# 获取所有用户
@users_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{
        "userId": user.userId,
        "name": user.name,
        "contact": user.contact,
        "identity": user.identity
    } for user in users]), 200

# 获取特定用户信息
@users_bp.route('/users/<int:userId>', methods=['GET'])
def get_user(userId):
    user = User.query.get(userId)
    if user is None:
        abort(404, description="User not found")
    return jsonify({
        "userId": user.userId,
        "name": user.name,
        "contact": user.contact,
        "identity": user.identity
    }), 200

# 添加新用户
@users_bp.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('contact') or not data.get('identity') or not data.get('password'):
        abort(400, description="Name, contact, identity, and password are required")
    
    new_user = User(
        name=data['name'],
        contact=data['contact'],
        identity=data['identity'],
        password=data['password']
    )
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({
        "userId": new_user.userId,
        "name": new_user.name,
        "contact": new_user.contact,
        "identity": new_user.identity
    }), 201

# 更新用户信息
@users_bp.route('/users/<int:userId>', methods=['PUT'])
def update_user(userId):
    user = User.query.get(userId)
    if user is None:
        abort(404, description="User not found")
    
    data = request.get_json()
    if not data or not data.get('contact'):
        abort(400, description="Contact is required")
    
    user.contact = data['contact']
    db.session.commit()
    
    return jsonify({
        "userId": user.userId,
        "name": user.name,
        "contact": user.contact,
        "identity": user.identity
    }), 200

# 删除用户
@users_bp.route('/users/<int:userId>', methods=['DELETE'])
def delete_user(userId):
    user = User.query.get(userId)
    if user is None:
        abort(404, description="User not found")
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({"message": "User deleted successfully"}), 200