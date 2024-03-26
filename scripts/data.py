class Highscore:
    def __init__(self) -> None:
        pass

    def get_highscore(self):
        with open("highscore.txt", "r") as highscore:
            highscore = highscore.read()

        return highscore

    def write_highscore(self, score):
        with open("highscore.txt", "w") as highscore:
            highscore.write(score)

        return True

highscore_text = "Highscore"

#highscore 
