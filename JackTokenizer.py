"""

"""
from enum import Enum

class Token_Types(Enum):
    """

    """
    keyword         = "KEYWORD"
    identifier      = "IDENTIFIER"
    int_const       = "INT_CONST"
    string_const    = "STRING_CONST"

class JackTokenizer():
    """

    """
    def __init__(self, inputFile):
        """
        Opens the input file/stream and gets ready to tokenize it
        :param inputFile:
        """
        pass


    def has_more_tokens(self):
        """
        Any more tokens in input?
        :return: bool
        """
        pass


    def advance(self):
        """
        Get the next token and make it cur token. This method should only be called if
        has more tokens is true. There is no initial token in cur.
        :return:
        """

    def tokenType(self):