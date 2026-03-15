---
name: protocol-design
description: 电子邀请函协议设计规范，定义 AI to AI 算力交易的底层数据结构、广播机制、守护进程规范。fullstack-dev 开发协议层时加载。
---

# 电子邀请函协议规范

## 协议定位

电子邀请函（Electronic Invitation）是 AiProtoMesh 的底层语言，是 AI Agent 之间发起算力交易的标准格式。所有交易从一封邀请函开始。

---

## 邀请函数据结构

```typescript
interface ElectronicInvitation {
  // 基础标识
  invitationId: string        // 全局唯一ID，链上生成
  version: string             // 协议版本，如 "1.0.0"
  timestamp: number           // 发出时间戳（Unix）
  expiresAt: number           // 过期时间戳

  // 需方信息
  requester: {
    agentId: string           // AI Agent 唯一标识
    walletAddress: string     // 结算钱包地址
    reputation: number        // 链上信誉分（0-100）
  }

  // 算力需求
  compute: {
    taskType: TaskType        // 任务类型（见下方枚举）
    modelRequired: string     // 所需模型，如 "llama3-70b"
    minVram: number           // 最低显存需求（GB）
    estimatedDuration: number // 预计时长（秒）
    maxLatency: number        // 最大可接受延迟（ms）
  }

  // 结算条件
  settlement: {
    currency: "TOKEN" | "USDC"  // 结算币种
    maxBudget: number           // 最高出价（TOKEN/小时）
    paymentModel: "per-task" | "per-hour"
    escrowAmount: number        // 托管金额
  }

  // 环境要求
  requirements: {
    region?: string[]         // 偏好地区（可选）
    greenEnergyOnly?: boolean // 是否只要绿色算力
    minReputation?: number    // 供方最低信誉分
  }

  // 协议签名
  signature: string           // 需方私钥签名，防伪造
  status: InvitationStatus    // 当前状态
}

// 任务类型枚举
enum TaskType {
  LLM_INFERENCE = "llm_inference",
  IMAGE_GENERATION = "image_generation",
  EMBEDDING = "embedding",
  FINE_TUNING = "fine_tuning",
  CUSTOM = "custom"
}

// 邀请函状态枚举
enum InvitationStatus {
  BROADCASTING = "broadcasting",  // 广播中
  ACCEPTED = "accepted",          // 已接单
  DEPLOYING = "deploying",        // 部署中
  ACTIVE = "active",              // 执行中
  COMPLETED = "completed",        // 已完成
  CANCELLED = "cancelled",        // 已取消
  EXPIRED = "expired"             // 已过期
}
```

---

## 三种广播方式

### 方式一：协议注册表 API（早期主力）
```
POST /api/v1/invitations/broadcast
{
  invitation: ElectronicInvitation,
  broadcastRadius: "global" | "regional"
}

供方通过 GET /api/v1/invitations/available 轮询可接单列表
```

### 方式二：SEO 植入（冷启动）
```
邀请函以结构化数据形式嵌入公开页面
供方守护进程爬取指定格式的页面
适合早期没有链上基础设施时使用
```

### 方式三：链上事件监听（长期目标）
```
需方调用合约 broadcastInvitation()
合约 emit InvitationBroadcast 事件
供方守护进程监听链上事件，实时响应
延迟最低，去中心化程度最高
```

---

## 守护进程规范（供方节点）

```
守护进程职责：
1. 持续监听广播（API轮询 or 链上事件）
2. 根据本地资源评估是否接单
3. 自动提交接单请求
4. 部署容器并建立连接
5. 定时上报任务心跳
6. 任务完成后提交证明触发结算

评估逻辑：
- 当前可用 VRAM >= 邀请函要求
- 预计收益 > 电力成本 * 安全系数（建议 1.3x）
- 信誉分符合需方要求
- 网络延迟在需方要求范围内
```

---

## 智能部署层规范

供方只需提供 API 端点或 SSH 通道，平台负责：

```
1. 匹配合适的模型权重
2. 切割独立容器（隔离不同任务）
3. 部署模型镜像
4. 建立安全通道
5. 返回接入点给需方
```

供方接入最低要求：
```yaml
minimum_requirements:
  interface: "SSH" or "REST API"
  vram: 8GB         # 最低显存
  bandwidth: 100Mbps
  uptime: 95%       # 月可用率
  os: "Linux (Ubuntu 20.04+)"
```

---

## 协议版本管理

- 当前版本：`1.0.0`
- 版本升级需要链上治理投票
- 旧版本邀请函兼容期：3 个月
- 不兼容变更需要主版本号递增（1.x.x → 2.0.0）
