import streamlit as st
import requests
import math
from datetime import datetime

# API URL（更新为你的 Flask 应用的实际 URL）
API_URL = "http://127.0.0.1:5000"

# 设置页面标题和布局
st.set_page_config(page_title="Library Management", layout="centered")

# 页面标题
st.title("📚 图书和借用管理系统")

# 每页显示的项目数量
ITEMS_PER_PAGE = 5

# 初始化分页状态
if "page" not in st.session_state:
    st.session_state.page = 1
if "borrow_page" not in st.session_state:
    st.session_state.borrow_page = 1


# 获取图书数据的函数
def fetch_books():
    try:
        response = requests.get(f"{API_URL}/books")
        if response.status_code == 200:
            return response.json()
        else:
            st.error("无法获取图书列表")
            return []
    except Exception as e:
        st.error(f"请求失败: {e}")
        return []


# 显示分页图书列表
def display_books_page(books):
    total_books = len(books)
    total_pages = max(1, math.ceil(total_books / ITEMS_PER_PAGE))  # 至少有一页

    # 确保页码在有效范围内
    st.session_state.page = min(max(1, st.session_state.page), total_pages)

    # 当前页的起始和终止索引
    start_index = (st.session_state.page - 1) * ITEMS_PER_PAGE
    end_index = start_index + ITEMS_PER_PAGE
    page_books = books[start_index:end_index]

    # 使用 Markdown 表格显示图书数据
    table_md = "| ID | 书名 | 作者 | ISBN | 类别 |\n"
    table_md += "|----|------|------|------|------|\n"
    for book in page_books:
        table_md += f"| {book['bookId']} | {book['title']} | {book['author']} | {book['isbn']} | {book['category']} |\n"
    st.markdown(table_md)

    # 分页按钮
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ 上一页", key="prev", disabled=(st.session_state.page <= 1)):
            st.session_state.page -= 1
    with col3:
        if st.button("下一页 ➡️", key="next", disabled=(st.session_state.page >= total_pages)):
            st.session_state.page += 1

    # 显示当前页码和总页数
    st.write(f"第 {st.session_state.page} 页，共 {total_pages} 页")


# 获取借用记录数据的函数
def fetch_borrows():
    try:
        response = requests.get(f"{API_URL}/borrows")
        if response.status_code == 200:
            return response.json()
        else:
            st.error("无法获取借用记录列表")
            return []
    except Exception as e:
        st.error(f"请求失败: {e}")
        return []


# 显示分页借用记录列表
def display_borrows_page(borrow_records):
    total_borrows = len(borrow_records)
    total_pages = max(1, math.ceil(total_borrows / ITEMS_PER_PAGE))  # 至少有一页

    # 确保页码在有效范围内
    st.session_state.borrow_page = min(max(1, st.session_state.borrow_page), total_pages)

    # 当前页的起始和终止索引
    start_index = (st.session_state.borrow_page - 1) * ITEMS_PER_PAGE
    end_index = start_index + ITEMS_PER_PAGE
    page_borrows = borrow_records[start_index:end_index]

    # 使用 Markdown 表格显示借用记录数据
    table_md = "| Record ID | User ID | Book ID | Borrow Date | Return Date | Status |\n"
    table_md += "|-----------|---------|---------|-------------|-------------|--------|\n"
    for record in page_borrows:
        borrow_date = record['borrowDate'] or "N/A"
        return_date = record['returnDate'] or "N/A"
        table_md += f"| {record['recordId']} | {record['userId']} | {record['bookId']} | {borrow_date} | {return_date} | {record['status']} |\n"
    st.markdown(table_md)

    # 分页按钮
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ 上一页", key="borrow_prev", disabled=(st.session_state.borrow_page <= 1)):
            st.session_state.borrow_page -= 1
    with col3:
        if st.button("下一页 ➡️", key="borrow_next", disabled=(st.session_state.borrow_page >= total_pages)):
            st.session_state.borrow_page += 1

    # 显示当前页码和总页数
    st.write(f"第 {st.session_state.borrow_page} 页，共 {total_pages} 页")


# 图书管理区域
with st.expander("📋 图书列表", expanded=True):
    books = fetch_books()
    if books:
        display_books_page(books)

# 查询特定图书信息
with st.expander("🔍 查询图书"):
    book_id = st.text_input("输入图书 ID", key="search_id")
    if st.button("查询图书", key="search_button"):
        if book_id:
            try:
                response = requests.get(f"{API_URL}/books/{book_id}")
                if response.status_code == 200:
                    book = response.json()
                    st.write(f"**书名:** {book['title']}")
                    st.write(f"**作者:** {book['author']}")
                    st.write(f"**ISBN:** {book['isbn']}")
                    st.write(f"**类别:** {book['category']}")
                elif response.status_code == 404:
                    st.warning("未找到该图书")
                else:
                    st.error("无法查询图书")
            except Exception as e:
                st.error(f"请求失败: {e}")
        else:
            st.warning("请输入图书 ID")
