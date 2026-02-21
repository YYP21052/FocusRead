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
        # ⚠️ 【极其重要】：因为通过科学上网拿到的源码，
        # 所以必须让代码也走你的代理通道！
        # 请确保把 7897 换成你实际使用的加速器/VPN的本地 HTTP 端口。
        proxies = {
            "http": "https://172.18.16.1:7897",
            "https": "https://172.18.16.1:7897",
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
        
        # 2. 设置编码。根据你发来的网页源码 <meta charset="utf-8" /> 确定
        response.encoding = 'utf-8' 
        
        # 3. 启动 BeautifulSoup 解析 (使用 lxml 引擎)
        soup = BeautifulSoup(response.text, 'lxml')
        
        # 定位 <h1 id="ChapterTitle">
        title_tag = soup.find('h1', id='ChapterTitle')
        chapter_title = title_tag.text.strip() if title_tag else "未找到标题"
        
        # 定位 <div id="Lab_Contents">
        content_div = soup.find('div', id='Lab_Contents')
        content_lines = [] # 用来暂存每一段文字
        
        if content_div:
            # 找到 div 里面所有的 <p> 标签
            paragraphs = content_div.find_all('p')
            for p in paragraphs:
                text = p.text.strip() # 去除两端的空白字符
                if text: # 如果提取出来有文字（过滤掉那些占位的空 <p/>）
                    content_lines.append(text)
        
        # 把每一段文字用回车符拼接成一篇完整的文章
        full_content = "\n".join(content_lines)
        
        # 6. 返回结构化的 JSON 数据给前端
        return jsonify({
            "status": "success",
            "message": "使用 requests 抓取成功！",
            "data": {
                "url": target_url,
                "title": chapter_title,
                # 为了防止浏览器页面显示太长卡顿，我们在 API 里只返回前 300 个字作为预览
                "content_preview": full_content[:300] + "\n\n......(内容太长，已省略)"
            }
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"requests 抓取失败: {str(e)}"
        })

if __name__ == '__main__':
    app.run(debug=True)