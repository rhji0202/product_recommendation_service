import sqlite3
import os
import json
from datetime import datetime

def create_database():
    # 데이터베이스 파일 경로
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
    os.makedirs(db_path, exist_ok=True)
    db_file = os.path.join(db_path, 'product_recommendation.db')
    
    # 데이터베이스 연결
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # 카테고리 테이블 생성 (Cafe24 API 참조)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        shop_no INTEGER NOT NULL DEFAULT 1,
        category_no INTEGER PRIMARY KEY,
        category_depth INTEGER NOT NULL,
        parent_category_no INTEGER,
        category_name TEXT NOT NULL,
        root_category_no INTEGER,
        use_display TEXT DEFAULT 'T',
        display_order INTEGER DEFAULT 0,
        hash_tags TEXT,
        created_at TEXT,
        updated_at TEXT
    )
    ''')
    
    # 상품 테이블 생성 (Cafe24 API 참조)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        product_no INTEGER PRIMARY KEY,
        shop_no INTEGER NOT NULL DEFAULT 1,
        mall_id TEXT,
        product_code TEXT,
        custom_product_code TEXT,
        product_name TEXT NOT NULL,
        eng_product_name TEXT,
        price REAL NOT NULL,
        retail_price REAL,
        price_excluding_tax REAL,
        tax REAL,
        simple_description TEXT,
        summary_description TEXT,
        translated_additional_description TEXT,
        manufacturer_name TEXT,
        supplier_name TEXT,
        brand_name TEXT,
        model_name TEXT,
        trend_name TEXT,
        origin_place_value TEXT,
        category_no INTEGER,
        shipping_scope TEXT,
        shipping_method TEXT,
        shipping_fee_type TEXT,
        shipping_fee REAL,
        shipping_rates TEXT,
        stock_quantity INTEGER DEFAULT 0,
        review_count INTEGER DEFAULT 0,
        question_count INTEGER DEFAULT 0,
        product_article_count INTEGER DEFAULT 0,
        color TEXT,
        expiration_date TEXT,
        promotion_period TEXT,
        created_date TEXT,
        updated_date TEXT,
        FOREIGN KEY (category_no) REFERENCES categories(category_no)
    )
    ''')
    
    # 상품 포인트 테이블 생성
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS product_points (
        point_id INTEGER PRIMARY KEY,
        product_no INTEGER NOT NULL,
        payment_method TEXT NOT NULL,
        type TEXT NOT NULL,
        value REAL NOT NULL,
        rate REAL,
        created_at TEXT,
        updated_at TEXT,
        FOREIGN KEY (product_no) REFERENCES products(product_no)
    )
    ''')
    
    # 상품 옵션 테이블 생성
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS product_options (
        option_id INTEGER PRIMARY KEY,
        product_no INTEGER NOT NULL,
        option_code TEXT NOT NULL,
        option_name TEXT NOT NULL,
        option_value TEXT NOT NULL,
        option_display TEXT DEFAULT 'T',
        created_at TEXT,
        updated_at TEXT,
        FOREIGN KEY (product_no) REFERENCES products(product_no)
    )
    ''')
    
    # 상품 옵션 값 테이블 생성
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS product_option_values (
        value_id INTEGER PRIMARY KEY,
        option_id INTEGER NOT NULL,
        value_no INTEGER NOT NULL,
        value_name TEXT NOT NULL,
        additional_price REAL DEFAULT 0,
        FOREIGN KEY (option_id) REFERENCES product_options(option_id)
    )
    ''')
    
    # 상품 품목(variants) 테이블 생성
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS product_variants (
        variant_id INTEGER PRIMARY KEY,
        product_no INTEGER NOT NULL,
        variants_code TEXT NOT NULL,
        options TEXT,
        additional_price REAL DEFAULT 0,
        stock_quantity INTEGER DEFAULT 0,
        display TEXT DEFAULT 'T',
        selling TEXT DEFAULT 'T',
        created_at TEXT,
        updated_at TEXT,
        FOREIGN KEY (product_no) REFERENCES products(product_no)
    )
    ''')
    
    # 사용자 테이블 생성
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        shop_no INTEGER NOT NULL DEFAULT 1,
        username TEXT NOT NULL UNIQUE,
        email TEXT UNIQUE,
        created_at TEXT,
        updated_at TEXT
    )
    ''')
    
    # 장바구니 테이블 생성 (Cafe24 API 참조)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS carts (
        cart_id INTEGER PRIMARY KEY,
        shop_no INTEGER NOT NULL DEFAULT 1,
        user_id INTEGER,
        session_id TEXT,
        basket_type TEXT DEFAULT 'A0000',
        created_at TEXT,
        updated_at TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    ''')
    
    conn.commit()
    return conn, cursor

