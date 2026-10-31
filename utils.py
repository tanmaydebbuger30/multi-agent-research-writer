def text_of(msg):
    """Extract plain text from a model response, whatever shape it comes in."""
    content = msg.content

    if isinstance(content, str):
        return content

    return "".join(
        block.get("text", "")

        for block in content
        if isinstance(block, dict) and block.get("type") == "text"

    )