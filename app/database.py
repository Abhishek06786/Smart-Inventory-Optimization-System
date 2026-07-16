import sqlite3
import bcrypt

DATABASE_NAME = "inventory.db"


def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# -------------------------------
# Create Table
# -------------------------------
def create_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        product_name TEXT NOT NULL,

        category TEXT NOT NULL,

        stock INTEGER NOT NULL,

        price REAL NOT NULL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,

        email TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()
    conn.close()


# -------------------------------
# Add Product
# -------------------------------
def add_product(product):

    conn = get_connection()
    cursor = conn.cursor()

    # Duplicate Product Check
    cursor.execute(
        """
        SELECT id
        FROM products
        WHERE LOWER(product_name)=LOWER(?)
        AND LOWER(category)=LOWER(?)
        """,
        (
            product.product_name,
            product.category
        )
    )

    if cursor.fetchone():

        conn.close()

        return False

    cursor.execute(
        """
        INSERT INTO products
        (product_name, category, stock, price)

        VALUES (?, ?, ?, ?)
        """,
        (
            product.product_name,
            product.category,
            product.stock,
            product.price
        )
    )

    conn.commit()
    conn.close()

    return True


# -------------------------------
# Get Products (Pagination + Search + Category Filter)
# -------------------------------
def get_products(
    page=1,
    limit=10,
    search="",
    category="All",
    stock_filter="All",
    sort_by="id",
    sort_order="desc"
):

    conn = get_connection()
    cursor = conn.cursor()

    offset = (page - 1) * limit

    allowed_columns = {
        "id": "id",
        "product_name": "product_name",
        "category": "category",
        "stock": "stock",
        "price": "price"
    }

    sort_column = allowed_columns.get(sort_by, "id")
    order = "ASC" if sort_order.lower() == "asc" else "DESC"

    query = """
        SELECT *
        FROM products
        WHERE 1=1
    """

    count_query = """
        SELECT COUNT(*)
        FROM products
        WHERE 1=1
    """

    params = []
    count_params = []

    # Search
    if search:

        keyword = f"%{search}%"

        query += """
            AND (
                product_name LIKE ?
                OR category LIKE ?
            )
        """

        count_query += """
            AND (
                product_name LIKE ?
                OR category LIKE ?
            )
        """

        params.extend([keyword, keyword])
        count_params.extend([keyword, keyword])

    # Category Filter
    if category != "All":

        query += " AND category=?"
        count_query += " AND category=?"

        params.append(category)
        count_params.append(category)

    # Stock Filter
    if stock_filter == "Low":

        query += " AND stock < 10"
        count_query += " AND stock < 10"

    elif stock_filter == "Out":

        query += " AND stock = 0"
        count_query += " AND stock = 0"

    elif stock_filter == "In":

        query += " AND stock >= 10"
        count_query += " AND stock >= 10"

    # Sorting
    query += f" ORDER BY {sort_column} {order}"

    # Pagination
    query += " LIMIT ? OFFSET ?"

    params.extend([limit, offset])

    cursor.execute(query, params)
    products = [dict(row) for row in cursor.fetchall()]

    cursor.execute(count_query, count_params)
    total = cursor.fetchone()[0]

    conn.close()

    return {
        "products": products,
        "total": total,
        "page": page,
        "limit": limit
    }
# -------------------------------
# Get Single Product
# -------------------------------
def get_product(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM products WHERE id=?",
        (id,)
    )

    product = cursor.fetchone()

    conn.close()

    if product:
        return dict(product)

    return None


