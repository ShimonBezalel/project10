"""

"""

from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine


FILE_PATH = 1

FILE_EXTENSION_XML = '.xml'
FILE_EXTENSION_JACK = '.jack'
FILE_EXTENSION_VM = '.vm'

class Analyzer():
    """

    :param filename:
    :return:
    """
    def __init__(self):
        pass

    def tokenize(self, filename):
        tokenizer = JackTokenizer(filename + FILE_EXTENSION_JACK)
        with open(filename + "T" + FILE_EXTENSION_XML, 'w') as out:
            out.write("<tokens>\n")
            while tokenizer.has_more_tokens():
                tokenizer.advance()
                out.write("<" + tokenizer.token_type().value + "> "
                          + tokenizer.cur_val + " </" +
                          tokenizer.token_type().value + ">\n")

                print(tokenizer.token_type().value.lower(), tokenizer.cur_val)
            out.write("</tokens>\n")

    def compile(self, source, destination):
        engine = CompilationEngine(source, destination)





if __name__ == '__main__':

    a = Analyzer()
    a.tokenize("tests/ExpressionLessSquare")

