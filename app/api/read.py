from flask import Blueprint, jsonify
import requests
from bs4 import BeautifulSoup
from app.extensions import redis_client # 预留给后续缓存功能使用

read_bp = Blueprint('read', __name__)

@read_bp.route('/scrape-test')
def scrape_test():
    target_url = "https://www.dxmwx.org/read/10409_77963.html"
    try:
        # 这里建议先尝试使用你的局域网 IP 192.168.1.15
        headers = {"User-Agent": "Mozilla/5.0 ..."} # 保持之前的 headers 不变

        response = requests.get(target_url, headers=headers, verify=False, timeout=15)
        response.encoding = 'utf-8' 
        soup = BeautifulSoup(response.text, 'lxml')
        
        title = soup.find('h1', id='ChapterTitle').text.strip()
        content_div = soup.find('div', id='Lab_Contents')
        # 开始解析内容
        content_lines = [] # 用来暂存每一段文字

        if content_div:
            # 找到 div 里面所有的 <p> 标签
            paragraphs = content_div.find_all('p')
            for p in paragraphs:
                text = p.text.strip() # 去除两端的空白字符
                if text: # 如果提取出来有文字（过滤掉那些占位的空 <p/>）
                    content_lines.append(text)
        
        full_content = "\n".join(content_lines)


        return jsonify({
            "status": "success",
            "message": "使用 requests 抓取成功！",
            "title": title,
            "content_preview": full_content[:300] + "\n\n......(内容太长，已省略)"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"requests 抓取失败: {str(e)}"
            })