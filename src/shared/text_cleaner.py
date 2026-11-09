import re
from typing import List


def clean_text(text: str) -> str:
    """Clean text by removing excessive whitespace and newlines."""
    if not text:
        return text
    text = re.sub(r"\s+", " ", text).strip()
    return text


def remove_tags(text: str) -> str:
    """Remove [1/100] style tags and similar patterns."""
    if not text:
        return text
    text = re.sub(r"\[\d+/\d+\]", "", text)
    text = re.sub(r"\[\d+-\d+\]", "", text)
    text = re.sub(r"\[[^\]]*\]", "", text)
    return clean_text(text)


def remove_links(text: str) -> str:
    """Remove URLs from text."""
    if not text:
        return text
    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    text = re.sub(r"t\.me/\S+", "", text)
    return clean_text(text)


def remove_usernames(text: str) -> str:
    """Remove @username mentions."""
    if not text:
        return text
    text = re.sub(r"@\w+", "", text)
    return clean_text(text)


def remove_custom_words(text: str, words: List[str] = None) -> str:
    """Remove specified custom words from text."""
    if not text:
        return text
    if words is None:
        words = []
    for word in words:
        text = re.sub(re.escape(word), "", text, flags=re.IGNORECASE)
    return clean_text(text)


def smart_filter(text: str, remove_custom: List[str] = None) -> str:
    """Apply all cleaning filters to text."""
    text = remove_tags(text)
    text = remove_links(text)
    text = remove_usernames(text)
    text = remove_custom_words(text, remove_custom)
    return clean_text(text)