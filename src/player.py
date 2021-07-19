import melee

class Player:

    def __init__(
            self,
            controller: melee.Controller,
            log: melee.Logger,
            port: int):
        self.controller = controller
        self.log = log
        self.port = port

    @abstractmethod
    def get_character(self) -> str:
        pass

    @abstractmethod
    def get_costume(self) -> int:
        pass

    @abstractmethod
    def step(self, state: melee.GameState):
        pass

