# Oak Optimizer

A Pokemon EXP calculator that helps you find the best grinding spots and calculate how many battles you need to level up.

Built for Professor Oak Challenge runs and anyone who wants to grind efficiently.

## Features

- **Expected EXP per battle** for every location, broken down by encounter type (grass, surfing, rock smash, fishing)
- **Efficiency rankings** that factor in encounter rates, not just raw EXP
- **Battle calculator** - tells you exactly how many battles to reach your target level
- **Lucky Egg support** with accurate 1.5× multiplier math
- **Game-accurate integer math** - floors after every operation, matching the actual Gen 3 engine

## Supported Games

| Game | File | Versions |
|------|------|----------|
| Ruby/Sapphire | `rs_wild_encounters.json` | Ruby, Sapphire |
| Emerald | `emerald_wild_encounters.json` | Emerald |
| FireRed/LeafGreen | `frlg_wild_encounters.json` | FireRed, LeafGreen |

## Installation

**Requirements:** Python 3.6+

No external dependencies - just clone and run:

```bash
git clone https://github.com/yourusername/Oak_Optimizer.git
cd Oak_Optimizer
python Exp_Calc.py
```

## Folder Structure

```
Oak_Optimizer/
├── Exp_Calc.py              # Main script
├── README.md
├── LICENSE
├── Sample CSVs/             # Pre-generated CSV outputs
│   ├── Emerald_Exp_Rates.csv
│   ├── RS_ExpRates.csv
│   └── FRLG_Exp_Rates.csv
└── Wild_Encounters/         # Encounter data from decomp projects
    ├── Gen1/                # (future)
    ├── Gen2/                # (future)
    └── Gen3/
        ├── emerald_wild_encounters.json
        ├── rs_wild_encounters.json
        └── frlg_wild_encounters.json
```

## Usage

Run the script and follow the interactive menus:

```bash
python Exp_Calc.py
```

### Menu Flow

#### 1. Select Encounter File

The tool auto-discovers JSON files in `Wild_Encounters/Gen*/`:

```
==================================================
SELECT ENCOUNTER FILE
==================================================

Found encounter files:
  1. Gen3/emerald_wild_encounters.json
  2. Gen3/rs_wild_encounters.json
  3. Gen3/frlg_wild_encounters.json
  4. Enter custom path

Select option:
```

#### 2. Select Game Version (if applicable)

For combined files (RS, FRLG), you can filter to a specific version:

```
----------------------------------------
GAME VERSION FILTER
----------------------------------------
Detected: FRLG combined file

  1. Show all versions
  2. FireRed only
  3. LeafGreen only

Select option [1]:
```

#### 3. Main Menu

```
============================================================
  GEN 3 EXP CALCULATOR - Emerald
============================================================

  Loaded: ./Wild_Encounters/Gen3/emerald_wild_encounters.json
  Locations: 156

  --- REPORTS ---
  1. View all locations
  2. View efficiency rankings
  3. Search location

  --- TOOLS ---
  4. Battle calculator (battles to level up)
  5. Export to file

  --- OPTIONS ---
  6. Settings (Lucky Egg, verbose)
  7. Change game file

  0. Exit

Select option:
```

### Menu Options Explained

#### 1. View All Locations
Shows every location with EXP per battle, encounter rate, and efficiency score:

```
Route 119
---------
  Grass                     | EXP:   189.4 | Rate: 20/16 | Eff:   236.7
  Surfing                   | EXP:   276.0 | Rate:  4/16 | Eff:    69.0
  Fishing: Old Rod          | EXP:    48.5 | Rate: 30/16 | Eff:    90.9
  Fishing: Good Rod         | EXP:   172.2 | Rate: 30/16 | Eff:   322.9
  Fishing: Super Rod        | EXP:   421.7 | Rate: 30/16 | Eff:   790.7
```

#### 2. View Efficiency Rankings
Shows the top 15 locations per encounter type, sorted by efficiency:

