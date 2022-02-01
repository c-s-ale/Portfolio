from flask import request, render_template, redirect
from flask import current_app as app
import os

from .inference import convert_to_transcription, WakeWord

@app.route('/', methods=['GET', 'POST'])
def index():
    if os.path.isfile("./tmp/wakeword.txt"):
        with open('./tmp/wakeword.txt', 'r') as f:
            wakeword_from_text = f.read()
        wakeword = WakeWord(wakeword_from_text)
        set_wake = False
    else:
        wakeword = WakeWord()
    
    default_wake = False
    command = ""
    does_not_contain_string = ""
    wakeword_string = ""
    default_wake_word = 'turtle'

    if request.method == "POST":
        print("FORM DATA RECEIVED")
        print(os.getcwd())

        if "audio_file" not in request.files:
            return redirect(request.url)

        file = request.files["audio_file"]

        if file.filename == "":
            return redirect(request.url)

        if "wake_file" in request.files:
            wake_file = request.files["wake_file"]
            if wake_file.filename == "":
                set_wake = False
            else:
                new_wake_word = convert_to_transcription(wake_file)
                wakeword.set_wakeword(new_wake_word[0])
                if os.path.isfile("./tmp/wakeword.txt"):
                    os.remove("./tmp/wakeword.txt")
                f = open("./tmp/wakeword.txt", "w")
                with open("./tmp/wakeword.txt", "w") as f:
                    f.write(new_wake_word[0])
                set_wake = True

        if wakeword.get_wakeword() == "":
            wakeword.set_wakeword(default_wake_word)
            default_wake = True
            new_wake_word = [default_wake_word]
            
        if file:
            command, wakeword_string, does_not_contain_string = wakeword.detect_wakeword_and_command(convert_to_transcription(file))

    return render_template('index.html', 
                            command=command, 
                            wakeword_string = wakeword_string, 
                            does_not_contain_string = does_not_contain_string, 
                            set_wake = set_wake,
                            wake_word_string = wakeword.get_wakeword(),
                            default_wake = default_wake)