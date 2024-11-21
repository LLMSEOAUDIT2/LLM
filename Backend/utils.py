# utils.py
import re

def markdown_to_html(markdown_text):
    """
    Convert Markdown to HTML by replacing Markdown symbols with corresponding HTML tags.
    """
    # Replace **...** with <strong>...</strong>
    html_text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", markdown_text)

    # Replace * or + at the start of a line with list <li>
    html_text = re.sub(r"^\* (.+)", r"<li>\1</li>", html_text, flags=re.MULTILINE)
    html_text = re.sub(r"^\+ (.+)", r"<li>\1</li>", html_text, flags=re.MULTILINE)

    # Wrap list items with <ul> tags
    if "<li>" in html_text:
        html_text = "<ul>" + html_text + "</ul>"

    # Replace newlines (\n) with <br> where appropriate
    html_text = re.sub(r"(?<!</li>)\n", r"<br>", html_text)

    return html_text
