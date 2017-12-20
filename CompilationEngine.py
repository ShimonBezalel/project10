"""

"""

from JackTokenizer import JackTokenizer, Token_Types, keywords



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
        self.indent = 0

        self.full_recursion()
        # with open(output_file) as self.output:
        #     pass


    def compile_class(self):
        """
        Compiles a complete class
        :return:
        """
        self.write('classDec', num_tabs=self.indent)

        self.tokenizer.advance()
        self.write_terminal(Token_Types.identifier, self.tokenizer.identifier())


        self.write('{')





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

        pass


    def compile_do(self):
        """
        Compile do statment
        :return:
        """
        pass


    def compile_let(self):
        """
        Compile let statement
        :return:
        """
        pass


    def compile_while(self):
        """

        :return:
        """
        pass


    def compile_return(self):
        """

        :return:
        """
        pass


    def compile_if(self):
        """

        :return:
        """
        pass


    def compile_expression(self):
        """
        Compile an expression
        :return:
        """
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
        pass


    def compile_expression_list(self):
        """
        Compile a comma-separated list of expressions, which may be empty
        :return:
        """
        pass


    def write(self, str, delim = True, num_tabs = 0, end = False):
        """

        :param str:
        :return:
        """
        if end:
            str = "/" + str
        if delim:
            self.output.write("\t" * num_tabs + "<" + str + ">\n")
        else:
            self.output.write("\t" * num_tabs + str + "\n")


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





