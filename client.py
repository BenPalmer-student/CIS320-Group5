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
        self.keylogger_thread = None

        title = ctk.CTkLabel(master=self.root, text='ByteBurglar', font=('Arial', 18))
        title.grid(row=0, column=0, padx=20, pady=10)

        self.create_button(BUTTON_START_KEYLOGGER_TEXT, self.toggle_keylogger).grid(
            row=1, column=0, padx=20, pady=10)

        self.create_button(BUTTON_STOP_KEYLOGGER_TEXT, self.deactivate_keylogger).grid(
            row=2, column=0, padx=20, pady=10)
        
        self.create_button(BUTTON_START_SNIFFER_TEXT, self.activate_packet_sniffer).grid(
            row=3, column=0, padx=20, pady=10)
        
        self.create_button(BUTTON_STOP_SNIFFER_TEXT, self.deactivate_packet_sniffer).grid(
            row=4, column=0, padx=20, pady=10)
        
        # Store a reference to the text widget to be used by other parts of the app.
        self.text = ctk.CTkTextbox(master=self.root, width=100, height=300, wrap='word')
        self.text.grid(row=5, column=0, padx=20, pady=10, sticky="nsew")

        self.create_button(BUTTON_STOP_SNIFFER_TEXT, self.deactivate_packet_sniffer).grid(
            row=4, column=0, padx=20, pady=10)
        
        self.create_button(BUTTON_CLOSE_TEXT, self.on_close).grid(
            row=6, column=0, padx=20, pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close) # handle x close button case

    def create_button(self, txt, command):
        return ctk.CTkButton(master=self.root, text=txt, command=command)

    def toggle_keylogger(self):
        if self.keylogger_thread is None or not self.keylogger_thread.is_alive():
            self.keylogger_thread = KeyloggerThread(app=self) # pass GUI reference
            self.keylogger_thread.start()

    def deactivate_keylogger(self):
        if self.keylogger_thread is not None:
            self.keylogger_thread.stop()
            self.keylogger_thread = None

    def activate_packet_sniffer(self):
        print("Packet sniffer activated!")

    def deactivate_packet_sniffer(self):
        print('Deactivating packet sniffer')

    def update_textbox(self, data):
        self.text.insert('end', data)
        self.text.see('end')  # Scroll to the end to show the latest data

    def on_close(self):
        if self.keylogger_thread is not None and self.keylogger_thread.is_alive():
            self.deactivate_keylogger()

        self.root.destroy()

if __name__ == "__main__":
    root = ctk.CTk()
    root._set_appearance_mode('dark')
    root.geometry("400x700")
    root.title("ByteBurglar")
    root.grid_columnconfigure(0, weight=1)
    ByteBurglarApp(root)
    root.mainloop()
