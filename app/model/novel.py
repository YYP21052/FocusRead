from app.extensions import db
from datetime import datetime

class Novel(db.Model):
    __tablename__ = 'novel'

    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(255), nullable=False) # 小说标题
    author = db.Column(db.String(255), nullable=False) # 作者
    source_url = db.Column(db.String(255), nullable=False) # 小说源地址
    created_at = db.Column(db.DateTime, default=datetime.utcnow) # 创作时间

    chapters = db.relationship('Chapter', backref='novel', lazy=True)

class Chapter(db.Model):
    __tablename__ = 'chapter'

    id = db.Column(db.Integer, primary_key=True)
    novel_id = db.Column(db.Integer, db.ForeignKey('novel.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False) # 章节标题
    content = db.Column(db.Text, nullable=True) # 抓取正文可能较慢，允许初始为空
    order_num = db.Column(db.Integer, nullable=False) # 章节序号，用于排序显示
    is_crawled = db.Column(db.Boolean, default=False)  # 标记正文是否已通过 Celery 异步抓取完毕
    created_at = db.Column(db.DateTime, default=datetime.utcnow) # 爬取时间

    __table_args__=(
        db.Index('idx_novel_order','novel_id', 'order_num'),
    )