# 添加新图书
with st.expander("➕ 添加新图书"):
    new_title = st.text_input("书名", key="new_title")
    new_author = st.text_input("作者", key="new_author")
    new_isbn = st.text_input("ISBN", key="new_isbn")
    new_category_id = st.text_input("类别 ID", key="new_category_id")

    if st.button("添加图书", key="add_button"):
        if new_title and new_author and new_isbn and new_category_id:
            new_book = {
                "title": new_title,
                "author": new_author,
                "isbn": new_isbn,
                "categoryId": int(new_category_id)
            }
            try:
                response = requests.post(f"{API_URL}/books", json=new_book)
                if response.status_code == 201:
                    st.success(f"图书 '{new_title}' 添加成功!")
                    st.session_state.page = 1  # 添加新图书后重置到第一页
                else:
                    st.error("添加图书失败")
            except Exception as e:
                st.error(f"请求失败: {e}")
        else:
            st.warning("请填写所有图书信息")

# 更新图书信息
with st.expander("📝 更新图书信息"):
    update_book_id = st.text_input("要更新的图书 ID", key="update_id")
    update_title = st.text_input("新书名", key="update_title")

    if st.button("更新图书", key="update_button"):
        if update_book_id and update_title:
            update_data = {"title": update_title}
            try:
                response = requests.put(f"{API_URL}/books/{update_book_id}", json=update_data)
                if response.status_code == 200:
                    st.success(f"图书 ID {update_book_id} 更新成功!")
                elif response.status_code == 404:
                    st.warning("未找到该图书")
                else:
                    st.error("更新图书失败")
            except Exception as e:
                st.error(f"请求失败: {e}")
        else:
            st.warning("请填写图书 ID 和新书名")

# 删除图书
with st.expander("❌ 删除图书"):
    delete_book_id = st.text_input("要删除的图书 ID", key="delete_id")

    if st.button("删除图书", key="delete_button"):
        if delete_book_id:
            try:
                response = requests.delete(f"{API_URL}/books/{delete_book_id}")
                if response.status_code == 204:
                    st.success(f"图书 ID {delete_book_id} 删除成功!")
                    st.session_state.page = 1  # 删除图书后重置到第一页
                elif response.status_code == 404:
                    st.warning("未找到该图书")
                else:
                    st.error("删除图书失败")
            except Exception as e:
                st.error(f"请求失败: {e}")
        else:
            st.warning("请输入图书 ID")

# 借用记录管理区域
with st.expander("📋 借用记录列表", expanded=True):
    borrow_records = fetch_borrows()
    if borrow_records:
        display_borrows_page(borrow_records)

# 创建新借用记录
with st.expander("➕ 创建新的借用记录"):
    new_user_id = st.text_input("用户 ID", key="new_user_id")
    new_book_id = st.text_input("图书 ID", key="new_book_id")

    if st.button("创建借用记录", key="create_borrow"):
        if new_user_id and new_book_id:
            new_borrow = {
                "userId": int(new_user_id),
                "bookId": int(new_book_id)
            }
            try:
                response = requests.post(f"{API_URL}/borrows", json=new_borrow)
                if response.status_code == 201:
                    st.success(f"借用记录创建成功！用户 ID: {new_user_id}, 图书 ID: {new_book_id}")
                    st.session_state.borrow_page = 1  # 创建新记录后重置到第一页
                else:
                    st.error("创建借用记录失败")
            except Exception as e:
                st.error(f"请求失败: {e}")
        else:
            st.warning("请填写用户 ID 和图书 ID")

# 更新借用记录状态为归还
with st.expander("🔄 更新借用状态为归还"):
    return_borrow_id = st.text_input("借用记录 ID", key="return_borrow_id")

    if st.button("归还图书", key="return_borrow"):
        if return_borrow_id:
            try:
                response = requests.put(f"{API_URL}/borrows/{return_borrow_id}/return")
                if response.status_code == 200:
                    st.success(f"借用记录 ID {return_borrow_id} 已更新为归还状态！")
                elif response.status_code == 404:
                    st.warning("未找到该借用记录")
                else:
                    st.error("更新借用记录状态失败")
            except Exception as e:
                st.error(f"请求失败: {e}")
        else:
            st.warning("请输入借用记录 ID")

