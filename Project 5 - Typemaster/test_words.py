from core.typing_test import TypingTest


test = TypingTest("python")


print(test.check_character("p"))
print(test.check_character("y"))
print(test.check_character("x"))

print("Position:", test.current_position)
print("Errors:", test.errors)