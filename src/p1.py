import melee
from player import Player

class MyPlayer(Player):
    def get_character(self) -> melee.Character:
        return melee.Character.FOX

    def get_costume(self) -> int:
        return 0

    def step(self, gamestate: melee.GameState):
        melee.techskill.multishine(
            ai_state=gamestate.players[self.port], controller=self.controller)
