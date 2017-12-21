"""

"""

from JackTokenizer import JackTokenizer, Token_Types, KEYWORDS

END_LINE = "\n"
EXPREESSIONS = {"INT_CONST": "integerConstant",
                "STRING_CONST": "stringConstant",
                "KEYWORD": "KeywordConstant",
                "IDENTIFIER": "identifier"}
# SPACE = " "

class CompilationEngine():
    """

    """

    def __init__(self, input_file, output_file):
        """
        Creates a new compilation engine with the given input and output. The next
        routine called must be compile_class()
        :param input_file:
        :param output_file:
        """
        self.tokenizer = JackTokenizer(input_file)
        self.output = open(output_file)
        # self.write("tokens")
        # self.indent = 0

        # self.full_recursion()
        # with open(output_file) as self.output:
        #     pass
        self.num_spaces = 0
        # self.prefix = ""


    def compile_class(self):
        """
        Compiles a complete class
        :return:
        """
        self.write('classDec', num_tabs=self.indent)

        self.tokenizer.advance()
        self.write_terminal(Token_Types.identifier, self.tokenizer.identifier())


        self.write('{')

    def eat(self, string):
        type = self.tokenizer.token_type()
        value = "not keyword and not symbol"
        if type == Token_Types.keyword:
           value = self.tokenizer.keyWord()
        elif type == Token_Types.symbol:
            value = self.tokenizer.symbol()

        if value != string:
            raise Exception(value + "- is not the expected string, " + string)
        self.tokenizer.advance()


    def compile_class_var_dec(self):
        """
        Compiles a static declaration or a field declaration.
        :return:
        """
        pass


    def compile_subroutine(self):
        """
        Compiles a complete method, function or constructor
        :return:
        """

        pass


    def compile_param_list(self):
        """
        Compiles a parameter list, which may be empty, not including the "()"
        :return:
        """

        pass


    def compile_var_dec(self):
        """
        Compiles a var declaration
        :return:
        """
        self.write("varDec", num_tabs=self.indent)
        self.write_terminal("varDec", 4)


    def compile_statements(self):
        """
        Compile a sequence of statements not including the "{}"
        :return:
        """
        if not self.tokenizer.token_type() in keywords:
            raise Exception("Can't use compile_statement if the current token isn't a keyword.");
        statement = self.tokenizer.keyWord()

        self.write(statement + "Statement", True)
        if statement == 'let':
            self.compile_let()
        elif statement == 'if':
            self.compile_if()
        elif statement == 'while':
            self.compile_while()
        elif statement == 'do':
            self.compile_do()
        elif statement == 'return':
            self.compile_return()
        else:
            raise Exception("Invalid statement.")
        self.write(statement + "Statement", True, True)

    def compile_do(self):
        """
        Compile do statment
        :return:
        """
        self.eat('do')
        self.num_spaces += 1
        self.write("<keyword> do </keyword>")

        self.compile_subroutineCall()

        self.eat(';')
        self.write("<symbol> ; </symbol>")
        self.num_spaces -= 1


    def compile_let(self):
        """
        Compile let statement
        :return:
        """
        self.eat('let')
        self.num_spaces += 1
        self.write("<keyword> let </keyword>")

        self.compile_var_dec()
        self.possible_array()

        self.eat('=')
        self.write("<symbol> = </symbol>")

        self.compile_expression()

        self.eat(';')
        self.write("<symbol> ; </symbol>")
        self.num_spaces -= 1
        # self.write("</letStatement>")

    def possible_array(self):
        try:
            self.eat('[')
        except:
            # There is no array
            return
        # There is an array
        self.write("<symbol> [ </symbol>")
        self.compile_expression()
        self.eat(']')
        self.write("<symbol> ] </symbol>")

    def compile_while(self):
        """

        :return:
        """
        self.eat('while')
        # self.write("<whileStatement>")
        self.num_spaces += 1
        self.write("<keyword> while </keyword>")

        self.eat('(')
        self.write("<symbol> ( </symbol>")
        self.compile_expression()
        self.eat(')')
        self.write("<symbol> ) </symbol>")

        self.eat('{')
        self.write("<symbol> { </symbol>")
        self.compile_statements()
        self.eat('}')
        self.write("<symbol> } </symbol>")

        self.num_spaces -= 1
        # self.write("</whileStatement>")



    def compile_return(self):
        """

        :return:
        """
        self.eat('return')
        self.num_spaces += 1
        self.write("<keyword> return </keyword>")

        try:
            self.eat(';')
        except: # would it work?
            self.compile_expression()
            self.eat(';')

        self.write("<symbol> ; </symbol>")
        self.num_spaces -= 1


    def compile_if(self):
        """

        :return:
        """
        self.eat('if')
        # self.write("<ifStatement>")
        self.num_spaces += 1
        self.write("<keyword> if </keyword>")

        self.eat('(')
        self.write("<symbol> ( </symbol>" + END_LINE)
        self.compile_expression()
        self.eat(')')
        self.write("<symbol> ) </symbol>" + END_LINE)

        self.eat('{')
        self.write("<symbol> { </symbol>" + END_LINE)
        self.compile_statements()
        self.eat('}')
        self.write("<symbol> } </symbol>" + END_LINE)
        self.possible_else()

        self.num_spaces -= 1
        # self.write("</ifStatement>" + END_LINE)

    def possible_else(self):
        try:
            self.eat('else')
        except:
            # There is no else so we can return
            return

        # There is an else, so we handle it properly
        self.write("<keyword> else </keyword>" + END_LINE)

        self.eat('{')
        self.write("<symbol> { </symbol>" + END_LINE)
        self.compile_statements()
        self.eat('}')
        self.write("<symbol> } </symbol>" + END_LINE)

    def compile_expression(self):
        """
        Compile an expression
        :return:
        """
        pass

    def compile_subroutineCall(self):
        pass

    def compile_term(self):
        """
        Compiles a temp. This routine is faced with a slight difficulty when trying to
        decide between some of the alternative parsing rules. Specifically,
        if the current token is an identifier, the routine must distinguish between a
        variable, an array entry, and a subroutine call. A single look-ahead token,
        which may be one of "[", "(", or "." suffices to distiguish between the three
        possibilities. Any other token is not part of this term and should not be
        advanced over.
        :return:
        """
        self.write("term", True)
        self.num_spaces += 1

        type = self.tokenizer.token_type()
        # maybe i should divide it for int and string
        if type == Token_Types.int_const or type == Token_Types.string_const :
            value = self.tokenizer.intVal() if type == Token_Types.int_const else self.tokenizer.stringVal()
            self.write("<" + EXPREESSIONS[type] + ">\t" +
                       value +
                       "\t</" + EXPREESSIONS[type] + ">")
        elif type == Token_Types.keyword:
            if self.tokenizer.keyWord().value in ["TRUE", "FALSE", "NULL", "THIS"]:
                self.write("<" + EXPREESSIONS[type] + ">\t" +
                           self.tokenizer.keyWord().value.lower() +
                           "\t</" + EXPREESSIONS[type] + ">" + END_LINE)
            else:
                raise Exception()
        elif type == Token_Types.identifier:
            self.term_identifier(self.tokenizer.identifier())

        self.num_spaces -= 1
        self.write("term", True, True)

    def term_identifier(self, var_name):
        # try:
        #     self.eat("[")
        # except:
        # if not self.tokenizer.has_more_tokens(): # already doing it by itself
        #     raise Exception()
        self.tokenizer.advance()
        if self.tokenizer.token_type() == Token_Types.symbol:
            next_symbol = self.tokenizer.symbol()
            if next_symbol == '[':
                self.eat('[')
                self.write("<symbol> [ </symbol>")
                self.compile_expression()
                self.eat(']')
                self.write("<symbol> ] </symbol>")

            elif next_symbol == '(':
                self.eat('(')
                self.write("<symbol> ( </symbol>")
                self.compile_expression()
                self.eat(')')
                self.write("<symbol> ) </symbol>")
            elif next_symbol == '.':
            else:
                raise Exception()

    def compile_expression_list(self):
        """
        Compile a comma-separated list of expressions, which may be empty
        :return:
        """
        pass


    def write(self, str, delim = False, end = False):
        """

        :param str:
        :return:
        """


        if end:
            str = "/" + str
        if delim:
            self.output.write("\t" * self.num_spaces + "<" + str + ">" + END_LINE)
        else:
            self.output.write("\t" * self.num_spaces + str + END_LINE)


    def write_terminal(self, t_type, arg):
        """

        :param t_type:
        :param arg:
        :return:
        """
        self.write(t_type.value, num_tabs=self.indent)
        self.write(t_type.value + " " + arg, delim=False,
                   num_tabs=self.indent + 1)
        self.write(t_type.value, num_tabs=self.indent, end=True)


    def write_recursive(self, name, advance_lim=1):
        """

        :param name:
        :param advance_lim:
        :return:
        """
        self.write(name, num_tabs=self.indent)

        self.indent += 1
        self.call_single()
        for _ in range(advance_lim - 1):
            if self.tokenizer.has_more_tokens():
                self.tokenizer.advance()
                self.call_single()
            else:
                raise ValueError("expected more tokens")

        # self.write(name + " " + arg, delim=False,
        #            num_tabs=self.indent + 1)
        self.write(name, num_tabs=self.indent, end=True)


    # def write_recursive(self, type):
    #     """
    #
    #     :param type:
    #     :return:
    #     """
    #     self.write(type.value, num_tabs=self.indent)
    #     self.indent += 1
    #
    #     # need some sort of termination in call compile
    #     # or type specific implementation
    #     self.full_recursion()
    #
    #     self.write(type.value, num_tabs=self.indent, end=True)



    def full_recursion(self):
        """

        :param token:
        :return:
        """
        while self.tokenizer.has_more_tokens():
            self.tokenizer.advance()

            type = self.tokenizer.token_type()

            terminal_arg = False

            if type == Token_Types.keyword:
                terminal_arg = self.tokenizer.keyWord()

            if type == Token_Types.symbol:
                terminal_arg = self.tokenizer.symbol()

            if type == Token_Types.identifier:
                terminal_arg = self.tokenizer.identifier()

            if type == Token_Types.int_const:
                terminal_arg = self.tokenizer.intVal()

            if type == Token_Types.string_const:
                terminal_arg = self.tokenizer.stringVal()

            if terminal_arg:
                self.write_terminal(type, terminal_arg)

            else:
                self.write_recursive(type)


    def call_single(self):
        """

        :return:
        """
        type = self.tokenizer.token_type()

        terminal_arg = False

        if type == Token_Types.keyword:
            terminal_arg = self.tokenizer.keyWord()

        if type == Token_Types.symbol:
            terminal_arg = self.tokenizer.symbol()

        if type == Token_Types.identifier:
            terminal_arg = self.tokenizer.identifier()

        if type == Token_Types.int_const:
            terminal_arg = self.tokenizer.intVal()

        if type == Token_Types.string_const:
            terminal_arg = self.tokenizer.stringVal()

        if terminal_arg:
            self.write_terminal(type, terminal_arg)

        else:
            self.write_recursive(type)





