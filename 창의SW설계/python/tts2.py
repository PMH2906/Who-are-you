from gtts import gTTS 
import os 
tts=gTTS(text="lee se mi",lang="en") 
tts.save("both2.mp3") 
os.system("both2.mp3") 
