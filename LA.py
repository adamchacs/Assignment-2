import re

# Token definitions
KEYWORDS = {"function", "integer", "boolean", "real", "if", "else", "fi", "while", "return", "get", "put"}
OPERATORS = {"==", "!=", ">", "<", "<=", "=>", "+", "-", "*", "/", "="}
SEPARATORS = {"(", ")", "{", "}", ";", ","}

# Regular expressions for FSM
identifier_re = r'^[a-zA-Z][a-zA-Z0-9]*$'
integer_re = r'^[0-9]+$'
real_re = r'^[0-9]+\.[0-9]+$'

# Token types
TOKEN_IDENTIFIER = "identifier"
TOKEN_INTEGER = "integer"
TOKEN_REAL = "real"
TOKEN_KEYWORD = "keyword"
TOKEN_OPERATOR = "operator"
TOKEN_SEPARATOR = "separator"
TOKEN_COMMENT = "comment"
TOKEN_UNKNOWN = "unknown"

class Lexer():
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []

    def is_keyword(self, word):
        return word in KEYWORDS

    def is_operator(self, char):
        return char in OPERATORS

    def is_separator(self, char):
        return char in SEPARATORS

    def tokenize(self):
        # Clear previous tokens
        self.tokens = []

        # Removing comments
        self.source_code = re.sub(r'\[\*.*?\*\]', '', self.source_code)

        # Split source code into tokens
        pattern = re.compile(r'\s+|([(){};,])|([<>!=]=|[-+*/=<>])')
        tokens = pattern.split(self.source_code)
        tokens = [t for t in tokens if t and not t.isspace()]  # Remove empty tokens and spaces

        i = 0
        while i < len(tokens):
            token = tokens[i]

            # Identifiers and Keywords
            if re.match(identifier_re, token):
                if self.is_keyword(token):
                    self.tokens.append((TOKEN_KEYWORD, token))
                else:
                    self.tokens.append((TOKEN_IDENTIFIER, token))

            # Real numbers (must be checked before integers)
            elif re.match(real_re, token):
                self.tokens.append((TOKEN_REAL, token))

            # Integers
            elif re.match(integer_re, token):
                self.tokens.append((TOKEN_INTEGER, token))

            # Operators
            elif self.is_operator(token):
                self.tokens.append((TOKEN_OPERATOR, token))

            # Separators
            elif self.is_separator(token):
                self.tokens.append((TOKEN_SEPARATOR, token))

            else:
                self.tokens.append((TOKEN_UNKNOWN, token))

            i += 1

    def write_tokens_to_file(self, output_file, test_case_number, rules):
        with open(output_file, 'a') as f:  # Open file in append mode
            # Header for the test case
            f.write(f"\n{'-'*40}\n")
            f.write(f"{'Test Case ' + str(test_case_number):^40}\n")
            f.write(f"{'-'*40}\n")
            
            # Write the source code for the test case
            f.write(f"{self.source_code}\n")
            
            # Write the token table
            f.write(f"\n{'-'*40}\n")
            f.write(f"{'Token':<15}{'Lexeme':<15}\n")
            f.write(f"{'-'*30}\n")  # Separator line for the token table

            # Write the tokens and lexemes
            for token, lexeme in self.tokens:
                f.write(f"{token:<15}{lexeme:<15}\n")
                f.write("Parsing Rules:\n")
                f.write(f"{'-'*40}\n")
                for rule in rules:
                    f.write(f"{rule}\n")

            f.write(f"{'-'*40}\n\n")  # End of test case section
