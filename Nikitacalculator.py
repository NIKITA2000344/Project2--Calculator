import customtkinter as ctk
import math
import time

# Unique Styling: Emerald & Dark Gray
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green") 

class NIKITAProCalculator(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NIKITA Elite v2.0")
        self.geometry("450x750") # Compact and Sleek
        self.resizable(False, False)

        self.data_input = ""
        self.vaani = ctk.StringVar()
        self.mode = "DEG" 

        self.setup_custom_ui()
        self.bind("<Key>", self.keyboard_logic)

    def setup_custom_ui(self):
        # Header Section
        self.header = ctk.CTkFrame(self, fg_color="#1a1a1a", height=50, corner_radius=0)
        self.header.pack(fill="x", side="top")

        self.status_label = ctk.CTkLabel(self.header, text="● READY", text_color="#00FF00", font=("Consolas", 12, "bold"))
        self.status_label.pack(side="left", padx=20)

        self.clock_label = ctk.CTkLabel(self.header, text="", font=("Consolas", 12))
        self.clock_label.pack(side="right", padx=20)
        self.update_clock()

        # Modern Neon Display
        self.display_container = ctk.CTkFrame(self, fg_color="transparent")
        self.display_container.pack(pady=20, padx=20, fill="x")

        self.display = ctk.CTkEntry(self.display_container, textvariable=self.vaani, font=("Orbitron", 32),
                                   height=100, corner_radius=10, fg_color="#0d0d0d", 
                                   text_color="#00FF00", border_color="#00FF00", border_width=1, justify="right")
        self.display.pack(fill="x")

        # Mode Selection (Segmented)
        self.seg_button = ctk.CTkSegmentedButton(self, values=["DEG", "RAD"], 
                                                selected_color="#00FF00", 
                                                selected_hover_color="#008000",
                                                command=self.change_mode)
        self.seg_button.set("DEG")
        self.seg_button.pack(pady=10)

        # Tabbed Layout for Features
        self.main_tabs = ctk.CTkTabview(self, segmented_button_selected_color="#2b2b2b")
        self.main_tabs.pack(fill="both", expand=True, padx=10, pady=10) # <-- FIXED: Pack karna zaroori tha
        
        tab_basic = self.main_tabs.add("Math")
        tab_adv = self.main_tabs.add("Scientific")

        # Layout Design
        basic_layout = [
            ['C', '⌫', '%', '÷'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '±', '=']
        ]

        # FIX: '√' button text is kept but handled correctly in logic
        adv_layout = [
            ['sin', 'cos', 'tan', '√'],
            ['log', 'ln', 'exp', '^'],
            ['π', 'e', '(', ')'],
            ['x²', 'mod', 'fact', 'gamma'],
            ['C', '⌫', '0', '=']
        ]

        self.build_buttons(tab_basic, basic_layout, is_basic=True)
        self.build_buttons(tab_adv, adv_layout, is_basic=False)

    def build_buttons(self, parent, layout, is_basic):
        for r, row in enumerate(layout):
            for c, char in enumerate(row):
                btn_color = "#242424"
                text_color = "white"
                
                if char == "=": btn_color = "#00FF00"; text_color = "black"
                elif char in ["C", "0"]: text_color = "#FF3131"
                elif char == "⌫": text_color = "#FF3131" # Safe handling
                elif not char.isdigit() and char not in [".", "±"]: text_color = "#00FF00"

                button = ctk.CTkButton(parent, text=char, width=80, height=60 if is_basic else 50,
                                      fg_color=btn_color, text_color=text_color,
                                      font=("Impact" if char == "=" else "Arial", 18, "bold"),
                                      hover_color="#333333",
                                      command=lambda x=char: self.handle_click(x))
                button.grid(row=r, column=c, padx=5, pady=5, sticky="all" if hasattr(ctk, "all") else "nsew")
        
        for i in range(4): parent.grid_columnconfigure(i, weight=1)

    def update_clock(self):
        self.clock_label.configure(text=time.strftime("%I:%M %p"))
        self.after(1000, self.update_clock)

    def change_mode(self, val):
        self.mode = val

    def handle_click(self, char):
        if char == "=":
            try:
                # Advanced Clean Logic
                raw = self.data_input.replace("÷", "/").replace("^", "**").replace("mod", "%")
                
                # Context injection for math functions
                ctx = {
                    "sin": lambda x: math.sin(math.radians(x) if self.mode == "DEG" else x),
                    "cos": lambda x: math.cos(math.radians(x) if self.mode == "DEG" else x),
                    "tan": lambda x: math.tan(math.radians(x) if self.mode == "DEG" else x),
                    "log": math.log10, "ln": math.log, "exp": math.exp, "sqrt": math.sqrt,
                    "fact": lambda x: math.factorial(int(x)), "gamma": math.gamma,
                    "π": math.pi, "e": math.e,
                    "int": int, "float": float # <-- FIXED: Numbers allow karne ke liye math contexts diye
                }
                
                # Safe eval with standard allowed safe types
                result = eval(raw, {"__builtins__": {"int": int, "float": float, "abs": abs}}, ctx)
                output = f"{result:.6g}" 
                self.vaani.set(output)
                self.data_input = str(output)
            except Exception:
                self.vaani.set("ERROR")
                self.data_input = ""
        
        elif char == "C":
            self.data_input = ""
            self.vaani.set("")
        elif char == "⌫":
            self.data_input = self.data_input[:-1]
            self.vaani.set(self.data_input)
        elif char == "x²":
            self.data_input += "**2"
            self.handle_click("=")
        elif char in ["sin", "cos", "tan", "log", "ln", "fact", "gamma", "exp"]:
            self.data_input += f"{char}("
            self.vaani.set(self.data_input)
        elif char == "√":
            self.data_input += "sqrt("
            self.vaani.set(self.data_input)
        elif char == "±":
            if self.data_input.startswith("-"): 
                self.data_input = self.data_input[1:]
            else: 
                self.data_input = "-" + self.data_input
            self.vaani.set(self.data_input)
        else:
            self.data_input += str(char)
            self.vaani.set(self.data_input)

    def keyboard_logic(self, event):
        if event.keysym == "Return": 
            self.handle_click("=")
        elif event.keysym == "BackSpace": 
            self.handle_click("⌫")
        elif event.char == "/":  
            self.handle_click("÷")
        elif event.char in "0123456789+-*().%^": 
            self.handle_click(event.char)

if __name__ == "__main__":
    app = NIKITAProCalculator()
    app.mainloop()
