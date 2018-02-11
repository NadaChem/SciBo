import asyncio


async def shell(command: str) -> str:
    """Runs a subprocess in shell and returns the output."""
    process = await asyncio.create_subprocess_shell(
        command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    results = await process.communicate()

    return ''.join(x.decode('utf-8') for x in results)


def no_codeblock(text: str) -> str:
    """
    Removes codeblocks (grave accents), python and sql syntax highlight indicators from a text if present.
    .. note:: only the start of a string is checked, the text is allowed to have grave accents in the middle
    """
    if text.startswith('```'):
        text = text[3:-3]

        if text.startswith(('py', 'sql')):
            text = '\n'.join(text.split('\n')[1:])

    if text.startswith('`'):
        text = text[1:-1]

    return text
