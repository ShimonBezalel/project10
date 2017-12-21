"""

"""
from enum import Enum, unique

import re


@unique
class Token_Types(Enum):
    """

    """
    keyword         = "KEYWORD"
    symbol          = "SYMBOL"
    identifier      = "IDENTIFIER"
    int_const       = "INT_CONST"
    string_const    = "STRING_CONST"


@unique
class Key_Words(Enum):
    """

    """
    class_key       = "CLASS"
    method          = "METHOD"
    function        = "FUNCTION"
    constructor     = "CONSTRUCTOR"
    int_key         = "INT"
    bool_key        = "BOOL"
    char_key        = "CHAR"
    void_key        = "VOID"
    var_key         = "VAR"
    static_key      = "STATIC"
    field_key       = "FIELD"
    let_key         = "LET"
    do_key          = "DO"
    if_key          = "IF"
    else_key        = "ELSE"
    while_key       = "WHILE"
    return_key      = "RETURN"
    true_key        = "TRUE"
    false_key       = "FALSE"
    null_key        = "NULL"
    this_key        = "THIS"

keywords = {
    'class',
    'constructor',
    'function',
    'method',
    'field',
    'static',
    'var',
    'int',
    'char',
    'boolean',
    'void',
    'true',
    'false',
    'null',
    'this',
    'let',
    'do',
    'if',
    'else',
    'while',
    'return'
}

symbols = {
    '{',
    '}',
    '(',
    ')',
    '[',
    ']',
    '.',
    ',',
    ';',
    '+',
    '-',
    '*',
    '/',
    '&',
    '|',
    '<',
    '>',
    '=',
    '~'
}

STRING_DELIM = "\""

INT_CONST_MIN = 0
INT_CONST_MAX = 32767

class Comp_Exp(Enum):
    """

    """
    comment = re.compile("\/\/.*")


class JackTokenizer():
    """

    """
    def __init__(self, inputFile):
        """
        Opens the input file/stream and gets ready to tokenize it
        :param inputFile:
        """
        with open(inputFile, 'r') as self.file:
            temp = self.file.read()

        # remove comments
        clean = Comp_Exp.comment.value.sub(" ", temp)

        # split up into lines
        self.lines = clean.split("\n")

        # assuming non-empty file
        self.cur_line = self.lines[0]
        self.cur_char = 0


    def has_more_tokens(self):
        """
        Any more tokens in input?
        :return: bool
        """
        return not (self.cur_line != self.lines[-1] and self.cur_char < self.c


    def advance(self):
        """
        Get the next token and make it cur token. This method should only be called if
        has more tokens is true. There is no initial token in cur.
        :return:
        """
        pass

    def token_type(self):
        """
        Returns the type of the tokenizer
        :return:
        """
        pass


    def keyWord(self):
        """
        Returns the keyword which is the current toekn. Shoulf be called only when
        token_type is KEYWORD
        :return:
        """
        pass


    def symbol(self):
        """
        Returns  a char representing current token. Only called when token_type is SYMBOL
        :return:  char
        """


    def identifier(self):
        """
        Returns an identifier string representing current token. Only called when
        token_type is IDENTIFIER
        :return: String
        """

        pass


    def intVal(self):
        """
        Returns an int value representing current token. Only called when token_type is
        INT_CONST
        :return: int
        """
        pass


    def stringVal(self):
        """
        Returns a string representing current token. Only called when token_type is
        StringConst
        :return: string
        """

        pass

