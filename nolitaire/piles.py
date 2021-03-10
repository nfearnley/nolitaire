from nolitaire.cards import Card

class Pile:
    def __init__(self, cards=[], pos=None):
        if pos is None:
            pos = 0, 0
        self.cards = []
        for card in cards:
            self.add(card)
        self.pos = pos

    def add(self, *cards):
        for card in cards:
            if not isinstance(card, Card):
                try:
                    self.add(*card)
                except (TypeError, AttributeError):
                    raise ValueError("invalid card: {card!r}")
                return
            if card not in self.cards:
                card.pile = self
                self.cards.append(card)

class Hand(Pile):
    def add(self, *cards):
        offset = len(self.cards)
        for card in cards:
            if isinstance(card, Card):
                card.pos = offset * 8, 0
                card.faceup = offset % 3 == 0
                offset += 1
        super().add(*cards)


class Foundation(Pile):
    pass

class Column(Pile):
    def add(self, *cards):
        offset = len(self.cards)
        for card in cards:
            if isinstance(card, Card):
                card.pos = 0, offset * 8
                offset += 1
        super().add(*cards)

