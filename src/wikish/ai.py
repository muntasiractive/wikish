import os
from rich.console import Console

console = Console()

try:
    import replicate
    REPLICATE_AVAILABLE = True
except Exception:
    REPLICATE_AVAILABLE = False

async def summarize(content: str) -> str:
    if not REPLICATE_AVAILABLE:
        return "Summarization is unavailable because the 'replicate' library failed to load (likely incompatible with this Python version)."
    
    if not os.getenv("REPLICATE_API_TOKEN"):
        return "Missing API token for summary generation. Please set REPLICATE_API_TOKEN in your .env file."
    
    try:
        with console.status("[cyan]Generating summary...[/cyan]"):
            return ''.join(replicate.run(
                'meta/meta-llama-3-70b-instruct',
                input={'prompt': f"Summarize in 300 words, no other output {content}"}
            ))
    except Exception as e:
        return f"Summary generation failed: {str(e)}"
