# Pytest Guide

## When to Use

- "写单元测试"
- "添加 pytest 测试"
- "这个函数需要测试覆盖"
- "运行测试看看有没有问题"

## Workflow

```
1. 分析需要测试的代码
2. 确定测试类型：unit / integration / e2e
3. 编写测试用例
4. 运行测试
5. 修复失败的测试
6. 确保测试通过
```

## Test Types

| 类型 | 适用场景 |
|------|----------|
| Unit | 单个函数/方法 |
| Integration | 多个模块协作 |
| E2E | 完整用户流程 |

## Pytest 常用命令

```bash
# 运行所有测试
pytest

# 运行指定文件
pytest test_file.py

# 运行指定测试函数
pytest test_file.py::test_function

# 显示详细输出
pytest -v

# 显示 print 输出
pytest -s

# 只运行失败的测试
pytest --lf

# 生成覆盖率报告
pytest --cov=src --cov-report=html
```

## 测试覆盖率检查

```bash
# 检查覆盖率
pytest --cov=. --cov-report=term-missing

# 覆盖率要求
- 核心业务: 80%+
- 公共模块: 70%+
- 工具函数: 60%+
```

## Mocking

```python
from unittest.mock import Mock, patch

# Mock 函数
@patch('module.function')
def test_that(mock_fn):
    mock_fn.return_value = 'mocked'
    # ...

# Mock 对象
def test_with_mock():
    mock_obj = Mock()
    mock_obj.method.return_value = 'value'
    # ...
```

## Fixtures

```python
import pytest

@pytest.fixture
def db_connection():
    # 创建测试数据库连接
    conn = create_test_db()
    yield conn
    # 清理
    conn.close()

def test_query(db_connection):
    # 使用 fixture
    result = db_connection.query("SELECT * FROM users")
    assert len(result) > 0
```

## Checklist

- [ ] 每个核心函数有至少一个测试
- [ ] 边界条件被测试
- [ ] 异常被正确处理
- [ ] 测试名称清晰描述测试内容
- [ ] 测试是独立的（不依赖顺序）
- [ ] 测试通过
- [ ] 覆盖率符合要求
