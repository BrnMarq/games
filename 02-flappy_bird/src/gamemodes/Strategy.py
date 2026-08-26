from gale.input_handler import InputData


class GameModeStrategy:
    def __init__(self, world, bird, score, state_machine):
        self.score = score
        pass

    def update(self, dt) -> None:
        pass

    def on_input(self, input_id: str, input_data: InputData) -> None:
        pass
