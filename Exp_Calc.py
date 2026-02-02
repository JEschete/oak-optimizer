#!/usr/bin/env python3
"""
Pokemon Gen 3 Expected EXP Calculator v2
Calculates the expected EXP yield per wild battle for each location,
broken down by encounter type (grass, surfing, fishing).

Gen 3 EXP Formula (wild Pokemon) with PROPER INTEGER MATH:
EXP = floor(floor(base_exp * level) / 7)

With Lucky Egg (1.5x multiplier applied with floor after each step):
EXP = floor(floor(floor(base_exp * level) / 7) * 3 / 2)

The game floors after EVERY multiplication/division operation.
"""

import json
import math
from collections import defaultdict
from typing import Dict, List, Tuple, Any, Optional

# =============================================================================
# GEN 3 BASE EXPERIENCE VALUES
# =============================================================================
BASE_EXP = {
    # Gen 1
    "SPECIES_BULBASAUR": 64, "SPECIES_IVYSAUR": 141, "SPECIES_VENUSAUR": 208,
    "SPECIES_CHARMANDER": 65, "SPECIES_CHARMELEON": 142, "SPECIES_CHARIZARD": 209,
    "SPECIES_SQUIRTLE": 66, "SPECIES_WARTORTLE": 143, "SPECIES_BLASTOISE": 210,
    "SPECIES_CATERPIE": 53, "SPECIES_METAPOD": 72, "SPECIES_BUTTERFREE": 160,
    "SPECIES_WEEDLE": 52, "SPECIES_KAKUNA": 71, "SPECIES_BEEDRILL": 159,
    "SPECIES_PIDGEY": 55, "SPECIES_PIDGEOTTO": 113, "SPECIES_PIDGEOT": 172,
    "SPECIES_RATTATA": 57, "SPECIES_RATICATE": 116,
    "SPECIES_SPEAROW": 58, "SPECIES_FEAROW": 162,
    "SPECIES_EKANS": 62, "SPECIES_ARBOK": 147,
    "SPECIES_PIKACHU": 82, "SPECIES_RAICHU": 122,
    "SPECIES_SANDSHREW": 93, "SPECIES_SANDSLASH": 163,
    "SPECIES_NIDORAN_F": 59, "SPECIES_NIDORINA": 117, "SPECIES_NIDOQUEEN": 194,
    "SPECIES_NIDORAN_M": 60, "SPECIES_NIDORINO": 118, "SPECIES_NIDOKING": 195,
    "SPECIES_CLEFAIRY": 68, "SPECIES_CLEFABLE": 129,
    "SPECIES_VULPIX": 63, "SPECIES_NINETALES": 178,
    "SPECIES_JIGGLYPUFF": 76, "SPECIES_WIGGLYTUFF": 109,
    "SPECIES_ZUBAT": 54, "SPECIES_GOLBAT": 171,
    "SPECIES_ODDISH": 78, "SPECIES_GLOOM": 132, "SPECIES_VILEPLUME": 184,
    "SPECIES_PARAS": 70, "SPECIES_PARASECT": 128,
    "SPECIES_VENONAT": 75, "SPECIES_VENOMOTH": 138,
    "SPECIES_DIGLETT": 81, "SPECIES_DUGTRIO": 153,
    "SPECIES_MEOWTH": 69, "SPECIES_PERSIAN": 148,
    "SPECIES_PSYDUCK": 80, "SPECIES_GOLDUCK": 174,
    "SPECIES_MANKEY": 74, "SPECIES_PRIMEAPE": 149,
    "SPECIES_GROWLITHE": 91, "SPECIES_ARCANINE": 194,
    "SPECIES_POLIWAG": 77, "SPECIES_POLIWHIRL": 131, "SPECIES_POLIWRATH": 185,
    "SPECIES_ABRA": 73, "SPECIES_KADABRA": 145, "SPECIES_ALAKAZAM": 186,
    "SPECIES_MACHOP": 75, "SPECIES_MACHOKE": 146, "SPECIES_MACHAMP": 193,
    "SPECIES_BELLSPROUT": 84, "SPECIES_WEEPINBELL": 151, "SPECIES_VICTREEBEL": 191,
    "SPECIES_TENTACOOL": 105, "SPECIES_TENTACRUEL": 205,
    "SPECIES_GEODUDE": 73, "SPECIES_GRAVELER": 134, "SPECIES_GOLEM": 177,
    "SPECIES_PONYTA": 152, "SPECIES_RAPIDASH": 192,
    "SPECIES_SLOWPOKE": 99, "SPECIES_SLOWBRO": 164,
    "SPECIES_MAGNEMITE": 89, "SPECIES_MAGNETON": 161,
    "SPECIES_FARFETCHD": 94,
    "SPECIES_DODUO": 96, "SPECIES_DODRIO": 158,
    "SPECIES_SEEL": 100, "SPECIES_DEWGONG": 176,
    "SPECIES_GRIMER": 90, "SPECIES_MUK": 157,
    "SPECIES_SHELLDER": 97, "SPECIES_CLOYSTER": 203,
    "SPECIES_GASTLY": 95, "SPECIES_HAUNTER": 126, "SPECIES_GENGAR": 190,
    "SPECIES_ONIX": 108,
    "SPECIES_DROWZEE": 102, "SPECIES_HYPNO": 165,
    "SPECIES_KRABBY": 115, "SPECIES_KINGLER": 206,
    "SPECIES_VOLTORB": 103, "SPECIES_ELECTRODE": 150,
    "SPECIES_EXEGGCUTE": 98, "SPECIES_EXEGGUTOR": 212,
    "SPECIES_CUBONE": 87, "SPECIES_MAROWAK": 124,
    "SPECIES_HITMONLEE": 139, "SPECIES_HITMONCHAN": 140,
    "SPECIES_LICKITUNG": 127,
    "SPECIES_KOFFING": 114, "SPECIES_WEEZING": 173,
    "SPECIES_RHYHORN": 135, "SPECIES_RHYDON": 204,
    "SPECIES_CHANSEY": 255,
    "SPECIES_TANGELA": 166,
    "SPECIES_KANGASKHAN": 175,
    "SPECIES_HORSEA": 83, "SPECIES_SEADRA": 155,
    "SPECIES_GOLDEEN": 111, "SPECIES_SEAKING": 170,
    "SPECIES_STARYU": 106, "SPECIES_STARMIE": 207,
    "SPECIES_MR_MIME": 136,
    "SPECIES_SCYTHER": 187,
    "SPECIES_JYNX": 137,
    "SPECIES_ELECTABUZZ": 156,
    "SPECIES_MAGMAR": 167,
    "SPECIES_PINSIR": 200,
    "SPECIES_TAUROS": 211,
    "SPECIES_MAGIKARP": 20, "SPECIES_GYARADOS": 214,
    "SPECIES_LAPRAS": 219,
    "SPECIES_DITTO": 61,
    "SPECIES_EEVEE": 92, "SPECIES_VAPOREON": 196, "SPECIES_JOLTEON": 197, "SPECIES_FLAREON": 198,
    "SPECIES_PORYGON": 130,
    "SPECIES_OMANYTE": 120, "SPECIES_OMASTAR": 199,
    "SPECIES_KABUTO": 119, "SPECIES_KABUTOPS": 201,
    "SPECIES_AERODACTYL": 202,
    "SPECIES_SNORLAX": 154,
    "SPECIES_ARTICUNO": 215, "SPECIES_ZAPDOS": 216, "SPECIES_MOLTRES": 217,
    "SPECIES_DRATINI": 67, "SPECIES_DRAGONAIR": 144, "SPECIES_DRAGONITE": 218,
    "SPECIES_MEWTWO": 220, "SPECIES_MEW": 64,
    
    # Gen 2
    "SPECIES_CHIKORITA": 64, "SPECIES_BAYLEEF": 141, "SPECIES_MEGANIUM": 208,
    "SPECIES_CYNDAQUIL": 65, "SPECIES_QUILAVA": 142, "SPECIES_TYPHLOSION": 209,
    "SPECIES_TOTODILE": 66, "SPECIES_CROCONAW": 143, "SPECIES_FERALIGATR": 210,
    "SPECIES_SENTRET": 57, "SPECIES_FURRET": 116,
    "SPECIES_HOOTHOOT": 58, "SPECIES_NOCTOWL": 162,
    "SPECIES_LEDYBA": 54, "SPECIES_LEDIAN": 134,
    "SPECIES_SPINARAK": 54, "SPECIES_ARIADOS": 134,
    "SPECIES_CROBAT": 204,
    "SPECIES_CHINCHOU": 90, "SPECIES_LANTURN": 156,
    "SPECIES_PICHU": 42, "SPECIES_CLEFFA": 37, "SPECIES_IGGLYBUFF": 39,
    "SPECIES_TOGEPI": 74, "SPECIES_TOGETIC": 114,
    "SPECIES_NATU": 73, "SPECIES_XATU": 171,
    "SPECIES_MAREEP": 59, "SPECIES_FLAAFFY": 117, "SPECIES_AMPHAROS": 194,
    "SPECIES_BELLOSSOM": 184,
    "SPECIES_MARILL": 58, "SPECIES_AZUMARILL": 153,
    "SPECIES_SUDOWOODO": 135,
    "SPECIES_POLITOED": 185,
    "SPECIES_HOPPIP": 74, "SPECIES_SKIPLOOM": 136, "SPECIES_JUMPLUFF": 176,
    "SPECIES_AIPOM": 94,
    "SPECIES_SUNKERN": 52, "SPECIES_SUNFLORA": 146,
    "SPECIES_YANMA": 147,
    "SPECIES_WOOPER": 52, "SPECIES_QUAGSIRE": 137,
    "SPECIES_ESPEON": 197, "SPECIES_UMBREON": 197,
    "SPECIES_MURKROW": 107,
    "SPECIES_SLOWKING": 164,
    "SPECIES_MISDREAVUS": 147,
    "SPECIES_UNOWN": 61,
    "SPECIES_WOBBUFFET": 177,
    "SPECIES_GIRAFARIG": 149,
    "SPECIES_PINECO": 60, "SPECIES_FORRETRESS": 118,
    "SPECIES_DUNSPARCE": 125,
    "SPECIES_GLIGAR": 108,
    "SPECIES_STEELIX": 196,
    "SPECIES_SNUBBULL": 63, "SPECIES_GRANBULL": 138,
    "SPECIES_QWILFISH": 100,
    "SPECIES_SCIZOR": 200,
    "SPECIES_SHUCKLE": 80,
    "SPECIES_HERACROSS": 200,
    "SPECIES_SNEASEL": 132,
    "SPECIES_TEDDIURSA": 124, "SPECIES_URSARING": 189,
    "SPECIES_SLUGMA": 78, "SPECIES_MAGCARGO": 154,
    "SPECIES_SWINUB": 78, "SPECIES_PILOSWINE": 160,
    "SPECIES_CORSOLA": 113,
    "SPECIES_REMORAID": 78, "SPECIES_OCTILLERY": 164,
    "SPECIES_DELIBIRD": 183,
    "SPECIES_MANTINE": 168,
    "SPECIES_SKARMORY": 168,
    "SPECIES_HOUNDOUR": 114, "SPECIES_HOUNDOOM": 179,
    "SPECIES_KINGDRA": 207,
    "SPECIES_PHANPY": 124, "SPECIES_DONPHAN": 189,
    "SPECIES_PORYGON2": 180,
    "SPECIES_STANTLER": 165,
    "SPECIES_SMEARGLE": 106,
    "SPECIES_TYROGUE": 91, "SPECIES_HITMONTOP": 138,
    "SPECIES_SMOOCHUM": 87, "SPECIES_ELEKID": 106, "SPECIES_MAGBY": 117,
    "SPECIES_MILTANK": 200,
    "SPECIES_BLISSEY": 255,
    "SPECIES_RAIKOU": 216, "SPECIES_ENTEI": 217, "SPECIES_SUICUNE": 215,
    "SPECIES_LARVITAR": 67, "SPECIES_PUPITAR": 144, "SPECIES_TYRANITAR": 218,
    "SPECIES_LUGIA": 220, "SPECIES_HO_OH": 220, "SPECIES_CELEBI": 64,
    
    # Gen 3
    "SPECIES_TREECKO": 65, "SPECIES_GROVYLE": 141, "SPECIES_SCEPTILE": 208,
    "SPECIES_TORCHIC": 65, "SPECIES_COMBUSKEN": 142, "SPECIES_BLAZIKEN": 209,
    "SPECIES_MUDKIP": 65, "SPECIES_MARSHTOMP": 142, "SPECIES_SWAMPERT": 210,
    "SPECIES_POOCHYENA": 55, "SPECIES_MIGHTYENA": 128,
    "SPECIES_ZIGZAGOON": 60, "SPECIES_LINOONE": 137,
    "SPECIES_WURMPLE": 54, "SPECIES_SILCOON": 72, "SPECIES_BEAUTIFLY": 161,
    "SPECIES_CASCOON": 72, "SPECIES_DUSTOX": 161,
    "SPECIES_LOTAD": 74, "SPECIES_LOMBRE": 141, "SPECIES_LUDICOLO": 181,
    "SPECIES_SEEDOT": 74, "SPECIES_NUZLEAF": 141, "SPECIES_SHIFTRY": 181,
    "SPECIES_TAILLOW": 59, "SPECIES_SWELLOW": 162,
    "SPECIES_WINGULL": 64, "SPECIES_PELIPPER": 164,
    "SPECIES_RALTS": 70, "SPECIES_KIRLIA": 140, "SPECIES_GARDEVOIR": 208,
    "SPECIES_SURSKIT": 63, "SPECIES_MASQUERAIN": 128,
    "SPECIES_SHROOMISH": 65, "SPECIES_BRELOOM": 165,
    "SPECIES_SLAKOTH": 83, "SPECIES_VIGOROTH": 126, "SPECIES_SLAKING": 210,
    "SPECIES_NINCADA": 65, "SPECIES_NINJASK": 155, "SPECIES_SHEDINJA": 95,
    "SPECIES_WHISMUR": 68, "SPECIES_LOUDRED": 126, "SPECIES_EXPLOUD": 184,
    "SPECIES_MAKUHITA": 47, "SPECIES_HARIYAMA": 184,
    "SPECIES_AZURILL": 33,
    "SPECIES_NOSEPASS": 108,
    "SPECIES_SKITTY": 65, "SPECIES_DELCATTY": 140,
    "SPECIES_SABLEYE": 98,
    "SPECIES_MAWILE": 98,
    "SPECIES_ARON": 96, "SPECIES_LAIRON": 152, "SPECIES_AGGRON": 205,
    "SPECIES_MEDITITE": 91, "SPECIES_MEDICHAM": 153,
    "SPECIES_ELECTRIKE": 59, "SPECIES_MANECTRIC": 168,
    "SPECIES_PLUSLE": 120, "SPECIES_MINUN": 120,
    "SPECIES_VOLBEAT": 146, "SPECIES_ILLUMISE": 146,
    "SPECIES_ROSELIA": 152,
    "SPECIES_GULPIN": 75, "SPECIES_SWALOT": 168,
    "SPECIES_CARVANHA": 88, "SPECIES_SHARPEDO": 175,
    "SPECIES_WAILMER": 137, "SPECIES_WAILORD": 206,
    "SPECIES_NUMEL": 88, "SPECIES_CAMERUPT": 175,
    "SPECIES_TORKOAL": 161,
    "SPECIES_SPOINK": 89, "SPECIES_GRUMPIG": 164,
    "SPECIES_SPINDA": 85,
    "SPECIES_TRAPINCH": 73, "SPECIES_VIBRAVA": 126, "SPECIES_FLYGON": 197,
    "SPECIES_CACNEA": 97, "SPECIES_CACTURNE": 177,
    "SPECIES_SWABLU": 74, "SPECIES_ALTARIA": 188,
    "SPECIES_ZANGOOSE": 165, "SPECIES_SEVIPER": 165,
    "SPECIES_LUNATONE": 150, "SPECIES_SOLROCK": 150,
    "SPECIES_BARBOACH": 92, "SPECIES_WHISCASH": 158,
    "SPECIES_CORPHISH": 111, "SPECIES_CRAWDAUNT": 161,
    "SPECIES_BALTOY": 60, "SPECIES_CLAYDOL": 189,
    "SPECIES_LILEEP": 99, "SPECIES_CRADILY": 199,
    "SPECIES_ANORITH": 99, "SPECIES_ARMALDO": 199,
    "SPECIES_FEEBAS": 61, "SPECIES_MILOTIC": 213,
    "SPECIES_CASTFORM": 147,
    "SPECIES_KECLEON": 132,
    "SPECIES_SHUPPET": 97, "SPECIES_BANETTE": 179,
    "SPECIES_DUSKULL": 97, "SPECIES_DUSCLOPS": 179,
    "SPECIES_TROPIUS": 169,
    "SPECIES_CHIMECHO": 147,
    "SPECIES_ABSOL": 174,
    "SPECIES_WYNAUT": 44,
    "SPECIES_SNORUNT": 74, "SPECIES_GLALIE": 187,
    "SPECIES_SPHEAL": 75, "SPECIES_SEALEO": 128, "SPECIES_WALREIN": 192,
    "SPECIES_CLAMPERL": 142, "SPECIES_HUNTAIL": 178, "SPECIES_GOREBYSS": 178,
    "SPECIES_RELICANTH": 198,
    "SPECIES_LUVDISC": 110,
    "SPECIES_BAGON": 89, "SPECIES_SHELGON": 144, "SPECIES_SALAMENCE": 218,
    "SPECIES_BELDUM": 103, "SPECIES_METANG": 153, "SPECIES_METAGROSS": 210,
    "SPECIES_REGIROCK": 217, "SPECIES_REGICE": 216, "SPECIES_REGISTEEL": 215,
    "SPECIES_LATIAS": 211, "SPECIES_LATIOS": 211,
    "SPECIES_KYOGRE": 218, "SPECIES_GROUDON": 218, "SPECIES_RAYQUAZA": 220,
    "SPECIES_JIRACHI": 215, "SPECIES_DEOXYS": 215,
}

