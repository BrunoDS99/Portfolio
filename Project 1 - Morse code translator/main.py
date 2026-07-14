import os, csv
from config import Config
from mappings import MorseMapping
from encoder import MorseEncoder
from decoder import MorseDecoder
from file_handler import FileHandler

def main():
    # Load mappings
    mapping = MorseMapping(Config.MORSE_CSV_PATH)

    encode_map = mapping.get_encode_map()
    decode_map = mapping.get_decode_map()

    # Create encoder/decoder
    encoder = MorseEncoder(encode_map, Config.UNKNOWN_SYMBOL)
    decoder = MorseDecoder(decode_map, Config.UNKNOWN_SYMBOL)

    # File handler
    files = FileHandler()
    
    print("MORSE TRANSLATOR")
    print("1. Text → Morse (input)")
    print("2. Morse → Text (input)")
    print("3. Text file → Morse")
    print("4. Morse file → Text")

    choice = input("Choose option: ")

    if choice == "1":
        text = input("Enter text: ")
        result = encoder.encode_text(text)
        print("\nMorse Output:")
        print(result)

    elif choice == "2":
        morse = input("Enter Morse: ")
        result = decoder.decode_text(morse)
        print("\nText Output:")
        print(result)
        
    if choice == "3":
        path = input("Enter text file path: ")

        text = files.read_text_file(path)
        result = encoder.encode_text(text)

        print("\nMorse Output:\n")
        print(result)

    elif choice == "4":
        path = input("Enter Morse file path: ")

        morse = files.read_text_file(path)
        result = decoder.decode_text(morse)

        print("\nText Output:\n")
        print(result)

    else:
        print("Invalid option")


if __name__ == "__main__":
    main()