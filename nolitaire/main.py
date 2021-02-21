import random
from os import X_OK
from pathlib import Path

import pygame
import pygame.sprite
import nygame
from nygame import DigiText as T



class Card(pygame.sprite.Sprite):
    SUITS = "HDCS"
    RANKS = list(range(1, 14))
    CARDW = 32
    CARDH = 48
    def __init__(self, suit, rank, card_board):
        super().__init__()
        self.suit = suit
        self.rank = rank
        src_x = (rank - 1) * self.CARDW
        src_y = self.SUITS.index(suit) * self.CARDH
        src_rect = pygame.rect.Rect(src_x, src_y, self.CARDW, self.CARDH)
        self.image = card_board.subsurface(src_rect)
        self.rect = self.image.get_rect()

class Game(nygame.Game):
    def __init__(self):
        super().__init__(bgcolor="#006000", size=(800, 600), showfps=True, fps=120)
        nygame.digifont.init()
        self.card_board = pygame.image.load(Path("data/trumps_royals_nums.png"))
        self.card_board.set_colorkey("#ff00ff")
        self.cards = pygame.sprite.LayeredUpdates()
        for suit in Card.SUITS:
            for rank in Card.RANKS:
                self.cards.add(Card(suit, rank, self.card_board))
        self.dragging = None
        self.drag_from = None

    def loop(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.grab_card()
            elif event.type == pygame.MOUSEBUTTONUP:
                self.drop_card()
        self.drag_card()

        T.color = "black"
        shadow = "..." + T("Hello, ", size=100) + T("World", size=100) + "!"
        T.color = "white"
        text = "..." + T("Hello, ", color="white", size=100) + T("World", color="pink", size=100) + "!"
        #rando = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
        #fonts = ["Arial", "Times New Roman", "Courier", "Consolas", "Comic Sans", "Papyrus"]
        #words = ["".join(random.choices(rando, k=random.randint(4,12))) for _ in range(8)]
        #garbo = [T(w, font=random.choice(fonts), size=random.randint(12, 56), color=random.randint(0, 0xFFFFFF) * 0x100 + 0xFF, bold=bool(random.randint(0, 1)), italic=bool(random.randint(0, 1))) for w in words]
        #garboge = T(garbo)
        #garboge.render_to(self.surface, (10, 200))
        #garboge.render_to(self.surface, (10, 220))
        #garboge.render_to(self.surface, (10, 240))
        shadow.render_to(self.surface, (14, 108))
        text.render_to(self.surface, (10, 100))
        self.cards.draw(self.surface)
    
    def grab_card(self):
        xy = pygame.mouse.get_pos()
        card = self.get_card_at(xy)
        if not card:
            return
        self.cards.move_to_front(card)
        x, y = xy
        self.drag_from = x - card.rect.x, y - card.rect.y
        self.dragging = card

    def drag_card(self):
        if not self.dragging:
            return
        x, y = pygame.mouse.get_pos()
        offx, offy = self.drag_from
        self.dragging.rect.topleft = x - offx, y - offy

    def drop_card(self):
        self.drag_from = None
        self.dragging = None
    
    def get_card_at(self, xy):
        try:
            card = self.cards.get_sprites_at(xy)[-1]
            return card
        except IndexError:
            return None


def perf(fn=None, *, sort=None):
    def wrapper(fn):
        def wrapped(*args, **kwargs):
            import cProfile
            pr = cProfile.Profile(builtins=False)
            pr.enable()
            fn(*args, **kwargs)
            pr.disable
            import pstats
            stats = pstats.Stats(pr)
            if sort:
                stats.sort_stats(sort)
            stats.print_stats()
        return wrapped
    if fn is not None:
        if not callable(fn):
            raise ValueError("BeepBoop")
        return wrapper(fn)
    return wrapper

@perf(sort="tottime")
def main():
    Game().run()
