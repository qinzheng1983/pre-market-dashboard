#!/usr/bin/env python3
"""
Tavily Web Search - AI 实时网页搜索工具
专为 LLM 和 AI Agent 设计的高性能搜索 API

官网: https://tavily.com
免费额度: 每月 1000 API Credits
"""

import argparse
import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class TavilySearchClient:
    """Tavily 搜索客户端"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('TAVILY_API_KEY')
        self.client = None
        self._init_client()
    
    def _init_client(self):
        """初始化客户端"""
        try:
            from tavily import TavilyClient
            if self.api_key:
                self.client = TavilyClient(api_key=self.api_key)
            else:
                self.client = TavilyClient()  # 从环境变量读取
        except ImportError:
            print("❌ 请先安装 tavily-python: pip install tavily-python")
        except Exception as e:
            print(f"❌ 初始化失败: {e}")
    
    def search(self, query: str, max_results: int = 5, 
               search_depth: str = "basic",
               include_answer: bool = True,
               include_raw_content: bool = False,
               time_range: str = None) -> Optional[Dict]:
        """
        执行网页搜索
        
        Args:
            query: 搜索查询
            max_results: 最大结果数 (默认5)
            search_depth: 搜索深度 (basic/advanced)
            include_answer: 是否包含 AI 生成的答案
            include_raw_content: 是否包含原始网页内容
            time_range: 时间范围 (day/week/month/year)
        """
        if not self.client:
            print("❌ 客户端未初始化，请检查 API Key")
            return None
        
        try:
            params = {
                'query': query,
                'max_results': max_results,
                'search_depth': search_depth,
                'include_answer': include_answer,
                'include_raw_content': include_raw_content
            }
            
            if time_range:
                params['time_range'] = time_range
            
            response = self.client.search(**params)
            return response
            
        except Exception as e:
            print(f"❌ 搜索失败: {e}")
            return None
    
    def extract(self, urls: List[str], extract_depth: str = "basic",
                max_chars: int = 4000) -> Optional[Dict]:
        """
        从 URL 提取内容
        
        Args:
            urls: URL 列表 (最多 20 个)
            extract_depth: 提取深度 (basic/advanced)
            max_chars: 最大字符数
        """
        if not self.client:
            print("❌ 客户端未初始化")
            return None
        
        try:
            response = self.client.extract(
                urls=urls,
                extract_depth=extract_depth,
                max_chars=max_chars
            )
            return response
            
        except Exception as e:
            print(f"❌ 提取失败: {e}")
            return None
    
    def get_news(self, topic: str, max_results: int = 5) -> Optional[Dict]:
        """
        获取特定主题的最新新闻
        
        Args:
            topic: 新闻主题
            max_results: 最大结果数
        """
        query = f"{topic} latest news {datetime.now().year}"
        return self.search(
            query=query,
            max_results=max_results,
            time_range='week',  # 最近一周
            search_depth='advanced'
        )

def print_search_results(results: Dict, compact: bool = False):
    """打印搜索结果"""
    if not results:
        return
    
    print("\n" + "="*70)
    print("🔍 搜索结果")
    print("="*70)
    
    # AI 生成的答案
    if results.get('answer'):
        print(f"\n🤖 AI 答案:\n{results['answer']}\n")
    
    # 搜索结果
    print(f"📊 找到 {len(results.get('results', []))} 条结果:\n")
    
    for i, result in enumerate(results.get('results', []), 1):
        if compact:
            print(f"{i}. {result.get('title', 'No title')}")
            print(f"   {result.get('url', 'No URL')}")
        else:
            print(f"\n{i}. {result.get('title', 'No title')}")
            print(f"   🔗 {result.get('url', 'No URL')}")
            print(f"   📄 {result.get('content', 'No content')[:200]}...")
            if result.get('published_date'):
                print(f"   📅 {result.get('published_date')}")
        print()

def main():
    parser = argparse.ArgumentParser(
        description='Tavily Web Search - AI 实时网页搜索',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 基础搜索
  tavily_search.py "Israel Iran conflict"
  
  # 深度搜索
  tavily_search.py "China economy 2025" --depth advanced --max 10
  
  # 获取最新新闻
  tavily_search.py "Middle East" --news --time-range week
  
  # 从 URL 提取内容
  tavily_search.py --extract "https://example.com/article"
  
  # 简洁模式
  tavily_search.py "BTC price" --compact

环境变量:
  TAVILY_API_KEY - Tavily API Key (从 https://app.tavily.com 获取)
  每月 1000 次免费额度，无需信用卡
        """
    )
    
    parser.add_argument('query', nargs='?', help='搜索查询')
    parser.add_argument('--max', type=int, default=5, help='最大结果数 (默认5)')
    parser.add_argument('--depth', type=str, default='basic', 
                       choices=['basic', 'advanced'],
                       help='搜索深度 (默认basic, advanced消耗2x额度)')
    parser.add_argument('--time-range', type=str, 
                       choices=['day', 'week', 'month', 'year'],
                       help='时间范围过滤')
    parser.add_argument('--news', action='store_true', help='新闻模式 (最近一周)')
    parser.add_argument('--extract', action='store_true', help='提取 URL 内容')
    parser.add_argument('--compact', action='store_true', help='简洁模式')
    parser.add_argument('--no-answer', action='store_true', 
                       help='不包含 AI 答案 (节省额度)')
    parser.add_argument('--raw', action='store_true', help='输出原始 JSON')
    parser.add_argument('--check', action='store_true', help='检查 API Key 状态')
    
    args = parser.parse_args()
    
    print("="*70)
    print("🔍 Tavily Web Search - AI 实时网页搜索")
    print("="*70)
    
    # 检查 API Key
    api_key = os.getenv('TAVILY_API_KEY')
    if args.check:
        if api_key:
            print(f"\n✅ API Key 已设置: {api_key[:8]}...{api_key[-4:]}")
            print("\n💡 测试连接...")
            client = TavilySearchClient(api_key)
            if client.client:
                print("✅ 连接成功!")
                print("\n📊 额度信息:")
                print("   每月免费额度: 1000 Credits")
                print("   basic 搜索: 1 Credit/次")
                print("   advanced 搜索: 2 Credits/次")
                print("\n获取 API Key: https://app.tavily.com")
            else:
                print("❌ 连接失败，请检查 API Key 是否有效")
        else:
            print("\n❌ API Key 未设置")
            print("\n设置方法:")
            print("   export TAVILY_API_KEY='tvly-xxxxxxxx'")
            print("\n获取 API Key:")
            print("   1. 访问 https://app.tavily.com")
            print("   2. 注册/登录账户")
            print("   3. 创建 API Key")
            print("   4. 每月 1000 次免费额度，无需信用卡")
        return
    
    if not api_key:
        print("\n❌ 错误: TAVILY_API_KEY 未设置")
        print("\n请设置环境变量:")
        print("   export TAVILY_API_KEY='tvly-xxxxxxxx'")
        print("\n或使用 --check 查看详细设置指南")
        return
    
    if not args.query:
        parser.print_help()
        print("\n" + "="*70)
        print("💡 快速开始:")
        print("="*70)
        print("\n1. 搜索最新新闻:")
        print('   tavily_search.py "Israel Iran latest"')
        print("\n2. 深度搜索:")
        print('   tavily_search.py "China economy" --depth advanced')
        print("\n3. 检查 API Key:")
        print('   tavily_search.py --check')
        return
    
    # 创建客户端
    client = TavilySearchClient(api_key)
    
    if not client.client:
        return
    
    # 执行搜索
    if args.news:
        print(f"\n📰 新闻模式: '{args.query}'")
        results = client.get_news(args.query, max_results=args.max)
    elif args.extract:
        print(f"\n📄 提取 URL: '{args.query}'")
        urls = [url.strip() for url in args.query.split(',')]
        results = client.extract(urls)
    else:
        print(f"\n🔍 搜索: '{args.query}'")
        print(f"   深度: {args.depth}, 最大结果: {args.max}")
        if args.time_range:
            print(f"   时间范围: {args.time_range}")
        
        results = client.search(
            query=args.query,
            max_results=args.max,
            search_depth=args.depth,
            time_range=args.time_range,
            include_answer=not args.no_answer
        )
    
    # 输出结果
    if results:
        if args.raw:
            print(json.dumps(results, indent=2, ensure_ascii=False))
        else:
            print_search_results(results, compact=args.compact)
    else:
        print("\n❌ 未找到结果")
    
    print("\n" + "="*70)
    print("💡 提示:")
    print("   - 每月 1000 次免费额度")
    print("   - basic 搜索: 1 Credit")
    print("   - advanced 搜索: 2 Credits")
    print("   - 官网: https://tavily.com")
    print("="*70)

if __name__ == "__main__":
    main()
