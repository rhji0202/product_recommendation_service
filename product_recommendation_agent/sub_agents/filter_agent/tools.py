from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from google.adk.tools import ToolContext

class FilterCriteria(BaseModel):
    min_price: Optional[int] = None
    max_price: Optional[int] = None
    brands: Optional[List[str]] = None
    model_names: Optional[List[str]] = None
    keywords: Optional[List[str]] = None

def filter_products(products: List[Dict[str, Any]], tool_context: ToolContext, filter_criteria: dict) -> Dict[str, Any]:
    """
    제공된 필터 기준에 따라 상품 목록을 필터링합니다.
    
    Args:
        products: 필터링할 상품 목록
        filter_criteria: 필터링 기준 (딕셔너리)
        
    Returns:
        Dict[str, Any]: 필터링된 상품 목록과 메타데이터
    """
    filtered_products = []
    
    # 필터 기준을 FilterCriteria 객체로 변환
    criteria = FilterCriteria(**filter_criteria) if filter_criteria else FilterCriteria()
    
    for product in products:
        # 모든 필터 조건을 만족하는지 확인
        meets_criteria = True
        
        # 가격 필터링
        if criteria.min_price is not None and product.get("price", 0) < criteria.min_price:
            meets_criteria = False
        
        if criteria.max_price is not None and product.get("price", 0) > criteria.max_price:
            meets_criteria = False
        
        # 브랜드 필터링
        if criteria.brands and product.get("brand_name") not in criteria.brands:
            meets_criteria = False
        
        # 모델명 필터링
        if criteria.model_names and product.get("model_name") not in criteria.model_names:
            meets_criteria = False
        
        # 키워드 필터링 (상품명이나 설명에 키워드가 포함되어 있는지)
        if criteria.keywords:
            keyword_match = False
            product_name = product.get("product_name", "").lower()
            description = product.get("summary_description", "").lower()
            
            for keyword in criteria.keywords:
                keyword = keyword.lower()
                if keyword in product_name or keyword in description:
                    keyword_match = True
                    break
            
            if not keyword_match:
                meets_criteria = False
        
        # 모든 조건을 만족하면 결과에 추가
        if meets_criteria:
            filtered_products.append(product)

    tool_context.state["filtered_products"] = filtered_products

    return {
        "filtered_products": filtered_products,
        "total_count": len(filtered_products),
        "status": "success"
    } 