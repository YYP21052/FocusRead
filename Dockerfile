
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 防止 Python 产生 .pyc 文件，并让日志实时输出
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 安装系统级依赖 (lxml 和 mysqlclient 编译所需)
RUN apt-get update && apt-get install -y \
    gcc \
    libxml2-dev \
    libxslt-dev \
    pkg-config \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# 先复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY . .

# 暴露端口
EXPOSE 5000

# 启动服务
CMD ["flask", "run", "--host=0.0.0.0"]