import tkinter as tk
from tkinter import Toplevel, Label
import speech_recognition as sr
import pyttsx3
import threading
import numpy as np
import pyaudio

voice_map = {
    "top left": (0, 0), "top middle": (0, 1), "top right": (0, 2),
    "middle left": (1, 0), "middle middle": (1, 1), "middle right": (1, 2),
    "bottom left": (2, 0), "bottom middle": (2, 1), "bottom right": (2, 2)
}

class VoiceTicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("🎙️ Accessible Tic Tac Toe")
        self.master.configure(bg="#f0f0f0")
        self.tts = pyttsx3.init()
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.game_started = False
        self.restart_mode = False

        self.create_ui()
        self.speak("Say 'start game' or press any cell to begin.")
        self.listen_in_background()

    def create_ui(self):
        self.buttons = [[tk.Button(self.master, text="", font=("Arial", 28, "bold"), width=6, height=3,
                                   bg="white", fg="black", relief="ridge", bd=3,
                                   command=lambda r=r, c=c: self.manual_move(r, c))
                         for c in range(3)] for r in range(3)]
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].grid(row=r, column=c, padx=5, pady=5)

    def speak(self, message):
        print(f"[SPEAK]: {message}")
        self.tts.say(message)
        self.tts.runAndWait()

    def listen_in_background(self):
        threading.Thread(target=self.listen_loop, daemon=True).start()

    def listen_loop(self):
        recognizer = sr.Recognizer()
        mic = sr.Microphone()
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)

        while True:
            with mic as source:
                try:
                    print("Listening...")
                    audio = recognizer.listen(source, timeout=5)
                    command = recognizer.recognize_google(audio).lower()
                    print(f"You said: {command}")

                    if not self.game_started and not self.restart_mode and "start game" in command:
                        self.start_game()
                    elif self.game_started and command in voice_map:
                        row, col = voice_map[command]
                        self.place_symbol(row, col)
                    else:
                        self.speak("Invalid command. Try again.")
                except sr.UnknownValueError:
                    continue
                except sr.WaitTimeoutError:
                    continue
                except sr.RequestError:
                    self.speak("Could not connect to internet for voice recognition.")
                    break

    def manual_move(self, row, col):
        if not self.game_started:
            self.start_game()
        self.place_symbol(row, col)

    def start_game(self):
        self.game_started = True
        self.restart_mode = False
        self.speak("Game started. Player X, your turn.")

    def place_symbol(self, row, col):
        if self.board[row][col] != "":
            self.speak("That spot is already taken.")
            return

        self.board[row][col] = self.current_player
        self.buttons[row][col].config(text=self.current_player)

        move_position = self.get_position_name(row, col)
        if self.current_player == "O":
            self.speak(f"Player 2 placed O in {move_position}.")

        if self.check_winner():
            self.speak(f"Player {self.current_player} wins!")
            self.show_message(f"🎉 Player {self.current_player} wins!")
            self.after_game()
        elif self.is_draw():
            self.speak("It's a draw!")
            self.show_message("🤝 It's a draw!")
            self.after_game()
        else:
            self.current_player = "O" if self.current_player == "X" else "X"
            self.speak(f"Player {self.current_player}, your turn.")

    def get_position_name(self, row, col):
        for name, pos in voice_map.items():
            if pos == (row, col):
                return name
        return f"row {row + 1}, column {col + 1}"

    def check_winner(self):
        b = self.board
        for i in range(3):
            if b[i][0] == b[i][1] == b[i][2] != "" or b[0][i] == b[1][i] == b[2][i] != "":
                return True
        return b[0][0] == b[1][1] == b[2][2] != "" or b[0][2] == b[1][1] == b[2][0] != ""

    def is_draw(self):
        return all(cell != "" for row in self.board for cell in row)

    def show_message(self, msg):
        top = Toplevel(self.master)
        top.configure(bg="white")
        top.overrideredirect(True)
        top.geometry("300x100+400+300")
        Label(top, text=msg, font=("Arial", 18, "bold"), fg="green", bg="white").pack(expand=True)
        self.master.after(2500, top.destroy)  # auto-close after 2.5 seconds

    def after_game(self):
        self.game_started = False
        self.restart_mode = True
        self.speak("Do you want to play again? Clap once to restart.")
        threading.Thread(target=self.detect_clap_restart, daemon=True).start()

    def detect_clap_restart(self):
        CHUNK = 1024
        RATE = 44100
        THRESHOLD = 2500
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE,
                        input=True, frames_per_buffer=CHUNK)
        while self.restart_mode:
            data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
            peak = np.abs(data).max()
            print(f"Audio peak: {peak}")
            if peak > THRESHOLD:
                self.speak("Clap detected! Restarting game.")
                stream.stop_stream()
                stream.close()
                p.terminate()
                self.reset_board()
                self.start_game()
                return

    def reset_board(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        for row in self.buttons:
            for btn in row:
                btn.config(text="")
        self.current_player = "X"

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceTicTacToe(root)
    root.mainloop()
