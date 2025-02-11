import streamlit as st
import numpy as np
import pretty_midi
import random
import os

# Define genre-based notes and instruments
GENRES = {
    "Pop": {
        "notes": list(range(60, 72)),
        "instruments": [0, 25]  # Piano, Guitar
    },
    "Rap": {
        "notes": list(range(50, 65)),
        "instruments": [118, 32]  # Drums, Bass
    },
    "Classical": {
        "notes": list(range(55, 80)),
        "instruments": [0, 40]  # Piano, Violin
    },
    "Jazz": {
        "notes": list(range(57, 75)),
        "instruments": [0, 64]  # Piano, Trumpet
    },
    "Rock": {
        "notes": list(range(52, 68)),
        "instruments": [25, 30]  # Electric Guitar, Distorted Guitar
    }
}

def generate_random_melody(length=32, genre_data=None):
    """Generate a melody based on genre."""
    if genre_data is None:
        genre_data = GENRES["Pop"]  # Default to Pop

    notes = genre_data["notes"]
    instruments = genre_data["instruments"]
    
    return [(random.choice(notes), random.choice(instruments)) for _ in range(length)]

def save_melody_to_midi(melody, filename="generated_music.mid"):
    """Convert melody into a MIDI file and save it."""
    midi = pretty_midi.PrettyMIDI()
    instrument_tracks = {}

    for note, instrument in melody:
        if instrument not in instrument_tracks:
            instrument_tracks[instrument] = pretty_midi.Instrument(program=instrument)
    
    start_time = 0
    for note, instrument in melody:
        midi_note = pretty_midi.Note(velocity=100, pitch=note, start=start_time, end=start_time + 0.5)
        instrument_tracks[instrument].notes.append(midi_note)
        start_time += 0.5

    for instrument in instrument_tracks.values():
        midi.instruments.append(instrument)

    midi.write(filename)
    return filename

# Streamlit UI
st.title("🎵 AI-Based Music Composer")
st.write("Select a genre and generate AI-composed music!")

# Genre selection
genre = st.selectbox("Choose a music genre:", list(GENRES.keys()))

if st.button("Generate Music"):
    st.write(f"Generating AI music for {genre}... 🎶")
    
    # Generate melody and save it as MIDI
    genre_data = GENRES[genre]
    melody = generate_random_melody(genre_data=genre_data)
    midi_file = save_melody_to_midi(melody)

    # Provide download link
    with open(midi_file, "rb") as file:
        st.download_button(label="🎼 Download AI-Generated Music", data=file, file_name=midi_file, mime="audio/midi")

    st.success("✅ AI-generated music is ready! Download and listen!")
