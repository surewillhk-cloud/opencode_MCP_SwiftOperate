# Integration Testing

## When to Use

- "写集成测试"
- "测试多个模块的协作"
- "API 接口测试"
- "数据库交互测试"

## 测试范围

Integration Test 介于 Unit Test 和 E2E 之间：
- 测试多个组件/模块的协作
- 不需要启动完整应用
- 通常涉及数据库、API、消息队列等

## API 测试

### 使用 requests

```python
import requests
import pytest

BASE_URL = "https://api.example.com"

def test_create_user():
    # 创建用户
    response = requests.post(f"{BASE_URL}/users", json={
        "name": "Test User",
        "email": "test@example.com"
    })
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test User"
    assert "id" in data
    
    # 清理
    requests.delete(f"{BASE_URL}/users/{data['id']}")
```

### 使用 pytest fixtures

```python
import pytest
import requests

@pytest.fixture
def api_client():
    return requests.Session()

@pytest.fixture
def test_user(api_client):
    # 创建测试用户
    user = api_client.post("/users", json={"name": "Test"})
    yield user.json()
    # 清理
    api_client.delete(f"/users/{user.json()['id']}")

def test_get_user(api_client, test_user):
    response = api_client.get(f"/users/{test_user['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test"
```

## 数据库测试

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture
def test_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_create_and_query(test_db):
    # 创建
    user = User(name="Test", email="test@example.com")
    test_db.add(user)
    test_db.commit()
    
    # 查询
    result = test_db.query(User).filter_by(email="test@example.com").first()
    assert result is not None
    assert result.name == "Test"
```

## 消息队列测试

```python
import pika

def test_message_queue():
    connection = pika.BlockingConnection()
    channel = connection.channel()
    
    # 发布消息
    channel.queue_declare(queue="test_queue")
    channel.basic_publish(
        exchange="",
        routing_key="test_queue",
        body="Hello World"
    )
    
    # 消费消息
    def callback(ch, method, properties, body):
        assert body == b"Hello World"
        ch.basic_ack(delivery_tag=method.delivery_tag)
        ch.stop_consuming()
    
    channel.basic_consume(queue="test_queue", on_message_callback=callback)
    channel.start_consuming()
    
    connection.close()
```

## 微服务集成测试

```python
import pytest
import requests

# 服务地址
USER_SERVICE = "http://localhost:8001"
ORDER_SERVICE = "http://localhost:8002"

def test_create_order_with_user():
    # 1. 创建用户
    user_resp = requests.post(f"{USER_SERVICE}/users", json={
        "name": "Customer",
        "email": "customer@test.com"
    })
    user_id = user_resp.json()["id"]
    
    # 2. 创建订单
    order_resp = requests.post(f"{ORDER_SERVICE}/orders", json={
        "user_id": user_id,
        "items": [{"product": "Book", "quantity": 2}]
    })
    assert order_resp.status_code == 201
    
    # 3. 验证
    order = order_resp.json()
    assert order["user_id"] == user_id
    
    # 清理
    requests.delete(f"{ORDER_SERVICE}/orders/{order['id']}")
    requests.delete(f"{USER_SERVICE}/users/{user_id}")
```

## Contract Testing

```python
# 使用 pytest-check Contracts

def test_api_contract():
    """验证 API 响应符合预期 Schema"""
    response = requests.get("/api/users/1")
    
    # 验证响应结构
    assert "id" in response.json()
    assert "name" in response.json()
    assert "email" in response.json()
    assert isinstance(response.json()["id"], int)
```

## 测试数据管理

```python
@pytest.fixture
def sample_data():
    return {
        "users": [
            {"name": "Alice", "email": "alice@test.com"},
            {"name": "Bob", "email": "bob@test.com"},
        ],
        "products": [
            {"name": "Product A", "price": 100},
            {"name": "Product B", "price": 200},
        ]
    }

@pytest.fixture
def seeded_db(test_db, sample_data):
    # 批量插入测试数据
    for user_data in sample_data["users"]:
        test_db.add(User(**user_data))
    test_db.commit()
    return test_db
```

## Mock 外部服务

```python
import responses

@responses.activate
def test_with_mocked_api():
    # Mock 外部 API
    responses.add(
        responses.GET,
        "https://external-api.com/users",
        json=[{"id": 1, "name": "Test"}],
        status=200
    )
    
    # 调用会返回 Mock 数据
    result = external_client.get_users()
    assert result == [{"id": 1, "name": "Test"}]
```

## 性能测试

```python
import time
import pytest

def test_response_time():
    start = time.time()
    response = requests.get("/api/users")
    elapsed = time.time() - start
    
    assert response.status_code == 200
    assert elapsed < 1.0, f"Response time {elapsed}s exceeds 1s"
```

## Checklist

- [ ] 测试模块间交互
- [ ] 测试 API 端点
- [ ] 测试数据库操作
- [ ] 测试错误处理
- [ ] 使用测试数据 fixtures
- [ ] 清理测试数据
- [ ] 测试通过
