import re


def get_num_figures(comment: str):
    if comment is None:
        return 0

    # regex pattern to match "n figures" or "n + m figures", or mixtures of both
    pattern = r"\d+\s*\+\s*\d+\s*figures|\d+\s*figures"
    matches = re.findall(pattern, comment)

    if len(matches) == 0:
        return 0
    else:
        num_figures = sum(sum(int(n) for n in re.findall(r"\d+", match))
                          for match in matches)
    return num_figures


def get_num_pages(comment: str):
    if comment is None:
        return 0

    # regex pattern to match "n pages" or "n + m pages", no mixtures
    pattern = r"\d+\s*\+\s*\d+\s*pages|\d+\s*pages"
    match = re.search(pattern, comment)

    if not match:
        return 0
    else:
        match = match.group()
        num_pages = sum(int(n) for n in re.findall(r"\d+", match))
    return num_pages


def get_number_eqs(summary: str):
    if summary is None:
        return 0

    pattern = r"\${1,2}([\s\S]+?)\${1,2}"
    matches = re.findall(pattern, summary)
    return len(matches)


def replace_eq(summary: str, replacement: str):
    if summary is None:
        return summary

    pattern = r"\${1,2}([\s\S]+?)\${1,2}"
    return re.sub(pattern, replacement, summary)
