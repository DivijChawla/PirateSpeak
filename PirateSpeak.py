import re

class Lexer:
    TOKEN_TYPES = {
        'KEYWORD': r'\b(ship|treasure|adventure|explore|deviate|sail|while|allHands|officerOnly|return|aye|nay)\b',
        'TYPE': r'\b(coin|scroll|loot|beacon|mark)\b',
        'IDENTIFIER': r'[a-zA-Z_][a-zA-Z0-9_]*',
        'NUMBER': r'\d+',
        'STRING': r'"[^"]*"',
        'CHAR': r"'.'",
        'FLOAT': r'\d+\.\d+',
        'SYMBOL': r'[{}();,]',
        'OPERATOR': r'[=<>!+\-*/&|]'
    }

    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.tokenize()

    def tokenize(self):
        code = self.code.strip()  # Remove leading and trailing whitespace
        while code:
            match = None
            for token_type, pattern in self.TOKEN_TYPES.items():  # Access TOKEN_TYPES using self
                regex = re.compile(pattern)
                match = regex.match(code)
                if match:
                    self.tokens.append((token_type, match.group(0)))
                    code = code[match.end():].lstrip()  # Remove matched part and any leading whitespace
                    break
            if not match:
                print(f"Unrecognized code: {code}")
                raise SyntaxError(f"Unexpected character: {code[0]}")
        self.tokens.append(('EOF', 'EOF'))

    def get_tokens(self):
        return self.tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[self.position]

    def eat(self, token_type):
        if self.current_token[0] == token_type:
            self.position += 1
            self.current_token = self.tokens[self.position]
        else:
            raise SyntaxError(f"Expected {token_type}, got {self.current_token[0]}")

    def parse(self):
        return self.parse_program()

    def parse_program(self):
        classes = []
        while self.current_token[0] != 'EOF':
            classes.append(self.parse_class_declaration())
        return classes

    def parse_class_declaration(self):
        self.eat('KEYWORD')  # ship
        class_name = self.current_token[1]
        self.eat('IDENTIFIER')
        self.eat('SYMBOL')  # {
        members = self.parse_member_declarations()
        self.eat('SYMBOL')  # }
        return {'type': 'class', 'name': class_name, 'members': members}

    def parse_member_declarations(self):
        members = []
        while self.current_token[0] != 'SYMBOL' or self.current_token[1] != '}':
            if self.current_token[0] == 'KEYWORD':
                if self.current_token[1] == 'allHands' or self.current_token[1] == 'officerOnly':
                    members.append(self.parse_member_declaration())
            else:
                break
        return members

    def parse_member_declaration(self):
        access_modifier = self.current_token[1]
        self.eat('KEYWORD')
        if self.current_token[1] == 'treasure':
            return self.parse_variable_declaration(access_modifier)
        elif self.current_token[1] == 'adventure':
            return self.parse_method_declaration(access_modifier)

    def parse_variable_declaration(self, access_modifier):
        self.eat('KEYWORD')  # treasure
        var_type = self.current_token[1]
        self.eat('TYPE')
        var_name = self.current_token[1]
        self.eat('IDENTIFIER')
        self.eat('SYMBOL')  # ;
        return {'type': 'variable', 'access': access_modifier, 'var_type': var_type, 'name': var_name}

    def parse_method_declaration(self, access_modifier):
        self.eat('KEYWORD')  # adventure
        method_name = self.current_token[1]
        self.eat('IDENTIFIER')
        self.eat('SYMBOL')  # (
        parameters = self.parse_parameter_list()
        self.eat('SYMBOL')  # )
        self.eat('SYMBOL')  # {
        body = self.parse_block_statement()
        self.eat('SYMBOL')  # }
        return {'type': 'method', 'access': access_modifier, 'name': method_name, 'params': parameters, 'body': body}

    def parse_parameter_list(self):
        parameters = []
        if self.current_token[0] == 'TYPE':
            parameters.append(self.parse_parameter())
            while self.current_token[0] == 'SYMBOL' and self.current_token[1] == ',':
                self.eat('SYMBOL')
                parameters.append(self.parse_parameter())
        return parameters

    def parse_parameter(self):
        param_type = self.current_token[1]
        self.eat('TYPE')
        param_name = self.current_token[1]
        self.eat('IDENTIFIER')
        return {'type': param_type, 'name': param_name}

    def parse_block_statement(self):
        statements = []
        while self.current_token[0] != 'SYMBOL' or self.current_token[1] != '}':
            statements.append(self.parse_statement())
        return statements

    def parse_statement(self):
        if self.current_token[1] == 'treasure':
            return self.parse_variable_declaration(None)
        elif self.current_token[1] == 'explore':
            return self.parse_if_statement()
        elif self.current_token[1] == 'sail':
            return self.parse_for_statement()
        elif self.current_token[1] == 'while':
            return self.parse_while_statement()
        elif self.current_token[1] == 'return':
            return self.parse_return_statement()
        elif self.current_token[0] == 'SYMBOL' and self.current_token[1] == '{':
            return self.parse_block_statement()
        else:
            return self.parse_expression_statement()

    def parse_if_statement(self):
        self.eat('KEYWORD')  # explore
        self.eat('SYMBOL')  # (
        condition = self.parse_expression()
        self.eat('SYMBOL')  # )
        if_body = self.parse_statement()
        else_body = None
        if self.current_token[0] == 'KEYWORD' and self.current_token[1] == 'deviate':
            self.eat('KEYWORD')  # deviate
            else_body = self.parse_statement()
        return {'type': 'if', 'condition': condition, 'if_body': if_body, 'else_body': else_body}

    def parse_for_statement(self):
        self.eat('KEYWORD')  # sail
        self.eat('SYMBOL')  # (
        init = None
        if self.current_token[0] != 'SYMBOL' or self.current_token[1] != ';':
            init = self.parse_expression()
        self.eat('SYMBOL')  # ;
        condition = None
        if self.current_token[0] != 'SYMBOL' or self.current_token[1] != ';':
            condition = self.parse_expression()
        self.eat('SYMBOL')  # ;
        update = None
        if self.current_token[0] != 'SYMBOL' or self.current_token[1] != ')':
            update = self.parse_expression()
        self.eat('SYMBOL')  # )
        body = self.parse_statement()
        return {'type': 'for', 'init': init, 'condition': condition, 'update': update, 'body': body}

    def parse_while_statement(self):
        self.eat('KEYWORD')  # while
        self.eat('SYMBOL')  # (
        condition = self.parse_expression()
        self.eat('SYMBOL')  # )
        body = self.parse_statement()
        return {'type': 'while', 'condition': condition, 'body': body}

    def parse_return_statement(self):
        self.eat('KEYWORD')  # return
        expr = None
        if self.current_token[0] != 'SYMBOL' or self.current_token[1] != ';':
            expr = self.parse_expression()
        self.eat('SYMBOL')  # ;
        return {'type': 'return', 'expression': expr}

    def parse_block_statement(self):
        self.eat('SYMBOL')  # {
        statements = []
        while self.current_token[0] != 'SYMBOL' or self.current_token[1] != '}':
            statements.append(self.parse_statement())
        self.eat('SYMBOL')  # }
        return {'type': 'block', 'statements': statements}

    def parse_expression_statement(self):
        expr = self.parse_expression()
        self.eat('SYMBOL')  # ;
        return {'type': 'expression', 'expression': expr}

    def parse_expression(self):
        return self.parse_assignment()

    def parse_assignment(self):
        left = self.parse_logical_or()
        if self.current_token[0] == 'OPERATOR' and self.current_token[1] == '=':
            self.eat('OPERATOR')
            right = self.parse_expression()
            return {'type': 'assignment', 'left': left, 'right': right}
        return left

    def parse_logical_or(self):
        left = self.parse_logical_and()
        while self.current_token[0] == 'OPERATOR' and self.current_token[1] == '||':
            self.eat('OPERATOR')
            right = self.parse_logical_and()
            left = {'type': 'logical_or', 'left': left, 'right': right}
        return left

    def parse_logical_and(self):
        left = self.parse_equality()
        while self.current_token[0] == 'OPERATOR' and self.current_token[1] == '&&':
            self.eat('OPERATOR')
            right = self.parse_equality()
            left = {'type': 'logical_and', 'left': left, 'right': right}
        return left

    def parse_equality(self):
        left = self.parse_comparison()
        while self.current_token[0] == 'OPERATOR' and self.current_token[1] in ('==', '!='):
            op = self.current_token[1]
            self.eat('OPERATOR')
            right = self.parse_comparison()
            left = {'type': 'equality', 'operator': op, 'left': left, 'right': right}
        return left

    def parse_comparison(self):
        left = self.parse_term()
        while self.current_token[0] == 'OPERATOR' and self.current_token[1] in ('<', '>', '<=', '>='):
            op = self.current_token[1]
            self.eat('OPERATOR')
            right = self.parse_term()
            left = {'type': 'comparison', 'operator': op, 'left': left, 'right': right}
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.current_token[0] == 'OPERATOR' and self.current_token[1] in ('+', '-'):
            op = self.current_token[1]
            self.eat('OPERATOR')
            right = self.parse_factor()
            left = {'type': 'term', 'operator': op, 'left': left, 'right': right}
        return left

    def parse_factor(self):
        left = self.parse_unary()
        while self.current_token[0] == 'OPERATOR' and self.current_token[1] in ('*', '/'):
            op = self.current_token[1]
            self.eat('OPERATOR')
            right = self.parse_unary()
            left = {'type': 'factor', 'operator': op, 'left': left, 'right': right}
        return left

    def parse_unary(self):
        if self.current_token[0] == 'OPERATOR' and self.current_token[1] in ('!', '-'):
            op = self.current_token[1]
            self.eat('OPERATOR')
            expr = self.parse_unary()
            return {'type': 'unary', 'operator': op, 'expression': expr}
        return self.parse_primary()

    def parse_primary(self):
        if self.current_token[0] == 'NUMBER':
            value = self.current_token[1]
            self.eat('NUMBER')
            return {'type': 'literal', 'value': int(value)}
        elif self.current_token[0] == 'FLOAT':
            value = self.current_token[1]
            self.eat('FLOAT')
            return {'type': 'literal', 'value': float(value)}
        elif self.current_token[0] == 'STRING':
            value = self.current_token[1]
            self.eat('STRING')
            return {'type': 'literal', 'value': value}
        elif self.current_token[0] == 'CHAR':
            value = self.current_token[1]
            self.eat('CHAR')
            return {'type': 'literal', 'value': value}
        elif self.current_token[0] == 'KEYWORD' and self.current_token[1] in ('aye', 'nay'):
            value = self.current_token[1]
            self.eat('KEYWORD')
            return {'type': 'literal', 'value': value == 'aye'}
        elif self.current_token[0] == 'IDENTIFIER':
            value = self.current_token[1]
            self.eat('IDENTIFIER')
            return {'type': 'identifier', 'value': value}
        elif self.current_token[0] == 'SYMBOL' and self.current_token[1] == '(':
            self.eat('SYMBOL')
            expr = self.parse_expression()
            self.eat('SYMBOL')
            return expr
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token}")

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


if __name__ == "__main__":
    # Example usage:
    source_code = """
    ship Pirate {
        allHands coin treasure gold;
        
        adventure buryTreasure(treasure chest) {
            if (chest == gold) {
                return aye;
            } else {
                return nay;
            }
        }
    }
    """

    lexer = Lexer(source_code)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    ast = parser.parse()

    interpreter = Interpreter(ast)
    interpreter.interpret()