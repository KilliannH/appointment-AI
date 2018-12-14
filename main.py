import signal
import snowboydecoder as snowboydecoder
import speech_recognition as sr  # Speech to text recognition
from Jarvis import Jarvis

jarvis = Jarvis()
interrupted = False

def audioRecorderCallback(fname):
    print("Snowdboy_engine : converting audio to text")
    r = sr.Recognizer()
    with sr.AudioFile(fname) as source:
        audio = r.record(source)  # read the entire audio file
    data = ""
    try:
        data = r.recognize_google(audio, language='fr-FR')
        print("You said: " + data)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        jarvis.speak("Je n'ai pas compris ce que tu as dit.")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        jarvis.speak("Je n'ai pas réussi à requêter Google, essaie encore !")

    return jarvis.think(data)


def detectedCallback():
    snowboydecoder.play_audio_file()

def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

model = 'jarvis.pmdl'

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.38)
print('Listening... Press Ctrl+C to exit')

# main loop
detector.start(detected_callback= detectedCallback,
               audio_recorder_callback= audioRecorderCallback,
               interrupt_check=interrupt_callback,
               sleep_time=0.01,
               silent_count_threshold=4)

# do not uncomment this line for keeping hotword detection loop
# detector.terminate()
