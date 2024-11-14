-- 创建 User 表
CREATE TABLE User (
    userId INT AUTO_INCREMENT PRIMARY KEY,       -- 用户ID，自增
    name VARCHAR(100) NOT NULL,                  -- 姓名
    contact VARCHAR(100),                        -- 联系方式
    identity ENUM('管理员', '普通用户') NOT NULL, -- 用户身份，枚举类型
    password VARCHAR(255) NOT NULL               -- 密码
);

-- 创建 Category 表
CREATE TABLE Category (
    categoryId INT AUTO_INCREMENT PRIMARY KEY,   -- 图书类别ID，自增
    name VARCHAR(100) NOT NULL                   -- 类别名称
);

-- 创建 Book 表
CREATE TABLE Book (
    bookId INT AUTO_INCREMENT PRIMARY KEY,       -- 图书ID，自增
    categoryId INT,                              -- 图书类别ID
    title VARCHAR(255) NOT NULL,                 -- 书名
    author VARCHAR(255),                         -- 作者
    isbn VARCHAR(20),                            -- ISBN
    FOREIGN KEY (categoryId) REFERENCES Category(categoryId) ON DELETE SET NULL  -- 外键约束，关联到Category表
);

-- 创建 BorrowRecord 表
CREATE TABLE BorrowRecord (
    recordId INT AUTO_INCREMENT PRIMARY KEY,     -- 借用ID，自增
    userId INT,                                  -- 用户ID
    bookId INT,                                  -- 图书ID
    borrowDate DATE NOT NULL,                    -- 借用时间
    returnDate DATE,                             -- 归还时间
    status ENUM('借出', '已归还') NOT NULL,      -- 借用状态
    FOREIGN KEY (userId) REFERENCES User(userId) ON DELETE CASCADE,  -- 外键约束，关联到User表
    FOREIGN KEY (bookId) REFERENCES Book(bookId) ON DELETE CASCADE   -- 外键约束，关联到Book表
);
