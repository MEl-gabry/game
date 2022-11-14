from .state import State
from random import randint
import pygame
from .consts import GAME_W, GAME_H
import os

class ComplexEvent(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.text = ""
        self.event_switch = 0
        self.image = 0

    def update(self, actions):
        if actions["start"] and not self.done:
            self.done = True
        elif actions["start"]:
            self.prev_state.events_created = 0
            self.exit_state()
        self.game.reset_keys()

    def render(self, display):
        self.prev_state.render(display)
        if self.image:
            display.blit(self.image, (3 * self.game.GAME_W, self.game.GAME_H/2))
        self.type_writer(display, self.text)

    def switch_event(self):
        self.exit_state()
        self.prev_state.trigger_event(self.event_switch)


class Switcher(ComplexEvent):
    def update(self, actions):
        if actions["start"] and not self.done:
            self.done = True
        elif actions["start"]:
            self.switch_event()
        self.game.reset_keys()


class AutoSwitch(ComplexEvent):
    def update(self, actions):
        self.switch_event()
    

class Pace(ComplexEvent):
    def __init__(self, game):
        ComplexEvent.__init__(self, game)
        self.d = 0
        self.event_switch = 1
        
    def update(self, actions):
        if self.game.fuel < self.d * self.game.fuel_per_distance:
            self.switch_event()
        if actions["start"] and not self.done:
            self.done = True
        elif actions["start"]:
            self.prev_state.events_created = 0
            self.exit_state()
            self.game.move(self.d)
        self.game.reset_keys()


class FastPace(Pace):
    def __init__(self, game):
        Pace.__init__(self, game)
        self.text = "You are now traveling at a fast pace."
        self.d = 100


class MediumPace(Pace):
    def __init__(self, game, ):
        Pace.__init__(self, game)
        self.text = "You are now traveling at a medium pace."
        self.d = 50


class SlowPace(Pace):
    def __init__(self, game):
        Pace.__init__(self, game)
        self.text = "You are now traveling at a slow pace."
        self.d = 25
        self.event_switch = 2


class Burn(Switcher):
    def __init__(self, game):
        Switcher.__init__(self, game)
        self.event_switch = 0
        if self.game.supplies == 0:
            self.text = "You don't have any supplies to burn."
            return
        fuel_gained = randint(1, 25)
        self.game.supplies -= 1
        self.game.fuel += fuel_gained
        self.text = f"{fuel_gained} fuel gained."


class BurnOut(Burn):
    def __init__(self, game):
        Burn.__init__(self, game)

    def update(self, actions):
        if actions["start"] and not self.done:
            self.done = True
        elif actions["start"]:
            self.prev_state.events_created = 0
            self.exit_state()
        self.game.reset_keys()


class FastASP(ComplexEvent):
    def __init__(self, game):
        ComplexEvent.__init__(self, game)
        self.distance = round(self.game.fuel / self.game.fuel_per_distance)

    def update(self, actions):
        self.game.move(self.distance)
        self.prev_state.events_created = 0
        self.exit_state()


class Distress(AutoSwitch):
    def __init__(self, game):
        AutoSwitch.__init__(self, game)
        self.event_switch = randint(6, 7)


class Pirates(ComplexEvent):
    def __init__(self, game):
        ComplexEvent.__init__(self, game)
        self.outcome = randint(0, 1)
        self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("assets", "sprites", "pirateship.png")), (GAME_W/4, GAME_H/4)), 180)
        if self.outcome == 1:
            ext_txt = "!"
            money_stole = 0
            if self.game.money > 0:
                money_stole = randint(1, self.game.money)
                ext_txt = f" and stole {money_stole} money!"
            self.game.damage_events += 1
            self.game.dmg_accept = False
            self.text = "The pirates attacked you damaging your ship" + ext_txt


class Fight(Pirates):
    def __init__(self, game):
        Pirates.__init__(self, game)
        if self.outcome == 0:
            fuel_gained = randint(1, 100)
            self.game.fuel += fuel_gained
            self.text = f"You have defeated the pirates and gained {fuel_gained} fuel!"


class Flee(Pirates):
    def __init__(self, game):
        Pirates.__init__(self, game)
        if self.outcome == 0:
            self.text = f"You have escaped the pirates!"


class Negotiate(Pirates):
    def __init__(self, game):
        Pirates.__init__(self, game)
        if self.outcome == 0:
            self.text = f"The pirates decided to let you go."


