import mido
import os
import random

def generate_full_bb_lick(output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    mid = mido.MidiFile(ticks_per_beat=480)
    track = mido.MidiTrack()
    mid.tracks.append(track)

    # 1. Pitch Definition (B.B. Box in G)
    # 67=G, 70=Bb, 72=C, 74=D
    # (Pitch, Duration, Velocity, CC1_Vibrato, Time_Offset)
    events = [
        (69, 120, 90, 0, 0),    # A (10th fret B) - The Slide start
        (71, 360, 110, 20, 10), # B (12th fret B) - The Slide target (Sting!)
        (67, 240, 95, 0, 5),    # G (12th fret G)
        (69, 120, 85, 0, 0),    # A (10th fret B) - Hammer-on start
        (71, 360, 105, 40, 5),  # B (12th fret B) - Hammer-on target
        (74, 960, 120, 95, 15)  # D (10th fret E) - THE BIG STING + VIBRATO
    ]

    print(f"Generating full phrase to: {output_path}")

    for pitch, duration, vel, vib_max, offset in events:
        # Subtle 'Human' delay
        start_delay = offset + random.randint(0, 10)
        
        # Note On
        track.append(mido.Message('note_on', note=pitch, velocity=vel, time=start_delay))
        
        # If the note has vibrato (CC#1), we 'bloom' it
        if vib_max > 0:
            # B.B. lets the note breathe before shaking it
            breathe_time = duration // 3
            for v in range(0, vib_max, 15):
                track.append(mido.Message('control_change', control=1, value=v, time=breathe_time // 4))
            
            track.append(mido.Message('note_off', note=pitch, velocity=0, time=duration // 2))
            # Reset vibrato immediately
            track.append(mido.Message('control_change', control=1, value=0, time=0))
        else:
            track.append(mido.Message('note_off', note=pitch, velocity=0, time=duration))

    mid.save(output_path)
    print("MIDI Exported. Recommended player: signalmidi.app")

if __name__ == "__main__":
    generate_full_bb_lick(r"D:\audio-tools\test\bb_king_full_phrase.mid")