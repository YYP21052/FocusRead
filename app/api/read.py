from flask import Blueprint, jsonify
import requests
from bs4 import BeautifulSoup
from app.extensions import db,redis_client # 预留给后续缓存功能使用
from app.model import Novel, Chapter, User

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

        ## 将爬取到的内容存入数据库
        # 先查询是否存在该小说
        novel =Novel.query.filter_by(title="斗破苍穹(测试)").first()
        if not novel:
            novel = Novel(title="斗破苍穹(测试)", author="天蚕土豆", source_url="https://www.dxmwx.org")
            db.session.add(novel)
            db.session.commit() # 先提交，以便获取到自动生成的 novel.id

        # 根据小说id和章节名称来判断是否在数据库中存在该章节
        existingChapter = Chapter.query.filter_by(novel_id=novel.id, title=title).first()
        if not existingChapter:
            newChapter = Chapter(
                novel_id=novel.id,
                title=title, 
                content=full_content, 
                order_num=1, # # 测试阶段暂时写死序号为 1
                is_crawled=True # 标记为已爬取
                )
            db.session.add(newChapter)
            db.session.commit()
            save_status= " 新章节已成功存入数据库"
        else:
            save_status = " 该章节已存在于数据库，无需重复存入"


        return jsonify({
            "status": "success",
            "message": save_status,
            "title": title,
            "novel_id": novel.id,
            "content_preview": full_content[:150] + "\n\n......(内容太长，已省略)"
        })
    except Exception as e:

        db.session.rollback() # 出现异常时回滚数据库操作
        return jsonify({
            "status": "error",
            "message": f"requests 抓取失败: {str(e)}"
            })