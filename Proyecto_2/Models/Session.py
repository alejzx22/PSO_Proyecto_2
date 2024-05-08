class Session:
    def __init__(self, n_instructions: int, instructions: list):
        self.n_instructions: int = n_instructions
        self.instructions: list = []

    def add_instruction(self, instruction: str):
        self.instructions.append(instruction)
