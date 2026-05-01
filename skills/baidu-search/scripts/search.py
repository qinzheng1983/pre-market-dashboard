#!/usr/bin/env python3
"""
Baidu AI Search Skill
Search the web using Baidu AI Search Engine (BDSE)
"""

import sys
import json
import requests
import os


def baidu_search(api_key, request_body: dict):
    """
    调用百度AI搜索API进行搜索
    :param api_key: 百度千帆API密钥
    :param request_body: 搜索请求参数字典
    :return: 搜索结果数据
    """
    # 百度AI搜索API接口地址
    url = "https://qianfan.baidubce.com/v2/ai_search/web_search"
    
    # 设置请求头
    headers = {
        "Authorization": f"Bearer {api_key}",
        "X-Appbuilder-From": "openclaw",
        "Content-Type": "application/json"
    }
    
    # 使用POST方法发送JSON数据到API
    response = requests.post(url, json=request_body, headers=headers)
    response.raise_for_status()
    
    # 解析JSON响应
    results = response.json()
    
    # 检查API返回是否包含错误信息
    if "code" in results:
        raise Exception(results.get("message", "Unknown error"))
    
    # 提取搜索结果数据
    datas = results.get("references", [])
    
    # 移除不需要的字段
    keys_to_remove = {"snippet"}
    for item in datas:
        for key in keys_to_remove:
            if key in item:
                del item[key]
    
    return datas


if __name__ == "__main__":
    # 检查命令行参数
    if len(sys.argv) < 2:
        print("Usage: python3 search.py <query_json>")
        sys.exit(1)
    
    # 获取命令行传入的查询参数
    query = sys.argv[1]
    parse_data = {}
    
    # 尝试解析JSON格式的查询参数
    try:
        parse_data = json.loads(query)
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        sys.exit(1)
    
    # 检查是否包含query字段
    if "query" not in parse_data:
        print("错误: 请求体中必须包含query字段。")
        sys.exit(1)
    
    # 从环境变量获取百度API密钥
    api_key = os.getenv("BAIDU_API_KEY")
    if not api_key:
        print("错误: 必须在环境变量中设置 BAIDU_API_KEY。")
        print("请访问 https://qianfan.cloud.baidu.com/ 申请API密钥")
        sys.exit(1)
    
    # 构建请求体数据
    request_body = {
        "messages": [
            {
                "content": parse_data["query"],
                "role": "user"
            }
        ],
        "search_source": "baidu_search_v2",
        "resource_type_filter": [
            {"type": "web", "top_k": parse_data.get("count", 10)}
        ]
    }
    
    # 添加时间过滤
    if "freshness" in parse_data and parse_data["freshness"]:
        request_body["search_recency_filter"] = parse_data["freshness"]
    
    try:
        # 调用百度搜索函数
        results = baidu_search(api_key, request_body)
        # 以格式化的JSON格式输出结果
        print(json.dumps(results, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"错误: {str(e)}")
        sys.exit(1)
