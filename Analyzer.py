"""

"""
import sys
import os
import traceback

from JackTokenizer import JackTokenizer, Token_Types, keywords
from CompilationEngine import CompilationEngine


FILE_PATH = 1

FILE_EXTENSION_ASM = '.asm'
FILE_EXTENSION_VM = '.vm'

def main(filename):
    """

    :param filename:
    :return:
    """
    tokenizer = JackTokenizer(filename)
    engine = CompilationEngine(filename, filename)

    while tokenizer.has_more_tokens():
        tokenizer.advance()
        type = tokenizer.token_type()

        if type == Token_Types.keyword:
            key = tokenizer.keyWord()
            # if key == 'class':



        if type == Token_Types.symbol:
            symbol = tokenizer.symbol()

        if type == Token_Types.identifier:
            identifier = tokenizer.identifier()

        if type == Token_Types.int_const:
            const = tokenizer.intVal()

        if type == Token_Types.string_const:
            const = tokenizer.stringVal()




if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("Error: Wrong number of arguments.\n"
              "Usage: VMTranslator file_name.vm or /existing_dir_path/")
    else:
        main(sys.argv[FILE_PATH])

