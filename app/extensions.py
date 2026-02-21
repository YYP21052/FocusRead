from flask_sqlalchemy import SQLAlchemy
from redis import Redis
import os

# 初始化 SQLAlchemy 实例
db = SQLAlchemy()

# 初始化 Redis 实例
# 这里的 host 使用 docker-compose 中定义的服务名 'redis'
redis_client = Redis(host='redis', port=6379, db=0, decode_responses=True)