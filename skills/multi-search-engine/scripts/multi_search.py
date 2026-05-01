#!/usr/bin/env python3
"""
Multi Search Engine - 多搜索引擎聚合工具
聚合多个搜索引擎结果，提供更全面的搜索结果
"""

import argparse
import json
import urllib.request
import urllib.parse
import ssl
from typing import List, Dict, Optional
from datetime import datetime
import re

class MultiSearchEngine:
    """多搜索引擎聚合器"""
    
    def __init__(self):
        self.engines = {
            'brave': {
                'name': 'Brave Search',
                'enabled': False,  # 需要 API key
                'requires_key': True
            },
            'duckduckgo': {
                'name': 'DuckDuckGo',
                'enabled': True,   # 无需 API key
                'requires_key': False
            },
            'searx': {
                'name': 'SearXNG',
                'enabled': True,   # 公共实例
                'requires_key': False
            },
            'bing': {
                'name': 'Bing',
                'enabled': False,  # 需要 API key
                'requires_key': True
            }
        }
        
    def search_duckduckgo(self, query: str, limit: int = 5) -> List[Dict]:
        """使用 DuckDuckGo 搜索 (HTML 解析)"""
        results = []
        try:
            # DuckDuckGo HTML 搜索
            url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
            
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            req = urllib.request.Request(url, headers=headers)
            
            with urllib.request.urlopen(req, context=ctx, timeout=15) as response:
                html = response.read().decode('utf-8', errors='ignore')
                
                # 简单解析搜索结果
                # DuckDuckGo HTML 格式
                title_pattern = r'<a[^>]*class="result__a"[^>]*>(.*?)</a>'
                url_pattern = r'<a[^>]*class="result__a"[^>]*href="([^"]*)"'
                snippet_pattern = r'<a[^>]*class="result__snippet"[^>]*>(.*?)</a>'
                
                titles = re.findall(title_pattern, html)[:limit]
                urls = re.findall(url_pattern, html)[:limit]
                snippets = re.findall(snippet_pattern, html)[:limit]
                
                for i in range(min(len(titles), limit)):
                    # 清理 HTML 标签
                    title = re.sub(r'<[^>]+>', '', titles[i]) if i < len(titles) else ""
                    snippet = re.sub(r'<[^>]+>', '', snippets[i]) if i < len(snippets) else ""
                    url = urls[i] if i < len(urls) else ""
                    
                    if title and url:
                        results.append({
                            'title': title,
                            'url': url,
                            'snippet': snippet[:200] + '...' if len(snippet) > 200 else snippet,
                            'engine': 'DuckDuckGo',
                            'rank': i + 1
                        })
                        
        except Exception as e:
            print(f"⚠️  DuckDuckGo 搜索失败: {e}")
            
        return results
        
    def search_searx(self, query: str, limit: int = 5) -> List[Dict]:
        """使用 SearXNG 公共实例搜索"""
        results = []
        
        # 公共 SearXNG 实例列表
        instances = [
            "https://search.sapti.me",
            "https://searx.be",
            "https://search.bus-hit.me"
        ]
        
        for instance in instances:
            try:
                url = f"{instance}/search?q={urllib.parse.quote(query)}&format=json"
                
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': 'application/json'
                }
                
                req = urllib.request.Request(url, headers=headers)
                
                with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
                    data = json.loads(response.read().decode('utf-8'))
                    
                    if 'results' in data:
                        for i, result in enumerate(data['results'][:limit]):
                            results.append({
                                'title': result.get('title', ''),
                                'url': result.get('url', ''),
                                'snippet': result.get('content', '')[:200] + '...',
                                'engine': f"SearXNG ({instance.split('/')[2]})",
                                'rank': i + 1
                            })
                            
                    if results:
                        break  # 成功获取结果
                        
            except Exception as e:
                continue  # 尝试下一个实例
                
        return results
        
    def search(self, query: str, engines: List[str] = None, limit: int = 5) -> Dict:
        """多引擎搜索"""
        if engines is None:
            engines = ['duckduckgo', 'searx']
            
        all_results = []
        engine_stats = {}
        
        print(f"🔍 正在搜索: '{query}'")
        print(f"   使用引擎: {', '.join(engines)}\n")
        
        for engine in engines:
            if engine == 'duckduckgo':
                print("⏳ DuckDuckGo 搜索中...")
                results = self.search_duckduckgo(query, limit)
                all_results.extend(results)
                engine_stats['DuckDuckGo'] = len(results)
                
            elif engine == 'searx':
                print("⏳ SearXNG 搜索中...")
                results = self.search_searx(query, limit)
                all_results.extend(results)
                engine_stats['SearXNG'] = len(results)
                
        # 去重（基于 URL）
        seen_urls = set()
        unique_results = []
        for r in all_results:
            if r['url'] not in seen_urls:
                seen_urls.add(r['url'])
                unique_results.append(r)
                
        # 排序（按引擎排名）
        unique_results.sort(key=lambda x: (x['engine'], x['rank']))
        
        return {
            'query': query,
            'engines_used': engines,
            'engine_stats': engine_stats,
            'total_results': len(unique_results),
            'results': unique_results[:limit * len(engines)]
        }
        
    def search_news(self, query: str, limit: int = 5) -> List[Dict]:
        """搜索新闻（专门优化）"""
        # 添加新闻相关关键词
        news_query = f"{query} news"
        return self.search(news_query, limit=limit)
        
    def search_finance(self, query: str, limit: int = 5) -> List[Dict]:
        """搜索财经信息"""
        finance_query = f"{query} stock market finance"
        return self.search(finance_query, limit=limit)

