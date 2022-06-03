import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/dpkubeck/BotBuddy/BotBuddy/big-genre-352220-1c4943dd91f7.json"

from google.cloud import texttospeech
import playsound

# Instantiates a client
client = texttospeech.TextToSpeechClient()

# Set the text input to be synthesized
synthesis_input = texttospeech.types.SynthesisInput(text="Do no evil!")

# Build the voice request, select the language code ("en-US") 
# ****** the NAME
# and the ssml voice gender ("neutral")
voice = texttospeech.types.VoiceSelectionParams(
    language_code='en-US',
    name='en-US-Wavenet-C',
    ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

# Select the type of audio file you want returned
audio_config = texttospeech.types.AudioConfig(
    audio_encoding=texttospeech.enums.AudioEncoding.MP3)

# Perform the text-to-speech request on the text input with the selected
# voice parameters and audio file type
response = client.synthesize_speech(synthesis_input, voice, audio_config)

# The response's audio_content is binary.
##with open('output.mp3', 'wb') as out:
    # Write the response to the output file.
##    out.write(response.audio_content)
##    print('Audio content written to file "output.mp3"')
    
playsound.playsound(response.audio_content)