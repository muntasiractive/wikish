from typing import Optional

class WikiResult:
    def __init__(self, pageid: str, title: str, description: str, content: Optional[str] = None, summary: Optional[str] = None):
        self.pageid = pageid
        self.title = title
        self.description = description
        self.summary: Optional[str] = summary
        self.content: Optional[str] = content
