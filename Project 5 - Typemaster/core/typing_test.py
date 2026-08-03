

class TypingTest:
    
    def __init__(self, text):
        self.original_text = text
        self.typed_text = ""
        
    def process_key(self, key, character):
        """
        Processes a keyboard event.

        Returns:
            True  -> Correct character
            False -> Incorrect character
            None  -> Key ignored
        """

        # Ignore keys that don't produce characters
        if not character:
            return None
        
        # Handle backspace
        if key == "BackSpace":
            if self.typed_text:
                self.typed_text = self.typed_text[:-1]
            return None
        
        #Prevent typing past the end
        if len(self.typed_text) >= len(self.original_text):
            return None
        
        expected = self.original_text[len(self.typed_text)]
        self.typed_text += character
        return character == expected
    
    @property
    def current_position(self):
        return len(self.typed_text)
    
    @property
    def finished(self):
        return self.current_position >= len(self.original_text)