```
Grass
------------------------------------------------------------
   #  Location                       Ver          EXP Rate      Eff
   1. Sky Pillar 5F                  Emerald   1212.1   10    757.6
   2. Sky Pillar 3F                  Emerald   1140.5   10    712.8
```

#### 3. Search Location
Find a specific location by name (partial match supported):

```
Enter location name (partial match OK): victory

Found 3 location(s):

Victory Road 1F (Emerald)
----------------------------------------
  Grass                     | EXP:   754.9 | Rate: 10 | Eff:   472.2
```

#### 4. Battle Calculator
Calculate how many battles you need to reach a target level:

```
==================================================
BATTLE CALCULATOR - How many battles to level up?
==================================================

Pokemon species (e.g., MUDKIP or mudkip): mudkip
Growth rate: medium_slow
Current level: 10
Current total EXP (from summary screen): 1000
Target level: 16

EXP needed to reach level 16: 1,535

Top 15 locations by efficiency:
   1. Sky Pillar 5F              (grass          ) - 1212.1 EXP, Eff: 757.6
   ...

Select number or search: 2

==================================================
RESULTS
==================================================
Pokemon: MUDKIP
Current: Level 10 (1,000 EXP)
Target:  Level 16 (2,535 EXP)
EXP Needed: 1,535

Location: ~~Safari Zone Northwest (grass)~~ (Not possible, fix later)
Expected EXP/battle: 465.1
Lucky Egg: No

>>> Estimated battles needed: 4 <<<
```

#### 5. Export to File
Export data in text or CSV format:

```
==================================================
EXPORT DATA
==================================================

  1. Full report (text)
  2. Full report + efficiency rankings (text)
  3. CSV format

  0. Cancel

Select format:
```

If a `Sample CSVs/` folder exists, exports default there.

#### 6. Settings
Toggle Lucky Egg (1.5× EXP) and verbose output:

```
==================================================
SETTINGS
==================================================

  1. Lucky Egg: OFF
  2. Verbose output: OFF

  0. Back to main menu

Toggle setting:
```

## CSV Output Format

| Column | Description |
|--------|-------------|
| Location | Map name (Route 101, Victory Road B1F, etc.) |
| Version | Ruby, Sapphire, Emerald, FireRed, or LeafGreen |
| Encounter Type | Grass, Surfing, Rock Smash, Fishing Old/Good/Super Rod |
| Expected EXP | Average EXP gained per battle |
| Encounter Rate | How often encounters trigger (higher = more frequent) |
| Efficiency Score | EXP × (Rate/16) - balances yield vs frequency |

## The Math

### EXP Formula
Gen 3 uses integer math with floor after each operation:

```
EXP = floor(base_exp × level / 7)
```

With Lucky Egg (1.5× applied as ×3 ÷2):
```
EXP = floor(floor(base_exp × level / 7) × 3 / 2)
```

### Expected Value
Each encounter slot has a probability from the game's data:

- **Grass (12 slots):** 20%, 20%, 10%, 10%, 10%, 10%, 5%, 5%, 4%, 4%, 1%, 1%
- **Surfing (5 slots):** 60%, 30%, 5%, 4%, 1%
- **Fishing:** Split by rod type with different slot distributions

For Pokemon with level ranges, EXP is calculated at each possible level and averaged.

### Efficiency Score
```
Efficiency = Expected EXP × (Encounter Rate / 16)
```

Higher encounter rate = more battles per minute = better grinding even if raw EXP is lower.

## Data Sources

Encounter data is from the pret decompilation projects:
- [pokeemerald](https://github.com/pret/pokeemerald)
- [pokeruby](https://github.com/pret/pokeruby) 
- [pokefirered](https://github.com/pret/pokefirered)

Files are located at `data/wild_encounters.json` in each repo.

## License

MIT License - see [LICENSE](LICENSE) file.

## Contributing

PRs welcome! Potential improvements:
- Gen 1/2 support (different EXP formulas)
- Gen 4+ support
- GUI version
