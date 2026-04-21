import re

def remove_empty_headings(text: str) -> str:
    """Removes headings that have no content beneath them."""
    pattern_to_remove = re.compile(r'##(.*)\n\n\n')
    return pattern_to_remove.sub('', text)

def format_wiki_content(title: str, content: str) -> str:
    """Formats raw wiki content into clean markdown."""
    content = content.replace("= ", "# ")
    while content.find("=#") != -1:
        content = content.replace("=#", "##")

    while content.find(" =") != -1:
        content = content.replace(" =", " ")

    return f"# {title}\n\n\n" + remove_empty_headings(content)
