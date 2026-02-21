from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>环境配置成功！</h1><p>你的 Flask 服务器正在完美运行。</p>"

@app.route('/api/scrape-test')
def scrape_test():
    target_url = "https://www.dxmwx.org/read/10409_77963.html"
    
    try:
        # ⚠️ 【极其重要】：请务必将 7890 替换为你真实的代理端口！
        proxies = {
            "http": "http://127.0.0.1:7897",
            "https": "http://127.0.0.1:7897",
        }
        
        # 伪装成正常的谷歌浏览器
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
        }

        # 使用最经典的 requests 发起请求
        # 加上 verify=False 忽略证书警告
        response = requests.get(
            target_url, 
            headers=headers, 
            proxies=proxies, 
            verify=False, 
            timeout=15
        )
        
        # 设置编码为 utf-8（根据你之前提供的源码）
        response.encoding = 'utf-8' 
        
        # 启动 BeautifulSoup 解析
        soup = BeautifulSoup(response.text, 'lxml')
        
        # --- 🎯 提取标题 ---
        title_tag = soup.find('h1', id='ChapterTitle')
        chapter_title = title_tag.text.strip() if title_tag else "未找到标题"
        
        # --- 🎯 提取正文 ---
        content_div = soup.find('div', id='Lab_Contents')
        content_lines = [] 
        
        if content_div:
            paragraphs = content_div.find_all('p')
            for p in paragraphs:
                text = p.text.strip()
                if text: 
                    content_lines.append(text)
        
        full_content = "\n".join(content_lines)
        
        return jsonify({
            "status": "success",
            "message": "使用 requests 抓取成功！",
            "data": {
                "title": chapter_title,
                "preview": full_content[:300] + "\n\n......(内容太长，已省略)"
            }
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"requests 抓取失败: {str(e)}"
        })

if __name__ == '__main__':
    app.run(debug=True)