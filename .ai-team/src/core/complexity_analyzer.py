from typing import Dict, Any, List, Optional
import re
import logging

logger = logging.getLogger(__name__)


class ComplexityLevel:
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    ADVANCED = "advanced"


COMPLEXITY_SCORES = {
    ComplexityLevel.LOW: 1,
    ComplexityLevel.MEDIUM: 2,
    ComplexityLevel.HIGH: 3,
    ComplexityLevel.ADVANCED: 4,
}


class ComplexityAnalyzer:
    """项目复杂度分析器"""

    FRONTEND_KEYWORDS = {
        "low": [
            "静态页面",
            "单页面",
            "简单表单",
            "展示页面",
            "landing page",
            "single page",
            "static",
            "simple form",
            "display page",
            "1-3 页",
            "1-3 pages",
            "3 页以内",
            "不超过3页",
        ],
        "medium": [
            "多页面",
            "用户登录",
            "注册",
            "表单提交",
            "列表页",
            "multiple pages",
            "login",
            "register",
            "form submit",
            "响应式",
            "轮播",
            "tabs",
            "modal",
            "4-10 页",
        ],
        "high": [
            "后台管理",
            "dashboard",
            "数据可视化",
            "图表",
            "echarts",
            "实时更新",
            "websocket",
            "复杂动画",
            "拖拽",
            "富文本编辑器",
            "编辑器",
            "多人协作",
            "实时协作",
            "11-20 页",
        ],
        "advanced": [
            "大型系统",
            "企业级",
            "saas",
            "ERP",
            "CRM",
            "OMS",
            "低代码",
            "可视化拖拽",
            "工作流引擎",
            "20+ 页",
            "50+ 页",
            "3D",
            "游戏",
            "AR/VR",
            "复杂动画引擎",
            "区块链",
            "defi",
            "blockchain",
            "crypto",
            "nft",
            "metaverse",
        ],
    }

    BACKEND_KEYWORDS = {
        "low": [
            "静态页面",
            "简单接口",
            "无数据库",
            "纯展示",
            "static",
            "simple api",
            "no database",
            "1-2 个接口",
            "1-2 apis",
        ],
        "medium": [
            "CURD",
            "增删改查",
            "mysql",
            "postgresql",
            "mongodb",
            "用户管理",
            "基本增删改查",
            "3-8 个接口",
            "redis 缓存",
            "简单文件上传",
        ],
        "high": [
            "第三方支付",
            "微信支付",
            "支付宝",
            "stripe",
            "payment",
            "短信验证码",
            "邮件服务",
            "websocket",
            "sse",
            "9-20 个接口",
            "多数据库",
            "分库分表",
            "任务队列",
            "celery",
            "mq",
            "搜索",
            "elasticsearch",
        ],
        "advanced": [
            "微服务",
            "microservice",
            "分布式",
            "区块链",
            "blockchain",
            "AI 集成",
            "机器学习",
            "大数据",
            "实时计算",
            "20+ 接口",
            "多租户",
            "sso",
            "oauth2",
            "高并发",
            "秒杀",
            "抢票",
            "实时推送",
        ],
    }

    UI_KEYWORDS = {
        "low": ["简单", "简洁", "basic", "simple", "minimal"],
        "medium": ["美观", "现代", "beautiful", "modern", "时尚"],
        "high": ["炫酷", "精美", "动画丰富", "complex", "animation"],
        "advanced": ["顶级设计", "获奖级别", "award winning", "独特设计语言"],
    }

    @classmethod
    def analyze(cls, task: str) -> Dict[str, Any]:
        """分析任务复杂度"""
        task_lower = task.lower()

        frontend_score = cls._analyze_dimension(task_lower, cls.FRONTEND_KEYWORDS)
        backend_score = cls._analyze_dimension(task_lower, cls.BACKEND_KEYWORDS)
        ui_score = cls._analyze_dimension(task_lower, cls.UI_KEYWORDS)

        frontend_level = cls._score_to_level(frontend_score)
        backend_level = cls._score_to_level(backend_score)
        ui_level = cls._score_to_level(ui_score)

        scores = [frontend_score, backend_score, ui_score]
        overall_score = sum(scores) / len(scores)

        if ComplexityLevel.ADVANCED in [frontend_level, backend_level, ui_level]:
            overall_level = ComplexityLevel.ADVANCED
        else:
            overall_level = cls._score_to_level(overall_score)

        frontend_details = cls._extract_details(
            task_lower, cls.FRONTEND_KEYWORDS, "frontend"
        )
        backend_details = cls._extract_details(
            task_lower, cls.BACKEND_KEYWORDS, "backend"
        )

        return {
            "overall_level": overall_level,
            "overall_score": overall_score,
            "frontend": {
                "level": frontend_level,
                "score": frontend_score,
                "details": frontend_details,
            },
            "backend": {
                "level": backend_level,
                "score": backend_score,
                "details": backend_details,
            },
            "ui": {
                "level": ui_level,
                "score": ui_score,
            },
        }

    @classmethod
    def _analyze_dimension(
        cls, task_lower: str, keywords: Dict[str, List[str]]
    ) -> float:
        """分析单个维度"""
        scores = {
            ComplexityLevel.LOW: 0,
            ComplexityLevel.MEDIUM: 0,
            ComplexityLevel.HIGH: 0,
            ComplexityLevel.ADVANCED: 0,
        }

        for level, keyword_list in keywords.items():
            for keyword in keyword_list:
                if keyword.lower() in task_lower:
                    scores[level] += 1

        if scores[ComplexityLevel.ADVANCED] > 0:
            return 4.0
        elif scores[ComplexityLevel.HIGH] > 0:
            return 3.0
        elif scores[ComplexityLevel.MEDIUM] > 0:
            return 2.0
        elif scores[ComplexityLevel.LOW] > 0:
            return 1.0
        return 1.5

    @classmethod
    def _score_to_level(cls, score: float) -> str:
        if score <= 1.2:
            return ComplexityLevel.LOW
        elif score <= 2.2:
            return ComplexityLevel.MEDIUM
        elif score <= 3.2:
            return ComplexityLevel.HIGH
        return ComplexityLevel.ADVANCED

    @classmethod
    def _extract_details(
        cls, task_lower: str, keywords: Dict[str, List[str]], dimension: str
    ) -> List[str]:
        """提取具体细节"""
        details = []
        for level, keyword_list in keywords.items():
            for keyword in keyword_list:
                if keyword.lower() in task_lower:
                    details.append(keyword)
        return list(set(details))[:5]

    @classmethod
    def get_complexity_description(cls, analysis: Dict[str, Any]) -> str:
        """获取复杂度描述"""
        level = analysis.get("overall_level", ComplexityLevel.MEDIUM)
        descriptions = {
            ComplexityLevel.LOW: "简单",
            ComplexityLevel.MEDIUM: "中等",
            ComplexityLevel.HIGH: "复杂",
            ComplexityLevel.ADVANCED: "高级",
        }
        return descriptions.get(level, "中等")
