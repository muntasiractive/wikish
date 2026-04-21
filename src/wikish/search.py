from typing import List, Optional
import aiohttp
import requests
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from .models import WikiResult

console = Console()

class WikiSearch:
    def __init__(self):
        self.results: List[WikiResult] = []
        self.base_url = "https://en.wikipedia.org/w/api.php"
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers={"User-Agent": "WikiSH/1.0 (https://github.com/yourusername/wikish)"})
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def search(self, query: str) -> bool:
        params = {
            "action": "query",
            "prop": "info|description",
            "format": "json",
            "titles": query,
            "generator": "search",
            "gsrsearch": query,
            "gsrlimit": 10
        }

        try:
            status = console.status("[cyan]Searching Wikipedia...[/cyan]")
            status.start()

            try:
                async with self.session.get(self.base_url, params=params) as response:
                    if response.status != 200:
                        raise requests.RequestException(f"Status code: {response.status}")
                    data = await response.json()
            finally:
                status.stop()

            if "query" not in data or "pages" not in data["query"]:
                console.print(Panel("[red bold]No results found[/red bold]", title="Search Error"))
                return False

            self.results = [
                WikiResult(
                    str(page["pageid"]),
                    page["title"],
                    page.get("description", "No description available")
                )
                for page in data["query"]["pages"].values()
            ]
            return True

        except Exception as e:
            console.print(Panel(f"[red bold]{str(e)}[/red bold]", title="Error"))
            return False

    def display_results(self):
        table = Table(title="Search Results", show_header=True, header_style="bold magenta")
        table.add_column("Index", style="cyan", width=6)
        table.add_column("Title", style="green")
        table.add_column("Description", style="yellow")

        for i, result in enumerate(self.results):
            table.add_row(str(i), result.title, result.description)

        console.print(Panel(table, border_style="green"))
