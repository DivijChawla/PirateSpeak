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

