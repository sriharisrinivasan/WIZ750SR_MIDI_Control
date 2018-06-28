import MIDI_Test
import Sys_Variables
import os
import threading
import time

note_list = []
octave_list = []
duration_list = []
velocity_list = []
bar_count = []
track_parse = 0


# Initialize the track_count variable for Monophonic and Polyphonic Music
track_count = 0

def send_note_on(channel_no):
    for k in range(len(note_list[channel_no])):
        print("Channel No: ",channel_no)
        Sys_Variables.channel = channel_no
        if channel_no == 0:
            Sys_Variables.instrument = Sys_Variables.chan0_inst
        else:
            Sys_Variables.instrument = Sys_Variables.chan1_inst
        print(Sys_Variables.channel)
        print(Sys_Variables.instrument)
        MIDI_Test.change_instrument()
        print("k: ",k)
        MIDI_Test.send_note(note_list[channel_no][k], Sys_Variables.channel, octave_list[channel_no][k], duration_list[channel_no][k], velocity_list[channel_no][k])


# Create note, duration, velocity and bar list for each track
def list_creation(no_of_tracks):
    global note_list, octave_list, duration_list, velocity_list, bar_count
    note_list = [[] for j in range(no_of_tracks)]
    octave_list = [[] for j in range(no_of_tracks)]
    duration_list = [[] for j in range(no_of_tracks)]
    velocity_list = [[] for j in range(no_of_tracks)]
    bar_count = [0 for j in range(no_of_tracks)]
		

# Function for converting the tracks to a single note, duration,velocity sequence (if polyphonic) and send the notes to the MIDI instrument for playing
def play_music():
    global note_list, octave_list, duration_list, velocity_list, bar_count
    # Pre-processing here
	# Send a Note Off command to the MIDI device
    MIDI_Test.stop()
	# Reset the global variables - scale and pitch
    Sys_Variables.scale = ""
    Sys_Variables.pitch = ""
    print(note_list[0])
    print(octave_list[0])
    print(duration_list[0])
    print(velocity_list[0])
    print(note_list[1])
    print(octave_list[1])
    print(duration_list[1])
    print(velocity_list[1])
    print(bar_count)
    start_time = time.time()
    print("Start time: ", start_time)
    if Sys_Variables.channel_sel == 0:
        thread0 = threading.Thread(target=send_note_on, args=(0,))
    elif Sys_Variables.channel_sel == 1:
        thread1 = threading.Thread(target=send_note_on, args=(1,))
    else:
        thread0 = threading.Thread(target=send_note_on, args=(0,))
        thread1 = threading.Thread(target=send_note_on, args=(1,))
    if Sys_Variables.channel_sel == 0:
        thread0.start()
    elif Sys_Variables.channel_sel == 1:
        thread1.start()
    else:
        thread0.start()
        thread1.start()
    if Sys_Variables.channel_sel == 0:
        thread0.join()
    elif Sys_Variables.channel_sel == 1:
        thread1.join()
    else:
        thread0.join()
        thread1.join()
    end_time = time.time()
    print("End time: ", end_time)
    # for k in range(len(note_list[0])):
        # MIDI_Test.send_note((i[k] for i in note_list), Sys_Variables.channel, (i[0] for i in octave_list), (i[0] for i in duration_list), (i[0] for i in velocity_list))

	# Disconnect from the MIDI device
    MIDI_Test.device_disconnect()
    print("duration for %dst and %dnd tracks: ",sum(duration_list[0]), sum(duration_list[1]))
    note_list = []
    octave_list = []
    duration_list = []
    velocity_list = []
    bar_count = 0
    Sys_Variables.channel = 0


