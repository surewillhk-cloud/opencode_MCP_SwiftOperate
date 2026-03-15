---
name: blockchain-standards
description: 区块链开发规范，包含智能合约编写、Solana/Base 部署、链上结算逻辑、安全审计清单。fullstack-dev 在开发合约相关功能时加载。
---

# 区块链开发规范

## 目标公链选择

| 公链 | 优势 | 适用场景 |
|------|------|---------|
| **Solana** | 高吞吐、低手续费、生态成熟 | 高频算力交易结算 |
| **Base** | EVM 兼容、Coinbase 背书、低费用 | 合规优先、对接以太坊生态 |

> AiProtoMesh 建议优先 Solana（交易频率高，手续费敏感），Base 作为备选。

---

## 智能合约开发规范

### 合约结构（以 Solana/Anchor 为例）

```
programs/
  aiprotomesh/
    src/
      lib.rs              ← 主入口
      instructions/
        broadcast.rs      ← 广播电子邀请函
        accept.rs         ← 接单逻辑
        settle.rs         ← 结算逻辑
        lock.rs           ← 供方锁仓
      state/
        invitation.rs     ← 邀请函数据结构
        task.rs           ← 任务状态
        reserve.rs        ← 储备金池
      errors.rs           ← 统一错误码
```

### 合约安全规范

每个合约函数必须包含：
- [ ] 权限验证（只有合法角色才能调用）
- [ ] 输入参数边界检查
- [ ] 防重入保护
- [ ] 事件日志（链上可追溯）
- [ ] 错误码统一定义，不允许裸露 panic

### 禁止行为
- ❌ 合约升级逻辑未经多签授权
- ❌ 私钥硬编码在任何文件里
- ❌ 未经测试网验证直接部署主网
- ❌ 储备金合约未设置时间锁

---

## 链上结算流程规范

```
任务创建 → 需方锁定 TOKEN（进入托管合约）
    ↓
供方接单 → 部署确认上链
    ↓
任务执行中 → 守护进程定时上报心跳
    ↓
任务完成 → 供方提交完成证明
    ↓
智能合约验证 → 自动划转 TOKEN 给供方
    ↓
平台手续费：0（平台不抽成）
```

---

## 测试网部署流程

```bash
# Solana 测试网
solana config set --url devnet
anchor build
anchor deploy

# 验证合约
anchor test

# 主网部署前必须完成
- [ ] 测试网完整跑通所有场景
- [ ] 第三方安全审计
- [ ] 多签钱包配置完成
- [ ] 储备金注入确认
```

---

## 链上事件监听规范

所有关键操作必须 emit 事件：

```rust
// 事件命名规范：动词 + 名词
emit!(InvitationBroadcast { ... });
emit!(TaskAccepted { ... });
emit!(TaskSettled { ... });
emit!(TokenLocked { ... });
emit!(ReserveBuyback { ... });
```

守护进程通过监听这些事件驱动后续自动化动作。
