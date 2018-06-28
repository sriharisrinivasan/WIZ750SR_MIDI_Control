import socket
import time
import Sys_Variables
import speech_recognition as sr
# This module is imported so that we can
# play the converted audio
import playsound


def speech_recognize():
    r = sr.Recognizer()
    r.dynamic_energy_threshold = False
    r.energy_threshold = 500
    with sr.Microphone() as source:                # use the default microphone as the audio source
        audio = r.listen(source, timeout=15.0)                   # listen for the first phrase and extract it into audio data
    try:
        speech_detected = r.recognize_google(audio)
        print("You said " + speech_detected.upper())    # recognize speech using Google Speech Recognition
        return speech_detected.upper()
    except LookupError:                           # speech is unintelligible
        print("Could not understand audio")

def device_connect():
    global s
    TCP_IP = Sys_Variables.IP_Address
    TCP_PORT = int(Sys_Variables.Port)
    BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    x = ''
    x = s.getpeername()
    available_ports = x
    if len(available_ports) > 1:
        print('MIDI device connectd at ',available_ports[0])
    else:
        print('No devices available')

def device_disconnect():
    global s
    TCP_IP = Sys_Variables.IP_Address
    TCP_PORT = int(Sys_Variables.Port)
    s.close()
    print('Device Disconnected')

def pitch_recognize(pitch):
    pitch_value = 0
    if pitch == 'C':
        pitch_value = 60
    elif pitch == 'Cs' or pitch == 'Df':
        pitch_value = 61
    elif pitch == 'D':
        pitch_value = 62
    elif pitch == 'Ds' or pitch == 'Ef':
        pitch_value = 63
    elif pitch == 'E':
        pitch_value = 64
    elif pitch == 'F':
        pitch_value = 65
    elif pitch == 'Fs' or pitch == 'Gf':
        pitch_value = 66
    elif pitch == 'G':
        pitch_value = 67
    elif pitch == 'Gs' or pitch == 'Af':
        pitch_value = 68
    elif pitch == 'A':
        pitch_value = 69
    elif pitch == 'As' or pitch == 'Bf':
        pitch_value = 70
    elif pitch == 'B':
        pitch_value = 71
    else:
        pitch_value = 0
    # print('Pitch Value =', pitch_value)
    return pitch_value


def midi_dev_read():
    global s
    device_connect()
    x = s.getpeername()
    available_ports = x
    if len(available_ports) > 1:
        return available_ports[0]
    # else:
        # print('No devices available')

def select_instrument():
    global s
    Instrument = Sys_Variables.instrument
    Channel_No = 0xC0 + Sys_Variables.channel
    Instrument_ID = 0
    for i in range(1,len(Sys_Variables.instrument_list)):
        if Sys_Variables.instrument == Sys_Variables.instrument_list[i]:
            Instrument_ID = i-1
    print('Selected Channel No : ', Channel_No)
    print('Selected Instrument : ', Instrument_ID)
    s.send(bytearray([Channel_No, Instrument_ID]))

def change_instrument():
    global s
    Instrument = Sys_Variables.instrument
    Channel_No = 0xC0 + Sys_Variables.channel
    if Instrument == 'Piano 1':
        Instrument_ID = 0
    elif Instrument == 'Piano 2':
        Instrument_ID = 1
    elif Instrument == 'Electric Piano':
        Instrument_ID = 2
    elif Instrument == 'Harpsichord':
        Instrument_ID = 3
    elif Instrument == 'Strings':
        Instrument_ID = 4
    print('Changed Channel No : ', Channel_No)
    print('Changed Instrument : ', Instrument_ID)
    s.send(bytearray([Channel_No, Instrument_ID]))

