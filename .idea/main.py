import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.uix.textinput import TextInput
import os

# This module is imported so that we can
# play the converted audio
import playsound
import MIDI_Test
import time
import Sys_Variables
import parse_music_file

def midi_test_app():
    print("Scale: ", Sys_Variables.scale)
    print("Pitch: ", Sys_Variables.pitch)
    print('Instrument: ', Sys_Variables.instrument)
    MIDI_Test.device_connect()
    MIDI_Test.change_instrument()
    if Sys_Variables.scale == "Major Scale":
        MIDI_Test.play_major(Sys_Variables.pitch)
    elif Sys_Variables.scale == "Minor Scale":
        MIDI_Test.play_minor(Sys_Variables.pitch)
    elif Sys_Variables.scale == "Chromatic Scale":
        MIDI_Test.play_chromatic(Sys_Variables.pitch)
    MIDI_Test.stop()
    MIDI_Test.device_disconnect()


def midi_test_voice():
    # Wait for wake up command
    mytext = MIDI_Test.speech_recognize()
    if mytext == "MIDI MASTER":
        # Playing the welcome message
        playsound.playsound("welcome.mp3", True)
        mytext = ""
        # Wait for wake up command
        mytext = MIDI_Test.speech_recognize()
        # Asking for Check for devices command
        if mytext == "CHECK FOR DEVICES":
            midi_device = MIDI_Test.midi_dev_read()
            print("Midi Device @ ", midi_device)
            if midi_device == '192.168.0.81':
                loop = 0
                while (loop == 0):
                    # Playing the PLAY MENU request message
                    playsound.playsound("PlayMenu.mp3", True)
                    mytext = ""
                    # Wait for Play MIDI response
                    mytext = MIDI_Test.speech_recognize()
                    if mytext == "MAJOR SCALE":
                        # Playing the pitch request message
                        playsound.playsound("PlayPitch.mp3", True)
                        mytext = ""
                        # Wait for Play MIDI response
                        mytext = MIDI_Test.speech_recognize()
                        MIDI_Test.play_major(mytext)
                    elif mytext == "MINOR SCALE":
                        # Playing the pitch request message
                        playsound.playsound("PlayPitch.mp3", True)
                        mytext = ""
                        # Wait for Play MIDI response
                        mytext = MIDI_Test.speech_recognize()
                        MIDI_Test.play_minor(mytext)
                    elif mytext == "CHROMATIC SCALE":
                        # Playing the pitch request message
                        playsound.playsound("PlayPitch.mp3", True)
                        mytext = ""
                        # Wait for Play MIDI response
                        mytext = MIDI_Test.speech_recognize()
                        MIDI_Test.play_chromatic(mytext)
                    # Playing the Yes Or No message to continue or not
                    playsound.playsound("YesOrNo.mp3", True)
                    mytext = ""
                    # Wait for the user response
                    mytext = MIDI_Test.speech_recognize()
                    if mytext == "NO":
                        loop = 1
                        MIDI_Test.s.close()
                        playsound.playsound("exit.mp3", True)
                        exit()
            else:
                # Playing no device info message
                playsound.playsound("nomidi_device.mp3", True)
                playsound.playsound("exit.mp3", True)
                exit()
        else:
            # Playing the device info message
            playsound.playsound("cannot_understand.mp3", True)
            # Playing the Yes Or No message to continue or not
            playsound.playsound("YesOrNo.mp3", True)
            mytext = ""
            # Wait for the user response
            mytext = MIDI_Test.speech_recognize()
            if mytext == "NO":
                loop = 1
                Midi_Test.s.close()
                playsound.playsound("exit.mp3", True)
                exit()
        return ActionApp()