class FShip(ComplexEvent):
    def __init__(self, game):
        ComplexEvent.__init__(self, game)
        self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("assets", "sprites", "spaceship.png")), (GAME_W/4, GAME_H/4)), 180)


class Accept(FShip):
    def __init__(self, game):
        FShip.__init__(self, game)
        fuel_gained = randint(1, 100)
        self.game.fuel += fuel_gained
        self.text = f"The ship has given you {fuel_gained} fuel!"
        self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("assets", "sprites", "spaceship.png")), (GAME_W/4, GAME_H/4)), 180)


class Deny(FShip):
    def __init__(self, game):
        FShip.__init__(self, game)
        self.text = "The ship has left."
        self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("assets", "sprites", "spaceship.png")), (GAME_W/4, GAME_H/4)), 180)


class Station(Switcher):
    def __init__(self, game):
        Switcher.__init__(self, game)
        self.image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "sprites", "station.png")), (GAME_W/3, GAME_H/3))

class BuySupplies(Station):
    def __init__(self, game):
        Station.__init__(self, game)
        self.event_switch = 4
        if self.game.money >= 50:
            self.text = "You have bought supplies."
            self.game.money -= 50
            self.game.supplies += 1
        else:
            self.text = "You don't have enough money."


class BuyFuel(Station):
    def __init__(self, game):
        Station.__init__(self, game)
        self.event_switch = 4
        if self.game.money >= 50:
            self.text = "You have bought fuel."
            self.game.money -= 50
            self.game.fuel += 100
        else:
            self.text = "You don't have enough money."


class SellArt(Station):
     def __init__(self, game):
        Station.__init__(self, game)
        self.event_switch = 4
        
        if len(self.game.artifacts) == 0:
            self.text = "You don't have any artifacts!"
            return
        
        sum = 0
        for key in self.game.artifacts:
            sum += self.game.artifacts[key]
            self.game.artifacts.pop(key)
        self.game.money += sum
        self.text = f"You gained {sum} money by selling the artifacts!"


class Leave(AutoSwitch):
    def __init__(self, game):
        AutoSwitch.__init__(self, game)
        self.event_switch = 0 if self.game.fuel > 0 else 3
    

class Replace(ComplexEvent):
    def __init__(self, game):
        ComplexEvent.__init__(self, game)
        self.event_switch = 5
        self.fixed = False
        if self.game.money >= 100:
            self.text = "You replaces the parts for 100 money."
            self.game.money -= 100
            self.fixed = True
            self.game.damage_events -= 1
        else:
            self.text = "You don't have enough money."

    def update(self, actions):
        if actions["start"] and not self.done:
            self.done = True
        elif actions["start"] and self.fixed:
            self.prev_state.events_created = 0
            self.exit_state()
        elif actions["start"] and not self.fixed:
            self.switch_event()
        self.game.reset_keys()


class Repair(Replace):
    def __init__(self, game):
        ComplexEvent.__init__(self, game)
        self.event_switch = 5
        self.fixed = False
        if self.game.supplies >= 1:
            self.text = "You fix the ship using your supplies!"
            self.game.damage_events -= 1
            self.game.supplies -= 1
            self.fixed = True
        else:
            self.text = "You don't have any supplies."


class Ignore(ComplexEvent):
    def update(self, actions):
        self.game.dmg_accept = True
        self.prev_state.events_created = 0
        self.exit_state()


class TakeArt(ComplexEvent):
    def __init__(self, game):
        ComplexEvent.__init__(self, game)
        event = randint(0, 2)
        if event == 0:
            self.text = "The artifact explodes damaging your ship!"
            self.game.damage_events += 1
        elif event == 1:
            self.text = "The artifact disappears as you take it!"
        else:
            self.text = "You take the artifact."
            self.game.artifacts[f"artifact{len(self.game.artifacts) + 1}"] = randint(1, 500)


class LeaveArt(ComplexEvent):
    def update(self, actions):
        self.prev_state.events_created = 0
        self.exit_state()

class LeavePlanet(LeaveArt):
    def __init__(self, game):
        ComplexEvent.__init__(self, game)
        self.image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "sprites", "planet.png")), (GAME_W/2, GAME_H/2))

class Supplies(ComplexEvent):
    def __init__(self, game):
        ComplexEvent.__init__(self, game)
        event = randint(0, 1)
        self.image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "sprites", "planet.png")), (GAME_W/2, GAME_H/2))
        if event == 0:
            self.text = "You did not find any supplies"
            self.game.supplies += 1
        elif event == 1:
            self.text = "You found supplies!"