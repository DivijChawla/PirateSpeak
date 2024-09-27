class Interpreter:
    def __init__(self, parser):
        self.parser = parser
        self.symbol_table = {}

    def interpret(self):
        program = self.parser.parse()
        for class_node in program:
            self.interpret_class(class_node)

    def interpret_class(self, class_node):
        class_name = class_node['name']
        self.symbol_table[class_name] = {}

        for member in class_node['members']:
            if member['type'] == 'variable':
                self.interpret_variable_declaration(class_name, member)
            elif member['type'] == 'method':
                self.interpret_method_declaration(class_name, member)

    def interpret_variable_declaration(self, class_name, variable_node):
        var_type = variable_node['var_type']
        var_name = variable_node['name']
        self.symbol_table[class_name][var_name] = None

    def interpret_method_declaration(self, class_name, method_node):
        method_name = method_node['name']
        self.symbol_table[class_name][method_name] = method_node  # Store method definition for later execution

    def execute_method(self, class_name, method_name, args):
        method_node = self.symbol_table[class_name][method_name]
        parameters = method_node['params']
        method_body = method_node['body']

        # Bind arguments to parameter names in the symbol table
        for i in range(len(parameters)):
            param_name = parameters[i]['name']
            param_value = args[i]  # Assuming arguments are passed correctly
            self.symbol_table[class_name][param_name] = param_value

        # Execute method body statements
        for statement in method_body:
            self.execute_statement(statement)

    def execute_statement(self, statement):
        if statement['type'] == 'expression':
            self.execute_expression(statement['expression'])
        elif statement['type'] == 'return':
            return self.execute_expression(statement['expression'])
        elif statement['type'] == 'if':
            if self.execute_expression(statement['condition']):
                self.execute_statement(statement['if_body'])
            elif statement['else_body'] is not None:
                self.execute_statement(statement['else_body'])
        elif statement['type'] == 'for':
            if statement['init']:
                self.execute_expression(statement['init'])
            while self.execute_expression(statement['condition']):
                self.execute_statement(statement['body'])
                if statement['update']:
                    self.execute_expression(statement['update'])
        elif statement['type'] == 'while':
            while self.execute_expression(statement['condition']):
                self.execute_statement(statement['body'])
        elif statement['type'] == 'block':
            for stmt in statement['statements']:
                self.execute_statement(stmt)
        elif statement['type'] == 'variable':
            self.execute_variable_declaration(statement)
        elif statement['type'] == 'assignment':
            self.execute_assignment(statement)
        else:
            raise RuntimeError(f"Unknown statement type: {statement['type']}")

    def execute_expression(self, expression):
        if expression['type'] == 'literal':
            return expression['value']
        elif expression['type'] == 'identifier':
            # Lookup identifier value in the symbol table
            # For simplicity, assuming direct values in symbol table for literals
            return self.symbol_table[expression['value']]
        elif expression['type'] == 'binary':
            left = self.execute_expression(expression['left'])
            right = self.execute_expression(expression['right'])
            if expression['operator'] == '+':
                return left + right
            elif expression['operator'] == '-':
                return left - right
            elif expression['operator'] == '*':
                return left * right
            elif expression['operator'] == '/':
                return left / right
            elif expression['operator'] == '&&':
                return left and right
            elif expression['operator'] == '||':
                return left or right
            elif expression['operator'] == '==':
                return left == right
            elif expression['operator'] == '!=':
                return left != right
            elif expression['operator'] == '<':
                return left < right
            elif expression['operator'] == '>':
                return left > right
            elif expression['operator'] == '<=':
                return left <= right
            elif expression['operator'] == '>=':
                return left >= right
            else:
                raise RuntimeError(f"Unknown operator: {expression['operator']}")
        elif expression['type'] == 'unary':
            if expression['operator'] == '-':
                return -self.execute_expression(expression['expression'])
            elif expression['operator'] == '!':
                return not self.execute_expression(expression['expression'])
            else:
                raise RuntimeError(f"Unknown unary operator: {expression['operator']}")
        else:
            raise RuntimeError(f"Unknown expression type: {expression['type']}")

    def execute_variable_declaration(self, variable_node):
        # Since PirateSpeak doesn't handle runtime variable declarations explicitly,
        # this method might not be used directly in the interpreter.
        pass

    def execute_assignment(self, assignment_node):
        left = assignment_node['left']
        right = self.execute_expression(assignment_node['right'])
        self.symbol_table[left['value']] = right
