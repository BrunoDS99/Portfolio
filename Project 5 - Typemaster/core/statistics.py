


class Statistics:
    
    def __init__(self):
        self.correct_characters = 0
        self.incorrect_characters = 0
        
    def register_results(self, correct):
        
        if correct:
            self.correct_characters += 1
        else:
            self.incorrect_characters += 1
    
    @property
    def errors(self):
        return self.incorrect_characters
    
    @property
    def total_characters(self):
        return self.correct_characters + self.incorrect_characters
    
    def accuracy(self):
        if self.total_characters == 0:
            return 100
        
        return round(self.correct_characters / self.total_characters * 100, 1)
    
    def wpm (self, elapsed_seconds):
        if elapsed_seconds == 0:
            return 0
        minutes = elapsed_seconds / 60
        return round((self.correct_characters / 5) / minutes)
    
    @property
    def words(self):
        return self.correct_characters // 5
    @property
    def characters(self):
        return self.correct_characters