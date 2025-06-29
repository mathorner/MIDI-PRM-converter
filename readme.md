# MIDI to Roland T-8 PRM Converter

This Python script batch-converts Playbeat-style MIDI rhythm files into `.PRM` pattern files compatible with the Roland T-8 drum machine.

Each `.mid` file is translated into a 32-step pattern file using a fixed voice mapping and exported into bank folders using the Roland T-8's naming convention.

---

## Features

- Converts all `.mid` files in a `files/` folder
- Outputs up to 4 banks (`PTN_BANK01` to `PTN_BANK04`)
- Each bank holds up to 16 files named like `T8_RHYTHM_PTN01_01.PRM`
- Voice mapping:
  - `C1` → BD (Kick)
  - `D1` → SD (Snare)
  - `G#1` → CH (Closed Hi-Hat)
  - `A#1` → OH (Open Hi-Hat)
  - `A1` → LT (Low Tom)
  - `C2` → HT (High Tom)
- MIDI velocity is mapped to PRM-style 1–9, A (max) levels
- Outputs properly formatted `.PRM` files with full header and step blocks

---

## Requirements

- Python 3.7+
- `mido` library

Install the dependency:
```bash
pip install mido

## folder structure

project-folder/
├── batch_midi_to_t8_prm.py
├── files/              # Put your .mid files here
│   ├── pattern1.mid
│   ├── pattern2.mid
│   └── ...

## How to Use

1.	Place all your .mid files in the files/ folder
2.	Run the script: python3 batch_midi_to_t8_prm.py
3.	The script will generate up to 4 output folders:
PTN_BANK01/
  ├── T8_RHYTHM_PTN01_01.PRM
  ├── T8_RHYTHM_PTN01_02.PRM
  └── ...
4. copy the output folders to your T-8 using the restore instructions here: https://static.roland.com/manuals/T-8_manual_v102/eng/28312320.html