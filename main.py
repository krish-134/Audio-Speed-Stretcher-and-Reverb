import os

import soundfile as sf

from pydub import AudioSegment

import pyrubberband as prband

from pedalboard import Pedalboard
from pedalboard import Reverb
from pedalboard import Convolution
from pedalboard import PitchShift

print("Hi! Let's change the speed of your song! You can add reverb too!")

# Taking in initial song name and file type of audio
song_name = input("First, what is the name of your file? (exclude the file type):\n")
file_type = input("What is the file type? (i.e., .wav or .mp3, don't forget the '.') \n")

# Loop for taking in speed change value with alternage input cases
i = 0
while i < 1:
    
    # Value to change the speed of the song by
    change_tempo_by = float(input("In a percentage (with 100 being original) much would you like to change the speed of the song by?\n"))
    
    if (change_tempo_by == 100.0):
        print("That will not change the song's speed! Please enter a value less than or greater than 100.")
    elif (change_tempo_by == 0.0):
        print("You can't change the song to 0 percent speed!")
    elif (change_tempo_by != 100.0):
        i = 1
    else:
        print("Wrong type of input, please try again.")

# To determine label for new audio file
if change_tempo_by > 100:
    slow_or_fast = " sped-up"
elif change_tempo_by < 100:
    slow_or_fast = " slowed"
else:
    slow_or_fast = ""

# Convert song to wav if given mp3
if (file_type == ".mp3"):
    song_mp3 = AudioSegment.from_mp3('Audio/'+song_name+file_type)
    song_mp3.export('Audio/'+song_name+slow_or_fast+".wav", format="wav")
    file_type = ".wav"

# Establishing initial relative path for audio file storage in project
song_path = 'Audio/'+song_name+slow_or_fast+file_type

# Loop to put reverb on song and handle other cases
i = 0
while i < 1:     
    effect_song = input("Do you want to put an reverb effect? (y/n)\n")
    #Effects to put onto song
    if effect_song.lower() == "y":
        reverb = Pedalboard([
        Convolution(song_path, 0.10),
        Reverb(room_size=0.20, wet_level = .10, dry_level = .90), 
             
        ])
        i = 1
    elif effect_song.lower() == "n":
        print("Skipping reverb effect.")
        i = 1
    else:
        print("Sorry that was the wrong input, try again.")

print("This may take up to a few minutes... wait for a completion statement.")

# Reading data from song
audio, sample_rate = sf.read(song_path)

# Stretch the speed of the audio
tempo_shift = prband.time_stretch(audio, sample_rate, change_tempo_by/100.0)

# Write tempo change to new audio file
sf.write("Audio/"+song_name+slow_or_fast+".wav", tempo_shift, sample_rate, format = "wav")

# Take data from audio after time change
audio_2, sample_rate_2 = sf.read(song_path)

# Shift the pitch of audio higher if sped up
pitch_shift = prband.pitch_shift(audio_2, sample_rate_2, change_tempo_by/100.0)

# Write pitch change to new audio file
sf.write("Audio/"+song_name+slow_or_fast+".wav", pitch_shift, sample_rate_2, format = "wav")

# Take data from audio after pitch change
audio_3, sample_rate_3 = sf.read(song_path)

# Pitching the song manually if it is slowed down
if change_tempo_by < 100:
    pitch_song_by = -(100 - change_tempo_by)/10.0
    pitch = Pedalboard([
    PitchShift(semitones = pitch_song_by),
    ])

# Pushing song through effects and write song file into 'Audio' folder
if (effect_song == "y") and (change_tempo_by < 100):
    all_effects = reverb(pitch(audio_3, sample_rate_3), sample_rate_3) 
    sf.write(song_path, all_effects, sample_rate_3)

elif (effect_song == "n") and (change_tempo_by < 100):
    all_effects = pitch(audio_3, sample_rate_3)
    sf.write(song_path, all_effects, sample_rate_3)

elif (effect_song == "y"):    
    all_effects = reverb(audio_3, sample_rate_3)
    sf.write(song_path, all_effects, sample_rate_3)

# Export final mp3 version of song
final_wav = AudioSegment.from_wav(song_path)
final_wav.export("Audio/"+song_name+slow_or_fast+".mp3")

# Removes wav file that was created in process of applying changes, so mp3 file remains
os.remove(song_path)

print("Complete! Now open the song in the Audio folder of this project!")