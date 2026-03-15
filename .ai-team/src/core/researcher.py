"""
Concurrent Research Module - 并发调研模块

在 Agent 执行前自动进行并发网络调研
支持 Serper API（需要配置 key）或免费搜索
"""

import os
import asyncio
import aiohttp
import logging
from typing import List, Dict, Any, Optional
from urllib.parse import quote

logger = logging.getLogger(__name__)

SEARCH_TIMEOUT = 15


class ConcurrentResearcher:
    """并发调研器 - 同时从多个来源获取信息"""

    def __init__(self):
        self.search_engines = {
            "web": self._search_web,
            "github": self._search_github,
            "docs": self._search_docs,
        }
        self.serper_api_key = os.getenv("SERPER_API_KEY")

    async def research(self, query: str, sources: List[str] = None) -> Dict[str, str]:
        """
        并发执行多个搜索任务

        Args:
            query: 搜索关键词
            sources: 要搜索的来源列表，默认全部

        Returns:
            {source: result} 的字典
        """
        if sources is None:
            sources = list(self.search_engines.keys())

        tasks = []
        for source in sources:
            if source in self.search_engines:
                tasks.append(
                    self._safe_search(source, self.search_engines[source], query)
                )

        results = await asyncio.gather(*tasks, return_exceptions=True)

        output = {}
        for source, result in zip(sources, results):
            if isinstance(result, Exception):
                output[source] = f"Error: {str(result)}"
                logger.warning(f"Search {source} failed: {result}")
            else:
                output[source] = result

        return output

    async def _safe_search(self, name: str, func, query: str) -> str:
        """安全执行搜索"""
        try:
            return await func(query)
        except Exception as e:
            logger.error(f"Search {name} error: {e}")
            return f"Search failed: {e}"

    async def _search_web(self, query: str) -> str:
        """Web 搜索 - 优先使用 Serper API，失败则用免费搜索"""
        if self.serper_api_key:
            return await self._search_serper(query)
        return await self._search_brave(query)

    async def _search_serper(self, query: str) -> str:
        """使用 Serper API（需要配置 SERPER_API_KEY）"""
        try:
            url = "https://google.serper.dev/search"
            headers = {
                "X-API-KEY": self.serper_api_key,
                "Content-Type": "application/json",
            }
            payload = {"q": query, "num": 5}

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=SEARCH_TIMEOUT),
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return self._parse_serper_results(data)
                    return f"Serper API returned status {resp.status}"
        except Exception as e:
            logger.warning(f"Serper failed: {e}, falling back to free search")
            return await self._search_brave(query)

    def _parse_serper_results(self, data: dict) -> str:
        """解析 Serper API 结果"""
        results = []
        organic = data.get("organic", [])
        for item in organic[:5]:
            title = item.get("title", "")
            link = item.get("link", "")
            snippet = item.get("snippet", "")[:150]
            results.append(f"- {title}: {snippet}... ({link})")

        if results:
            return "Web Search Results:\n" + "\n".join(results)
        return "No web results found"

    async def _search_brave(self, query: str) -> str:
        """使用 DuckDuckGo HTML（免费，无需 API key）"""
        try:
            url = f"https://html.duckduckgo.com/html/?q={quote(query)}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=SEARCH_TIMEOUT),
                ) as resp:
                    if resp.status == 200:
                        text = await resp.text()
                        return self._parse_ddg_html(text)
                    return f"Search returned status {resp.status}"
        except Exception as e:
            return (
                f"Web search failed: {e}. Configure SERPER_API_KEY for better results."
            )

    def _parse_ddg_html(self, html: str) -> str:
        """解析 DuckDuckGo HTML 结果"""
        import re

        results = []

        titles = re.findall(r'<a class="result__a"[^>]*>(.*?)</a>', html)
        urls = re.findall(r'<a class="result__a"[^>]*href="(.*?)"', html)
        snippets = re.findall(r'<a class="result__snippet"[^>]*>(.*?)</a>', html)

        for i, (title, url) in enumerate(zip(titles[:5], urls[:5])):
            title = title.replace("<em>", "").replace("</em>", "").strip()
            snippet = (
                snippets[i].replace("<em>", "").replace("</em>", "").strip()[:150]
                if i < len(snippets)
                else ""
            )
            results.append(f"- {title}: {snippet}...")

        if results:
            return "Web Search Results:\n" + "\n".join(results)
        return "No web results found"

    def _parse_brave_results(self, data: dict) -> str:
        """解析 Brave Search 结果"""
        results = []
        web = data.get("web", {}).get("results", [])
        for item in web[:5]:
            title = item.get("title", "")
            url = item.get("url", "")
            desc = item.get("description", "")[:150]
            results.append(f"- {title}: {desc}... ({url})")

        if results:
            return "Web Search Results:\n" + "\n".join(results)
        return "No web results found"

    async def _search_github(self, query: str) -> str:
        """GitHub 搜索 - 使用 GitHub API"""
        try:
            token = os.getenv("GITHUB_TOKEN")
            url = f"https://api.github.com/search/repositories?q={quote(query)}&sort=stars&order=desc&per_page=5"
            headers = {
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "LLM-Agent-Team",
            }
            if token:
                headers["Authorization"] = f"token {token}"

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=SEARCH_TIMEOUT),
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return self._parse_github_api_results(data)
                    return f"GitHub search returned status {resp.status}"
        except Exception as e:
            return f"GitHub search failed: {e}"

    def _parse_github_api_results(self, data: dict) -> str:
        """解析 GitHub API 结果"""
        results = []
        items = data.get("items", [])
        for item in items[:5]:
            name = item.get("full_name", "")
            desc = item.get("description", "")[:150] or "No description"
            stars = item.get("stargazers_count", 0)
            url = item.get("html_url", "")
            results.append(f"- {name} ⭐{stars}: {desc} ({url})")

        if results:
            return "GitHub Top Repos:\n" + "\n".join(results)
        return "No GitHub repos found"

    async def _search_docs(self, query: str) -> str:
        """文档搜索 - 并行查询多个官方文档"""
        results = []
        async with aiohttp.ClientSession() as session:
            tasks = [
                self._search_mdn(query, session),
                self._search_react_docs(query, session),
                self._search_nodejs_docs(query, session),
            ]
            docs_results = await asyncio.gather(*tasks, return_exceptions=True)

            for content in docs_results:
                if isinstance(content, str) and content:
                    results.append(content)

        if results:
            return "Documentation Results:\n" + "\n".join(results[:3])
        return f"No documentation found for '{query}'"

    async def _search_mdn(self, query: str, session: aiohttp.ClientSession) -> str:
        """搜索 MDN"""
        try:
            url = f"https://developer.mozilla.org/en-US/search?q={quote(query)}"
            async with session.get(
                url, timeout=aiohttp.ClientTimeout(total=SEARCH_TIMEOUT)
            ) as resp:
                if resp.status == 200:
                    text = await resp.text()
                    import re

                    titles = re.findall(r'<a[^>]*href="([^"]*)"[^>]*>([^<]*)</a>', text)
                    relevant = [
                        (t[0], t[1])
                        for t in titles[:5]
                        if query.lower() in t[1].lower()
                    ]
                    if relevant:
                        return "MDN: " + ", ".join([t[1].strip() for t in relevant[:3]])
            return ""
        except:
            return ""

    async def _search_react_docs(
        self, query: str, session: aiohttp.ClientSession
    ) -> str:
        """搜索 React 文档"""
        try:
            url = f"https://react.dev/search?q={quote(query)}"
            async with session.get(
                url, timeout=aiohttp.ClientTimeout(total=SEARCH_TIMEOUT)
            ) as resp:
                if resp.status == 200:
                    text = await resp.text()
                    import re

                    titles = re.findall(
                        r'<a[^>]*class="[^"]*text[^"]*"[^>]*>([^<]*)</a>', text
                    )
                    relevant = [
                        t.strip() for t in titles[:5] if query.lower() in t.lower()
                    ]
                    if relevant:
                        return "React Docs: " + ", ".join(relevant[:3])
            return ""
        except:
            return ""

    async def _search_nodejs_docs(
        self, query: str, session: aiohttp.ClientSession
    ) -> str:
        """搜索 Node.js 文档"""
        try:
            url = f"https://nodejs.org/api?q={quote(query)}"
            async with session.get(
                url, timeout=aiohttp.ClientTimeout(total=SEARCH_TIMEOUT)
            ) as resp:
                if resp.status == 200:
                    text = await resp.text()
                    import re

                    titles = re.findall(
                        r'<a[^>]*href="(/api/[^"]*)"[^>]*>([^<]*)</a>', text
                    )
                    relevant = [
                        t[1].strip()
                        for t in titles[:5]
                        if query.lower() in t[1].lower()
                    ]
                    if relevant:
                        return "Node.js Docs: " + ", ".join(relevant[:3])
            return ""
        except:
            return ""


def run_concurrent_research(query: str) -> Dict[str, str]:
    """同步包装器 - 供外部调用"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    researcher = ConcurrentResearcher()
    return loop.run_until_complete(researcher.research(query))


def format_research_for_context(results: Dict[str, str]) -> str:
    """将调研结果格式化为 context 字符串"""
    lines = ["\n=== Concurrent Research Results ==="]

    for source, content in results.items():
        lines.append(f"\n--- {source.upper()} ---")
        lines.append(content)

    lines.append("\n=== End of Research ===\n")
    return "\n".join(lines)


if __name__ == "__main__":
    result = run_concurrent_research("react typescript best practices")
    print(format_research_for_context(result))
