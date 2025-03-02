from __future__ import annotations

import functools


def bold(text: str) -> str:
    return f"<b>{text}</b>"


def colored(text: str, color: str) -> str:
    return f"<font color={color!r}>{text}</font>"


@functools.cache
def color_text(input_text: str, text: str, color: str, case_sensitive: bool = False):
    """Color first occurences of input_text chars in text with given color."""

    def converter(x):
        return x if case_sensitive else x.lower()

    input_text = input_text if case_sensitive else input_text.lower()
    output_text = ""
    to_color = ""
    for char in text:
        if input_text and converter(char) == input_text[0]:
            to_color += char
            input_text = input_text[1:]
        else:
            if to_color:
                output_text += bold(colored(to_color, color))
                to_color = ""
            output_text += char
    if to_color:
        output_text += bold(colored(to_color, color))
    return output_text


if __name__ == "__main__":
    pat = "aab"
    candidates = ["aaaaab", "aacb", "abc", "abbaab"] * 10000
    print(color_text("ac", "abbbbc", "green"))
