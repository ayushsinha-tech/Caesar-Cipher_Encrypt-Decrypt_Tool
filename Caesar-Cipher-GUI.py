import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
import io

class CaesarCipherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Caesar Cipher")
        self.root.geometry("1000x800")
        self.root.resizable(True, True)
        
        
        self.bg_color = "#1e1e2e"
        self.fg_color = "#ffffff"
        self.accent_color = "#5b9ef5"
        self.success_color = "#2ea04d"
        self.input_bg = "#2d2d3d"
        self.border_color = "#404050"
        
        self.root.configure(bg=self.bg_color)
        
        
        self.setup_styles()
        
        
        self.create_widgets()
    #Configure style
    def setup_styles(self):
        """Configure ttk styles for dark theme."""
        style = ttk.Style()
        style.theme_use('clam')
        
        
        style.configure('TFrame', background=self.bg_color)
        style.configure('TLabel', background=self.bg_color, foreground=self.fg_color)
        style.configure('Title.TLabel', background=self.bg_color, foreground=self.accent_color, 
                       font=('Segoe UI', 28, 'bold'))
        style.configure('Subtitle.TLabel', background=self.bg_color, foreground='#a0a0a0',
                       font=('Segoe UI', 11))
        style.configure('Section.TLabel', background=self.bg_color, foreground=self.fg_color,
                       font=('Segoe UI', 12, 'bold'))
        
        style.configure('TScale', background=self.bg_color, troughcolor=self.input_bg)
        style.map('TScale', background=[('active', self.bg_color)])
        
    
        style.configure('Encrypt.TButton', font=('Segoe UI', 11, 'bold'), padding=10)
        style.map('Encrypt.TButton',
                 background=[('active', '#4a7fd7'), ('pressed', '#3d64b8')])
        
        style.configure('Decrypt.TButton', font=('Segoe UI', 11, 'bold'), padding=10)
        style.map('Decrypt.TButton',
                 background=[('active', '#239641'), ('pressed', '#1b7533')])
        
        style.configure('Action.TButton', font=('Segoe UI', 10), padding=5)
    
    def create_widgets(self):
        """Create all GUI widgets."""
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        
        self.create_header(main_frame)
        
        
        self.create_input_section(main_frame)
        
        
        self.create_shift_section(main_frame)
        
        
        self.create_action_section(main_frame)
        
    
        self.create_result_section(main_frame)
        
        
        self.create_footer(main_frame)
    
    def create_header(self, parent):
        """Create header with title and description."""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        
        title_label = ttk.Label(header_frame, text="🔐 Caesar Cipher", 
                               style='Title.TLabel')
        title_label.pack()
        
        
        subtitle_label = ttk.Label(header_frame, 
                                  text="Encrypt or Decrypt messages using the Caesar Cipher technique.",
                                  style='Subtitle.TLabel')
        subtitle_label.pack()
    
    def create_input_section(self, parent):
        """Create input text area section."""
        input_frame = ttk.Frame(parent)
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        
        label_frame = ttk.Frame(input_frame)
        label_frame.pack(fill=tk.X, pady=(0, 8))
        
        label = ttk.Label(label_frame, text="Input Text", style='Section.TLabel')
        label.pack(side=tk.LEFT)
        
        self.char_counter = ttk.Label(label_frame, text="0 / 1000", 
                                     foreground='#808080')
        self.char_counter.pack(side=tk.RIGHT)
        
        
        self.input_text = tk.Text(input_frame, height=6, font=('Courier', 10),
                                  bg=self.input_bg, fg=self.fg_color,
                                  insertbackground=self.accent_color,
                                  wrap=tk.WORD, borderwidth=1, relief=tk.SOLID)
        self.input_text.pack(fill=tk.BOTH, expand=True)
        self.input_text.bind('<KeyRelease>', self.update_char_counter)
        
        
        self.input_text.configure(highlightthickness=1, 
                                 highlightbackground=self.border_color,
                                 highlightcolor=self.accent_color)
    
    def update_char_counter(self, event=None):
        """Update character counter."""
        count = len(self.input_text.get("1.0", tk.END)) - 1  # Exclude newline
        count = min(count, 1000)  # Max 1000 characters
        self.char_counter.config(text=f"{count} / 1000")
    
    def create_shift_section(self, parent):
        """Create shift value slider section."""
        shift_frame = ttk.Frame(parent)
        shift_frame.pack(fill=tk.X, pady=(0, 30))
        
        
        label_frame = ttk.Frame(shift_frame)
        label_frame.pack(fill=tk.X, pady=(0, 12))
        
        label = ttk.Label(label_frame, text="Shift (Key)", style='Section.TLabel')
        label.pack(side=tk.LEFT)
        
        self.shift_value_label = ttk.Label(label_frame, text="Shift: 0", 
                                          foreground=self.accent_color,
                                          font=('Segoe UI', 11, 'bold'))
        self.shift_value_label.pack(side=tk.RIGHT)
        
        
        self.shift_slider = ttk.Scale(shift_frame, from_=-25, to=25, orient=tk.HORIZONTAL,
                                     command=self.update_shift_value)
        self.shift_slider.set(0)
        self.shift_slider.pack(fill=tk.X, pady=(0, 8))
        
        
        range_frame = ttk.Frame(shift_frame)
        range_frame.pack(fill=tk.X)
        
        ttk.Label(range_frame, text="-25", foreground='#808080').pack(side=tk.LEFT)
        ttk.Label(range_frame, text="25", foreground='#808080').pack(side=tk.RIGHT)
        
        
        info_label = ttk.Label(shift_frame, 
                              text="Positive shifts move letters forward. Negative shifts move letters backward.",
                              foreground='#707080', font=('Segoe UI', 9))
        info_label.pack(fill=tk.X, pady=(12, 0))
    
    def update_shift_value(self, value):
        """Update shift value label."""
        shift = int(float(value))
        self.shift_value_label.config(text=f"Shift: {shift}")
    
    def create_action_section(self, parent):
        """Create encrypt/decrypt buttons."""
        actions_frame = ttk.Frame(parent)
        actions_frame.pack(fill=tk.X, pady=(0, 20))
        
        label = ttk.Label(actions_frame, text="Actions", style='Section.TLabel')
        label.pack(pady=(0, 12))
        
        button_frame = ttk.Frame(actions_frame)
        button_frame.pack(fill=tk.X)
        
        
        encrypt_btn = tk.Button(button_frame, text="🔒 Encrypt", 
                               bg=self.accent_color, fg=self.fg_color,
                               font=('Segoe UI', 11, 'bold'),
                               padx=20, pady=12, border=0, cursor='hand2',
                               command=self.encrypt)
        encrypt_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        
        decrypt_btn = tk.Button(button_frame, text="🔓 Decrypt", 
                               bg=self.success_color, fg=self.fg_color,
                               font=('Segoe UI', 11, 'bold'),
                               padx=20, pady=12, border=0, cursor='hand2',
                               command=self.decrypt)
        decrypt_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    def create_result_section(self, parent):
        """Create result display section."""
        result_frame = ttk.Frame(parent)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        
        label_frame = ttk.Frame(result_frame)
        label_frame.pack(fill=tk.X, pady=(0, 8))
        
        label = ttk.Label(label_frame, text="Result", style='Section.TLabel')
        label.pack(side=tk.LEFT)
        
        copy_btn = tk.Button(label_frame, text="📋 Copy", 
                            bg=self.input_bg, fg=self.accent_color,
                            font=('Segoe UI', 9),
                            border=0, cursor='hand2',
                            command=self.copy_result)
        copy_btn.pack(side=tk.RIGHT)
        
        
        self.result_text = tk.Text(result_frame, height=5, font=('Courier', 10),
                                   bg=self.input_bg, fg=self.accent_color,
                                   insertbackground=self.accent_color,
                                   wrap=tk.WORD, borderwidth=1, relief=tk.SOLID,
                                   state=tk.DISABLED)
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        self.result_text.configure(highlightthickness=1,
                                  highlightbackground=self.border_color,
                                  highlightcolor=self.accent_color)
    
    def create_footer(self, parent):
        """Create footer with additional options."""
        footer_frame = ttk.Frame(parent)
        footer_frame.pack(fill=tk.X, pady=(20, 0))
        
        
        brute_force_btn = tk.Button(footer_frame, text="🔍 Brute Force (Try All Shifts)", 
                                   bg=self.input_bg, fg=self.fg_color,
                                   font=('Segoe UI', 10),
                                   padx=15, pady=8, border=1,
                                   borderwidth=1, cursor='hand2',
                                   command=self.brute_force)
        brute_force_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        
        clear_btn = tk.Button(footer_frame, text="🗑️ Clear All", 
                             bg=self.input_bg, fg=self.fg_color,
                             font=('Segoe UI', 10),
                             padx=15, pady=8, border=1,
                             borderwidth=1, cursor='hand2',
                             command=self.clear_all)
        clear_btn.pack(side=tk.LEFT)
    
    def caesar_cipher(self, text, shift, decrypt=False):
        """Perform Caesar Cipher encryption/decryption."""
        if decrypt:
            shift = -shift
        
        result = ""
        for char in text:
            if char.isalpha():
                start = ord('A') if char.isupper() else ord('a')
                shifted = (ord(char) - start + shift) % 26
                result += chr(start + shifted)
            else:
                result += char
        
        return result
    
    def encrypt(self):
        """Encrypt the input text."""
        text = self.input_text.get("1.0", tk.END).strip()
        
        if not text:
            messagebox.showwarning("Warning", "Please enter text to encrypt.")
            return
        
        shift = int(float(self.shift_slider.get()))
        result = self.caesar_cipher(text, shift, decrypt=False)
        self.display_result(result)
    
    def decrypt(self):
        """Decrypt the input text."""
        text = self.input_text.get("1.0", tk.END).strip()
        
        if not text:
            messagebox.showwarning("Warning", "Please enter text to decrypt.")
            return
        
        shift = int(float(self.shift_slider.get()))
        result = self.caesar_cipher(text, shift, decrypt=True)
        self.display_result(result)
    
    def brute_force(self):
        """Try all possible shifts."""
        text = self.input_text.get("1.0", tk.END).strip()
        
        if not text:
            messagebox.showwarning("Warning", "Please enter text for brute force.")
            return
        
        
        brute_window = tk.Toplevel(self.root)
        brute_window.title("Brute Force Decryption - All Shifts")
        brute_window.geometry("800x600")
        brute_window.configure(bg=self.bg_color)
        
        
        frame = ttk.Frame(brute_window)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        
        title = ttk.Label(frame, text="All Possible Decryptions", style='Section.TLabel')
        title.pack(pady=(0, 10))
        
        
        canvas = tk.Canvas(frame, bg=self.input_bg, highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        
        for shift in range(26):
            decrypted = self.caesar_cipher(text, shift, decrypt=True)
            
            shift_frame = ttk.Frame(scrollable_frame)
            shift_frame.pack(fill=tk.X, padx=10, pady=8)
            
            
            shift_label = ttk.Label(shift_frame, text=f"Shift {shift:2d}:", 
                                   width=10, foreground=self.accent_color,
                                   font=('Segoe UI', 10, 'bold'))
            shift_label.pack(side=tk.LEFT)
            
            
            result_label = ttk.Label(shift_frame, text=decrypted,
                                    font=('Courier', 10))
            result_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def display_result(self, result):
        """Display result in result text area."""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", result)
        self.result_text.config(state=tk.DISABLED)
    
    def copy_result(self):
        """Copy result to clipboard."""
        result = self.result_text.get("1.0", tk.END).strip()
        
        if not result:
            messagebox.showwarning("Warning", "No result to copy.")
            return
        
        self.root.clipboard_clear()
        self.root.clipboard_append(result)
        messagebox.showinfo("Success", "Result copied to clipboard!")
    
    def clear_all(self):
        """Clear all input and results."""
        self.input_text.delete("1.0", tk.END)
        self.shift_slider.set(0)
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        self.result_text.config(state=tk.DISABLED)
        self.update_char_counter()


if __name__ == "__main__":
    root = tk.Tk()
    app = CaesarCipherGUI(root)
    root.mainloop()