import pygame
import pygame.sprite
import nygame

from nolitaire.cards import Card, Suit, Rank
from nolitaire.piles import Column, Foundation, Hand
from nolitaire.utils import take_choices

class NolitaireGroup(pygame.sprite.LayeredUpdates):
    def get_sprite_at(self, xy):
        try:
            return self.get_sprites_at(xy)[-1]
        except IndexError:
            return None



class Game(nygame.Game):
    def __init__(self):
        super().__init__(bgcolor="#006000", size=(288, 240), scale=1, showfps=True, fps=120)
        Card.init()
        self.cards = NolitaireGroup(Card(suit, rank) for suit in Suit for rank in Rank)
        deck = list(self.cards)
        self.columns = [Column(pos=(8+i*40, 64)) for i in range(7)]
        for i, col in enumerate(self.columns):
            card_count = len(self.columns) - i
            taken, deck = take_choices(deck, k=card_count)
            taken[-1].faceup = True
            col.add(taken)
        self.foundations = [Foundation(pos=(40+i*10,0)) for i in range(4)]
        self.hand = Hand(pos=(8,176))
        self.hand.add(deck)
        self.groups = self.foundations + self.columns + [self.hand]
        self.dragging = None
        self.drag_from = None

    def loop(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    shifted = pygame.key.get_mods() & pygame.KMOD_SHIFT
                    if shifted:
                        self.grab("pile")
                    else:
                        self.grab("card")
                elif event.button == 3:
                    self.flip()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.drop()
            elif event.type == pygame.MOUSEMOTION:
                self.drag()
            elif event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_5:
                    self.scale = event.key - pygame.K_1 + 1
                    self.reset_display()
        self.cards.draw(self.surface)

    def grab(self, target_type):
        xy = self.mouse_pos
        card = self.cards.get_sprite_at(xy)
        if not card:
            return
        x, y = xy
        if target_type == "card":
            card.groups()[0].move_to_front(card)
            target = card
        elif target_type == "pile":
            target = card.pile
        else:
            raise ValueError(f"Invalid target_type: {target_type!r}")
        self.drag_from = x - target.pos[0], y - target.pos[1]
        self.dragging = target

    def drag(self):
        if not self.dragging:
            return
        x, y = self.mouse_pos
        offx, offy = self.drag_from
        newpos = x - offx, y - offy
        self.dragging.pos = newpos

    def drop(self):
        self.drag_from = None
        self.dragging = None
    
    def flip(self):
        xy = self.mouse_pos
        card = self.cards.get_sprite_at(xy)
        if not card:
            return
        card.faceup = not card.faceup


#@nygame.perf(sort="tottime")
def main():
    Game().run()

