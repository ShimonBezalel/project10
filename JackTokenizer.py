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

    # def str_all(self):
    #     conc_str = ''
    #     for key in self:
    #         conc_str += key.value.lower() + "|"
    #     return conc_str[:-1]

def gen_keywords():
    conc_str = ''
    for key in Key_Words:
        conc_str += key.value.lower() + "\\s|"
    return conc_str[:-1]

def gen_symbols():
    conc_str = ''
    for symbol in symbols:
        conc_str += "\\" + symbol + "|"
    return conc_str[:-1]

#
# keywords = {
#     'class',
#     'constructor',
#     'function',
#     'method',
#     'field',
#     'static',
#     'var',
#     'int',
#     'char',
#     'boolean',
#     'void',
#     'true',
#     'false',
#     'null',
#     'this',
#     'let',
#     'do',
#     'if',
#     'else',
#     'while',
#     'return'
# }

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

# STRING_DELIM = "\""

INT_CONST_MIN = 0
INT_CONST_MAX = 32767

class Comp_Exp(Enum):
    """

    """
    comment = re.compile("\/\/.*")
    # string_single_line = re.compile("\".*\"")
    string_single_line = re.compile("(\"([^\\\"]*(\\\")*[^\\\"]*)*\")")
    string_multi_line_open = re.compile("(\"([^\\\"]*(\\\")*[^\\\"]*)*)")
    # string_multi_line_close = re.compile(".*\"")
    keywords = re.compile(gen_keywords())
    symbols = re.compile(gen_symbols())
    floats = re.compile("((\d+\.\d+)|(\d+))")
    ints = re.compile("\d+")
    identifiers = re.compile("\w")
    spaces = re.compile("\s+")


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
        self.cur_token = None
        self.cur_line_index = 0
        self.cur_line = self.lines[self.cur_line_index]


    def has_more_tokens(self):
        """
        Any more tokens in input?
        :return: bool
        """
        return not (self.cur_line != self.lines[-1] and
                    self.cur_char < self.cur_line.__len__())


    def advance(self):
        """
        Get the next token and make it cur token. This method should only be called if
        has more tokens is true. There is no initial token in cur.
        :return:
        """
        self.cur_type, self.cur_val = self.get_token()

    def token_type(self):
        """
        Returns the type of the tokenizer
        :return:
        """
        return self.cur_type


    def keyWord(self):
        """
        Returns the keyword which is the current toekn. Should be called only when
        token_type is KEYWORD
        :return:
        """
        assert self.cur_type is Token_Types.keyword
        return self.cur_val


    def symbol(self):
        """
        Returns  a char representing current token. Only called when token_type is SYMBOL
        :return:  char
        """
        assert self.cur_type is Token_Types.symbol
        return self.cur_val


    def identifier(self):
        """
        Returns an identifier string representing current token. Only called when
        token_type is IDENTIFIER
        :return: String
        """
        assert self.cur_type is Token_Types.identifier
        return self.cur_val


    def intVal(self):
        """
        Returns an int value representing current token. Only called when token_type is
        INT_CONST
        :return: int
        """
        assert self.cur_type is Token_Types.int_const
        return self.cur_val


    def stringVal(self):
        """
        Returns a string representing current token. Only called when token_type is
        StringConst
        :return: string
        """
        assert self.cur_type is Token_Types.string_const
        return self.cur_val

    def get_token(self):
        """

        :return:
        """
        # tokens = []
        while self.cur_line:
            # In case of a token match, we yield it and substitute it from what is left
            # of the current line being read

            string_match = Comp_Exp.string_single_line.value.match(self.cur_line)
            # Found a full string in what is left of the current line.
            # Note the string-const values have their "" symbols left out.
            if string_match:
                # tokens.append((Token_Types.string_const, string_match.group(0)))
                yield (Token_Types.string_const, string_match.group(0)[1:-1])
                self.cur_line = self.cur_line[string_match.end():]
                continue

            begin_string_match = Comp_Exp.string_multi_line_open.value.match(
                self.cur_line)
            # Only the opening of a string found in current line. In this case we must
            # find the end rest of the string a lop them together. This can be done by
            # adding the next row to the current row and continuing from there.
            if begin_string_match:
                self.cur_line_index += 1
                self.cur_line = self.cur_line + "\n" + self.lines[self.cur_line_index]
                continue

            keyword_match = Comp_Exp.kewords.value.match(self.cur_line)
            if keyword_match:
                # remove space
                yield (Token_Types.keyword, keyword_match.group(0)[:-1])
                self.cur_line = self.cur_line[keyword_match.end():]
                continue

            # keyword_match = Comp_Exp.kewords.value.match(self.cur_line)
            # if keyword_match:
            #     yield (Token_Types.keyword, keyword_match.group(0))
            #     self.cur_line = self.cur_line[keyword_match.end():]
            #     continue

            symbols_match = Comp_Exp.symbols.value.match(self.cur_line)
            if symbols_match:
                yield (Token_Types.symbol, symbols_match.group(0))
                self.cur_line = self.cur_line[symbols_match.end():]
                continue

            int_match = Comp_Exp.ints.value.match(self.cur_line)
            if int_match:
                yield (Token_Types.int_const, int_match.group(0))
                self.cur_line = self.cur_line[symbols_match.end():]
                continue

            identifier_match = Comp_Exp.identifiers.value.match(self.cur_line)
            if identifier_match:
                yield (Token_Types.identifier, identifier_match.group(0))
                self.cur_line = self.cur_line[symbols_match.end():]
                continue

            space_match = Comp_Exp.spaces.value.match(self.cur_line)
            if space_match:
                # yield (Token_Types.identifier, identifier_match.group(0))
                self.cur_line = self.cur_line[space_match.end():]
                continue

        self.cur_line_index += 1

        assert self.has_more_tokens()

        self.cur_line = self.lines[self.cur_line_index]




if __name__ == '__main__':

    f = JackTokenizer("tests/Main.jack")
    while f.has_more_tokens():
        f.advance()
        print(f.token_type().value, f.get_token())















