import re

def parse_response(content: str) -> dict:
    code_match = re.search(r"```(?:python)?\n(.*?)```", content, re.DOTALL)
    code = code_match.group(1).strip() if code_match else ""

    title_match = re.search(r"\*\*(.*?)\*\*", content)
    title = title_match.group(1).strip() if title_match else ""

    return {
        "code": code,
        "title": title
    }
