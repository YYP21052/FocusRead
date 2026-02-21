from flask import Flask
from app.extensions import db
import os

def create_app():
    app = Flask(__name__)

    # ⚠️ 修改这里：设置一个本地调试用的默认数据库连接串
    # 注意：这里的 host 是 127.0.0.1，因为你在本地运行，要连 Docker 映射出来的 3306 端口
    default_db_url = 'mysql+pymysql://focus_user:focus_pass@127.0.0.1:3306/focusread'

    # 获取环境变量 DATABASE_URL，如果找不到，就使用 default_db_url
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', default_db_url)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 初始化扩展
    db.init_app(app)

    # 注册蓝图
    from app.api.read import read_bp
    app.register_blueprint(read_bp, url_prefix='/api')

    return app