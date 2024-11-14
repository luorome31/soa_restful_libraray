from extensions import db
class User(db.Model):
    __tablename__ = 'User'  # 注意表名需要与数据库中的表名完全一致
    userId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    contact = db.Column(db.String(255), nullable=False)
    identity = db.Column(db.String(50), nullable=False)  # 管理员 or 普通用户
    password = db.Column(db.String(255), nullable=False)

# 定义 Category 表
class Category(db.Model):
    __tablename__ = 'Category'  # 与数据库中的表名一致
    categoryId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)

# 定义 Book 表
class Book(db.Model):
    __tablename__ = 'Book'  # 与数据库中的表名一致
    bookId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    categoryId = db.Column(db.Integer, db.ForeignKey('Category.categoryId'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    isbn = db.Column(db.String(255), nullable=False)
    
    category = db.relationship('Category', back_populates='books')

# 定义 BorrowRecord 表
class BorrowRecord(db.Model):
    __tablename__ = 'BorrowRecord'  # 与数据库中的表名一致
    recordId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer, db.ForeignKey('User.userId'), nullable=False)
    bookId = db.Column(db.Integer, db.ForeignKey('Book.bookId'), nullable=False)
    borrowDate = db.Column(db.DateTime, nullable=False)
    returnDate = db.Column(db.DateTime)
    status = db.Column(db.String(50), nullable=False)  # 状态: 归还, 未归还
    
    user = db.relationship('User', back_populates='borrowed_books')
    book = db.relationship('Book', back_populates='borrowed_books')

# 定义反向关系
Category.books = db.relationship('Book', back_populates='category')
User.borrowed_books = db.relationship('BorrowRecord', back_populates='user')
Book.borrowed_books = db.relationship('BorrowRecord', back_populates='book')