# =============================================================================
# GROWTH RATE DATA - Total EXP needed to reach each level
# =============================================================================
# Growth rate types in Gen 3
GROWTH_RATES = {
    "ERRATIC": "erratic",
    "FAST": "fast", 
    "MEDIUM_FAST": "medium_fast",
    "MEDIUM_SLOW": "medium_slow",
    "SLOW": "slow",
    "FLUCTUATING": "fluctuating"
}

def exp_for_level_erratic(n: int) -> int:
    """Erratic growth rate formula"""
    if n <= 1:
        return 0
    elif n <= 50:
        return (n ** 3 * (100 - n)) // 50
    elif n <= 68:
        return (n ** 3 * (150 - n)) // 100
    elif n <= 98:
        return (n ** 3 * ((1911 - 10 * n) // 3)) // 500
    else:  # 99-100
        return (n ** 3 * (160 - n)) // 100

def exp_for_level_fast(n: int) -> int:
    """Fast growth rate: 4n³/5"""
    if n <= 1:
        return 0
    return (4 * n ** 3) // 5

def exp_for_level_medium_fast(n: int) -> int:
    """Medium Fast growth rate: n³"""
    if n <= 1:
        return 0
    return n ** 3

def exp_for_level_medium_slow(n: int) -> int:
    """Medium Slow growth rate: 6n³/5 - 15n² + 100n - 140"""
    if n <= 1:
        return 0
    return (6 * n ** 3) // 5 - 15 * n ** 2 + 100 * n - 140

def exp_for_level_slow(n: int) -> int:
    """Slow growth rate: 5n³/4"""
    if n <= 1:
        return 0
    return (5 * n ** 3) // 4

def exp_for_level_fluctuating(n: int) -> int:
    """Fluctuating growth rate formula"""
    if n <= 1:
        return 0
    elif n <= 15:
        return (n ** 3 * (((n + 1) // 3) + 24)) // 50
    elif n <= 36:
        return (n ** 3 * (n + 14)) // 50
    else:
        return (n ** 3 * ((n // 2) + 32)) // 50

GROWTH_RATE_FUNCTIONS = {
    "erratic": exp_for_level_erratic,
    "fast": exp_for_level_fast,
    "medium_fast": exp_for_level_medium_fast,
    "medium_slow": exp_for_level_medium_slow,
    "slow": exp_for_level_slow,
    "fluctuating": exp_for_level_fluctuating,
}

# Pokemon to Growth Rate mapping (Gen 1-3)
SPECIES_GROWTH_RATE = {
    # Starters and evolutions - Medium Slow
    "SPECIES_BULBASAUR": "medium_slow", "SPECIES_IVYSAUR": "medium_slow", "SPECIES_VENUSAUR": "medium_slow",
    "SPECIES_CHARMANDER": "medium_slow", "SPECIES_CHARMELEON": "medium_slow", "SPECIES_CHARIZARD": "medium_slow",
    "SPECIES_SQUIRTLE": "medium_slow", "SPECIES_WARTORTLE": "medium_slow", "SPECIES_BLASTOISE": "medium_slow",
    "SPECIES_CHIKORITA": "medium_slow", "SPECIES_BAYLEEF": "medium_slow", "SPECIES_MEGANIUM": "medium_slow",
    "SPECIES_CYNDAQUIL": "medium_slow", "SPECIES_QUILAVA": "medium_slow", "SPECIES_TYPHLOSION": "medium_slow",
    "SPECIES_TOTODILE": "medium_slow", "SPECIES_CROCONAW": "medium_slow", "SPECIES_FERALIGATR": "medium_slow",
    "SPECIES_TREECKO": "medium_slow", "SPECIES_GROVYLE": "medium_slow", "SPECIES_SCEPTILE": "medium_slow",
    "SPECIES_TORCHIC": "medium_slow", "SPECIES_COMBUSKEN": "medium_slow", "SPECIES_BLAZIKEN": "medium_slow",
    "SPECIES_MUDKIP": "medium_slow", "SPECIES_MARSHTOMP": "medium_slow", "SPECIES_SWAMPERT": "medium_slow",
    
    # Fast growth Pokemon
    "SPECIES_CATERPIE": "medium_fast", "SPECIES_METAPOD": "medium_fast", "SPECIES_BUTTERFREE": "medium_fast",
    "SPECIES_WEEDLE": "medium_fast", "SPECIES_KAKUNA": "medium_fast", "SPECIES_BEEDRILL": "medium_fast",
    "SPECIES_PIDGEY": "medium_slow", "SPECIES_PIDGEOTTO": "medium_slow", "SPECIES_PIDGEOT": "medium_slow",
    "SPECIES_RATTATA": "medium_fast", "SPECIES_RATICATE": "medium_fast",
    "SPECIES_SPEAROW": "medium_fast", "SPECIES_FEAROW": "medium_fast",
    "SPECIES_EKANS": "medium_fast", "SPECIES_ARBOK": "medium_fast",
    "SPECIES_PIKACHU": "medium_fast", "SPECIES_RAICHU": "medium_fast", "SPECIES_PICHU": "medium_fast",
    "SPECIES_SANDSHREW": "medium_fast", "SPECIES_SANDSLASH": "medium_fast",
    "SPECIES_NIDORAN_F": "medium_slow", "SPECIES_NIDORINA": "medium_slow", "SPECIES_NIDOQUEEN": "medium_slow",
    "SPECIES_NIDORAN_M": "medium_slow", "SPECIES_NIDORINO": "medium_slow", "SPECIES_NIDOKING": "medium_slow",
    "SPECIES_CLEFAIRY": "fast", "SPECIES_CLEFABLE": "fast", "SPECIES_CLEFFA": "fast",
    "SPECIES_VULPIX": "medium_fast", "SPECIES_NINETALES": "medium_fast",
    "SPECIES_JIGGLYPUFF": "fast", "SPECIES_WIGGLYTUFF": "fast", "SPECIES_IGGLYBUFF": "fast",
    "SPECIES_ZUBAT": "medium_fast", "SPECIES_GOLBAT": "medium_fast", "SPECIES_CROBAT": "medium_fast",
    "SPECIES_ODDISH": "medium_slow", "SPECIES_GLOOM": "medium_slow", "SPECIES_VILEPLUME": "medium_slow", "SPECIES_BELLOSSOM": "medium_slow",
    "SPECIES_PARAS": "medium_fast", "SPECIES_PARASECT": "medium_fast",
    "SPECIES_VENONAT": "medium_fast", "SPECIES_VENOMOTH": "medium_fast",
    "SPECIES_DIGLETT": "medium_fast", "SPECIES_DUGTRIO": "medium_fast",
    "SPECIES_MEOWTH": "medium_fast", "SPECIES_PERSIAN": "medium_fast",
    "SPECIES_PSYDUCK": "medium_fast", "SPECIES_GOLDUCK": "medium_fast",
    "SPECIES_MANKEY": "medium_fast", "SPECIES_PRIMEAPE": "medium_fast",
    "SPECIES_GROWLITHE": "slow", "SPECIES_ARCANINE": "slow",
    "SPECIES_POLIWAG": "medium_slow", "SPECIES_POLIWHIRL": "medium_slow", "SPECIES_POLIWRATH": "medium_slow", "SPECIES_POLITOED": "medium_slow",
    "SPECIES_ABRA": "medium_slow", "SPECIES_KADABRA": "medium_slow", "SPECIES_ALAKAZAM": "medium_slow",
    "SPECIES_MACHOP": "medium_slow", "SPECIES_MACHOKE": "medium_slow", "SPECIES_MACHAMP": "medium_slow",
    "SPECIES_BELLSPROUT": "medium_slow", "SPECIES_WEEPINBELL": "medium_slow", "SPECIES_VICTREEBEL": "medium_slow",
    "SPECIES_TENTACOOL": "slow", "SPECIES_TENTACRUEL": "slow",
    "SPECIES_GEODUDE": "medium_slow", "SPECIES_GRAVELER": "medium_slow", "SPECIES_GOLEM": "medium_slow",
    "SPECIES_PONYTA": "medium_fast", "SPECIES_RAPIDASH": "medium_fast",
    "SPECIES_SLOWPOKE": "medium_fast", "SPECIES_SLOWBRO": "medium_fast", "SPECIES_SLOWKING": "medium_fast",
    "SPECIES_MAGNEMITE": "medium_fast", "SPECIES_MAGNETON": "medium_fast",
    "SPECIES_FARFETCHD": "medium_fast",
    "SPECIES_DODUO": "medium_fast", "SPECIES_DODRIO": "medium_fast",
    "SPECIES_SEEL": "medium_fast", "SPECIES_DEWGONG": "medium_fast",
    "SPECIES_GRIMER": "medium_fast", "SPECIES_MUK": "medium_fast",
    "SPECIES_SHELLDER": "slow", "SPECIES_CLOYSTER": "slow",
    "SPECIES_GASTLY": "medium_slow", "SPECIES_HAUNTER": "medium_slow", "SPECIES_GENGAR": "medium_slow",
    "SPECIES_ONIX": "medium_fast", "SPECIES_STEELIX": "medium_fast",
    "SPECIES_DROWZEE": "medium_fast", "SPECIES_HYPNO": "medium_fast",
    "SPECIES_KRABBY": "medium_fast", "SPECIES_KINGLER": "medium_fast",
    "SPECIES_VOLTORB": "medium_fast", "SPECIES_ELECTRODE": "medium_fast",
    "SPECIES_EXEGGCUTE": "slow", "SPECIES_EXEGGUTOR": "slow",
    "SPECIES_CUBONE": "medium_fast", "SPECIES_MAROWAK": "medium_fast",
    "SPECIES_HITMONLEE": "medium_fast", "SPECIES_HITMONCHAN": "medium_fast", "SPECIES_HITMONTOP": "medium_fast", "SPECIES_TYROGUE": "medium_fast",
    "SPECIES_LICKITUNG": "medium_fast",
    "SPECIES_KOFFING": "medium_fast", "SPECIES_WEEZING": "medium_fast",
    "SPECIES_RHYHORN": "slow", "SPECIES_RHYDON": "slow",
    "SPECIES_CHANSEY": "fast", "SPECIES_BLISSEY": "fast",
    "SPECIES_TANGELA": "medium_fast",
    "SPECIES_KANGASKHAN": "medium_fast",
    "SPECIES_HORSEA": "medium_fast", "SPECIES_SEADRA": "medium_fast", "SPECIES_KINGDRA": "medium_fast",
    "SPECIES_GOLDEEN": "medium_fast", "SPECIES_SEAKING": "medium_fast",
    "SPECIES_STARYU": "slow", "SPECIES_STARMIE": "slow",
    "SPECIES_MR_MIME": "medium_fast",
    "SPECIES_SCYTHER": "medium_fast", "SPECIES_SCIZOR": "medium_fast",
    "SPECIES_JYNX": "medium_fast", "SPECIES_SMOOCHUM": "medium_fast",
    "SPECIES_ELECTABUZZ": "medium_fast", "SPECIES_ELEKID": "medium_fast",
    "SPECIES_MAGMAR": "medium_fast", "SPECIES_MAGBY": "medium_fast",
    "SPECIES_PINSIR": "slow",
    "SPECIES_TAUROS": "slow",
    "SPECIES_MAGIKARP": "slow", "SPECIES_GYARADOS": "slow",
    "SPECIES_LAPRAS": "slow",
    "SPECIES_DITTO": "medium_fast",
    "SPECIES_EEVEE": "medium_fast", "SPECIES_VAPOREON": "medium_fast", "SPECIES_JOLTEON": "medium_fast", 
    "SPECIES_FLAREON": "medium_fast", "SPECIES_ESPEON": "medium_fast", "SPECIES_UMBREON": "medium_fast",
    "SPECIES_PORYGON": "medium_fast", "SPECIES_PORYGON2": "medium_fast",
    "SPECIES_OMANYTE": "medium_fast", "SPECIES_OMASTAR": "medium_fast",
    "SPECIES_KABUTO": "medium_fast", "SPECIES_KABUTOPS": "medium_fast",
    "SPECIES_AERODACTYL": "slow",
    "SPECIES_SNORLAX": "slow",
    "SPECIES_ARTICUNO": "slow", "SPECIES_ZAPDOS": "slow", "SPECIES_MOLTRES": "slow",
    "SPECIES_DRATINI": "slow", "SPECIES_DRAGONAIR": "slow", "SPECIES_DRAGONITE": "slow",
    "SPECIES_MEWTWO": "slow", "SPECIES_MEW": "medium_slow",
    
    # Gen 2
    "SPECIES_SENTRET": "medium_fast", "SPECIES_FURRET": "medium_fast",
    "SPECIES_HOOTHOOT": "medium_fast", "SPECIES_NOCTOWL": "medium_fast",
    "SPECIES_LEDYBA": "fast", "SPECIES_LEDIAN": "fast",
    "SPECIES_SPINARAK": "fast", "SPECIES_ARIADOS": "fast",
    "SPECIES_CHINCHOU": "slow", "SPECIES_LANTURN": "slow",
    "SPECIES_TOGEPI": "fast", "SPECIES_TOGETIC": "fast",
    "SPECIES_NATU": "medium_fast", "SPECIES_XATU": "medium_fast",
    "SPECIES_MAREEP": "medium_slow", "SPECIES_FLAAFFY": "medium_slow", "SPECIES_AMPHAROS": "medium_slow",
    "SPECIES_MARILL": "fast", "SPECIES_AZUMARILL": "fast", "SPECIES_AZURILL": "fast",
    "SPECIES_SUDOWOODO": "medium_fast",
    "SPECIES_HOPPIP": "medium_slow", "SPECIES_SKIPLOOM": "medium_slow", "SPECIES_JUMPLUFF": "medium_slow",
    "SPECIES_AIPOM": "fast",
    "SPECIES_SUNKERN": "medium_slow", "SPECIES_SUNFLORA": "medium_slow",
    "SPECIES_YANMA": "medium_fast",
    "SPECIES_WOOPER": "medium_fast", "SPECIES_QUAGSIRE": "medium_fast",
    "SPECIES_MURKROW": "medium_slow",
    "SPECIES_MISDREAVUS": "fast",
    "SPECIES_UNOWN": "medium_fast",
    "SPECIES_WOBBUFFET": "medium_fast", "SPECIES_WYNAUT": "medium_fast",
    "SPECIES_GIRAFARIG": "medium_fast",
    "SPECIES_PINECO": "medium_fast", "SPECIES_FORRETRESS": "medium_fast",
    "SPECIES_DUNSPARCE": "medium_fast",
    "SPECIES_GLIGAR": "medium_slow",
    "SPECIES_SNUBBULL": "fast", "SPECIES_GRANBULL": "fast",
    "SPECIES_QWILFISH": "medium_fast",
    "SPECIES_SHUCKLE": "medium_slow",
    "SPECIES_HERACROSS": "slow",
    "SPECIES_SNEASEL": "medium_slow",
    "SPECIES_TEDDIURSA": "medium_fast", "SPECIES_URSARING": "medium_fast",
    "SPECIES_SLUGMA": "medium_fast", "SPECIES_MAGCARGO": "medium_fast",
    "SPECIES_SWINUB": "slow", "SPECIES_PILOSWINE": "slow",
    "SPECIES_CORSOLA": "fast",
    "SPECIES_REMORAID": "medium_fast", "SPECIES_OCTILLERY": "medium_fast",
    "SPECIES_DELIBIRD": "fast",
    "SPECIES_MANTINE": "slow",
    "SPECIES_SKARMORY": "slow",
    "SPECIES_HOUNDOUR": "slow", "SPECIES_HOUNDOOM": "slow",
    "SPECIES_PHANPY": "medium_fast", "SPECIES_DONPHAN": "medium_fast",
    "SPECIES_STANTLER": "slow",
    "SPECIES_SMEARGLE": "fast",
    "SPECIES_MILTANK": "slow",
    "SPECIES_RAIKOU": "slow", "SPECIES_ENTEI": "slow", "SPECIES_SUICUNE": "slow",
    "SPECIES_LARVITAR": "slow", "SPECIES_PUPITAR": "slow", "SPECIES_TYRANITAR": "slow",
    "SPECIES_LUGIA": "slow", "SPECIES_HO_OH": "slow", "SPECIES_CELEBI": "medium_slow",
    
    # Gen 3
    "SPECIES_POOCHYENA": "medium_fast", "SPECIES_MIGHTYENA": "medium_fast",
    "SPECIES_ZIGZAGOON": "medium_fast", "SPECIES_LINOONE": "medium_fast",
    "SPECIES_WURMPLE": "medium_fast", "SPECIES_SILCOON": "medium_fast", "SPECIES_BEAUTIFLY": "medium_fast",
    "SPECIES_CASCOON": "medium_fast", "SPECIES_DUSTOX": "medium_fast",
    "SPECIES_LOTAD": "medium_slow", "SPECIES_LOMBRE": "medium_slow", "SPECIES_LUDICOLO": "medium_slow",
    "SPECIES_SEEDOT": "medium_slow", "SPECIES_NUZLEAF": "medium_slow", "SPECIES_SHIFTRY": "medium_slow",
    "SPECIES_TAILLOW": "medium_slow", "SPECIES_SWELLOW": "medium_slow",
    "SPECIES_WINGULL": "medium_fast", "SPECIES_PELIPPER": "medium_fast",
    "SPECIES_RALTS": "slow", "SPECIES_KIRLIA": "slow", "SPECIES_GARDEVOIR": "slow",
    "SPECIES_SURSKIT": "medium_fast", "SPECIES_MASQUERAIN": "medium_fast",
    "SPECIES_SHROOMISH": "fluctuating", "SPECIES_BRELOOM": "fluctuating",
    "SPECIES_SLAKOTH": "slow", "SPECIES_VIGOROTH": "slow", "SPECIES_SLAKING": "slow",
    "SPECIES_NINCADA": "erratic", "SPECIES_NINJASK": "erratic", "SPECIES_SHEDINJA": "erratic",
    "SPECIES_WHISMUR": "medium_slow", "SPECIES_LOUDRED": "medium_slow", "SPECIES_EXPLOUD": "medium_slow",
    "SPECIES_MAKUHITA": "fluctuating", "SPECIES_HARIYAMA": "fluctuating",
    "SPECIES_NOSEPASS": "medium_fast",
    "SPECIES_SKITTY": "fast", "SPECIES_DELCATTY": "fast",
    "SPECIES_SABLEYE": "medium_slow",
    "SPECIES_MAWILE": "fast",
    "SPECIES_ARON": "slow", "SPECIES_LAIRON": "slow", "SPECIES_AGGRON": "slow",
    "SPECIES_MEDITITE": "medium_fast", "SPECIES_MEDICHAM": "medium_fast",
    "SPECIES_ELECTRIKE": "slow", "SPECIES_MANECTRIC": "slow",
    "SPECIES_PLUSLE": "medium_fast", "SPECIES_MINUN": "medium_fast",
    "SPECIES_VOLBEAT": "erratic", "SPECIES_ILLUMISE": "fluctuating",
    "SPECIES_ROSELIA": "medium_slow",
    "SPECIES_GULPIN": "fluctuating", "SPECIES_SWALOT": "fluctuating",
    "SPECIES_CARVANHA": "slow", "SPECIES_SHARPEDO": "slow",
    "SPECIES_WAILMER": "fluctuating", "SPECIES_WAILORD": "fluctuating",
    "SPECIES_NUMEL": "medium_fast", "SPECIES_CAMERUPT": "medium_fast",
    "SPECIES_TORKOAL": "medium_fast",
    "SPECIES_SPOINK": "fast", "SPECIES_GRUMPIG": "fast",
    "SPECIES_SPINDA": "fast",
    "SPECIES_TRAPINCH": "medium_slow", "SPECIES_VIBRAVA": "medium_slow", "SPECIES_FLYGON": "medium_slow",
    "SPECIES_CACNEA": "medium_slow", "SPECIES_CACTURNE": "medium_slow",
    "SPECIES_SWABLU": "erratic", "SPECIES_ALTARIA": "erratic",
    "SPECIES_ZANGOOSE": "erratic",
    "SPECIES_SEVIPER": "fluctuating",
    "SPECIES_LUNATONE": "fast", "SPECIES_SOLROCK": "fast",
    "SPECIES_BARBOACH": "medium_fast", "SPECIES_WHISCASH": "medium_fast",
    "SPECIES_CORPHISH": "fluctuating", "SPECIES_CRAWDAUNT": "fluctuating",
    "SPECIES_BALTOY": "medium_fast", "SPECIES_CLAYDOL": "medium_fast",
    "SPECIES_LILEEP": "erratic", "SPECIES_CRADILY": "erratic",
    "SPECIES_ANORITH": "erratic", "SPECIES_ARMALDO": "erratic",
    "SPECIES_FEEBAS": "erratic", "SPECIES_MILOTIC": "erratic",
    "SPECIES_CASTFORM": "medium_fast",
    "SPECIES_KECLEON": "medium_slow",
    "SPECIES_SHUPPET": "fast", "SPECIES_BANETTE": "fast",
    "SPECIES_DUSKULL": "fast", "SPECIES_DUSCLOPS": "fast",
    "SPECIES_TROPIUS": "slow",
    "SPECIES_CHIMECHO": "fast",
    "SPECIES_ABSOL": "medium_slow",
    "SPECIES_SNORUNT": "medium_fast", "SPECIES_GLALIE": "medium_fast",
    "SPECIES_SPHEAL": "medium_slow", "SPECIES_SEALEO": "medium_slow", "SPECIES_WALREIN": "medium_slow",
    "SPECIES_CLAMPERL": "erratic", "SPECIES_HUNTAIL": "erratic", "SPECIES_GOREBYSS": "erratic",
    "SPECIES_RELICANTH": "slow",
    "SPECIES_LUVDISC": "fast",
    "SPECIES_BAGON": "slow", "SPECIES_SHELGON": "slow", "SPECIES_SALAMENCE": "slow",
    "SPECIES_BELDUM": "slow", "SPECIES_METANG": "slow", "SPECIES_METAGROSS": "slow",
    "SPECIES_REGIROCK": "slow", "SPECIES_REGICE": "slow", "SPECIES_REGISTEEL": "slow",
    "SPECIES_LATIAS": "slow", "SPECIES_LATIOS": "slow",
    "SPECIES_KYOGRE": "slow", "SPECIES_GROUDON": "slow", "SPECIES_RAYQUAZA": "slow",
    "SPECIES_JIRACHI": "slow", "SPECIES_DEOXYS": "slow",
}

# =============================================================================
# ENCOUNTER RATE CONFIGURATIONS
# =============================================================================
LAND_ENCOUNTER_RATES = [20, 20, 10, 10, 10, 10, 5, 5, 4, 4, 1, 1]
WATER_ENCOUNTER_RATES = [60, 30, 5, 4, 1]
ROCK_SMASH_ENCOUNTER_RATES = [60, 30, 5, 4, 1]
FISHING_ENCOUNTER_RATES = [70, 30, 60, 20, 20, 40, 40, 15, 4, 1]
FISHING_GROUPS = {
    "old_rod": [0, 1],
    "good_rod": [2, 3, 4],
    "super_rod": [5, 6, 7, 8, 9]
}


# =============================================================================
# EXP CALCULATION FUNCTIONS (with proper integer math)
# =============================================================================

def calculate_exp_integer(base_exp: int, level: int, lucky_egg: bool = False) -> int:
    """
    Calculate EXP gained from defeating a wild Pokemon in Gen 3.
    Uses proper integer math with floor after each operation.
    
    Base formula: EXP = floor(floor(base_exp * level) / 7)
    With Lucky Egg: EXP = floor(floor(floor(base_exp * level) / 7) * 3 / 2)
    
    Gen 3 applies 1.5x as *3 then /2 with floor between.
    """
    # Step 1: base_exp * level (already integers, no floor needed)
    exp = base_exp * level
    
    # Step 2: divide by 7 (floor)
    exp = exp // 7
    
    # Step 3: Lucky Egg multiplier (1.5x = *3/2 with floor between)
    if lucky_egg:
        exp = exp * 3
        exp = exp // 2
    
    return exp


def calculate_expected_exp_for_slot(
    species: str, 
    min_level: int, 
    max_level: int, 
    lucky_egg: bool = False
) -> float:
    """
    Calculate the expected EXP for a single encounter slot.
    
    For level ranges, we calculate EXP for each possible level
    and average them (uniform distribution).
    """
    if species not in BASE_EXP:
        print(f"Warning: Unknown species {species}, using default base_exp of 50")
        base_exp = 50
    else:
        base_exp = BASE_EXP[species]
    
    # Calculate EXP for each possible level and average
    total_exp = 0
    num_levels = max_level - min_level + 1
    
    for level in range(min_level, max_level + 1):
        total_exp += calculate_exp_integer(base_exp, level, lucky_egg)
    
    return total_exp / num_levels


def normalize_rates(rates: List[int], indices: List[int] = None) -> List[float]:
    """Normalize encounter rates to probabilities (sum to 1)."""
    if indices is not None:
        subset_rates = [rates[i] for i in indices]
        total = sum(subset_rates)
        return [r / total for r in subset_rates]
    else:
        total = sum(rates)
        return [r / total for r in rates]


def calculate_encounter_type_expected_exp(
    mons: List[Dict],
    encounter_rates: List[int],
    indices: List[int] = None,
    lucky_egg: bool = False
) -> Tuple[float, List[Dict]]:
    """
    Calculate expected EXP for an encounter type.
    
    Returns:
        Tuple of (expected_exp, breakdown_list)
    """
    if indices is not None:
        working_mons = [mons[i] for i in indices]
        working_rates = [encounter_rates[i] for i in indices]
    else:
        working_mons = mons
        working_rates = encounter_rates[:len(mons)]
    
    probabilities = normalize_rates(working_rates, None)
    
    total_expected_exp = 0.0
    breakdown = []
    
    for i, (mon, prob) in enumerate(zip(working_mons, probabilities)):
        species = mon["species"]
        min_level = mon["min_level"]
        max_level = mon["max_level"]
        
        slot_exp = calculate_expected_exp_for_slot(species, min_level, max_level, lucky_egg)
        contribution = slot_exp * prob
        total_expected_exp += contribution
        
        breakdown.append({
            "slot": i,
            "species": species.replace("SPECIES_", ""),
            "min_level": min_level,
            "max_level": max_level,
            "probability": prob,
            "expected_exp": slot_exp,
            "contribution": contribution
        })
    
    return total_expected_exp, breakdown


def calculate_efficiency_score(expected_exp: float, encounter_rate: int) -> float:
    """
    Calculate grinding efficiency score.
    
    Efficiency = Expected EXP × (Encounter Rate / 16)
    
    In Gen 3, encounter_rate is typically 0-16 where higher = more frequent.
    This weighs high EXP with high encounter frequency.
    """
    if encounter_rate <= 0:
        return 0.0
    return expected_exp * (encounter_rate / 16.0)


# =============================================================================
# GROWTH RATE / BATTLE COUNTING FUNCTIONS
# =============================================================================

def get_total_exp_for_level(species: str, level: int) -> int:
    """Get total EXP needed to reach a given level for a species."""
    if species not in SPECIES_GROWTH_RATE:
        # Default to medium_fast if unknown
        growth_rate = "medium_fast"
    else:
        growth_rate = SPECIES_GROWTH_RATE[species]
    
    func = GROWTH_RATE_FUNCTIONS[growth_rate]
    return func(level)


def get_exp_needed(species: str, current_level: int, current_exp: int, target_level: int) -> int:
    """
    Calculate total EXP needed to go from current state to target level.
    
    Args:
        species: Pokemon species (SPECIES_XXX format)
        current_level: Current level
        current_exp: Current total EXP (what the game shows)
        target_level: Target level to reach
    
    Returns:
        EXP needed to reach target_level
    """
    target_exp = get_total_exp_for_level(species, target_level)
    return max(0, target_exp - current_exp)


def calculate_battles_needed(
    exp_needed: int, 
    expected_exp_per_battle: float,
    lucky_egg: bool = False
) -> Tuple[int, int]:
    """
    Calculate number of battles needed to gain required EXP.
    
    Returns:
        Tuple of (minimum_battles, expected_battles)
        - minimum_battles: Absolute minimum if you got max EXP every time
        - expected_battles: Expected number based on average
    """
    if expected_exp_per_battle <= 0:
        return (float('inf'), float('inf'))
    
    expected_battles = math.ceil(exp_needed / expected_exp_per_battle)
    
    return expected_battles


# =============================================================================
# DATA PROCESSING
# =============================================================================

def format_map_name(map_name: str) -> str:
    """Convert MAP_ROUTE101 to Route 101, etc."""
    name = map_name.replace("MAP_", "")
    if name.startswith("ROUTE"):
        route_num = name.replace("ROUTE", "")
        return f"Route {route_num}"
    name = name.replace("_", " ").title()
    return name


def detect_game_version(data: Dict) -> str:
    """
    Auto-detect which game the encounter data is from.
    
    Ruby/Sapphire JSON has base_labels like "Route101_Ruby", "Route101_Sapphire"
    Emerald JSON has base_labels like "gRoute101"
    """
    for group in data.get("wild_encounter_groups", []):
        if not group.get("for_maps", False):
            continue
        for encounter in group.get("encounters", []):
            base_label = encounter.get("base_label", "")
            if "_Ruby" in base_label or "_Sapphire" in base_label:
                return "RS"  # Ruby/Sapphire combined file
            elif base_label.startswith("g"):
                return "Emerald"
    return "Unknown"


def get_encounter_rates_from_json(data: Dict) -> Dict[str, List[int]]:
    """
    Extract encounter rates from the JSON header instead of hardcoding.
    """
    rates = {}
    for group in data.get("wild_encounter_groups", []):
        if not group.get("for_maps", False):
            continue
        for field in group.get("fields", []):
            field_type = field.get("type", "")
            enc_rates = field.get("encounter_rates", [])
            if enc_rates:
                rates[field_type] = enc_rates
            # Also grab fishing groups if present
            if "groups" in field:
                rates["fishing_groups"] = field["groups"]
    return rates


def process_encounters(data: Dict, lucky_egg: bool = False, game_filter: str = None) -> Dict[str, Dict]:
    """
    Process wild encounter data and calculate expected EXP for each location.
    
    Args:
        data: The loaded JSON data
        lucky_egg: Whether to apply Lucky Egg bonus
        game_filter: Optional filter - "Ruby", "Sapphire", "Emerald", or None for all
    """
    results = defaultdict(lambda: defaultdict(dict))
    
    # Detect game and get rates from JSON
    detected_game = detect_game_version(data)
    json_rates = get_encounter_rates_from_json(data)
    
    # Use rates from JSON if available, otherwise fall back to hardcoded
    land_rates = json_rates.get("land_mons", LAND_ENCOUNTER_RATES)
    water_rates = json_rates.get("water_mons", WATER_ENCOUNTER_RATES)
    rock_rates = json_rates.get("rock_smash_mons", ROCK_SMASH_ENCOUNTER_RATES)
    fish_rates = json_rates.get("fishing_mons", FISHING_ENCOUNTER_RATES)
    fish_groups = json_rates.get("fishing_groups", FISHING_GROUPS)
    
    for group in data.get("wild_encounter_groups", []):
        if not group.get("for_maps", False):
            continue
        
        for encounter in group.get("encounters", []):
            map_name = encounter.get("map", "Unknown")
            base_label = encounter.get("base_label", "")
            
            # Determine version from base_label
            if "_Ruby" in base_label:
                version = "Ruby"
            elif "_Sapphire" in base_label:
                version = "Sapphire"
            elif detected_game == "Emerald":
                version = "Emerald"
            else:
                version = "Unknown"
            
            # Apply game filter if specified
            if game_filter and version != game_filter:
                continue
            
            location_key = f"{map_name}_{version}"
            formatted_name = format_map_name(map_name)
            
            results[location_key]["map_name"] = map_name
            results[location_key]["formatted_name"] = formatted_name
            results[location_key]["version"] = version
            
            # Process each encounter type
            encounter_types = [
                ("land_mons", "grass", land_rates, None),
                ("water_mons", "surfing", water_rates, None),
                ("rock_smash_mons", "rock_smash", rock_rates, None),
            ]
            
            for data_key, result_key, rates, indices in encounter_types:
                if data_key in encounter:
                    mon_data = encounter[data_key]
                    mons = mon_data.get("mons", [])
                    if mons:
                        exp, breakdown = calculate_encounter_type_expected_exp(
                            mons, rates, indices, lucky_egg
                        )
                        enc_rate = mon_data.get("encounter_rate", 0)
                        efficiency = calculate_efficiency_score(exp, enc_rate)
                        results[location_key][result_key] = {
                            "expected_exp": exp,
                            "breakdown": breakdown,
                            "encounter_rate": enc_rate,
                            "efficiency": efficiency
                        }
            
            # Process fishing (separate by rod)
            if "fishing_mons" in encounter:
                fish_data = encounter["fishing_mons"]
                mons = fish_data.get("mons", [])
                enc_rate = fish_data.get("encounter_rate", 0)
                
                for rod_name, rod_indices in fish_groups.items():
                    if len(mons) > max(rod_indices):
                        exp, breakdown = calculate_encounter_type_expected_exp(
                            mons, fish_rates, rod_indices, lucky_egg
                        )
                        efficiency = calculate_efficiency_score(exp, enc_rate)
                        results[location_key][f"fishing_{rod_name}"] = {
                            "expected_exp": exp,
                            "breakdown": breakdown,
                            "encounter_rate": enc_rate,
                            "efficiency": efficiency
                        }
    
    return dict(results)


# =============================================================================
# OUTPUT GENERATION
# =============================================================================

def generate_report(results: Dict[str, Dict], verbose: bool = False, lucky_egg: bool = False, game: str = None) -> str:
    """Generate a formatted report of expected EXP by location."""
    lines = []
    egg_str = " (WITH LUCKY EGG)" if lucky_egg else ""
    game_str = f" - {game}" if game else ""
    lines.append("=" * 80)
    lines.append(f"POKEMON GEN 3 EXPECTED EXP PER BATTLE BY LOCATION{egg_str}{game_str}")
    lines.append("Using proper integer math (floor after each operation)")
    lines.append("=" * 80)
    lines.append("")
    
    by_version = defaultdict(list)
    for key, data in results.items():
        version = data.get("version", "Unknown")
        by_version[version].append((key, data))
    
    for version in ["Ruby", "Sapphire", "Emerald", "Unknown"]:
        if version not in by_version:
            continue
            
        lines.append(f"\n{'='*40}")
        lines.append(f"  {version.upper()} VERSION")
        lines.append(f"{'='*40}\n")
        
        locations = sorted(by_version[version], key=lambda x: x[1].get("formatted_name", ""))
        
        for key, data in locations:
            formatted_name = data.get("formatted_name", key)
            
            encounter_types = []
            for etype in ["grass", "surfing", "rock_smash", "fishing_old_rod", 
                          "fishing_good_rod", "fishing_super_rod"]:
                if etype in data:
                    encounter_types.append(etype)
            
            if not encounter_types:
                continue
            
            lines.append(f"\n{formatted_name}")
            lines.append("-" * len(formatted_name))
            
            for etype in encounter_types:
                edata = data[etype]
                exp = edata["expected_exp"]
                eff = edata.get("efficiency", 0)
                enc_rate = edata.get("encounter_rate", 0)
                
                etype_display = etype.replace("_", " ").title().replace("Fishing ", "Fishing: ")
                
                lines.append(f"  {etype_display:25s} | EXP: {exp:7.1f} | Rate: {enc_rate:2d}/16 | Eff: {eff:7.1f}")
                
                if verbose:
                    lines.append(f"    {'Species':15s} | {'Lvl':9s} | {'Prob':6s} | {'EXP':6s} | {'Contrib':7s}")
                    lines.append(f"    {'-'*55}")
                    for slot in edata["breakdown"]:
                        species = slot["species"]
                        level_str = f"{slot['min_level']}-{slot['max_level']}"
                        prob = f"{slot['probability']*100:.1f}%"
                        exp_str = f"{slot['expected_exp']:.1f}"
                        contrib = f"{slot['contribution']:.2f}"
                        lines.append(f"    {species:15s} | {level_str:9s} | {prob:6s} | {exp_str:6s} | {contrib:7s}")
                    lines.append("")
    
    return "\n".join(lines)


def generate_csv(results: Dict[str, Dict]) -> str:
    """Generate CSV output."""
    lines = []
    lines.append("Location,Version,Encounter Type,Expected EXP,Encounter Rate,Efficiency Score")
    
    for key, data in sorted(results.items()):
        formatted_name = data.get("formatted_name", key)
        version = data.get("version", "Unknown")
        
        for etype in ["grass", "surfing", "rock_smash", "fishing_old_rod", 
                      "fishing_good_rod", "fishing_super_rod"]:
            if etype in data:
                edata = data[etype]
                exp = edata["expected_exp"]
                rate = edata.get("encounter_rate", 0)
                eff = edata.get("efficiency", 0)
                etype_display = etype.replace("_", " ").title()
                lines.append(f'"{formatted_name}",{version},{etype_display},{exp:.2f},{rate},{eff:.2f}')
    
    return "\n".join(lines)


def generate_efficiency_summary(results: Dict[str, Dict]) -> str:
    """Generate summary sorted by efficiency score."""
    lines = []
    lines.append("\n" + "=" * 80)
    lines.append("TOP GRINDING LOCATIONS BY EFFICIENCY SCORE")
    lines.append("Efficiency = Expected EXP × (Encounter Rate / 16)")
    lines.append("=" * 80)
    
    for etype in ["grass", "surfing", "rock_smash", "fishing_old_rod", 
                  "fishing_good_rod", "fishing_super_rod"]:
        
        locations = []
        for key, data in results.items():
            if etype in data:
                locations.append({
                    "name": data.get("formatted_name", key),
                    "version": data.get("version", "Unknown"),
                    "exp": data[etype]["expected_exp"],
                    "rate": data[etype].get("encounter_rate", 0),
                    "efficiency": data[etype].get("efficiency", 0)
                })
        
        if not locations:
            continue
        
        # Sort by efficiency
        locations.sort(key=lambda x: x["efficiency"], reverse=True)
        
        etype_display = etype.replace("_", " ").title()
        lines.append(f"\n{etype_display}")
        lines.append("-" * 60)
        lines.append(f"  {'#':>2s}  {'Location':30s} {'Ver':8s} {'EXP':>7s} {'Rate':>4s} {'Eff':>8s}")
        
        for i, loc in enumerate(locations[:15], 1):
            lines.append(f"  {i:2d}. {loc['name']:30s} {loc['version']:8s} {loc['exp']:7.1f} {loc['rate']:4d} {loc['efficiency']:8.1f}")
    
    return "\n".join(lines)


def clear_screen():
    """Clear terminal screen."""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def pause():
    """Wait for user to press Enter."""
    input("\nPress Enter to continue...")


def select_json_file() -> str:
    """Let user select or enter a JSON file path."""
    import os
    
    # Look for JSON files in current directory and common locations
    json_files = []
    search_paths = [
        '.', 
        './data', 
        '../data', 
        os.path.expanduser('~'),
        '/mnt/user-data/uploads',  # Claude uploads directory
    ]
    
    for path in search_paths:
        if os.path.exists(path):
            try:
                for f in os.listdir(path):
                    if f.endswith('.json') and ('encounter' in f.lower() or 'wild' in f.lower()):
                        full_path = os.path.join(path, f)
                        if full_path not in json_files:
                            json_files.append(full_path)
            except PermissionError:
                pass
    
    print("\n" + "=" * 50)
    print("SELECT ENCOUNTER FILE")
    print("=" * 50)
    
    if json_files:
        print("\nFound encounter files:")
        for i, f in enumerate(json_files, 1):
            print(f"  {i}. {f}")
        print(f"  {len(json_files) + 1}. Enter custom path")
        
        choice = input("\nSelect option: ").strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(json_files):
                return json_files[idx]
        except ValueError:
            pass
    
    # Custom path
    return input("Enter path to wild_encounters.json: ").strip()


def select_game_version(data: Dict) -> Optional[str]:
    """Let user select game version filter for RS files."""
    detected = detect_game_version(data)
    
    if detected == "Emerald":
        print(f"\nDetected: Emerald (no version filter needed)")
        return None
    
    print("\n" + "-" * 40)
    print("GAME VERSION FILTER")
    print("-" * 40)
    print(f"Detected: {detected} combined file")
    print("\n  1. Show all versions")
    print("  2. Ruby only")
    print("  3. Sapphire only")
    
    choice = input("\nSelect option [1]: ").strip() or "1"
    
    if choice == "2":
        return "Ruby"
    elif choice == "3":
        return "Sapphire"
    return None


def settings_menu(settings: Dict) -> Dict:
    """Configure settings like Lucky Egg."""
    while True:
        clear_screen()
        print("=" * 50)
        print("SETTINGS")
        print("=" * 50)
        print(f"\n  1. Lucky Egg: {'ON' if settings['lucky_egg'] else 'OFF'}")
        print(f"  2. Verbose output: {'ON' if settings['verbose'] else 'OFF'}")
        print("\n  0. Back to main menu")
        
        choice = input("\nToggle setting: ").strip()
        
        if choice == "1":
            settings['lucky_egg'] = not settings['lucky_egg']
        elif choice == "2":
            settings['verbose'] = not settings['verbose']
        elif choice == "0":
            break
    
    return settings


def view_location_report(results: Dict, settings: Dict, game_label: str):
    """View the full location report."""
    clear_screen()
    output = generate_report(results, settings['verbose'], settings['lucky_egg'], game_label)
    print(output)
    pause()


def view_efficiency_rankings(results: Dict):
    """View efficiency-sorted rankings."""
    clear_screen()
    output = generate_efficiency_summary(results)
    print(output)
    pause()


def search_location(results: Dict, settings: Dict):
    """Search for a specific location."""
    clear_screen()
    print("=" * 50)
    print("SEARCH LOCATION")
    print("=" * 50)
    
    query = input("\nEnter location name (partial match OK): ").strip().lower()
    
    found = []
    for key, data in results.items():
        if query in data.get("formatted_name", "").lower():
            found.append((key, data))
    
    if not found:
        print("\nNo locations found.")
        pause()
        return
    
    print(f"\nFound {len(found)} location(s):\n")
    
    for key, data in found:
        name = data.get("formatted_name", key)
        version = data.get("version", "")
        print(f"\n{name} ({version})")
        print("-" * 40)
        
        for etype in ["grass", "surfing", "rock_smash", "fishing_old_rod", 
                      "fishing_good_rod", "fishing_super_rod"]:
            if etype in data:
                edata = data[etype]
                exp = edata["expected_exp"]
                eff = edata.get("efficiency", 0)
                rate = edata.get("encounter_rate", 0)
                etype_display = etype.replace("_", " ").title()
                print(f"  {etype_display:25s} | EXP: {exp:7.1f} | Rate: {rate:2d} | Eff: {eff:7.1f}")
    
    pause()


def battle_calculator_menu(results: Dict, settings: Dict):
    """Battle calculator to determine battles needed for leveling."""
    clear_screen()
    print("=" * 60)
    print("BATTLE CALCULATOR - How many battles to level up?")
    print("=" * 60)
    
    # Get Pokemon info
    species_input = input("\nPokemon species (e.g., MUDKIP or mudkip): ").strip().upper()
    if not species_input.startswith("SPECIES_"):
        species_input = f"SPECIES_{species_input}"
    
    if species_input not in SPECIES_GROWTH_RATE:
        print(f"Warning: Unknown species {species_input}, using medium_fast growth rate")
        growth_rate = "medium_fast"
    else:
        growth_rate = SPECIES_GROWTH_RATE[species_input]
        print(f"Growth rate: {growth_rate}")
    
    try:
        current_level = int(input("Current level: "))
        current_exp = int(input("Current total EXP (from summary screen): "))
        target_level = int(input("Target level: "))
    except ValueError:
        print("Invalid input!")
        pause()
        return
    
    # Calculate EXP needed
    exp_needed = get_exp_needed(species_input, current_level, current_exp, target_level)
    print(f"\nEXP needed to reach level {target_level}: {exp_needed:,}")
    
    # Get location
    print("\n" + "-" * 40)
    print("Select grinding location")
    print("-" * 40)
    
    # Collect locations with encounters
    all_locations = []
    for key, data in results.items():
        for etype in ["grass", "surfing", "rock_smash", "fishing_old_rod", 
                      "fishing_good_rod", "fishing_super_rod"]:
            if etype in data:
                all_locations.append({
                    "key": key,
                    "data": data,
                    "etype": etype,
                    "exp": data[etype]["expected_exp"],
                    "eff": data[etype].get("efficiency", 0)
                })
    
    # Sort by efficiency
    all_locations.sort(key=lambda x: x["eff"], reverse=True)
    
    print("\nTop 15 locations by efficiency:")
    for i, loc in enumerate(all_locations[:15], 1):
        name = loc["data"].get("formatted_name", "")
        etype = loc["etype"].replace("_", " ")
        print(f"  {i:2d}. {name:25s} ({etype:15s}) - {loc['exp']:.1f} EXP, Eff: {loc['eff']:.1f}")
    
    print("\n  Or enter a location name to search")
    
    loc_input = input("\nSelect number or search: ").strip()
    
    selected = None
    try:
        idx = int(loc_input) - 1
        if 0 <= idx < len(all_locations[:15]):
            selected = all_locations[idx]
    except ValueError:
        # Search by name
        loc_input_lower = loc_input.lower()
        for loc in all_locations:
            if loc_input_lower in loc["data"].get("formatted_name", "").lower():
                selected = loc
                break
    
    if not selected:
        print("Location not found!")
        pause()
        return
    
    expected_exp = selected["exp"]
    lucky_egg = settings['lucky_egg']
    
    # Recalculate with lucky egg if enabled (need to reprocess)
    if lucky_egg:
        # Get the raw encounter data and recalculate
        etype = selected["etype"]
        edata = selected["data"][etype]
        # The expected_exp in results was already calculated with/without lucky egg
        # based on settings, so we can use it directly
        pass
    
    # Calculate battles
    battles = calculate_battles_needed(exp_needed, expected_exp, lucky_egg)
    
    print(f"\n{'=' * 50}")
    print(f"RESULTS")
    print(f"{'=' * 50}")
    print(f"Pokemon: {species_input.replace('SPECIES_', '')}")
    print(f"Current: Level {current_level} ({current_exp:,} EXP)")
    print(f"Target:  Level {target_level} ({get_total_exp_for_level(species_input, target_level):,} EXP)")
    print(f"EXP Needed: {exp_needed:,}")
    print(f"")
    print(f"Location: {selected['data']['formatted_name']} ({selected['etype'].replace('_', ' ')})")
    print(f"Expected EXP/battle: {expected_exp:.1f}")
    print(f"Lucky Egg: {'Yes' if lucky_egg else 'No'}")
    print(f"")
    print(f">>> Estimated battles needed: {battles:,} <<<")
    
    pause()


def export_menu(results: Dict, settings: Dict, game_label: str):
    """Export data to file."""
    clear_screen()
    print("=" * 50)
    print("EXPORT DATA")
    print("=" * 50)
    print("\n  1. Full report (text)")
    print("  2. Full report + efficiency rankings (text)")
    print("  3. CSV format")
    print("\n  0. Cancel")
    
    choice = input("\nSelect format: ").strip()
    
    if choice == "0":
        return
    
    filename = input("Output filename: ").strip()
    if not filename:
        print("Cancelled.")
        pause()
        return
    
    if choice == "1":
        output = generate_report(results, settings['verbose'], settings['lucky_egg'], game_label)
    elif choice == "2":
        output = generate_report(results, settings['verbose'], settings['lucky_egg'], game_label)
        output += generate_efficiency_summary(results)
    elif choice == "3":
        output = generate_csv(results)
        if not filename.endswith('.csv'):
            filename += '.csv'
    else:
        print("Invalid choice.")
        pause()
        return
    
    try:
        with open(filename, 'w') as f:
            f.write(output)
        print(f"\nExported to: {filename}")
    except Exception as e:
        print(f"\nError writing file: {e}")
    
    pause()


def main_menu():
    """Main interactive menu."""
    clear_screen()
    print("=" * 60)
    print("  POKEMON GEN 3 EXP CALCULATOR")
    print("  Using proper integer math (floor after each operation)")
    print("=" * 60)
    
    # Select JSON file
    json_path = select_json_file()
    
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        print(f"\nLoaded: {json_path}")
    except FileNotFoundError:
        print(f"\nError: File not found: {json_path}")
        pause()
        return
    except json.JSONDecodeError:
        print(f"\nError: Invalid JSON file")
        pause()
        return
    
    # Select game version
    game_filter = select_game_version(data)
    detected_game = detect_game_version(data)
    game_label = game_filter if game_filter else detected_game
    
    # Settings
    settings = {
        'lucky_egg': False,
        'verbose': False
    }
    
    # Process initial data
    results = process_encounters(data, settings['lucky_egg'], game_filter)
    
    # Main loop
    while True:
        clear_screen()
        egg_status = " [Lucky Egg ON]" if settings['lucky_egg'] else ""
        print("=" * 60)
        print(f"  GEN 3 EXP CALCULATOR - {game_label}{egg_status}")
        print("=" * 60)
        print(f"\n  Loaded: {json_path}")
        print(f"  Locations: {len(results)}")
        
        print("\n  --- REPORTS ---")
        print("  1. View all locations")
        print("  2. View efficiency rankings")
        print("  3. Search location")
        
        print("\n  --- TOOLS ---")
        print("  4. Battle calculator (battles to level up)")
        print("  5. Export to file")
        
        print("\n  --- OPTIONS ---")
        print("  6. Settings (Lucky Egg, verbose)")
        print("  7. Change game file")
        
        print("\n  0. Exit")
        
        choice = input("\nSelect option: ").strip()
        
        if choice == "1":
            view_location_report(results, settings, game_label)
        elif choice == "2":
            view_efficiency_rankings(results)
        elif choice == "3":
            search_location(results, settings)
        elif choice == "4":
            # Reprocess with current lucky egg setting
            results = process_encounters(data, settings['lucky_egg'], game_filter)
            battle_calculator_menu(results, settings)
        elif choice == "5":
            export_menu(results, settings, game_label)
        elif choice == "6":
            old_lucky = settings['lucky_egg']
            settings = settings_menu(settings)
            # Reprocess if lucky egg changed
            if settings['lucky_egg'] != old_lucky:
                results = process_encounters(data, settings['lucky_egg'], game_filter)
        elif choice == "7":
            # Restart with new file
            main_menu()
            return
        elif choice == "0":
            clear_screen()
            print("Thanks for using the Gen 3 EXP Calculator!")
            break


def main():
    """Entry point."""
    main_menu()


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()