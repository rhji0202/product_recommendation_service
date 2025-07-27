import sqlite3
from typing import Dict, Any, List
import os
from google.adk.tools import ToolContext

def get_db_connection():
    try:
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../data/product_recommendation.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        raise

def search_product_by_keyword(keywords: List[str], tool_context: ToolContext) -> Dict[str, Any]:
    print(f"search_product_by_keyword: {keywords}")

    conn = get_db_connection()
    cursor = conn.cursor()

    # 키워드를 포함하는 상품 검색 (LIKE 사용하여 부분 매칭)
    query = "SELECT * FROM products WHERE "

    # OR 조건으로 검색
    where_conditions: List[str] = []
    params: List[str] = []
    for keyword in keywords:
        where_conditions.append("product_name LIKE ?")
        params.append(f"%{keyword}%")
        where_conditions.append("summary_description LIKE ?")
        params.append(f"%{keyword}%")        

    where_clause = " OR ".join(where_conditions)
    query += f" {where_clause} ORDER BY product_name"

    cursor.execute(query, params)
    products = cursor.fetchall()

    # 검색 결과 가져오기
    conn.close()

    print(f"products: {products}")

    result = []
    for product in products:
        result.append({
            "id": product["product_no"],
            "product_name": product["product_name"],
            "summary_description": product["summary_description"],
            "model_name": product["model_name"],
            "brand_name": product["brand_name"],
            "price": product["price"]
        })

    tool_context.state["products"] = result
    return {"status": "success", "total_count": len(products), "products": result}