import random
from faker import Faker
from datetime import datetime, timedelta

# 初始化 Faker 库
fake = Faker()

# 生成用户数据的 SQL 插入语句
def generate_user_sql(num_users):
    sql_statements = []
    for _ in range(num_users):
        name = fake.name()
        contact = fake.phone_number()
        identity = random.choice(['管理员', '普通用户'])
        password = fake.password()
        
        sql = f"INSERT INTO User (name, contact, identity, password) VALUES ('{name}', '{contact}', '{identity}', '{password}');"
        sql_statements.append(sql)
    
    return sql_statements

# 生成图书类别数据的 SQL 插入语句
def generate_category_sql(num_categories):
    sql_statements = []
    categories = ["计算机科学", "文学", "历史", "艺术", "数学", "自然科学"]
    for i in range(num_categories):
        category_name = random.choice(categories)
        sql = f"INSERT INTO Category (name) VALUES ('{category_name}');"
        sql_statements.append(sql)
    
    return sql_statements

# 生成图书数据的 SQL 插入语句
def generate_book_sql(num_books, num_categories):
    sql_statements = []
    for _ in range(num_books):
        title = fake.sentence(nb_words=4)
        author = fake.name()
        isbn = fake.isbn13()
        category_id = random.randint(1, num_categories)
        
        sql = f"INSERT INTO Book (title, author, isbn, categoryId) VALUES ('{title}', '{author}', '{isbn}', {category_id});"
        sql_statements.append(sql)
    
    return sql_statements

# 生成借阅记录数据的 SQL 插入语句
def generate_borrow_record_sql(num_records, num_users, num_books):
    sql_statements = []
    for _ in range(num_records):
        user_id = random.randint(1, num_users)
        book_id = random.randint(1, num_books)
        borrow_date = fake.date_this_year(before_today=True, after_today=False)
        return_date = borrow_date + timedelta(days=random.randint(5, 30))  # 归还时间为借用时间后 5 到 30 天
        status = random.choice(['借出', '已归还'])
        
        sql = f"INSERT INTO BorrowRecord (userId, bookId, borrowDate, returnDate, status) VALUES ({user_id}, {book_id}, '{borrow_date}', '{return_date}', '{status}');"
        sql_statements.append(sql)
    
    return sql_statements

# 写入 SQL 插入语句到文件
def write_to_sql_file(file_name, sql_statements):
    with open(file_name, 'w', encoding='utf-8') as f:
        for statement in sql_statements:
            f.write(statement + '\n')
    print(f"SQL 插入语句已写入文件: {file_name}")

# 生成数据并写入 SQL 文件
def generate_sql_data():
    num_users = 50  # 模拟 50 个用户
    num_categories = 6  # 模拟 6 个图书类别
    num_books = 200  # 模拟 200 本图书
    num_borrow_records = 500  # 模拟 500 条借阅记录

    # 生成 SQL 插入语句
    user_sql = generate_user_sql(num_users)
    category_sql = generate_category_sql(num_categories)
    book_sql = generate_book_sql(num_books, num_categories)
    borrow_record_sql = generate_borrow_record_sql(num_borrow_records, num_users, num_books)

    # 合并所有插入语句
    all_sql_statements = user_sql + category_sql + book_sql + borrow_record_sql

    # 写入到 SQL 文件
    write_to_sql_file('insert_data.sql', all_sql_statements)

# 执行生成 SQL 插入语句
if __name__ == "__main__":
    generate_sql_data()
