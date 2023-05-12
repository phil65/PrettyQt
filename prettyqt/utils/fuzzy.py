from __future__ import annotations

import functools


# def fuzzy_search(search_set, text):
#     for i, word in enumerate(text.split(' ')):
#         token = list(word.lower())

#         if i is not 0:
#           search_set = matches

#         matches = []
#         for string in search_set:
#           token_index, string_index = 0, 0
#           matched_positions = []
#           string = string.lower()

#           while string_index < len(string):
#             if string[string_index] == token[token_index]:
#               matched_positions.append(string_index)
#               token_index += 1

#               if token_index >= len(token):
#                 # matches.append({
#                 #     'match': string,
#                 #     'positions': matched_positions
#                 # })
#                 matches.append(string)

#                 break
#             string_index += 1

#     return matches


def bold(text: str) -> str:
    return f"<b>{text}</b>"


def colored(text: str, color: str) -> str:
    return f"<font color={color!r}>{text}</font>"


def color_text(input_text: str, text: str, color: str, case_sensitive: bool = False):
    def converter(x):
        return x if case_sensitive else x.lower()

    output_text = ""
    for char in text:
        if input_text and converter(char) == converter(input_text[0]):
            output_text += bold(colored(char, color))
            input_text = input_text[1:]
        else:
            output_text += char
    return output_text


@functools.cache
def fuzzy_match_simple(pattern: str, instring: str, case_sensitive: bool = False) -> bool:
    """Return True if each character in pattern is found in order in instring.

    Arguments:
        pattern: the pattern to be matched
        instring: the containing string to search against
        case_sensitive: whether to match case-sensitively

    Returns:
        True if there is a match, False otherwise
    """
    p_idx, s_idx, p_len, s_len = 0, 0, len(pattern), len(instring)
    if not case_sensitive:
        pattern = pattern.lower()
        instring = instring.lower()
    while (p_idx != p_len) and (s_idx != s_len):
        if pattern[p_idx] == instring[s_idx]:
            p_idx += 1
        s_idx += 1
    return p_len != 0 and s_len != 0 and p_idx == p_len


@functools.cache
def fuzzy_match(
    pattern: str,
    instring: str,
    adj_bonus: int = 5,
    sep_bonus: int = 10,
    camel_bonus: int = 10,
    lead_penalty: int = -3,
    max_lead_penalty: int = -9,
    unmatched_penalty: int = -1,
) -> tuple[bool, int]:
    """Return match boolean and match score.

    Arguments:
        pattern: the pattern to be matched
        instring: the containing string to search against
        adj_bonus: bonus for adjacent matches
        sep_bonus: bonus if match occurs after a separator
        camel_bonus: bonus if match is uppercase
        lead_penalty: penalty applied for each letter before 1st match
        max_lead_penalty: maximum total ``lead_penalty``
        unmatched_penalty: penalty for each unmatched letter

    Returns:
        2-tuple with match truthiness at idx 0 and score at idx 1
    """
    score, p_idx, s_idx, p_len = 0, 0, 0, len(pattern)
    prev_match, prev_lower = False, False
    prev_sep = True  # so that matching first letter gets sep_bonus
    best_letter: str = ""
    best_lower: str | None = None
    best_letter_idx: int | None = None
    best_letter_score = 0
    matched_indices: list[int | None] = []

    for s_idx, s_char in enumerate(instring):
        p_char = pattern[p_idx] if (p_idx != p_len) else None
        p_lower = p_char.lower() if p_char else None
        s_lower, s_upper = s_char.lower(), s_char.upper()

        next_match = p_char and p_lower == s_lower
        rematch = best_letter and best_lower == s_lower

        advanced = next_match and best_letter
        p_repeat = best_letter and p_char and best_lower == p_lower

        if advanced or p_repeat:
            score += best_letter_score
            matched_indices.append(best_letter_idx)
            best_letter, best_lower, best_letter_idx = "", None, None
            best_letter_score = 0

        if next_match or rematch:
            new_score = 0

            # apply penalty for each letter before the first match
            # using max because penalties are negative (so max = smallest)
            if p_idx == 0:
                score += max(s_idx * lead_penalty, max_lead_penalty)

            # apply bonus for consecutive matches
            if prev_match:
                new_score += adj_bonus

            # apply bonus for matches after a separator
            if prev_sep:
                new_score += sep_bonus

            # apply bonus across camelCase boundaries
            if prev_lower and s_char == s_upper and s_lower != s_upper:
                new_score += camel_bonus

            # update pattern index iff the next pattern letter was matched
            if next_match:
                p_idx += 1

            # update best letter match (may be next or rematch)
            if new_score >= best_letter_score:
                # apply penalty for now-skipped letter
                if best_letter:
                    score += unmatched_penalty
                best_letter = s_char
                best_lower = best_letter.lower()
                best_letter_idx = s_idx
                best_letter_score = new_score

            prev_match = True

        else:
            score += unmatched_penalty
            prev_match = False

        prev_lower = s_char == s_lower and s_lower != s_upper
        prev_sep = s_char in "_ "

    if best_letter:
        score += best_letter_score
        matched_indices.append(best_letter_idx)

    return p_idx == p_len, score


# def get_best_matches_alt(
#     search_str: str,
#     collection: list[str],
#     # accessor: Callable[[str], Any] = lambda x: x,
#     sort_results: bool = True,
# ) -> Generator[str, None, None]:
#     """Return list of suggestions for matches of search string inside collection.

#     Arguments:
#         search_str:   A partial string which is typically entered by a user.
#         collection:   A collection of strings to get filtered.
#         accessor:     If the `collection` is not an iterable of strings,
#                       then use the accessor to fetch the string that
#                       will be used for fuzzy matching.
#         sort_results: The suggestions are sorted by considering the
#                       smallest contiguous match, followed by where the
#                       match is found in the full string. If two suggestions
#                       have the same rank, they are then sorted
#                       alpha-numerically. This parameter controls the
#                       *last tie-breaker-alpha-numeric sorting*. The sorting
#                       based on match length and position will be intact.

#     Returns:
#         suggestions (generator): A generator object that produces a list of
#             suggestions narrowed down from `collection` using the `input`.
#     """
#     suggestions: list[tuple[int, int, str, str]] = []
#     pat = ".*?".join(map(re.escape, search_str))
#     pat = f"(?=({pat}))"  # lookahead regex to manage overlapping matches
#     regex = re.compile(pat, re.IGNORECASE)
#     for item in collection:
#         if r := list(regex.finditer(accessor(item))):
#             best = min(r, key=lambda x: len(x.group(1)))  # find shortest match
#             suggestions.append((len(best.group(1)), best.start(), accessor(item), item))

#     if sort_results:
#         return (z[-1] for z in sorted(suggestions))
#     else:
#         return (z[-1] for z in sorted(suggestions, key=lambda x: x[:2]))


def accessor(x: tuple[str, int]) -> int:
    return x[1]


def get_best_matches(search_string: str, candidates: list[str]) -> list[tuple[str, int]]:
    """Return sorted list of all matches."""
    results: list[tuple[str, int]] = [
        (candidate, i[1])
        for candidate in candidates
        if (i := fuzzy_match(search_string, candidate))[0]
    ]
    return sorted(results, key=accessor, reverse=True)


if __name__ == "__main__":
    import time

    pat = "aab"
    candidates = ["aaaaab", "aacb", "abc", "abbaab"] * 10000
    a = time.time()
    get_best_matches(pat, candidates)
    print(time.time() - a)
