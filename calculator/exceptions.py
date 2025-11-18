class DivisionByZeroError(ZeroDivisionError):
    def __init__(self):
        super().__init__("Division by zero is not allowed.")
