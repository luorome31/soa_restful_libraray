import mysql.connector
from faker import Faker
import random
from datetime import datetime, timedelta
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,  # 记录 INFO 级别以上的日志
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # 输出到控制台
        logging.FileHandler("library_management.log", mode='a')  # 输出到文件
    ]
)

# 初始化 Faker 库
fake = Faker()

# 创建数据库连接
def create_connection():
    try:
        conn = mysql.connector.connect(
            host="106.54.229.203",        # 数据库主机地址
            user="root",             # 数据库用户名
            password="",# 数据库密码
            database="restful",    # 目标数据库
            port=3310                     # 设置 MySQL 连接端口为 3310

        )
        logging.info("数据库连接成功")
        return conn
    except mysql.connector.Error as err:
        logging.error(f"数据库连接失败: {err}")
        raise

# 插入用户数据
def insert_user(cursor, num_users):
    logging.info(f"开始插入 {num_users} 条用户数据...")
    for _ in range(num_users):
        name = fake.name()
        contact = fake.phone_number()
        identity = random.choice(['管理员', '普通用户'])
        password = fake.password()
        
        try:
            cursor.execute("""
                INSERT INTO User (name, contact, identity, password)
                VALUES (%s, %s, %s, %s)
            """, (name, contact, identity, password))
            logging.debug(f"成功插入用户: {name}")
        except mysql.connector.Error as err:
            logging.error(f"插入用户失败: {err}")
            continue  # 继续插入其他数据

# 插入图书类别数据
def insert_category(cursor, num_categories):
    logging.info(f"开始插入 {num_categories} 条图书类别数据...")
    categories = ["计算机科学", "文学", "历史", "艺术", "数学", "自然科学"]
    for i in range(num_categories):
        category_name = random.choice(categories)
        try:
            cursor.execute("""
                INSERT INTO Category (name)
                VALUES (%s)
            """, (category_name,))
            logging.debug(f"成功插入类别: {category_name}")
        except mysql.connector.Error as err:
            logging.error(f"插入类别失败: {err}")
            continue

# 插入图书数据
def insert_book(cursor, num_books, num_categories):
    logging.info(f"开始插入 {num_books} 条图书数据...")
    for _ in range(num_books):
        title = fake.sentence(nb_words=4)
        author = fake.name()
        isbn = fake.isbn13()
        category_id = random.randint(1, num_categories)
        
        try:
            cursor.execute("""
                INSERT INTO Book (title, author, isbn, categoryId)
                VALUES (%s, %s, %s, %s)
            """, (title, author, isbn, category_id))
            logging.debug(f"成功插入书籍: {title}")
        except mysql.connector.Error as err:
            logging.error(f"插入书籍失败: {err}")
            continue

# 插入借阅记录数据
def insert_borrow_record(cursor, num_records, num_users, num_books):
    logging.info(f"开始插入 {num_records} 条借阅记录数据...")
    for _ in range(num_records):
        user_id = random.randint(1, num_users)
        book_id = random.randint(1, num_books)
        borrow_date = fake.date_this_year(before_today=True, after_today=False)
        return_date = borrow_date + timedelta(days=random.randint(5, 30))  # 归还时间为借用时间后 5 到 30 天
        status = random.choice(['借出', '已归还'])

        try:
            cursor.execute("""
                INSERT INTO BorrowRecord (userId, bookId, borrowDate, returnDate, status)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, book_id, borrow_date, return_date, status))
            logging.debug(f"成功插入借阅记录: 用户 {user_id} 借阅了书籍 {book_id}")
        except mysql.connector.Error as err:
            logging.error(f"插入借阅记录失败: {err}")
            continue

def main():
    # 连接数据库
    conn = None
    cursor = None
    try:
        conn = create_connection()
        cursor = conn.cursor()

        # 插入数据
        num_users = 50  # 模拟 50 个用户
        num_categories = 6  # 模拟 6 个图书类别
        num_books = 200  # 模拟 200 本图书
        num_borrow_records = 500  # 模拟 500 条借阅记录

        insert_category(cursor, num_categories)
        insert_user(cursor, num_users)
        insert_book(cursor, num_books, num_categories)
        insert_borrow_record(cursor, num_borrow_records, num_users, num_books)

        # 提交事务
        conn.commit()
        logging.info("数据插入完成，已提交事务")

    except mysql.connector.Error as err:
        logging.error(f"数据库操作失败: {err}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        logging.info("数据库连接已关闭")

if __name__ == "__main__":
    main()
