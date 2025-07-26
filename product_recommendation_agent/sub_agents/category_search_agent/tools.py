import sqlite3
import os
import json
from typing import List

def get_db_connection():
    """데이터베이스 연결을 생성하고 반환합니다."""
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../data/product_recommendation.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def search_category_by_keyword(keywords: List[str]):
    print(f"search_category_by_keyword: {keywords}")
    """
    키워드를 기반으로 카테고리를 검색합니다.
    
    Args:
        keywords: 검색할 키워드 리스트
        
    Returns:
        List[{
            "category_no": int,
            "category_name": str,
            "category_depth": int,
            "parent_category_no": int,
            "root_category_no": int,
            "hash_tags": List[str]
        }]
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 키워드를 포함하는 카테고리 검색
    search_query = f"%{keywords[0]}%"
    cursor.execute("""
        SELECT 
            category_no,
            category_name,
            category_depth,
            parent_category_no,
            root_category_no,
            hash_tags
        FROM categories
        WHERE category_name IN (?) AND use_display = 'T'
        ORDER BY category_depth, display_order
    """, (search_query,))
    
    categories = []
    for row in cursor.fetchall():
        hash_tags = []
        if row['hash_tags']:
            try:
                hash_tags = json.loads(row['hash_tags'])
            except json.JSONDecodeError:
                pass
                
        categories.append({
            'category_no': row['category_no'],
            'category_name': row['category_name'],
            'category_depth': row['category_depth'],
            'parent_category_no': row['parent_category_no'],
            'root_category_no': row['root_category_no'],
            'hash_tags': hash_tags
        })
    
    conn.close()
    return categories
