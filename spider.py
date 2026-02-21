import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    # 1. 设置请求头（模拟浏览器，防止被简单反爬拦截）
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        # 2. 发送 GET 请求
        response = requests.get(url, headers=headers, timeout=10)
        
        # 检查请求是否成功
        response.raise_for_status()
        
        # 自动处理编码问题（解决中文乱码）
        response.encoding = response.apparent_encoding

        # 3. 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # --- 4. 提取数据的示例 (根据你的目标网页修改) ---
        
        # 获取网页标题
        title = soup.title.string if soup.title else "无标题"
        print(f"网页标题: {title}\n")

        # 示例 A：获取所有 <h1> 标签的内容
        h1_tags = soup.find_all('h1')
        for h1 in h1_tags:
            print(f"标题内容: {h1.get_text(strip=True)}")

        # 示例 B：根据 Class 查找特定内容（例如小说正文或文章列表）
        # 假设正文在 <div class="content"> 中
        content_div = soup.find('div', class_='content')
        if content_div:
            print("找到正文内容了！")
            # print(content_div.get_text())

    except requests.exceptions.RequestException as e:
        print(f"请求发生错误: {e}")

# 替换成你想要爬取的网址
target_url = "https://www.69shuba.com/txt/90384/40699435" 
scrape_website(target_url)