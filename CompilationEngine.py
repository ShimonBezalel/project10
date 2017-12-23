"""

"""

from JackTokenizer import JackTokenizer, Token_Types, KEYWORDS

END_LINE    = "\n"
TAB         = "\t"

EXPREESSIONS = {"INT_CONST": "integerConstant",
                "STRING_CONST": "stringConstant",
                "KEYWORD": "KeywordConstant",
                "IDENTIFIER": "identifier"}
STATEMENTS  = ['let', 'if', 'while', 'do', 'return']
OPERANDS    = ['+', '-', '*', '&quot', '&amp', '|', '&lt', '&gt', '=']

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
        self.num_spaces = 0

        while self.tokenizer.has_more_tokens():
            self.tokenizer.advance()
            assert self.tokenizer.token_type() == Token_Types.keyword
            if self.tokenizer.keyWord() == 'class':
                self.compile_class()
            else:
                raise KeyError("Received a token that does not fit the begining of a "
                               "module. " + self.tokenizer.keyWord() + " in " + input_file)

    def compile_class(self):
        """
        Compiles a complete class
        :return:
        """
        self.write('class', delim=True)
        self.num_spaces += 1
        self.write_terminal(self.tokenizer.token_type().value, self.tokenizer.keyWord())
        self.eat('class')

        t_type, class_name = self.tokenizer.token_type(), self.tokenizer.keyWord()
        self.write_terminal(t_type.value, class_name)

        self.tokenizer.advance()

        t_type, symbol = self.tokenizer.token_type(), self.tokenizer.keyWord()
        self.write_terminal(t_type.value, symbol)
        self.eat('{')

        t_type, token = self.tokenizer.token_type(), self.tokenizer.keyWord()
        while token != '}':
            assert t_type == Token_Types.keyword
            if token == 'var':
                self.compile_class_var_dec()
            elif token == 'function':
                self.compile_subroutine()

            self.tokenizer.advance()

            t_type, token = self.tokenizer.token_type(), self.tokenizer.keyWord()

        assert t_type == Token_Types.symbol
        self.write_terminal(t_type.value, token)
        self.num_spaces -= 1
        self.write('class', delim=True, end=True)

    def eat(self, string):
        """
        If the given string is the same as current token (only if it keyword or symbol) the
        tokenizer of the object will be advanced, otherwise an exception will be raised.
        :param string: the expected string.
        :raise: the current token is not the expected string.
        """
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
        self.write('subroutineDec', delim=True)
        self.num_spaces += 1
        self.write_terminal(self.tokenizer.token_type().value, self.tokenizer.keyWord())

        # self.eat('function' | 'method' | 'constructor')
        self.tokenizer.advance()

        t_type, func_type = self.tokenizer.token_type(), self.tokenizer.keyWord()
        self.write_terminal(t_type.value, func_type)

        # self.eat('void' | some other type)
        self.tokenizer.advance()

        t_type, func_name = self.tokenizer.token_type(), self.tokenizer.keyWord()
        self.write_terminal(t_type.value, func_name)

        t_type, symbol = self.tokenizer.token_type(), self.tokenizer.keyWord()
        self.write_terminal(t_type.value, symbol)
        self.eat('(')

        self.compile_param_list()

        t_type, symbol = self.tokenizer.token_type(), self.tokenizer.keyWord()
        self.write_terminal(t_type.value, symbol)
        self.eat(')')

        t_type, symbol = self.tokenizer.token_type(), self.tokenizer.keyWord()
        self.write_terminal(t_type.value, symbol)
        self.eat('{')

        t_type, token = self.tokenizer.token_type(), self.tokenizer.keyWord()
        while token != '}':
            assert t_type == Token_Types.keyword
            if token == 'var':
                self.compile_var_dec()
            elif token in STATEMENTS:
                self.compile_statements()
            self.tokenizer.advance()
            t_type, token = self.tokenizer.token_type(), self.tokenizer.keyWord()

        assert t_type == Token_Types.symbol
        self.write_terminal(t_type, token)
        self.num_spaces -= 1
        self.write('subroutineDec', delim=True, end=True)
        # self.eat('}')

    def compile_param_list(self):
        """
        Compiles a parameter list, which may be empty, not including the "()"
        :return:
        """
        self.write('paramaterList', delim=True)
        self.num_spaces += 1

        t_type, token = self.tokenizer.token_type(), self.tokenizer.keyWord()
        while token != ')':
            # Write var type
            self.write_terminal(t_type, token)

            self.tokenizer.advance()

            # Write var name
            t_type, token = self.tokenizer.token_type(), self.tokenizer.keyWord()
            self.write_terminal(t_type, token)

            # Press on
            self.tokenizer.advance()

            t_type, token = self.tokenizer.token_type(), self.tokenizer.keyWord()

        assert t_type == Token_Types.symbol
        self.num_spaces -= 1
        self.write('paramaterList', delim=True, end=True)

    def compile_var_dec(self):
        """
        Compiles a var declaration
        :return:
        """
        pass

    def compile_statements(self):
        """
        Compile a sequence of 0 or more statements, not including the "{}".
        """
        # if self.tokenizer.token_type() != Token_Types.keyword:
        #     return
        #     # raise Exception("Can't use compile_statement if the current token isn't a keyword.")
        # statement = self.tokenizer.keyWord()
        # if statement not in ['let', 'if', 'while', 'do', 'return']:
        #     return
        self.write("statements", True)
        self.num_spaces += 1

        if (self.tokenizer.token_type() == Token_Types.keyword and
                    self.tokenizer.keyWord() in STATEMENTS):
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
            # else:
            #     raise Exception("Invalid statement.")
            self.write(statement + "Statement", True, True)
        self.compile_statements()

        self.num_spaces -= 1
        self.write("statements", True, True)

    def compile_do(self):
        """
        Compile do statement.
        :return:
        """
        self.eat('do')
        self.num_spaces += 1
        self.write("<keyword> do </keyword>")

        # is the check is necessary?  probably not..
        if type != Token_Types.identifier:
            raise Exception()
        self.write("<identifier>\t" + self.tokenizer.identifier() + "\t</identifier>")
        self.tokenizer.advance()
        self.subroutineCall_continue()

        self.eat(';')
        self.write("<symbol> ; </symbol>")
        self.num_spaces -= 1


    def compile_let(self):
        """
        Compile let statement.
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
        """
        Compile 0 or 1 array.
        """
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
        Compile while statement.
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
        Compile return statement.
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
        Compile if statement.
        """
        self.eat('if')
        # self.write("<ifStatement>")
        self.num_spaces += 1
        self.write("<keyword> if </keyword>")

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
        self.possible_else()

        self.num_spaces -= 1
        # self.write("</ifStatement>" + END_LINE)

    def possible_else(self):
        """
        Compile 0 or 1 else sections.
        """
        try:
            self.eat('else')
        except:
            # There is no else so we can return
            return

        # There is an else, so we handle it properly
        self.write("<keyword> else </keyword>")

        self.eat('{')
        self.write("<symbol> { </symbol>")
        self.compile_statements()
        self.eat('}')
        self.write("<symbol> } </symbol>")

    def compile_expression(self):
        """
        Compile an expression.
        :return:
        """
        self.write("expression", True)
        self.num_spaces += 1

        self.compile_term()
        self.possible_op_term()

        self.num_spaces -= 1
        self.write("expression", True, True)

    def subroutineCall_continue(self):
        """
        After an identifier there can be a '.' or '(', otherwise it not function call
        (subroutineCall).
        :return:
        """
        # should i check every time if it's type symbol?
        symbol = self.tokenizer.symbol()
        if symbol == '(':
            self.eat('(')
            self.write("<symbol> ( </symbol>")
            self.compile_expression_list()
            self.eat(')')
            self.write("<symbol> ) </symbol>")

        elif symbol == '.':
            self.eat('.')
            self.write("<symbol> . </symbol>")

            self.write("<identifier>\t" + self.tokenizer.identifier() + "\t</identifier>")
            self.tokenizer.advance()

            self.eat('(')
            self.write("<symbol> ( </symbol>")
            self.compile_expression_list()
            self.eat(')')
            self.write("<symbol> ) </symbol>")

        else:
            raise Exception("If there is a symbol in the subroutineCall it have to be . or (.")

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
        # If the token is a string_const or int_const
        if type in [Token_Types.string_const, Token_Types.int_const] :
            value = self.tokenizer.intVal() if type == Token_Types.int_const else self.tokenizer.stringVal()
            self.write("<" + EXPREESSIONS[type] + ">\t" +
                       value +
                       "\t</" + EXPREESSIONS[type] + ">")
            self.tokenizer.advance()

        # If the token is a keyword
        elif type == Token_Types.keyword:
            if self.tokenizer.keyWord().value in ["TRUE", "FALSE", "NULL", "THIS"]:
                self.write("<" + EXPREESSIONS[type] + ">\t" +
                           self.tokenizer.keyWord().value.lower() +
                           "\t</" + EXPREESSIONS[type] + ">")
                self.tokenizer.advance()
            else:
                raise Exception()

        # If the token is an identifier
        elif type == Token_Types.identifier:
            # value = self.tokenizer.identifier()
            self.write("<identifier>\t" + self.tokenizer.identifier() + "\t</identifier>")
            self.tokenizer.advance()
            self.possible_identifier_continue()

        # If the token is an symbol
        elif type == Token_Types.symbol:
            if self.tokenizer.symbol() == '(':
                self.eat('(')
                self.write("<symbol> ( </symbol>")
                self.compile_expression()
                self.eat(')')
                self.write("<symbol> ) </symbol>")
            elif self.tokenizer.symbol() in ["-", "~"]:
                self.eat(self.tokenizer.symbol())
                self.write("<symbol>\t" + self.tokenizer.symbol() + "\t</symbol>")
                self.compile_term()
            else:
                raise Exception()

        else:
            raise Exception("Invalid token for creating term.")

        self.num_spaces -= 1
        self.write("term", True, True)

    def possible_identifier_continue(self):
        """
        In a term if identifier continues with
        - '[' - it's a call of an array
        - '.' or '('  - it's part of subroutineCall (function call)
        - nothing - it's a variable
        This functions handle every one of this situations after the original identifier was
        handled.
        """
        # try:
        #     self.eat("[")
        # except:
        # if not self.tokenizer.has_more_tokens(): # already doing it by itself
        #     raise Exception()
        if self.tokenizer.token_type() == Token_Types.symbol:
            if self.tokenizer.symbol() == '[':
                self.eat('[')
                self.write("<symbol> [ </symbol>")
                self.compile_expression()
                self.eat(']')
                self.write("<symbol> ] </symbol>")
                return

            try:
                self.subroutineCall_continue()
            except Exception:
                # raise Exception("If there is a symbol in the token it have to be . or [ or (.")
                return

    def possible_op_term(self):
        """
        If the next token is a suitable operation symbol than compile more terms,
        otherwise return nothing.
        """
        # There is no op term
        if self.tokenizer.token_type() != Token_Types.symbol:
            # raise Exception("After term can be only nothing or (op term)*.")
            return
        op = self.tokenizer.symbol()

        if op not in OPERANDS:
            # raise Exception("Invalid operator use in term.")
            return # should it be like this?

        try:
            self.eat(op)
        except Exception:
            return
        # There is op term
        self.write("<symbol>\t" + op + "\t</symbol>")
        self.compile_term()

        self.possible_op_term()

    def compile_expression_list(self):
        """
        Compile a comma-separated list of expressions, which may be empty.
        """
        self.write("expressionList", True)
        self.num_spaces += 1

        try:
            self.compile_expression()
        except Exception:
            return
        self.possible_more_expression()

        self.num_spaces -= 1
        self.write("expressionList", True, True)

    def possible_more_expression(self):
        """
        If the next token is a ',' than compile more expressions,
        otherwise return nothing.
        """
        try:
            self.eat(',')
        except Exception:
            return
        self.write("<symbol> , </symbol>")
        self.compile_expression()

        self.possible_more_expression()

    def write(self, statement, delim = False, end = False, new_line=True):
        """

        :param statement:
        :return:
        """

        if end:
            statement = "/" + statement
        if delim:
            self.output.write(TAB * self.num_spaces + "<" + statement + ">")
        else:
            self.output.write(TAB * self.num_spaces + statement)
        if new_line:
            self.output.write(END_LINE)

    def write_terminal(self, t_type, arg):
        """

        :param t_type:
        :param arg:
        :return:
        """
        self.write(t_type, delim=True, new_line=False)
        self.write(" " + arg + " ", delim=False, new_line=False)
        self.write(t_type, delim=True, new_line=False, end=True)


    # def write_recursive(self, name, advance_lim=1):
    #     """
    #
    #     :param name:
    #     :param advance_lim:
    #     :return:
    #     """
    #     self.write(name, num_tabs=self.indent)
    #
    #     self.indent += 1
    #     self.call_single()
    #     for _ in range(advance_lim - 1):
    #         if self.tokenizer.has_more_tokens():
    #             self.tokenizer.advance()
    #             self.call_single()
    #         else:
    #             raise ValueError("expected more tokens")
    #
    #     # self.write(name + " " + arg, delim=False,
    #     #            num_tabs=self.indent + 1)
    #     self.write(name, num_tabs=self.indent, end=True)


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



    # def full_recursion(self):
    #     """
    #
    #     :param token:
    #     :return:
    #     """
    #     while self.tokenizer.has_more_tokens():
    #         self.tokenizer.advance()
    #
    #         type = self.tokenizer.token_type()
    #
    #         terminal_arg = False
    #
    #         if type == Token_Types.keyword:
    #             terminal_arg = self.tokenizer.keyWord()
    #
    #         if type == Token_Types.symbol:
    #             terminal_arg = self.tokenizer.symbol()
    #
    #         if type == Token_Types.identifier:
    #             terminal_arg = self.tokenizer.identifier()
    #
    #         if type == Token_Types.int_const:
    #             terminal_arg = self.tokenizer.intVal()
    #
    #         if type == Token_Types.string_const:
    #             terminal_arg = self.tokenizer.stringVal()
    #
    #         if terminal_arg:
    #             self.write_terminal(type, terminal_arg)
    #
    #         else:
    #             self.write_recursive(type)


    # def call_single(self):
    #     """
    #
    #     :return:
    #     """
    #     type = self.tokenizer.token_type()
    #
    #     terminal_arg = False
    #
    #     if type == Token_Types.keyword:
    #         terminal_arg = self.tokenizer.keyWord()
    #
    #     if type == Token_Types.symbol:
    #         terminal_arg = self.tokenizer.symbol()
    #
    #     if type == Token_Types.identifier:
    #         terminal_arg = self.tokenizer.identifier()
    #
    #     if type == Token_Types.int_const:
    #         terminal_arg = self.tokenizer.intVal()
    #
    #     if type == Token_Types.string_const:
    #         terminal_arg = self.tokenizer.stringVal()
    #
    #     if terminal_arg:
    #         self.write_terminal(type, terminal_arg)
    #
    #     else:
    #         self.write_recursive(type)





