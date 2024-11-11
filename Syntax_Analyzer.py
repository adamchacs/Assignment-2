class Parser():
    def __init__(self, tokens, switch=True):
        self.tokens = tokens
        self.position = 0
        self.switch = switch
        self.parsing_rules = []  # Store parsing rules for each token

    def next_token(self):
        if self.position < len(self.tokens):
            token = self.tokens[self.position]
            self.position += 1
            return token
        return None

    def peek(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def parse(self):
        self.E()
        return self.parsing_rules  # Return all parsing rules for the tokens

    def E(self):
        if self.switch:
            rule = "<Expression> -> <Term> <Expression Prime>"
            self.parsing_rules.append(rule)
        self.T()
        self.E_prime()

    def E_prime(self):
        if self.switch:
            rule = "<Expression Prime> -> + <Term> <Expression Prime> | - <Term> <Expression Prime> | epsilon"
            self.parsing_rules.append(rule)
        token = self.peek()
        if token and token[1] in ('+', '-'):
            operator_token = self.next_token()
            self.parsing_rules.append(f"Token: Operator Lexeme: {operator_token[1]}")
            self.T()
            self.E_prime()
        else:
            self.parsing_rules.append("<Expression Prime> -> epsilon")

    def T(self):
        if self.switch:
            rule = "<Term> -> <Factor> <Term Prime>"
            self.parsing_rules.append(rule)
        self.F()
        self.T_prime()

    def T_prime(self):
        if self.switch:
            rule = "<Term Prime> -> * <Factor> <Term Prime> | / <Factor> <Term Prime> | epsilon"
            self.parsing_rules.append(rule)
        token = self.peek()
        if token and token[1] in ('*', '/'):
            operator_token = self.next_token()
            self.parsing_rules.append(f"Token: Operator Lexeme: {operator_token[1]}")
            self.F()
            self.T_prime()
        else:
            self.parsing_rules.append("<Term Prime> -> epsilon")

    def F(self):
        if self.switch:
            rule = "<Factor> -> <Identifier>"
            self.parsing_rules.append(rule)
        token = self.next_token()
        if token and token[0] == 'identifier':
            self.parsing_rules.append(f"Token: Identifier Lexeme: {token[1]}")
        else:
            self.error("Identifier expected")

    def error(self, message):
        token = self.peek()
        if token:
            error_message = f"Syntax error: {message} at token {token[1]}"
        else:
            error_message = f"Syntax error: {message} at end of input"
        self.parsing_rules.append(error_message)
        print(error_message)
        exit(1)
