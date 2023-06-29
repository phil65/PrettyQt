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


# from pygments.token import Other
# from pygments.lexer import include, default

#     tokens = {
#         'root': [
#             (r'\|', Other.Alternate),
#             (r'\(\?[iLmsux]+\)', Other.Directive),
#             (r'\(\?:', Other.Open.NonCapturing),
#             (r'(\(\?P<)(.*?)(>)', Other.Open.NamedCapturing),
#             (r'\(\?=', Other.Open.Lookahead),
#             (r'\(\?!', Other.Open.NegativeLookahead),
#             (r'\(\?<!', Other.Open.NegativeLookbehind),
#             (r'\(\?<', Other.Open.Lookbehind),
#             (r'(\(\?P=)(\w+)(?=\))', Other.Open.ExistsNamed),
#             (r'\(\?\(\d+\)', Other.Open.Exists),
#             (r'\(\?#.*?\)', Other.Comment),
#             (r'\(', Other.Open.Capturing),
#             (r'\)', Other.CloseParen),
#             (r'\[', Other.CharClass, 'charclass_start'),
#             (r'\\[1-9][0-9]?', Other.Backref),
#             include('only_in_verbose'),
#             include('suspicious'),
#             include('meta'),
#             (r'[{}]', Other.UnescapedCurly),  # legal in sre, illegal in regex
#             include('simpleliteral'),
#             (r'[^\\()|\[\]]+', Other.Literals), # TODO
#         ],
#         'suspicious': [
#             # misdone backreferences, tabs, newlines, and bel
#             (r'[\x00-\x08\x0a\x0d]', Other.Suspicious),
#         ],
#         'charclass_start': [
#             (r'\^', Other.NegateCharclass, 'charclass_squarebracket_special'),
#             default('charclass_squarebracket_special'),
#         ],
#         'charclass_squarebracket_special': [
#             (r'\]', Other.Literal.CloseCharClass, 'charclass_rest'),
#             default('charclass_rest'),
#         ],
#         'charclass_rest': [
#             (r'\]', Other.CloseCharClass, '#pop:3'),
#             (r'\\-', Other.EscapedDash),
#             (r'[\-^]', Other.Special),
#             include('simpleliteral'),
#             (r'\\.', Other.Suspicious),
#         ],
#         'meta': [
#             (r'\.', Other.Dot),
#             (r'\^', Other.Anchor.Beginning),
#             (r'\$', Other.Anchor.End),
#             (r'\\b', Other.Anchor.WordBoundary),
#             (r'\\A', Other.Anchor.BeginningOfString),
#             (r'\\Z', Other.Anchor.EndOfString),
#             (r'\*\?', Other.Repetition.NongreedyStar),
#             (r'\*', Other.Repetition.Star),
#             (r'\+\?', Other.Repetition.NongreedyPlus),
#             (r'\+', Other.Repetition.Plus),
#             (r'\?\?', Other.Repetition.NongreedyQuestion),
#             (r'\?', Other.Repetition.Question),
#             (r'\{\d+,(?:\d+)?\}\??', Other.Repetition.Curly),
#             (r'\{,?\d+\}\??', Other.Repetition.Curly),
#         ],
#         'simpleliteral': [
#             (r'[^\\^-]', Other.Literal),
#             (r'\\0[0-7]{0,3}', Other.Literal.Oct),  # \0 is legal
#             (r'\\x[0-9a-fA-F]{2}', Other.Literal.Hex),
#             (r'\\u[0-9a-fA-F]{4}', Other.Literal.Unicode),
#             (r'\\U[0-9a-fA-F]{8}', Other.Literal.LongUnicode),
#             (r'\\[\[\]]', Other.Literal.Bracket),
#             (r'\\[()]', Other.Literal.Paren),
#             (r'\\t', Other.Tab),
#             (r'\\n', Other.Newline),
#             (r'\\\.', Other.Literal.Dot),
#             (r'\\\\', Other.Literal.Backslash),
#             (r'\\\*', Other.Literal.Star),
#             (r'\\\+', Other.Literal.Plus),
#             (r'\\\|', Other.Literal.Alternation),
#             (r'\\\^', Other.Literal.Caret),
#             (r'\\\$', Other.Literal.Dollar),
#             (r'\\\?', Other.Literal.Question),
#             (r'\\[{}]', Other.Literal.Curly),
#             (r'\\\'', Other.Suspicious.Squo),
#             (r'\\\"', Other.Suspicious.Dquo),
#             (r'\\[sSwWdD]', Other.BuiltinCharclass),
#             (r'\\.', Other.Suspicious), # Other unnecessary escapes
#         ],
#         'only_in_verbose': [],
#     }


if __name__ == "__main__":
    from prettyqt import custom_widgets, widgets

    app = widgets.app()
    widget = custom_widgets.RegexLineEdit()
    widget.show()
    widget.value_changed.connect(print)
    app.exec()
