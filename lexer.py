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

# Example usage (unchanged)
code = '''
ship BlackPearl {
    allHands treasure coin goldPieces;
    officerOnly treasure scroll message;

    allHands adventure sail() {
        sail (coin i = 0; i < 10; i++) {
            print("Sailing...");
        }
    }

    allHands adventure checkTreasure() {
        explore (goldPieces > 100) {
            print("Plenty of gold!");
        } deviate {
            print("We need more gold!");
        }
    }

    allHands adventure searchForGold() {
        while (goldPieces < 100) {
            print("Searching for gold...");
            goldPieces = goldPieces + 10;
        }
    }
}
'''

try:
    lexer = Lexer(code)
    tokens = lexer.get_tokens()
    print(tokens)
except SyntaxError as e:
    print(f"SyntaxError: {e}")
