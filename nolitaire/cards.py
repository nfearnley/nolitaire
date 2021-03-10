from enum import Enum
from pathlib import Path

import pygame


class Suit(Enum):
    Hearts = H = 0
    Diamonds = D = 1
    Clubs = C = 2
    Spades = S = 3


class Rank(Enum):
    Ace = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Jack = 11
    Queen = 12
    King = 13


class Extras(Enum):
    Joker = 1
    Back = 2


class CardSheet:
    CARDW = 32
    CARDH = 48
    TEXTURE = None
    CARD_TEXTURES = {}

    def __init__(self):
        self.TEXTURE = pygame.image.load(Path("data/trumps_royals_nums.png"))
        self.TEXTURE.set_colorkey("#ff00ff")
        for suit in Suit:
            for rank in Rank:
                src_x = (rank.value - 1) * self.CARDW
                src_y = suit.value * self.CARDH
                src_rect = pygame.rect.Rect(src_x, src_y, self.CARDW, self.CARDH)
                self.CARD_TEXTURES[suit, rank] = self.TEXTURE.subsurface(src_rect)
        for extra in Extras:
            src_x = (extra.value - 1) * self.CARDW
            src_y = 4 * self.CARDH
            src_rect = pygame.rect.Rect(src_x, src_y, self.CARDW, self.CARDH)
            self.CARD_TEXTURES[None, extra] = self.TEXTURE.subsurface(src_rect)
    
    def __getitem__(self, key):
        return self.CARD_TEXTURES[key]


class Card(pygame.sprite.Sprite):
    CARDSHEET = None
    def __init__(self, suit, rank, pos=(0, 0), pile=None, faceup=False):
        super().__init__()
        self.suit = suit
        self.rank = rank
        self.pos = pos
        self.pile = pile
        self.faceup = faceup

    @property
    def image(self):
        if self.faceup:
            image = self.CARDSHEET[self.suit, self.rank]
        else:
            image = self.CARDSHEET[None, Extras.Back]
        return image

    @property
    def rect(self):
        pilepos = getattr(self.pile, "pos", (0,0))
        return self.image.get_rect().move(self.pos).move(pilepos)

    @classmethod
    def init(cls):
        """Called once to initialize the Card class"""
        cls.CARDSHEET = CardSheet()

    def __str__(self):
        return f"Card(suit={self.suit.name!r}, rank={self.rank.name!r})"
