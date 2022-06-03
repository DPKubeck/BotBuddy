from polly import Polly

tts = Polly('Joanna')
tts.say('Hi there, I\'m very glad you\'re reading my article. Leave a comment if you find it useful.')
tts.saveToFile('Hi there, save the speech for later', 'joanna.mp3')