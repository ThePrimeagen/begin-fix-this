import melee
from player import Player

class Game:
    def __init__(self,
            console: melee.Console,
            p1: Player,
            p2: Player,
            log: melee.Logger,
            connect_code: str = ""):

        self.console = console
        self.log = log
        self.p1 = p1
        self.p2 = p2
        self.connect_code = connect_code

def run_game_loop(game: Game):
    console = game.console
    p1 = game.p1
    p2 = game.p2

    while True:
        # "step" to the next frame
        gamestate = console.step()
        if gamestate is None:
            continue

        # The console object keeps track of how long your bot is taking to process frames
        #   And can warn you if it's taking too long
        if console.processingtime * 1000 > 12:
            print("WARNING: Last frame took " + str(console.processingtime*1000) + "ms to process.")

        # What menu are we in?
        if gamestate.menu_state in [melee.Menu.IN_GAME, melee.Menu.SUDDEN_DEATH]:
            p1.step(gamestate)
            p2.step(gamestate)

            melee.techskill.multishine(ai_state=gamestate.players[game.p2_port], controller=p2)

            # Log this frame's detailed info if we're in game
            if game.log:
                game.log.logframe(gamestate)
                game.log.writeframe()
        else:
            melee.MenuHelper.menu_helper_simple(gamestate,
                    p1,
                    p1.get_character(),
                    melee.Stage.YOSHIS_STORY,
                    game.connect_code,
                    costume=p1.get_costume(),
                    autostart=False,
                    swag=False)

            melee.MenuHelper.menu_helper_simple(gamestate,
                    p2,
                    p2.get_character(),
                    melee.Stage.YOSHIS_STORY,
                    game.connect_code,
                    costume=p2.get_costume(),
                    autostart=True,
                    swag=False)

            # If we're not in game, don't log the frame
            if game.log:
                game.log.skipframe()

