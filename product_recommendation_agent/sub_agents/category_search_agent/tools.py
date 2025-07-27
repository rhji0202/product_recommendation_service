import sqlite3
import os
import json
import ast
from typing import List
from google.adk.tools import ToolContext

def get_db_connection():
    """데이터베이스 연결을 생성하고 반환합니다."""
    try:
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../data/product_recommendation.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        raise

from typing import Dict, Any

def search_category_by_keyword(keywords: List[str], tool_context: ToolContext) -> Dict[str, Any]:
    print(f"search_category_by_keyword: {keywords}")
    """
    키워드를 기반으로 카테고리를 검색합니다.
    
    Args:
        keywords: 검색할 키워드 리스트
        
    Returns:
        Dict[str, Any]: Dictionary with categories in a structured for ADK
    """

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # 키워드를 포함하는 카테고리 검색 (LIKE 사용하여 부분 매칭)
        # 여러 키워드에 대해 OR 조건으로 검색
        where_conditions: List[str] = []
        params: List[str] = []
        
        for keyword in keywords:
            # 대소문자 구분 없이 검색하기 위해 LOWER 사용
            where_conditions.append("category_name LIKE ?")
            params.append(f"%{keyword}%")
            
            # 해시태그에서도 키워드 검색
            where_conditions.append("hash_tags LIKE ?")
            params.append(f"%{keyword}%")
        
        where_clause = " OR ".join(where_conditions)
        
        query = f"""
            SELECT 
                category_no,
                category_name,
                full_category_name,
                full_category_no,
                category_depth,
                parent_category_no,
                root_category_no,
                hash_tags
            FROM categories
            WHERE ({where_clause}) AND use_display = 'T'
            ORDER BY category_depth, display_order
        """
        
        print(f"Executing query: {query}")
        print(f"With params: {params}")
        
        cursor.execute(query, params)
        
        categories: List[Dict[str, Any]] = []
        for row in cursor.fetchall():
            print(f"Found category: {row['category_name']}")
            hash_tags = []
            if row['hash_tags']:
                try:
                    # 먼저 JSON으로 파싱 시도
                    hash_tags = json.loads(row['hash_tags'])
                except json.JSONDecodeError:
                    try:
                        # JSON이 실패하면 Python 리스트 문자열로 파싱 시도 (ast.literal_eval 사용)
                        hash_tags = ast.literal_eval(row['hash_tags'])
                        if not isinstance(hash_tags, list):
                            hash_tags = [str(hash_tags)]
                    except (SyntaxError, ValueError):
                        # 모든 파싱이 실패하면 단순 문자열로 처리
                        hash_tags = [row['hash_tags']]
                    
            categories.append({
                'category_no': row['category_no'],
                'category_name': row['category_name'],
                'category_depth': row['category_depth'],
                'parent_category_no': row['parent_category_no'],
                'root_category_no': row['root_category_no'],
                'hash_tags': hash_tags
            })
        
        print(f"Found {len(categories)} categories")
        tool_context.state["categories"] = categories
        return {
            "status": "success",
            "total_count": len(categories),
            "categories": categories
        }
    
    except Exception as e:
        print(f"Error during database operation: {e}")
        return {"status": "error", "message": str(e)}
    finally:
        if conn:
            conn.close()
