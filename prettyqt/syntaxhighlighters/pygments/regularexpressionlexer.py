from __future__ import annotations

from pygments.lexer import RegexLexer, bygroups
from pygments.token import Comment, Keyword, Name, Number, Operator, Text, Token


class CustomLexer(RegexLexer):
    name = "regex"
    aliases = ["regex"]
    filenames: list[str] = []

    tokens = {
        "root": [
            (r"\w+", Name),
            (r"\d+", Number),
            (r"[\s\,\:\-\"\']+", Text),
            (r"[\$\^]", Token),
            (r"[\+\*\.\?]", Operator),
            (
                r"(\()([\?\<\>\!\=\:]{2,3}.+?)(\))",
                bygroups(Keyword.Namespace, Name.Function, Keyword.Namespace),
            ),
            (r"(\()(\?\#.+?)(\))", bygroups(Comment, Comment, Comment)),
            (r"[\(\)]", Keyword.Namespace),
            (r"[\[\]]", Name.Class),
            (r"\\\w", Keyword),
            (r"[\{\}]", Operator),
        ]
    }
