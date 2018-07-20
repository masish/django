import enum


class Postion(enum.IntEnum):
    GK = 1
    DF = 2
    MF = 3
    FW = 4

    @classmethod
    def get_choices(cls):
        return tuple((x.value, x.name) for x in cls)


class Vote_result(enum.IntEnum):
    NOTYET = 0
    MISS = 1
    HIT = 2

    @classmethod
    def get_vote_result(cls):
        return tuple((x.value, x.name) for x in cls)