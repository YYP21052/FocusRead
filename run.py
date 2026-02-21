from app import create_app

app = create_app()

if __name__ == '__main__':
    # 必须绑定 0.0.0.0 才能在 Docker 外部访问
    app.run(host='0.0.0.0', port=5000, debug=True)