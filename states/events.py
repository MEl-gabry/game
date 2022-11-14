from . import complex_events
from .game_over import GameOver
import pygame
import os
from .consts import GAME_W, GAME_H

simple_events = [
    {
        "text": "How fast do you want to travel?",
        "options": {
            "Fast Pace": complex_events.FastPace, 
            "Medium Pace": complex_events.MediumPace, 
            "Slow Pace": complex_events.SlowPace
        }
    },
    {
        "text": "You don't have enough fuel to go this fast!",
        "options": {
            "Burn resources for fuel": complex_events.Burn, 
            "Go at a slower pace": complex_events.AutoSwitch
        }
    },
    {
        "text": "You don't have enough fuel to go at the slowest pace!",
        "options": {
            "Burn resources for fuel": complex_events.Burn, 
            "Go as fast as possible": complex_events.FastASP
        }
    },
    {
        "text": "You are out of fuel!",
        "options": {
            "Burn resources for fuel": complex_events.BurnOut, 
            "Send out a distress call": complex_events.Distress,
            "End game": GameOver
        }
    },
    {
        "text": "You arrive at a station.",
        "options": {
            "Buy Supplies": complex_events.BuySupplies, 
            "Buy fuel": complex_events.BuyFuel,
            "Sell Artifacts": complex_events.SellArt,
            "Leave": complex_events.Leave
        },
        "image": pygame.transform.scale(pygame.image.load(os.path.join("assets", "sprites", "station.png")), (GAME_W/4, 2 * GAME_H/3)),
        "coords": (GAME_W/2, GAME_H/16)
    },
    {
        "text": "Your ship has been damaged!",
        "options": {
            "Replace": complex_events.Replace, 
            "Repair": complex_events.Repair,
            "Ignore": complex_events.Ignore
        }
    },
    {
        "text": "You are being attacked by pirates!",
        "options": {
            "Fight back": complex_events.Fight, 
            "Flee": complex_events.Flee,
            "Negotiate": complex_events.Negotiate
        },
        "image": pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("assets", "sprites", "pirateship.png")), (GAME_W/4, GAME_H/4)), 180),
        "coords": (GAME_W/2, GAME_H/3)
    },
    {
        "text": "You have run into a friendly ship! They are offering you fuel!",
        "options": {
            "Accept": complex_events.Accept, 
            "Deny": complex_events.Deny,
        },
        "image": pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("assets", "sprites", "spaceship.png")), (GAME_W/4, GAME_H/4)), 180),
        "coords": (GAME_W/2, GAME_H/3)
    },
    {
        "text": "You have run into a strange artifact!",
        "options": {
            "Take It": complex_events.TakeArt, 
            "Leave It": complex_events.LeaveArt
        }
    },
    {
        "text": "You discovered a new planet!",
        "options": {
            "Scavenge for supplies": complex_events.Supplies, 
            "Leave It": complex_events.LeavePlanet
        },
        "image": pygame.transform.scale(pygame.image.load(os.path.join("assets", "sprites", "planet.png")), (3 * GAME_W/4, 3 * GAME_H/4)),
        "coords": (GAME_W/3, GAME_H/16)
    }
]