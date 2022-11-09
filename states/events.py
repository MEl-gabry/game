from . import complex_events
from .game_over import GameOver

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
        }
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
        }
    },
    {
        "text": "You have run into a friendly ship! They are offering you fuel!",
        "options": {
            "Accept": complex_events.Accept, 
            "Deny": complex_events.Deny,
        }
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
            "Leave It": complex_events.LeaveArt
        }
    }
]