def send_note(note, channel, octave, duration, velocity):
    print('Note = ', note)
    print('Octave = ', octave)
    print('Duration = ', duration)
    print('Velocity = ', velocity)

    if velocity == 0:
        stop()
        time.sleep(duration)
    else:
        if (type(note)) is list:
            no_of_notes = len(note)
        else:
            no_of_notes = 1
        print("No of notes: ",no_of_notes)
        if no_of_notes > 1:
            Pitch_Value = []
            for i in range(no_of_notes):
                temp = pitch_recognize(note[i])
                Pitch_Value.append(temp)
                print(Pitch_Value)
        else:
            Pitch_Value = pitch_recognize(note)
        # Note ON Command : (0x9,0x<Channel No>)
        Channel_No = 0x90 + Sys_Variables.channel
        if no_of_notes > 1:
            note_on = []
            for j in range(no_of_notes):
                note_on.append(Channel_No)
                note_on.append(Pitch_Value[j]+(octave[j]-4)*12)
                note_on.append(velocity)
            print(note_on)
        else:
            note_on = ''
            note_on = [Channel_No,Pitch_Value+(octave-4)*12,velocity]
            print(note_on)
        s.send(bytearray(note_on))
        time.sleep(duration)

def stop():
    note_off = [0x80, 0, 0]
    s.send(bytearray(note_off))

def play_major(pitch):
    Channel_No = 0x90
    Velocity = 112
    Major = []
    pitch_value = pitch_recognize(pitch)
    # The pitch has not been recognized properly
    # if pitch_value == 0:
    #     # Playing the exit message
    #     playsound.playsound("PitchUnrecognized.mp3", True)
    #     mytext = ""
    #     # Wait for the user response
    #     mytext = speech_recognize()
    #     if mytext == "NO":
    #         s.close()
    #         playsound.playsound("exit.mp3", True)
    #         exit()

    delay = 0.15

    practise_loop = 5

    # Major Scale in the tonic defined by pitch
    octave = 0 # C Middle Scale
    k = [0,2,4,5,7,9,11,12]
    for i in range(0,8):
        Major.append([Channel_No, pitch_value+(octave*12)+k[i], Velocity])

    for j in range(0,8):
        s.send(bytearray(Major[j]))
        time.sleep(delay)

    for k in range(6,-1,-1):
        s.send(bytearray(Major[k]))
        time.sleep(delay)

    time.sleep(delay*2)


def play_minor(pitch):
    Channel_No = 0x90
    Velocity = 112
    Minor = []
    pitch_value = pitch_recognize(pitch)
    # The pitch has not been recognized properly
    # if pitch_value == 0:
    #     # Playing the exit message
    #     playsound.playsound("PitchUnrecognized.mp3", True)
    #     mytext = ""
    #     # Wait for the user response
    #     mytext = speech_recognize()
    #     if mytext == "NO":
    #         s.close()
    #         playsound.playsound("exit.mp3", True)
    #         exit()

    delay = 0.15

    practise_loop = 5

    # Minor Scale in the tonic defined by pitch
    octave = 0 # C Middle Scale
    k = [0,2,3,5,7,8,10,12]
    for i in range(0,8):
        Minor.append([Channel_No, pitch_value+(octave*12)+k[i], Velocity])

    for j in range(0,8):
        s.send(bytearray(Minor[j]))
        time.sleep(delay)

    for k in range(6,-1,-1):
        s.send(bytearray(Minor[k]))
        time.sleep(delay)

    time.sleep(delay*2)


def play_chromatic(pitch):
    Channel_No = 0x90
    Velocity = 112
    Chromatic = []
    pitch_value = pitch_recognize(pitch)
    # The pitch has not been recognized properly
    # if pitch_value == 0:
    #     # Playing the exit message
    #     playsound.playsound("PitchUnrecognized.mp3", True)
    #     mytext = ""
    #     # Wait for the user response
    #     mytext = speech_recognize()
    #     if mytext == "NO":
    #         s.close()
    #         playsound.playsound("exit.mp3", True)
    #         exit()

    delay = 0.15

    practise_loop = 5

    # Chromatic Scale starting from the tone defined by pitch
    octave = 0 # Middle Octave
    for i in range(0,13):
        Chromatic.append([Channel_No, pitch_value+(octave*12)+i, Velocity])

    for j in range(0,13):
        s.send(bytearray(Chromatic[j]))
        time.sleep(delay)

    for k in range(11,-1,-1):
        s.send(bytearray(Chromatic[k]))
        time.sleep(delay)

    time.sleep(delay*2)




