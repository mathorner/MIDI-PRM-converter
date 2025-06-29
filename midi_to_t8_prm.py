import os
import mido

INPUT_DIR = "files"
BANK_PREFIX = "PTN_BANK"
MAX_BANKS = 4
MAX_PATTERNS_PER_BANK = 16
TOTAL_STEPS = 32

NOTE_TO_LABEL = {
    36: 'BD',  # Kick - C1
    38: 'SD',  # Snare - D1
    44: 'CH',  # Closed HH - G#1
    46: 'OH',  # Open HH - A#1
    45: 'LT',  # Low Tom - A1
    48: 'HT',  # High Tom - C2
}

VOICE_ORDER = ['AC', 'BD', 'SD', 'LT', 'HT', 'CY', 'CH', 'OH']

def velocity_to_char(velocity):
    level = min((velocity - 1) // 13 + 1, 10)
    return hex(level)[2:].upper()

def convert_midi_to_prm(midi_path):
    mid = mido.MidiFile(midi_path)
    note_events = []
    for track in mid.tracks:
        abs_time = 0
        for msg in track:
            abs_time += msg.time
            if msg.type == 'note_on' and msg.velocity > 0 and msg.note in NOTE_TO_LABEL:
                note_events.append((abs_time, msg.note, msg.velocity))
    if not note_events:
        return None  # Skip empty files

    max_tick = max(tick for tick, _, _ in note_events)
    ticks_per_step = max_tick / TOTAL_STEPS

    steps = []
    for _ in range(TOTAL_STEPS):
        steps.append({label: '000AA' for label in VOICE_ORDER})

    for tick, note, velocity in note_events:
        step_index = min(int(tick / ticks_per_step), TOTAL_STEPS - 1)
        label = NOTE_TO_LABEL[note]
        velocity_char = velocity_to_char(velocity)
        steps[step_index][label] = f"1{velocity_char}0AA"

    return steps

def write_prm(steps, filepath):
    with open(filepath, "w") as f:
        f.write("LENGTH\t= 32\n")
        f.write("SCALE\t= 1\n")
        f.write("SHUFFLE\t= 0\n")
        f.write("FLAM\t= 36\n")
        for i, step in enumerate(steps, start=1):
            line = f"STEP {i}\t= " + " ".join(f"{label}={step[label]}" for label in VOICE_ORDER)
            f.write(line + "\n")

def main():
    midi_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".mid")]
    total_files = min(len(midi_files), MAX_BANKS * MAX_PATTERNS_PER_BANK)
    print(f"Found {len(midi_files)} MIDI files. Converting {total_files}...")

    for i in range(total_files):
        bank_index = i // MAX_PATTERNS_PER_BANK + 1
        file_index = i % MAX_PATTERNS_PER_BANK + 1

        if bank_index > MAX_BANKS:
            print("Reached maximum bank limit.")
            break

        bank_folder = f"{BANK_PREFIX}{bank_index:02}"
        os.makedirs(bank_folder, exist_ok=True)
        filename = f"T8_RHYTHM_PTN{bank_index:02}_{file_index:02}.PRM"
        midi_path = os.path.join(INPUT_DIR, midi_files[i])
        prm_path = os.path.join(bank_folder, filename)

        steps = convert_midi_to_prm(midi_path)
        if steps:
            write_prm(steps, prm_path)
            print(f"→ {filename}")
        else:
            print(f"Skipping {midi_files[i]} (no note data)")

    print("Done.")

if __name__ == "__main__":
    main()