# import tkinter as tk
import customtkinter as ctk  # import customtkinter instead of tkinter.
from Keylogger.client import start_keylogger

def activate_keylogger():
    # main.button_pressed_keylogger = True
    print("Keylogger activated!")
    # start_keylogger = Keylogger()
    # start_keylogger.start()

def deactivate_keylogger():
    print('Deacting keylogger')
    # stop_keylogger = Keylogger()
    # stop_keylogger.stop()

def activate_packet_sniffer():
    # main.button_pressed_p_s = True
    print("Packet sniffer activated!")

def deactivate_packet_sniffer():
    print('Deactivating packet sniffer.')

def main():
    # here we add the UI
    # start_keylogger()
    window = ctk.CTk()  # Use CTk instead of Tk
    ctk.set_appearance_mode('dark')

    window.geometry("300x500")  # Window size x,y
    window.title("ByteBurglar")  # Window title

    title = ctk.CTkLabel(window, text='ByteBurglar', font=('Arial', 18))  # Use CTkLabel instead of Label
    title.pack(padx=20, pady=20)  # Title placement x,y;
        #y starts at 0 at the top and as 0 increases y moves down. If you want a button further down you increase y
        
    button_keylogger = ctk.CTkButton(window, text='Start keylogger', command=activate_keylogger) #creating buttons
    button_keylogger.pack(padx=20, pady=10)

    button_keylogger_stop = ctk.CTkButton(window, text = 'Stop keylogger', command = deactivate_keylogger)
    button_keylogger_stop.pack(padx = 20, pady =0)


    button_packet_sniffer = ctk.CTkButton(window, text='Start packet sniffer', command=activate_packet_sniffer)
    button_packet_sniffer.pack(padx=20, pady=20)

    button_packet_sniffer_stop = ctk.CTkButton(window, text='Stop packet sniffer', command=deactivate_packet_sniffer)
    button_packet_sniffer_stop.pack(padx=20, pady=0)


    button_close = ctk.CTkButton(window, text='Close', command=window.destroy)
    button_close.pack(padx=20, pady=60)

    window.mainloop()


if __name__ == "__main__":
    main()
