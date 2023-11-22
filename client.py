import customtkinter as ctk
from Keylogger.client import KeyloggerThread

BUTTON_START_KEYLOGGER_TEXT = 'Start keylogger'
BUTTON_STOP_KEYLOGGER_TEXT = 'Stop keylogger'
BUTTON_START_SNIFFER_TEXT = 'Start packet sniffer'
BUTTON_STOP_SNIFFER_TEXT = 'Stop packet sniffer'
BUTTON_CLOSE_TEXT = 'Close'

class ByteBurglarApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("300x500")
        self.root.title("ByteBurglar")
        ctk.set_appearance_mode('dark')

        self.keylogger_thread = None

        title = ctk.CTkLabel(root, text='ByteBurglar', font=('Arial', 18))
        title.pack(padx=20, pady=20)  # Title placement x,y;
            #y starts at 0 at the top and as 0 increases y moves down. If you want a button further down you increase y

        self.button_keylogger = ctk.CTkButton(root, text=BUTTON_START_KEYLOGGER_TEXT, command=self.toggle_keylogger)
        self.button_keylogger.pack(padx=20, pady=10)

        self.button_keylogger_stop = ctk.CTkButton(root, text=BUTTON_STOP_KEYLOGGER_TEXT, command=self.deactivate_keylogger)
        self.button_keylogger_stop.pack(padx=20, pady=0)

        self.button_packet_sniffer = ctk.CTkButton(root, text=BUTTON_START_SNIFFER_TEXT, command=self.activate_packet_sniffer)
        self.button_packet_sniffer.pack(padx=20, pady=20)

        self.button_packet_sniffer_stop = ctk.CTkButton(root, text=BUTTON_STOP_SNIFFER_TEXT, command=self.deactivate_packet_sniffer)
        self.button_packet_sniffer_stop.pack(padx=20, pady=0)

        self.button_close = ctk.CTkButton(root, text=BUTTON_CLOSE_TEXT, command=self.on_close)
        self.button_close.pack(padx=20, pady=60)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close) # handle x close button case

    def toggle_keylogger(self):
        if self.keylogger_thread is None or not self.keylogger_thread.is_alive():
            self.keylogger_thread = KeyloggerThread()
            self.keylogger_thread.start()
            print("Keylogger activated!")

    def deactivate_keylogger(self):
        if self.keylogger_thread is not None:
            self.keylogger_thread.stop()
            self.keylogger_thread.join()
            self.keylogger_thread = None
            print('Keylogger deactivated!')

    def activate_packet_sniffer(self):
        print("Packet sniffer activated!")

    def deactivate_packet_sniffer(self):
        print('Deactivating packet sniffer')

    def on_close(self):
        if self.keylogger_thread is not None and self.keylogger_thread.is_alive():
            self.deactivate_keylogger()

        self.root.destroy()

if __name__ == "__main__":
    root = ctk.CTk()
    app = ByteBurglarApp(root)
    root.mainloop()
