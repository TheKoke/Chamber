from backend.shield import Shield
from backend.chamber import Chamber


class ExperimenthalHall:
    def __init__(self, chamber: Chamber, shield: Shield) -> None:
        self.__chamber = chamber
        self.__shield = shield


if __name__ == '__main__':
    pass
