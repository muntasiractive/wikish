import asyncio
import typer
import mdv
import sys
from rich.console import Console, Group
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.markdown import Markdown
from rich.theme import Theme
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich.box import ROUNDED
from wikipedia import wikipedia as wiki

from .search import WikiSearch
from .ai import summarize, REPLICATE_AVAILABLE
from .utils import format_wiki_content

# Custom vibrant theme
THEME = Theme({
    "info": "cyan",
    "warning": "bold yellow",
    "error": "bold red",
    "success": "bold green",
    "heading": "bold magenta",
    "link": "underline blue",
    "index": "bold cyan",
})

console = Console(theme=THEME)

app = typer.Typer(pretty_exceptions_enable=False)

def show_splash():
    """Displays a beautiful splash screen with ASCII art."""
    ascii_art = """
[bold cyan] ██╗    ██╗ ██╗ ██╗  ██╗ ██╗ ███████╗ ██╗  ██╗ [/bold cyan]
[bold cyan] ██║    ██║ ██║ ██║ ██╔╝ ██║ ██╔════╝ ██║  ██║ [/bold cyan]
[bold cyan] ██║ █╗ ██║ ██║ █████╔╝  ██║ ███████╗ ███████║ [/bold cyan]
[bold cyan] ██║███╗██║ ██║ ██╔═██╗  ██║ ╚════██║ ██╔══██║ [/bold cyan]
[bold cyan] ╚███╔███╔╝ ██║ ██║  ██╗ ██║ ███████║ ██║  ██║ [/bold cyan]
[bold cyan]  ╚══╝╚══╝  ╚═╝ ╚═╝  ╚═╝ ╚═╝ ╚══════╝ ╚═╝  ╚═╝ [/bold cyan]
    """
    
    tagline = Text("Entertainment - Knowledge - Productivity", style="italic green")
    subtext = Text("& much more!", style="dim white")
    
    content = Group(
        Align.center(ascii_art),
        Align.center(tagline),
        Align.center(subtext)
    )
    
    banner = Panel(
        content,
        box=ROUNDED,
        padding=(1, 2),
        border_style="bright_blue",
        subtitle="v1.0.0",
        subtitle_align="right"
    )
    console.print(banner)

def create_results_table(results):
    """Creates a stylized table for search results."""
    table = Table(
        title="[bold cyan]Search Results[/bold cyan]",
        box=ROUNDED,
        header_style="bold magenta",
        expand=True
    )
    table.add_column("idx", style="dim", width=4, justify="right")
    table.add_column("Article Title", style="bold green", ratio=2)
    table.add_column("Snippet", style="yellow", ratio=3)

    for i, res in enumerate(results):
        table.add_row(str(i), res.title, res.description)
    return table

async def search_loop(query: str):
    show_splash()
    
    async with WikiSearch() as wiki_search:
        if not await wiki_search.search(query):
            # If search failed, let's try to ask for a new query instead of exiting
            query = Prompt.ask("[info]Try a different search term?[/info]")
            if not query:
                return
            if not await wiki_search.search(query):
                raise typer.Exit(code=1)

        console.print(create_results_table(wiki_search.results))

        while True:
            console.print("\n[dim]Tip: Enter index to read, 's' to search again, or 'q' to quit[/dim]")
            ans = Prompt.ask("[bold green]Choose action[/bold green]", default="0")
            
            if ans.lower() == 'q':
                break
            if ans.lower() == 's':
                new_query = Prompt.ask("[info]Search Wikipedia[/info]")
                if not new_query: continue
                if await wiki_search.search(new_query):
                    console.clear()
                    show_splash()
                    console.print(create_results_table(wiki_search.results))
                continue

            try:
                idx = int(ans)
                result = wiki_search.results[idx]
                
                with console.status(f"[info]Fetching '{result.title}'...[/info]"):
                    page = wiki.page(result.title)
                    formatted_content = format_wiki_content(result.title, page.content)
                    result.content = formatted_content
                    # mdv styling
                    styled_text = mdv.main(formatted_content, tab_length=8).replace('0m\n', '0m\n\n\n')
                    md_view = Markdown(styled_text)

                while True:
                    console.clear()
                    console.print(Panel(
                        f"[heading]📖 {result.title}[/heading]\n[dim]{result.description}[/dim]",
                        border_style="green",
                        box=ROUNDED
                    ))

                    with console.pager(styles=True):
                        console.print(md_view)

                    actions = ["n", "q"]
                    action_labels = "[bold cyan]n[/bold cyan]: New Result | [bold red]q[/bold red]: Quit"
                    if REPLICATE_AVAILABLE:
                        actions.append("s")
                        action_labels = "[bold yellow]s[/bold yellow]: AI Summary | " + action_labels
                    
                    console.print(Panel(action_labels, title="Commands", border_style="dim"))
                    
                    action = Prompt.ask("Action", choices=actions, default="n")

                    if action == "q":
                        sys.exit(0)
                    elif action == "s":
                        if not result.summary:
                            result.summary = await summarize(result.content)
                        console.clear()
                        console.print(Panel(
                            result.summary, 
                            title=f"🤖 AI Summary: {result.title}", 
                            border_style="yellow",
                            box=ROUNDED,
                            padding=(1, 2)
                        ))
                        Prompt.ask("\n[dim]Press Enter to return to article[/dim]")
                    elif action == "n":
                        console.clear()
                        show_splash()
                        console.print(create_results_table(wiki_search.results))
                        break

            except (ValueError, IndexError):
                console.print("[warning]Invalid index or action. Please try again.[/warning]")
            except Exception as e:
                console.print(f"[error]Error: {str(e)}[/error]")
                if not Confirm.ask("Go back to search results?"):
                    break

@app.command()
def run(
    query: str = typer.Argument(None, help="Search term (optional, will prompt if missing)"),
):
    """🚀 Search and read Wikipedia articles with a beautiful CLI interface."""
    if not query:
        show_splash()
        query = Prompt.ask("[bold cyan]What would you like to learn about?[/bold cyan]")
    
    if query:
        asyncio.run(search_loop(query))
    else:
        console.print("[warning]No search term provided. Exiting.[/warning]")

if __name__ == "__main__":
    app()
