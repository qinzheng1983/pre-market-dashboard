import subprocess
import sys
import os

os.environ['EMAIL_SENDER'] = '13911658378@139.com'
os.environ['EMAIL_PASSWORD'] = 'f79d697414966c63d600'

with open('reports/pre_market_briefing_20260603.html', 'r') as f:
    content = f.read()

cmd = [
    sys.executable, 'skills/email-reporter/scripts/email_reporter.py', 'send',
    '--to', '13911658378@139.com',
    '--subject', '盘前简报 — 2026年6月3日（周三）08:30 CFO结构版',
    '--content', content,
    '--attachment', 'reports/pre_market_briefing_20260603.html',
    '--provider', '139'
]

result = subprocess.run(cmd, capture_output=True, text=True)
print('STDOUT:', result.stdout)
print('STDERR:', result.stderr)
print('RETURN CODE:', result.returncode)