def print_results(results: Dict, show_json: bool = False):
    """打印搜索结果"""
    if show_json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return
        
    print("=" * 70)
    print(f"📊 搜索结果: '{results['query']}'")
    print("=" * 70)
    
    print(f"\n📈 统计:")
    print(f"   使用引擎: {', '.join(results['engines_used'])}")
    for engine, count in results['engine_stats'].items():
        print(f"   {engine}: {count} 条结果")
    print(f"   去重后总计: {results['total_results']} 条\n")
    
    print("-" * 70)
    
    for i, result in enumerate(results['results'], 1):
        print(f"\n{i}. {result['title']}")
        print(f"   🔗 {result['url']}")
        print(f"   📝 {result['snippet']}")
        print(f"   🔍 来源: {result['engine']}")
        
    print("\n" + "=" * 70)

def main():
    parser = argparse.ArgumentParser(
        description='Multi Search Engine - 多搜索引擎聚合工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  %(prog)s "Python tutorial"                    # 基本搜索
  %(prog)s "USD CNY exchange rate" --limit 10   # 获取更多结果
  %(prog)s "AAPL stock" --finance               # 财经搜索模式
  %(prog)s "Israel Iran conflict" --news        # 新闻搜索模式
  %(prog)s "Python" --json                      # JSON 输出
        """
    )
    
    parser.add_argument('query', nargs='?', help='搜索关键词')
    parser.add_argument('--limit', type=int, default=5, help='每个引擎结果数量 (默认: 5)')
    parser.add_argument('--engines', type=str, help='指定引擎 (comma-separated: duckduckgo,searx)')
    parser.add_argument('--news', action='store_true', help='新闻搜索模式')
    parser.add_argument('--finance', action='store_true', help='财经搜索模式')
    parser.add_argument('--json', action='store_true', help='JSON 格式输出')
    parser.add_argument('--list-engines', action='store_true', help='列出可用引擎')
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("🔍 Multi Search Engine - 多搜索引擎聚合")
    print("=" * 70)
    
    search_engine = MultiSearchEngine()
    
    if args.list_engines:
        print("\n📚 可用搜索引擎:")
        print("-" * 40)
        for key, engine in search_engine.engines.items():
            status = "✅" if engine['enabled'] else "🔧"
            key_req = " (需要 API Key)" if engine['requires_key'] else ""
            print(f"{status} {key}: {engine['name']}{key_req}")
        print("\n💡 提示: 当前使用 DuckDuckGo 和 SearXNG (无需 API Key)")
        return
        
    if not args.query:
        parser.print_help()
        print("\n" + "=" * 70)
        print("💡 快速开始:")
        print("=" * 70)
        print("\n1. 基本搜索:")
        print('   python3 multi_search.py "Python tutorial"')
        print("\n2. 财经搜索:")
        print('   python3 multi_search.py "AAPL stock price" --finance')
        print("\n3. 新闻搜索:")
        print('   python3 multi_search.py "tech news" --news')
        print("\n4. 列出引擎:")
        print('   python3 multi_search.py --list-engines')
        return
        
    # 解析引擎列表
    engines = None
    if args.engines:
        engines = [e.strip() for e in args.engines.split(',')]
        
    # 执行搜索
    try:
        if args.news:
            print(f"\n📰 新闻搜索模式\n")
            results = search_engine.search_news(args.query, args.limit)
        elif args.finance:
            print(f"\n💰 财经搜索模式\n")
            results = search_engine.search_finance(args.query, args.limit)
        else:
            results = search_engine.search(args.query, engines, args.limit)
            
        print_results(results, args.json)
        
    except Exception as e:
        print(f"\n❌ 搜索失败: {e}")
        print("\n💡 提示:")
        print("   - 检查网络连接")
        print("   - 尝试使用 --list-engines 查看可用引擎")
        print("   - 某些引擎可能需要代理才能访问")
        
    print("\n" + "=" * 70)
    print("⚠️  免责声明: 搜索结果来自第三方搜索引擎，仅供参考")
    print("=" * 70)

if __name__ == "__main__":
    main()