# Function for parsing the input file for the music in a given syntax and protocol
def parse_music():
    global note_list, octave_list, duration_list, velocity_list, bar_count, track_parse, track_count
	# Connect to the MIDI device
    MIDI_Test.device_connect()
	# Select the Instrument voicing
    MIDI_Test.change_instrument()
    with open(Sys_Variables.music_filename) as f:
		# Parse and read the music input file as list of lines
        lines = f.readlines()
	# Create a new list for parsed output
    k = []
    for i in lines:
        # Remove new line characters from the list
        j = i.replace('\n','')
		# Remove tab space characters from the list
        j = j.replace('\t','')
		# Remove space from the list
        j = j.replace(' ','')
		# Remove ( character from the list
        j = j.replace('(','')
		# Remove ) character from the list
        j = j.replace(')','')
        # Add the list element to a new list if it is not null element
        if i != '':
            k.append(j)
    print("\nUnedited file: \n", lines)
    print("\nEdited file: \n", k)
	# Parse through the stripped down new list k
    for i in k:
        # Convert the list element to all upper case for the alphabets
        x = i.upper()
		# Ignore commands starting with # as these are comments
        if "#" in x:
            pass
        #STOP - End Of File command
        #Parse the note, duration and velocity of the polyphonic tracks into a single list and send to the MIDI instrument
		#Send the note, duration and velocity of the monophonic track to the MIDI instrument
        elif "STOP" in x:
            play_music()
		# Parse Tempo command - TMP(<tempo value>)
		# For instance, TMP(88) - 88 beats per minute			
        elif "TMP" in x:
			# Remove TMP from the command and parse the rest of the command
            Sys_Variables.tempo = int(x[3:])
            print("Tempo = ", Sys_Variables.tempo)
			
		# Parse Time Signature command
		# Usage - TS(<beats per measure>,<base note duration for BPM>)
		# For instance, TS(4,4) refers to quarter note as base note duration for BPM, and 4 beats per measure - the typical 4/4 time signature
        elif "TS" in x:
			# Remove TS from the command and parse the rest of the command
            x1 = i[2:]
            x1 = x1.split(",")
            Sys_Variables.beatspermeasure = int(x1[0])
            print("Beats per Measure = ", Sys_Variables.beatspermeasure)
            Sys_Variables.measure = int(x1[1])
            print("Measure = ", Sys_Variables.measure)
        # POLY - Polyphonic command
        #  Usage - POLY(<no of tracks>)
        #  For Instance, POLY(2)
        #  2 tracks
        elif "POLY" in x:
            #Remove POLY from the command and parse the rest of the command
            Sys_Variables.no_of_tracks = int(x[4:])
            print("No of tracks = ", Sys_Variables.no_of_tracks)
            list_creation(Sys_Variables.no_of_tracks)
		# MONO - Monophonic command
		# Usage - MONO
        elif "MONO" in x:
			# Assign no of tracks to One, for decoding and playing
            Sys_Variables.no_of_tracks = 1
        # CLEF - Treble/Alto/Tenor/Bass
        # Usage - CLEF(BASS)
        # For selecting Bass Clef
        elif "CLEF" in x:
            # Treble Clef
            if x[4:] == "TREBLE":
                track_count += 1
            # Alto Clef
            elif x[4:] == "ALTO":
                track_count += 1
            # Tenor Clef
            elif x[4:] == "TENOR":
                track_count += 1
            # Bass Clef
            else: # BASS - the only remaining CLEF
                track_count += 1
            print("Track Count = ", track_count)
        elif "{" in x:
            track_parse = 1
        elif "}" in x:
            track_parse = 0
            Sys_Variables.channel += 1
            print("Channel: ", Sys_Variables.channel)
        elif (track_parse == 1):
			# '\' is the identifier for the start of the bar, just pass this as it is more for the user convenience
            if "b:" in x:
                pass
			# '/' is the identifier for the end of the bar, increase the bar count
            elif ":b" in x:
                bar_count[Sys_Variables] += 1
			
            # Parse Velocity command
            # Usage - VEL(<Velocity value>)
            # For instance, VEL(100) signifies a note velocity of 100 (in a range from 0 to 255)
            # The velocity applies to all notes after the command, until a new velocity command or a 'Send Note with Velocity' command is sent
            elif "VEL" in x:
                # Remove VEL from the command and parse the rest of the command
                Sys_Variables.velocity = int(x[3:])
				
            # Send Note with Velocity
            # Usage - SNV(<Note No>,<Duration>,<Velocity>)
            # For instance, SNV(C4,4,115)
            # Note - C4, Duration - Quarter Note, Velocity - 115 and applicable to all notes after this command
            elif "SNV" in x:
                # Remove SNV from the command and parse the rest of the command
                x1 = i[3:]
                print(x1)
                x1 = x1.split(",")
                print(x1)
                t = x1[0]
                print(t)
                if "s" in t:
                    Sys_Variables.note = t[0:2]
                    print("Note: ", Sys_Variables.note)
                    Sys_Variables.octave = int(t[2:])
                    print("Octave: ", Sys_Variables.octave)
                elif "f" in t:
                    Sys_Variables.note = t[0:2]
                    print("Note: ", Sys_Variables.note)
                    Sys_Variables.octave = int(t[2:])
                    print("Octave: ", Sys_Variables.octave)
                else:
                    Sys_Variables.note = t[0]
                    print("Note: ", Sys_Variables.note)
                    Sys_Variables.octave = int(t[1:])
                    print("Octave: ", Sys_Variables.octave)
                Sys_Variables.duration = (60/Sys_Variables.tempo)*Sys_Variables.measure/float(x1[1])
                print("Duration: ", Sys_Variables.duration)
                Sys_Variables.velocity = int(x1[2])
                print("Velocity: ", Sys_Variables.velocity)
                note_list[Sys_Variables.channel].append(Sys_Variables.note)
                octave_list[Sys_Variables.channel].append(Sys_Variables.octave)
                duration_list[Sys_Variables.channel].append(Sys_Variables.duration)
                velocity_list[Sys_Variables.channel].append(Sys_Variables.velocity)
				
            # Send Note without Velocity
            # Usage - SNV(<Note No>,<Duration>)
            # For instance, SN(D3,8)
            # Note - D3, Duration - Eighth Note, Velocity - previously set velocity (from either VEL or SNV commands whichever is the latest)
            elif "SN" in x:
                # Remove SN from the command and parse the rest of the command
                x1 = i[2:]
                print(x1)
                x1 = x1.split(",")
                print(x1)
                t = x1[0]
                print(t)
                if "s" in t:
                    Sys_Variables.note = t[0:2]
                    print("Note: ", Sys_Variables.note)
                    Sys_Variables.octave = int(t[2:])
                    print("Octave: ", Sys_Variables.octave)
                elif "f" in t:
                    Sys_Variables.note = t[0:2]
                    print(Sys_Variables.note)
                    Sys_Variables.octave = int(t[2:])
                    print("Octave: ", Sys_Variables.octave)
                else:
                    Sys_Variables.note = t[0]
                    print("Note: ", Sys_Variables.note)
                    Sys_Variables.octave = int(t[1:])
                    print("Octave: ", Sys_Variables.octave)
                Sys_Variables.duration = (60/Sys_Variables.tempo)*Sys_Variables.measure/float(x1[1])
                print("Duration: ", Sys_Variables.duration)
                print("Velocity: ", Sys_Variables.velocity)
                note_list[Sys_Variables.channel].append(Sys_Variables.note)
                octave_list[Sys_Variables.channel].append(Sys_Variables.octave)
                duration_list[Sys_Variables.channel].append(Sys_Variables.duration)
                velocity_list[Sys_Variables.channel].append(Sys_Variables.velocity)

            # Send Rest
            # Usage - SR(<Duration>)
            # For instance, SR(1)
            # Rest for Duration - Whole Note
            elif "SR" in x:
                Sys_Variables.duration = (60/Sys_Variables.tempo)*Sys_Variables.measure/float(i[2:])
                note_list[Sys_Variables.channel].append('R')
                octave_list[Sys_Variables.channel].append(0)
                duration_list[Sys_Variables.channel].append(Sys_Variables.duration)
                velocity_list[Sys_Variables.channel].append(0)

            # Send Chord
            # Usage - SC(<Base Note>,<Chord Type>,<Inversion>,<Duration>)
            # For instance, SC(C5,Maj7,0,16)
            # Inversion parameters: 0 - No Inversion, 1 - First Inversion, 2 - Second Inversion based upon base note
            # Send C Major 7 chord (Octave 5) no inversion for sixteenth note duration
            elif "SC" in x:
                # Remove SC from the command and parse the rest of the command
                x1 = i[2:]
                x1 = x1.split(",")
                t = x1[0]
                Sys_Variables.note = t[0]
                Sys_Variables.octave = int(t[1])
                Sys_Variables.chord_type = x1[1]
                Sys_Variables.duration = (60/Sys_Variables.tempo)*Sys_Variables.measure/float(x1[1])

            # Send multiple notes without Velocity
            # Usage - SMN(<No of Notes - 'n'>,<Note No '1'>,...,<Note No 'n',<Duration>)
            # For instance, SMN(3,C2,E2,G2,8)
            # Send the 3 notes C2, E2 and G2 together for a duration of eighth note
            # Velocity - previously set velocity (from either VEL or SNV commands whichever is the latest)
            elif "SMN" in x:
                # Remove SMN from the command and parse the rest of the command
                x1 = i[3:]
                x1 = x1.split(",")
                print(x1)
                t = int(x1[0])
                mn_note = []
                mn_octave = []
                temp = 0
                for i in range(t):
                    t1 = x1[i+1]
                    print(t1)
                    if "s" in t1:
                        Sys_Variables.note = t1[0:2]
                        print("Note: ", Sys_Variables.note)
                        mn_note.append(Sys_Variables.note)
                        Sys_Variables.octave = int(t1[2:])
                        print("Octave: ", Sys_Variables.octave)
                        mn_octave.append(Sys_Variables.octave)
                    elif "f" in t1:
                        Sys_Variables.note = t1[0:2]
                        print("Note: ", Sys_Variables.note)
                        mn_note.append(Sys_Variables.note)
                        Sys_Variables.octave = int(t1[2:])
                        print("Octave: ", Sys_Variables.octave)
                        mn_octave.append(Sys_Variables.octave)
                    else:
                        Sys_Variables.note = t1[0]
                        print("Note: ", Sys_Variables.note)
                        mn_note.append(Sys_Variables.note)
                        Sys_Variables.octave = int(t1[1:])
                        print("Octave: ", Sys_Variables.octave)
                        mn_octave.append(Sys_Variables.octave)
                    temp += 1
                print(temp)
                print(float(x1[temp+1]))
                Sys_Variables.duration = (60/Sys_Variables.tempo)*Sys_Variables.measure/float(x1[temp+1])
                note_list[Sys_Variables.channel].append(mn_note)
                octave_list[Sys_Variables.channel].append(mn_octave)
                duration_list[Sys_Variables.channel].append(Sys_Variables.duration)
                velocity_list[Sys_Variables.channel].append(Sys_Variables.velocity)





			

