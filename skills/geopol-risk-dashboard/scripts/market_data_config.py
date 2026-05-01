#!/usr/bin/env python3
"""
真实市场数据获取器
基于已验证的数据源配置
"""

import tomllib
from datetime import datetime
from pathlib import Path

class MarketDataConfig:
    """市场数据配置管理器"""
    
    def __init__(self):
        self.config_path = Path('/root/.openclaw/workspace/skills/geopol-risk-dashboard/config/data_sources.toml')
        self.data = self._load_config()
    
    def _load_config(self):
        """加载配置文件"""
        with open(self.config_path, 'rb') as f:
            return tomllib.load(f)
    
    def get_asset_data(self, asset_key):
        """获取指定资产的数据"""
        return self.data.get('assets', {}).get(asset_key, {})
    
    def get_all_assets(self):
        """获取所有资产数据"""
        return self.data.get('assets', {})
    
    def get_report_info(self):
        """获取报告信息"""
        return self.data.get('report', {})
    
    def print_summary(self):
        """打印数据摘要"""
        print("=" * 70)
        print("📊 已保存的市场数据配置")
        print("=" * 70)
        
        report = self.get_report_info()
        print(f"\n版本: {report.get('version')}")
        print(f"更新时间: {report.get('last_updated')}")
        print(f"数据期间: {report.get('report_period')}")
        
        print("\n" + "-" * 70)
        print(f"{'资产':<20} {'起始':<12} {'结束':<12} {'变化':<10}")
        print("-" * 70)
        
        assets = self.get_all_assets()
        for key, data in assets.items():
            name = data.get('name', key)
            start = data.get('start_value', 0)
            end = data.get('end_value', 0)
            change = data.get('change_pct', 0)
            print(f"{name:<20} {start:<12.2f} {end:<12.2f} {change:+.2f}%")
        
        print("-" * 70)
        print("\n⚠️  重要提醒:")
        print(self.data.get('notes', {}).get('warning', ''))

if __name__ == "__main__":
    config = MarketDataConfig()
    config.print_summary()
