import numpy as np
import pretty_midi
import random

GENRES = {
    "pop": {
        "notes": list(range(60, 72)),  
        "instruments": [0, 25] 
    },
    "rap": {
        "notes": list(range(50, 65)),  
        "instruments": [118, 32]  
    },
    "classical": {
        "notes": list(range(55, 80)), 
        "instruments": [0, 40]  
    },
    "jazz": {
        "notes": list(range(57, 75)), 
        "instruments": [0, 64] 
    },
    "rock": {
        "notes": list(range(52, 68)), 
        "instruments": [25, 30] 
    }
}

def get_user_genre():
    
    print("Available genres: Pop, Rap, Classical, Jazz, Rock")
    genre = input("Enter your preferred genre: ").strip().lower()
    return GENRES.get(genre, GENRES["pop"]) 

def generate_random_melody(length=None, genre_data=None):
   
    if genre_data is None:
        genre_data = GENRES["pop"] 
    
    if length is None:
        length = random.randint(16, 32) 
    
    notes = genre_data["notes"]
    instruments = genre_data["instruments"]
    
    return [(random.choice(notes), random.choice(instruments)) for _ in range(length)]

def save_melody_to_midi(melody, filename="music.mid"):
    """Convert melody into a MIDI file"""
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
    print(f"🎶 Music saved as {filename}")

def fitness_function(melody):
    """Improved fitness function: reward smooth transitions & note variety."""
    unique_notes = len(set([n for n, _ in melody]))
    smoothness = sum(abs(melody[i][0] - melody[i+1][0]) for i in range(len(melody)-1))
    return unique_notes - (smoothness / len(melody)) 

def crossover(melody1, melody2):
    """Crossover: Combine two melodies at a random point."""
    split = random.randint(4, len(melody1) - 4)  
    return melody1[:split] + melody2[split:]

def mutate(melody, mutation_rate=0.5, genre_data=None):
    """Mutation: Randomly change notes or instruments."""
    if genre_data is None:
        genre_data = GENRES["pop"]  
    
    for i in range(len(melody)):
        if random.random() < mutation_rate:  
            melody[i] = (random.choice(genre_data["notes"]), random.choice(genre_data["instruments"]))
    return melody

def evolve_melodies(population_size=10, generations=5):
    """Genetic Algorithm: Evolve the best melody."""
    genre_data = get_user_genre()  
    population = [generate_random_melody(genre_data=genre_data) for _ in range(population_size)]
    random.shuffle(population)  

    for generation in range(generations):
        fitness_scores = [fitness_function(m) for m in population]
        sorted_population = [x for _, x in sorted(zip(fitness_scores, population), key=lambda pair: pair[0], reverse=True)]

        top_half = sorted_population[: len(sorted_population) // 2]
        new_population = top_half[:]
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(top_half, 2)
            child = crossover(parent1, parent2)
            child = mutate(child, genre_data=genre_data)
            new_population.append(child)

        population = new_population
        print(f"🎵 Generation {generation+1} Best Fitness: {max(fitness_scores)}")

    best_melody = sorted_population[0]
    save_melody_to_midi(best_melody, "best_music.mid")
    print("🎶 Best evolved music saved as best_music.mid")


evolve_melodies()
