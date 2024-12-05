from app.utils.matching_utils import _match, MatchedLine
from commons import Line


def test_match_typical_case():
    azure_lines = [
        Line(polygons=[], content="hello everyone", confidence=1.0, spans=[]),
        Line(polygons=[], content="I love you so much", confidence=1.0, spans=[]),
        Line(polygons=[], content="bye bye", confidence=1.0, spans=[])
    ]
    matched_lines = [MatchedLine(azure_line) for azure_line in azure_lines]
    aws_strings = [
        "hellp everyone",
        "meow meow meow",
        "I lovc you su much",
        "bye ble",
        "bye bye"
    ]

    _match(matched_lines, aws_strings)

    assert matched_lines[0].aws_string == "hellp everyone"
    assert matched_lines[1].aws_string == "I lovc you su much"
    assert matched_lines[2].aws_string == "bye bye"

    unmatched_aws_strings = set(aws_strings) - set(
        matched_line.aws_string for matched_line in matched_lines if matched_line.aws_string
    )
    assert unmatched_aws_strings == {"meow meow meow", "bye ble"}


def test_match_partial_match():
    azure_lines = [
        Line(polygons=[], content="hello everyone", confidence=1.0, spans=[]),
        Line(polygons=[], content="hello", confidence=1.0, spans=[]),
    ]
    matched_lines = [MatchedLine(azure_line) for azure_line in azure_lines]
    aws_strings = [
        "hello e",
    ]

    _match(matched_lines, aws_strings)

    assert matched_lines[0].aws_string == None
    assert matched_lines[1].aws_string == "hello e"

    unmatched_aws_strings = set(aws_strings) - set(
        matched_line.aws_string for matched_line in matched_lines if matched_line.aws_string
    )
    assert unmatched_aws_strings == set()


def test_match_no_match():
    azure_lines = [
        Line(polygons=[], content="hello everyone", confidence=1.0, spans=[]),
    ]
    matched_lines = [MatchedLine(azure_line) for azure_line in azure_lines]
    aws_strings = [
        "abc",
        "def",
    ]

    _match(matched_lines, aws_strings, is_gpt=True)

    assert matched_lines[0].aws_string == None

    unmatched_aws_strings = set(aws_strings) - set(
        matched_line.aws_string for matched_line in matched_lines if matched_line.aws_string
    )
    assert unmatched_aws_strings == {"abc", "def"}