def insert_sample_data(conn, cursor):
    current_time = datetime.now().isoformat()
    
    # 카테고리 샘플 데이터 추가 (제공된 JSON 형식 참조)
    categories = [
        (1, 27, 1, 1, "(large scale classification) Bottoms", 27, "T", 0, json.dumps(["tag1", "tag2"]), current_time, current_time),
        (1, 28, 1, 1, "(large scale classification) Accessories", 28, "T", 0, json.dumps(["tag1", "tag2"]), current_time, current_time),
        (1, 29, 2, 27, "Jeans", 27, "T", 0, json.dumps(["denim", "casual"]), current_time, current_time),
        (1, 30, 2, 27, "Slacks", 27, "T", 0, json.dumps(["formal", "office"]), current_time, current_time),
        (1, 31, 2, 28, "Bags", 28, "T", 0, json.dumps(["fashion", "carry"]), current_time, current_time),
        (1, 32, 2, 28, "Hats", 28, "T", 0, json.dumps(["cap", "headwear"]), current_time, current_time),
        (1, 33, 1, 1, "Electronics", 33, "T", 0, json.dumps(["tech", "gadgets"]), current_time, current_time),
        (1, 34, 2, 33, "Smartphones", 33, "T", 0, json.dumps(["mobile", "phones"]), current_time, current_time)
    ]
    
    cursor.executemany('''
    INSERT OR REPLACE INTO categories (
        shop_no, category_no, category_depth, parent_category_no, 
        category_name, root_category_no, use_display, display_order, 
        hash_tags, created_at, updated_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', categories)
    
    # 사용자 샘플 데이터 추가
    users = [
        (1, 1, 'user1', 'user1@example.com', current_time, current_time),
        (1, 2, 'user2', 'user2@example.com', current_time, current_time),
        (1, 3, 'user3', 'user3@example.com', current_time, current_time)
    ]
    
    cursor.executemany('''
    INSERT OR REPLACE INTO users (shop_no, user_id, username, email, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', users)
    
    # 상품 샘플 데이터 추가
    products = [
        (1001, 1, 'ectque005', 'P1001', 'CP1001', '클래식 청바지', None, 59000, 70000, 50000, 9000, 
         '편안한 착용감', '클래식 청바지', None, '리바이스 코리아', '리바이스 공급사', '리바이스', 'CL-001', '트렌디', 
         '한국', 29, '국내배송', '택배', 'R', 2500, None, 100, 5, 0, 0, 
         json.dumps(["#000000", "#0000FF"]), None, None, current_time, current_time),
        
        (1002, 1, 'ectque005', 'P1002', 'CP1002', '슬림핏 슬랙스', None, 45000, 55000, 40000, 5000, 
         '세련된 디자인', '슬림핏 슬랙스', None, '자라 코리아', '자라 공급사', '자라', 'SL-002', '오피스룩', 
         '한국', 30, '국내배송', '택배', 'R', 2500, None, 80, 3, 0, 0, 
         json.dumps(["#000000", "#808080"]), None, None, current_time, current_time),
        
        (1003, 1, 'ectque005', 'P1003', 'CP1003', '가죽 크로스백', None, 89000, 99000, 80000, 9000, 
         '고급 가죽', '가죽 크로스백', None, '코치 코리아', '코치 공급사', '코치', 'CB-003', '럭셔리', 
         '미국', 31, '국내/해외배송', '택배', 'R', 2500, None, 50, 8, 0, 0, 
         json.dumps(["#000000", "#8B4513"]), None, None, current_time, current_time),
        
        (1004, 1, 'ectque005', 'P1004', 'CP1004', '베이직 볼캡', None, 25000, 30000, 22000, 3000, 
         '심플한 디자인', '베이직 볼캡', None, '뉴에라 코리아', '뉴에라 공급사', '뉴에라', 'BC-004', '캐주얼', 
         '중국', 32, '국내배송', '택배', 'R', 2500, None, 120, 2, 0, 0, 
         json.dumps(["#000000", "#FFFFFF", "#FF0000"]), None, None, current_time, current_time),
        
        (20, 1, 'ectque005', 'P000000X', '', 'iPhone X', 'iPhone Ten', 11000, 0, 10000, 1000, 
         'This is Product Description.', 'This is Product Summary.', 'This is a translated additional description of product.', 
         'APPLE', 'SUPPLIER NAME', '', 'A1865', '', 'Korea', 34, 'Domestic/International shipping', 'Courier Service', 
         'R', 2500, None, 10, 0, 0, 0, json.dumps(["#000000", "#C20F0A"]), 
         json.dumps({"start_date": "2019-07-08", "end_date": "2019-09-14"}), 
         json.dumps({"start_date": "2019-07-11T00:00:00+09:00", "end_date": "2019-07-16T23:55:00+09:00", "dc_price": "220"}), 
         current_time, current_time),
        
        (21, 1, 'ectque005', 'P000000X', '', 'iPhone X', 'iPhone Ten', 11000, 0, 10000, 1000, 
         'This is Product Description.', 'This is Product Summary.', 'This is a translated additional description of product.', 
         'APPLE', 'SUPPLIER NAME', '', 'A1865', '', 'Korea', 34, 'Domestic/International shipping', 'Courier Service', 
         'W', None, json.dumps([
             {"shipping_rates_min": "1.00", "shipping_rates_max": "2.00", "shipping_fee": "2500.00"},
             {"shipping_rates_min": "2.00", "shipping_rates_max": "3.00", "shipping_fee": "3000.00"}
         ]), 10, 0, 0, 0, json.dumps(["#000000", "#C20F0A"]), 
         json.dumps({"start_date": "2019-07-08", "end_date": "2019-09-14"}), 
         json.dumps({"start_date": "2019-07-11T00:00:00+09:00", "end_date": "2019-07-16T23:55:00+09:00", "dc_price": "220.00"}), 
         current_time, current_time)
    ]
    
    cursor.executemany('''
    INSERT OR REPLACE INTO products (
        product_no, shop_no, mall_id, product_code, custom_product_code, product_name, 
        eng_product_name, price, retail_price, price_excluding_tax, tax, 
        simple_description, summary_description, translated_additional_description, 
        manufacturer_name, supplier_name, brand_name, model_name, trend_name, 
        origin_place_value, category_no, shipping_scope, shipping_method, 
        shipping_fee_type, shipping_fee, shipping_rates, stock_quantity, 
        review_count, question_count, product_article_count, color, 
        expiration_date, promotion_period, created_date, updated_date
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', products)
    
    # 상품 포인트 샘플 데이터 추가
    points = [
        (1, 20, 'card', 'P', 110.00, 10.00, current_time, current_time),
        (2, 20, 'cash', 'W', 100.00, None, current_time, current_time),
        (3, 21, 'mileage', 'W', 100.00, None, current_time, current_time)
    ]
    
    cursor.executemany('''
    INSERT OR REPLACE INTO product_points (
        point_id, product_no, payment_method, type, value, rate, created_at, updated_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', points)
    
    # 상품 옵션 샘플 데이터 추가
    options = [
        (1, 1001, 'OPT_SIZE', '사이즈', '사이즈 선택', 'T', current_time, current_time),
        (2, 1001, 'OPT_COLOR', '색상', '색상 선택', 'T', current_time, current_time),
        (3, 1002, 'OPT_SIZE', '사이즈', '사이즈 선택', 'T', current_time, current_time),
        (4, 1002, 'OPT_COLOR', '색상', '색상 선택', 'T', current_time, current_time),
        (5, 1003, 'OPT_COLOR', '색상', '색상 선택', 'T', current_time, current_time),
        (6, 1004, 'OPT_SIZE', '사이즈', '사이즈 선택', 'T', current_time, current_time),
        (7, 1004, 'OPT_COLOR', '색상', '색상 선택', 'T', current_time, current_time),
        (8, 20, 'OPT_COLOR', '색상', '색상 선택', 'T', current_time, current_time),
        (9, 21, 'OPT_COLOR', '색상', '색상 선택', 'T', current_time, current_time)
    ]
    
    cursor.executemany('''
    INSERT OR REPLACE INTO product_options (
        option_id, product_no, option_code, option_name, option_value, 
        option_display, created_at, updated_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', options)
    
    # 옵션 값 샘플 데이터 추가
    option_values = [
        (1, 1, 1, '28', 0),
        (2, 1, 2, '30', 0),
        (3, 1, 3, '32', 0),
        (4, 1, 4, '34', 2000),
        (5, 2, 1, '블루', 0),
        (6, 2, 2, '블랙', 0),
        (7, 3, 1, '28', 0),
        (8, 3, 2, '30', 0),
        (9, 3, 3, '32', 0),
        (10, 4, 1, '그레이', 0),
        (11, 4, 2, '네이비', 0),
        (12, 5, 1, '블랙', 0),
        (13, 5, 2, '브라운', 0),
        (14, 6, 1, 'FREE', 0),
        (15, 7, 1, '블랙', 0),
        (16, 7, 2, '화이트', 0),
        (17, 7, 3, '레드', 0),
        (18, 8, 1, 'Black', 0),
        (19, 8, 2, 'Red', 0),
        (20, 9, 1, 'Black', 0),
        (21, 9, 2, 'Red', 0)
    ]
    
    cursor.executemany('''
    INSERT OR REPLACE INTO product_option_values (
        value_id, option_id, value_no, value_name, additional_price
    )
    VALUES (?, ?, ?, ?, ?)
    ''', option_values)
    
    # 상품 품목(variants) 샘플 데이터 추가
    variants = [
        (1, 1001, 'V1001-1', json.dumps([{"option_code": "OPT_SIZE", "value_no": 1}, {"option_code": "OPT_COLOR", "value_no": 1}]), 0, 20, 'T', 'T', current_time, current_time),
        (2, 1001, 'V1001-2', json.dumps([{"option_code": "OPT_SIZE", "value_no": 1}, {"option_code": "OPT_COLOR", "value_no": 2}]), 0, 15, 'T', 'T', current_time, current_time),
        (3, 1001, 'V1001-3', json.dumps([{"option_code": "OPT_SIZE", "value_no": 2}, {"option_code": "OPT_COLOR", "value_no": 1}]), 0, 25, 'T', 'T', current_time, current_time),
        (4, 1001, 'V1001-4', json.dumps([{"option_code": "OPT_SIZE", "value_no": 2}, {"option_code": "OPT_COLOR", "value_no": 2}]), 0, 20, 'T', 'T', current_time, current_time),
        (5, 1002, 'V1002-1', json.dumps([{"option_code": "OPT_SIZE", "value_no": 1}, {"option_code": "OPT_COLOR", "value_no": 1}]), 0, 15, 'T', 'T', current_time, current_time),
        (6, 1002, 'V1002-2', json.dumps([{"option_code": "OPT_SIZE", "value_no": 2}, {"option_code": "OPT_COLOR", "value_no": 2}]), 0, 10, 'T', 'T', current_time, current_time),
        (7, 1003, 'V1003-1', json.dumps([{"option_code": "OPT_COLOR", "value_no": 1}]), 0, 25, 'T', 'T', current_time, current_time),
        (8, 1003, 'V1003-2', json.dumps([{"option_code": "OPT_COLOR", "value_no": 2}]), 5000, 15, 'T', 'T', current_time, current_time),
        (9, 1004, 'V1004-1', json.dumps([{"option_code": "OPT_SIZE", "value_no": 1}, {"option_code": "OPT_COLOR", "value_no": 1}]), 0, 30, 'T', 'T', current_time, current_time),
        (10, 1004, 'V1004-2', json.dumps([{"option_code": "OPT_SIZE", "value_no": 1}, {"option_code": "OPT_COLOR", "value_no": 2}]), 0, 25, 'T', 'T', current_time, current_time),
        (11, 1004, 'V1004-3', json.dumps([{"option_code": "OPT_SIZE", "value_no": 1}, {"option_code": "OPT_COLOR", "value_no": 3}]), 2000, 20, 'T', 'T', current_time, current_time),
        (12, 20, 'V20-1', json.dumps([{"option_code": "OPT_COLOR", "value_no": 1}]), 0, 5, 'T', 'T', current_time, current_time),
        (13, 20, 'V20-2', json.dumps([{"option_code": "OPT_COLOR", "value_no": 2}]), 0, 5, 'T', 'T', current_time, current_time),
        (14, 21, 'V21-1', json.dumps([{"option_code": "OPT_COLOR", "value_no": 1}]), 0, 5, 'T', 'T', current_time, current_time),
        (15, 21, 'V21-2', json.dumps([{"option_code": "OPT_COLOR", "value_no": 2}]), 0, 5, 'T', 'T', current_time, current_time)
    ]
    
    cursor.executemany('''
    INSERT OR REPLACE INTO product_variants (
        variant_id, product_no, variants_code, options, additional_price,
        stock_quantity, display, selling, created_at, updated_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', variants)
    
    # 장바구니 샘플 데이터 추가
    carts = [
        (1, 1, 1, 'session1', 'A0000', current_time, current_time),
        (2, 1, 2, 'session2', 'A0000', current_time, current_time),
        (3, 1, 3, 'session3', 'A0001', current_time, current_time)
    ]
    
    cursor.executemany('''
    INSERT OR REPLACE INTO carts (
        cart_id, shop_no, user_id, session_id, basket_type, created_at, updated_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', carts)
    
    conn.commit()

def main():
    print("초기 데이터베이스 설정을 시작합니다...")
    conn, cursor = create_database()
    print("테이블이 성공적으로 생성되었습니다.")
    
    insert_sample_data(conn, cursor)
    print("샘플 데이터가 성공적으로 추가되었습니다.")
    
    # 데이터베이스 연결 종료
    cursor.close()
    conn.close()
    print("데이터베이스 설정이 완료되었습니다.")

if __name__ == "__main__":
    main()
