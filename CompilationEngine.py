"""

"""



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
        pass


    def compile_class(self):
        """
        Compiles a complete class
        :return:
        """
        pass


    def compile_class_car_dec(self):
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
        pass


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