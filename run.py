from app import create_app
from app.extensions import db
from app.model import User,Novel,Chapter

app = create_app()

if __name__ == '__main__':

    with app.app_context(): 
        db.create_all()
        print("数据库表结构初始化完成")

    # 必须绑定 0.0.0.0 才能在 Docker 外部访问
    app.run(host='0.0.0.0', port=5000, debug=True)