class CustomPopup(Popup):

    ip_address_text_input = ObjectProperty()
    port_text_input = ObjectProperty()

    def btn_set_IP_Address_press(self):
        Sys_Variables.IP_Address = self.ip_address_text_input.text
        print("IP Address: ",Sys_Variables.IP_Address)
    def btn_set_IP_Address_release(self):
        pass
    def btn_set_Port_press(self):
        port_inp = TextInput()
        Sys_Variables.Port = self.port_text_input.text
        print("Port: ",Sys_Variables.Port)
    def btn_set_Port_release(self):
        pass
    # def __init__(self):
    #     return CustomPopup()
    # def btn_set_IP_Address_press(self):
    #     print("IP Address: ", self.IP_Address_text_input.text)
    #     Sys_Variables.IP_Address = self.IP_Address_text_input.text
    # def btn_set_IP_Address_release(self):
    #     pass
    # def btn_set_Port_press(self):
    #     print("Port: ", self.Port_text_input.text)
    #     Sys_Variables.Port = self.Port_text_input.text
    # def btn_set_Port_release(self):
    #     pass


class LoadDialog(BoxLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class Controller(BoxLayout):

    def __init__(self):
        super(Controller, self).__init__()
    def btn_play_press(self):
        self.lbl.text = "MIDI Test running....."
    def btn_play_release(self):
        midi_test_app()
        self.lbl.text = "Completed"
    def btn_reset_interface_press(self):
        Sys_Variables.IP_Address = ""
        Sys_Variables.Port = ""
    def btn_reset_interface_release(self):
        pass
    def btn_midi_net_press(self):
        the_popup = CustomPopup()
        the_popup.open()
    def btn_midi_net_release(self):
        pass
    def btn_play_chan0(self):
        Sys_Variables.channel_sel = 0
        if Sys_Variables.os == "Android":
            Sys_Variables.music_filename = "/storage/emulated/0/MIDI_Test/Rev4/Bach_Minue_in_G_Minor.txt"
        parse_music_file.parse_music()
        self.lbl.text = "Completed"
    def btn_play_chan1(self):
        Sys_Variables.channel_sel = 1
        if Sys_Variables.os == "Android":
            Sys_Variables.music_filename = "/storage/emulated/0/MIDI_Test/Rev4/Bach_Minue_in_G_Minor.txt"
        parse_music_file.parse_music()
        self.lbl.text = "Completed"
    def spinner_sel_scale(self, value):
        Sys_Variables.scale = value
        print("Scale Selected: " + Sys_Variables.scale)
    def spinner_sel_pitch(self, value):
        Sys_Variables.pitch = value
        print("Pitch Selected: " + Sys_Variables.pitch)
    def spinner_sel_instrument(self, value):
        Sys_Variables.instrument = value
        print("Instrument Selected: ", Sys_Variables.instrument)
    def spinner_sel_chan0_inst(self, value):
        Sys_Variables.chan0_inst = value
    def spinner_sel_chan1_inst(self, value):
        Sys_Variables.chan1_inst = value
        print("Instrument Selected: " + Sys_Variables.instrument)
    def dismiss_popup(self):
        self._popup.dismiss()
    def show_load(self):
        content = LoadDialog(load=self.load_file, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()
    def load_file(self, path, filename):
        Sys_Variables.music_filename =  os.path.join(path, filename[0])
        self.dismiss_popup()
    def play_file_press(self):
        self.lbl.text = "MIDI Test running....."
    def play_file_release(self):
        Sys_Variables.channel_sel = 2
        parse_music_file.parse_music()
        self.lbl.text = "Completed"
    def voice_control(self):
        midi_test_voice()
    def exit_test(self):
        exit()


class ActionApp(App):
    ip_add_val = Sys_Variables.IP_Address
    port_val = str(Sys_Variables.Port)
    scale_val = Sys_Variables.scale_list
    pitch_val = Sys_Variables.pitch_list
    instrument_val = Sys_Variables.instrument_list
    chan0_inst_val = Sys_Variables.instrument_list
    chan1_inst_val = Sys_Variables.instrument_list
    file_path = ''
    if Sys_Variables.os == 'Android':
        file_path = Sys_Variables.Android_Path
    def build(self):
        return Controller()


myApp = ActionApp()

if __name__ == "__main__":
    myApp.run()

# myApp = TestApp()
# myApp.run()