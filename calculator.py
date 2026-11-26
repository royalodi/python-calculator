"""
Python GUI Calculator
Edition: Demo Desktop App
Language: Python 3 + tkinter
Run: python calculator.py
"""

import tkinter as tk
from tkinter import font as tkfont
import math


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Desktop Calculator — Python Tkinter")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1d2e")

        # State
        self.expression = ""
        self.op_left = None
        self.op_symbol = None
        self.display_var = tk.StringVar(value="0")
        self.history_var = tk.StringVar(value="")
        self.new_number = True
        self.last_result = None

        self._build_ui()
        self._bind_keys()

    def _build_ui(self):
        # ── Display ──────────────────────────────────────────
        display_frame = tk.Frame(self.root, bg="#0f1117", padx=20, pady=16)
        display_frame.pack(fill="x")

        # History label (small expression)
        hist_font = tkfont.Font(family="Segoe UI", size=13)
        tk.Label(
            display_frame, textvariable=self.history_var,
            font=hist_font, bg="#0f1117", fg="#7b7f9a",
            anchor="e"
        ).pack(fill="x")

        # Main display
        disp_font = tkfont.Font(family="Segoe UI", size=38, weight="bold")
        tk.Label(
            display_frame, textvariable=self.display_var,
            font=disp_font, bg="#0f1117", fg="#e4e6f1",
            anchor="e", wraplength=340
        ).pack(fill="x")

        # ── Button Grid ─────────────────────────────────────
        btn_frame = tk.Frame(self.root, bg="#1a1d2e", padx=12, pady=12)
        btn_frame.pack(fill="both")

        # Button layout: [text, col, row, colspan, style]
        buttons = [
            # Row 0 — Utility
            ("AC",   0, 0, 1, "util"),
            ("+/-",  1, 0, 1, "util"),
            ("%",    2, 0, 1, "util"),
            ("÷",    3, 0, 1, "op"),
            # Row 1
            ("7",    0, 1, 1, "num"),
            ("8",    1, 1, 1, "num"),
            ("9",    2, 1, 1, "num"),
            ("×",    3, 1, 1, "op"),
            # Row 2
            ("4",    0, 2, 1, "num"),
            ("5",    1, 2, 1, "num"),
            ("6",    2, 2, 1, "num"),
            ("−",    3, 2, 1, "op"),
            # Row 3
            ("1",    0, 3, 1, "num"),
            ("2",    1, 3, 1, "num"),
            ("3",    2, 3, 1, "num"),
            ("+",    3, 3, 1, "op"),
            # Row 4
            ("0",    0, 4, 2, "num"),   # colspan=2
            (".",    2, 4, 1, "num"),
            ("=",    3, 4, 1, "eq"),
        ]

        styles = {
            "num":  {"bg": "#252840", "fg": "#e4e6f1", "active": "#2d3158"},
            "util": {"bg": "#3a3d5c", "fg": "#e4e6f1", "active": "#4a4d6c"},
            "op":   {"bg": "#6366f1", "fg": "#ffffff", "active": "#4f52d8"},
            "eq":   {"bg": "#10b981", "fg": "#ffffff", "active": "#0d9668"},
        }

        btn_font = tkfont.Font(family="Segoe UI", size=18, weight="bold")
        GAP = 6

        for (text, col, row, colspan, style) in buttons:
            s = styles[style]
            b = tk.Button(
                btn_frame, text=text,
                font=btn_font,
                bg=s["bg"], fg=s["fg"],
                activebackground=s["active"], activeforeground=s["fg"],
                relief="flat", cursor="hand2", bd=0,
                command=lambda t=text: self._on_button(t)
            )
            b.grid(
                row=row, column=col, columnspan=colspan,
                padx=GAP//2, pady=GAP//2, sticky="nsew",
                ipadx=10, ipady=18
            )

        for i in range(4):
            btn_frame.columnconfigure(i, weight=1, minsize=72)
        for i in range(5):
            btn_frame.rowconfigure(i, weight=1, minsize=62)

    def _bind_keys(self):
        keys = {
            "0": "0", "1": "1", "2": "2", "3": "3", "4": "4",
            "5": "5", "6": "6", "7": "7", "8": "8", "9": "9",
            "KP_0": "0", "KP_1": "1", "KP_2": "2", "KP_3": "3", "KP_4": "4",
            "KP_5": "5", "KP_6": "6", "KP_7": "7", "KP_8": "8", "KP_9": "9",
            "plus": "+", "KP_Add": "+",
            "minus": "−", "KP_Subtract": "−",
            "asterisk": "×", "KP_Multiply": "×",
            "slash": "÷", "KP_Divide": "÷",
            "period": ".", "KP_Decimal": ".",
            "equal": "=", "Return": "=", "KP_Enter": "=",
            "BackSpace": "⌫", "Escape": "AC", "c": "AC", "C": "AC",
            "percent": "%"
        }
        for k, v in keys.items():
            self.root.bind(f"<{k}>", lambda e, t=v: self._on_button(t))

    def _on_button(self, text):
        if text in "0123456789":
            self._digit(text)
        elif text == ".":
            self._decimal()
        elif text in ("+", "−", "×", "÷"):
            self._operator(text)
        elif text == "=":
            self._equals()
        elif text == "AC":
            self._clear()
        elif text == "+/-":
            self._negate()
        elif text == "%":
            self._percent()
        elif text == "⌫":
            self._backspace()

    # ── Core Logic ───────────────────────────────────────────

    def _digit(self, d):
        if self.new_number:
            self.display_var.set(d)
            self.new_number = False
        else:
            cur = self.display_var.get()
            if cur == "0":
                self.display_var.set(d)
            else:
                if len(cur.replace("-", "").replace(".", "")) < 12:
                    self.display_var.set(cur + d)

    def _decimal(self):
        if self.new_number:
            self.display_var.set("0.")
            self.new_number = False
        elif "." not in self.display_var.get():
            self.display_var.set(self.display_var.get() + ".")

    def _operator(self, op):
        try:
            val = float(self.display_var.get())
            if self.op_symbol and not self.new_number:
                self._equals(chain=True)
                val = float(self.display_var.get())
            sym_map = {"−": "-", "×": "*", "÷": "/"}
            self.op_left = val
            self.op_symbol = sym_map.get(op, op)
            self.expression = f"{val}{self.op_symbol}"
            self.history_var.set(f"{self._fmt(val)} {op}")
            self.new_number = True
        except Exception:
            self._error()

    def _equals(self, chain=False):
        if self.op_left is None or not self.op_symbol:
            return
        try:
            val2 = float(self.display_var.get())
            if self.op_symbol == "+":
                result = self.op_left + val2
            elif self.op_symbol == "-":
                result = self.op_left - val2
            elif self.op_symbol == "*":
                result = self.op_left * val2
            elif self.op_symbol == "/":
                if val2 == 0:
                    raise ZeroDivisionError("Cannot divide by zero")
                result = self.op_left / val2
            else:
                raise ValueError("Unknown operator")

            if not math.isfinite(result):
                raise OverflowError("Result out of range")

            if result == int(result) and abs(result) < 1e12:
                result = int(result)

            history = f"{self.history_var.get()} {self._fmt(val2)} ="
            self.history_var.set(history)
            self.display_var.set(self._fmt(result))
            self.last_result = result
            self.expression = ""
            self.op_left = None
            self.op_symbol = None
            self.new_number = not chain
        except ZeroDivisionError:
            self.display_var.set("Error")
            self.history_var.set("Cannot divide by zero")
            self.expression = ""
            self.op_left = None
            self.op_symbol = None
            self.new_number = True
        except Exception:
            self._error()

    def _clear(self):
        self.expression = ""
        self.op_left = None
        self.op_symbol = None
        self.display_var.set("0")
        self.history_var.set("")
        self.new_number = True
        self.last_result = None

    def _negate(self):
        try:
            val = float(self.display_var.get())
            self.display_var.set(self._fmt(-val))
        except Exception:
            pass

    def _percent(self):
        try:
            val = float(self.display_var.get())
            self.display_var.set(self._fmt(val / 100))
            self.new_number = True
        except Exception:
            pass

    def _backspace(self):
        if self.new_number:
            return
        cur = self.display_var.get()
        new = cur[:-1]
        self.display_var.set(new if new and new != "-" else "0")

    def _error(self):
        self.display_var.set("Error")
        self.expression = ""
        self.op_left = None
        self.op_symbol = None
        self.new_number = True

    def _fmt(self, val):
        """Format number nicely."""
        if isinstance(val, float):
            if val == int(val):
                return str(int(val))
            # Limit decimal places
            s = f"{val:.10f}".rstrip("0")
            if "." in s and len(s.split(".")[1]) > 8:
                s = f"{val:.8g}"
            return s
        return str(val)


def main():
    root = tk.Tk()
    root.geometry("360x560")
    Calculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