# -------------------------------
# Update Product
# -------------------------------
def update_product(id, product):

    conn = get_connection()
    cursor = conn.cursor()

    # Duplicate Check (except current product)
    cursor.execute(
        """
        SELECT id
        FROM products
        WHERE LOWER(product_name)=LOWER(?)
        AND LOWER(category)=LOWER(?)
        AND id != ?
        """,
        (
            product.product_name,
            product.category,
            id
        )
    )

    if cursor.fetchone():

        conn.close()

        return False

    cursor.execute(
        """
        UPDATE products

        SET
            product_name=?,
            category=?,
            stock=?,
            price=?

        WHERE id=?
        """,
        (
            product.product_name,
            product.category,
            product.stock,
            product.price,
            id
        )
    )

    conn.commit()
    conn.close()

    return True


# -------------------------------
# Delete Product
# -------------------------------
def delete_product(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM products WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()


# -------------------------------
# Dashboard Statistics
# -------------------------------
def get_dashboard_stats():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM products")
    total_products = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM products WHERE stock < 10")
    low_stock = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM products WHERE stock = 0")
    out_of_stock = cursor.fetchone()[0]

    cursor.execute("""
        SELECT SUM(stock * price)
        FROM products
    """)

    total_value = cursor.fetchone()[0]

    conn.close()

    if total_value is None:
        total_value = 0

    return {
        "total_products": total_products,
        "low_stock": low_stock,
        "out_of_stock": out_of_stock,
        "inventory_value": round(total_value, 2)
    }


# -------------------------------
# Analytics - Products by Category
# -------------------------------
def get_category_data():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            category,
            COUNT(*) AS total_products
        FROM products
        GROUP BY category
        ORDER BY category
    """)

    data = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return data


# -------------------------------
# Analytics - Stock by Category
# -------------------------------
def get_stock_data():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            category,
            SUM(stock) AS total_stock
        FROM products
        GROUP BY category
        ORDER BY category
    """)

    data = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return data


# -------------------------------
# Analytics - Inventory Value
# -------------------------------
def get_inventory_value_data():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            category,
            SUM(stock * price) AS inventory_value
        FROM products
        GROUP BY category
        ORDER BY category
    """)

    data = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return data
# -------------------------------
# Get All Categories
# -------------------------------
def get_all_categories():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT category
        FROM products
        ORDER BY category
    """)

    categories = [row[0] for row in cursor.fetchall()]

    conn.close()

    return categories

# -------------------------------
# Total Categories
# -------------------------------

def get_total_categories():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(DISTINCT category)
        FROM products
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total

def get_low_stock_products():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT product_name, stock
        FROM products
        WHERE stock BETWEEN 1 AND 9
        ORDER BY stock ASC
    """)

    rows = cursor.fetchall()

    conn.close()

    return [

        {

            "product_name": row[0],
            "stock": row[1]

        }

        for row in rows

    ]
# -------------------------------
# Register User
# -------------------------------

def register_user(user):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE email=?",
        (user.email,)
    )

    if cursor.fetchone():

        conn.close()
        return False

    hashed_password = bcrypt.hashpw(
        user.password.encode(),
        bcrypt.gensalt()
    ).decode()

    cursor.execute(
        """
        INSERT INTO users(name,email,password)
        VALUES(?,?,?)
        """,
        (
            user.name,
            user.email,
            hashed_password
        )
    )

    conn.commit()
    conn.close()

    return True


# -------------------------------
# Login User
# -------------------------------

def login_user(user):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE email=?
        """,
        (user.email,)
    )

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return None

    if bcrypt.checkpw(
        user.password.encode(),
        row["password"].encode()
    ):

        return {
            "id": row["id"],
            "name": row["name"],
            "email": row["email"]
        }

    return None


# -------------------------------
# Update Password
# -------------------------------

def update_password(email, new_password):

    conn = get_connection()
    cursor = conn.cursor()

    hashed_password = bcrypt.hashpw(
        new_password.encode(),
        bcrypt.gensalt()
    ).decode()

    cursor.execute(
        """
        UPDATE users
        SET password=?
        WHERE email=?
        """,
        (
            hashed_password,
            email
        )
    )

    conn.commit()

    updated = cursor.rowcount

    conn.close()

    return updated > 0