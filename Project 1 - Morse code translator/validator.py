class Validator:

    def __init__(self, encode_map, decode_map):
        self.encode_map = encode_map
        self.decode_map = decode_map

    def clean_input(self, text: str) -> str:
        return " ".join(text.strip().split())

    def validate_text_input(self, text: str) -> bool:
        if not text or text.strip() == "":
            raise ValueError("Input text is empty")

        for char in text.upper():
            if char != " " and char not in self.encode_map:
                raise ValueError(f"Unsupported character: {char}")

        return True

    def validate_morse_input(self, morse: str) -> bool:
        if not morse or morse.strip() == "":
            raise ValueError("Morse input is empty")

        valid_symbols = {".", "-", " ", "/"}

        for symbol in morse:
            if symbol not in valid_symbols:
                raise ValueError(f"Invalid Morse symbol: {symbol}")

        return True