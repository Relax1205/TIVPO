# calculator.py
import tkinter as tk
from tkinter import messagebox
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор с багами")
        self.root.resizable(False, False)
        self.root.configure(bg="#2c3e50")
        
        # Центрирование окна
        window_width = 350
        window_height = 500
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.expression = ""
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        
        # Хранение оригинальных цветов кнопок
        self.button_colors = {}

        self.create_widgets()

    def create_widgets(self):
        # Основной фрейм
        main_frame = tk.Frame(self.root, bg="#2c3e50", padx=10, pady=10)
        main_frame.pack(expand=True, fill="both")

        # Дисплей с красивым стилем
        display_frame = tk.Frame(main_frame, bg="#34495e", relief="sunken", bd=2)
        display_frame.pack(fill="x", pady=(0, 15))

        display = tk.Entry(
            display_frame,
            textvariable=self.display_var,
            font=("Arial", 24, "bold"),
            justify="right",
            state="readonly",
            width=15,
            bg="#ecf0f1",
            fg="#2c3e50",
            bd=0,
            readonlybackground="#ecf0f1"
        )
        display.pack(padx=10, pady=10, fill="x")

        # Фрейм для кнопок
        button_frame = tk.Frame(main_frame, bg="#2c3e50")
        button_frame.pack(expand=True, fill="both")

        # Кнопки с улучшенным дизайном
        buttons = [
            ('C', 0, 0, '#e74c3c', 'white'),       # 🔴 БАГ 2: C не всегда очищает
            ('÷', 0, 1, '#3498db', 'white'), 
            ('×', 0, 2, '#3498db', 'white'), 
            ('-', 0, 3, '#3498db', 'white'),
            
            ('7', 1, 0, '#ecf0f1', '#2c3e50'), 
            ('8', 1, 1, '#ecf0f1', '#2c3e50'), 
            ('9', 1, 2, '#ecf0f1', '#2c3e50'), 
            ('+', 1, 3, '#3498db', 'white', 1, 2),  # Высокая кнопка
            
            ('4', 2, 0, '#ecf0f1', '#2c3e50'), 
            ('5', 2, 1, '#ecf0f1', '#2c3e50'), 
            ('6', 2, 2, '#ecf0f1', '#2c3e50'),
            
            ('1', 3, 0, '#ecf0f1', '#2c3e50'), 
            ('2', 3, 1, '#ecf0f1', '#2c3e50'), 
            ('3', 3, 2, '#ecf0f1', '#2c3e50'),
            ('=', 3, 3, '#2ecc71', 'white', 2, 1),  # Большая кнопка =
            
            ('0', 4, 0, '#ecf0f1', '#2c3e50', 1, 2),  # Широкая кнопка 0
            ('.', 4, 2, '#ecf0f1', '#2c3e50'),
        ]

        # Настройка сетки
        for i in range(5):
            button_frame.grid_rowconfigure(i, weight=1, uniform="row")
        for i in range(4):
            button_frame.grid_columnconfigure(i, weight=1, uniform="col")

        for button_config in buttons:
            text, row, col, bg_color, fg_color, *args = button_config
            rowspan = args[0] if len(args) > 0 else 1
            colspan = args[1] if len(args) > 1 else 1

            btn = tk.Button(
                button_frame,
                text=text,
                font=("Arial", 16, "bold"),
                bg=bg_color,
                fg=fg_color,
                relief="raised",
                bd=3,
                padx=10,
                pady=10,
                command=lambda t=text: self.on_button_click(t)
            )
            
            # Сохраняем оригинальные цвета
            self.button_colors[btn] = (bg_color, fg_color)
            
            # Эффекты при наведении с правильным сохранением цветов
            btn.bind("<Enter>", lambda e, b=btn: self.on_enter(b))
            btn.bind("<Leave>", lambda e, b=btn: self.on_leave(b))
            
            btn.grid(
                row=row, 
                column=col, 
                rowspan=rowspan,
                columnspan=colspan, 
                padx=3, 
                pady=3, 
                sticky="nsew"
            )

    def on_enter(self, button):
        """Обработчик наведения на кнопку"""
        if button in self.button_colors:
            bg_color, fg_color = self.button_colors[button]
            light_bg = self.lighten_color(bg_color)
            button.configure(bg=light_bg)

    def on_leave(self, button):
        """Обработчик ухода с кнопки"""
        if button in self.button_colors:
            bg_color, fg_color = self.button_colors[button]
            button.configure(bg=bg_color, fg=fg_color)

    def lighten_color(self, color):
        """Осветляет цвет для эффекта наведения"""
        if color.startswith('#'):
            r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
            r = min(255, r + 30)
            g = min(255, g + 30)
            b = min(255, b + 30)
            return f"#{r:02x}{g:02x}{b:02x}"
        return color

    def on_button_click(self, char):
        if char == 'C':
            self.display_var.set("0")
            self.expression = ""
            # 🔴 БАГ 2: Иногда оставляет следы
            self.root.after(500, lambda: self.display_var.set("0" if self.expression == "" else self.expression))

        elif char == '=':
            # 🔴 БАГ 5: Первое нажатие = игнорируется
            if not hasattr(self, 'equals_pressed'):
                self.equals_pressed = True
                return  # Игнорируем первое нажатие

            try:
                # 🔴 БАГ 3: × выполняет сложение
                expr = self.expression.replace('×', '+')
                # 🔴 БАГ 4: Вычисление слева направо
                result = self.left_to_right_eval(expr)
                self.display_var.set(str(result))
                self.expression = str(result)
            except Exception as e:
                # 🔴 БАГ 1: Деление на ноль → inf, а не ошибка
                try:
                    result = eval(self.expression.replace('×', '*').replace('÷', '/'))
                    self.display_var.set(str(result))
                except ZeroDivisionError:
                    self.display_var.set("inf")  # ❌ Должно быть "Ошибка"
                except:
                    self.display_var.set("Error")

        else:
            if self.display_var.get() == "0" or self.display_var.get() == "inf":
                self.display_var.set("")
            self.expression += char
            self.display_var.set(self.expression)

    def left_to_right_eval(self, expr):
        # 🔴 БАГ 4: 2+3×4 = 20, а не 14
        tokens = []
        current = ''
        for c in expr:
            if c in '+-×÷':
                if current:
                    tokens.append(float(current))
                    current = ''
                tokens.append(c)
            else:
                current += c
        if current:
            tokens.append(float(current))

        if not tokens or len(tokens) == 0:
            return 0

        result = tokens[0]
        i = 1
        while i < len(tokens) - 1:
            op = tokens[i]
            val = tokens[i + 1]
            if op == '+':
                result += val
            elif op == '-':
                result -= val
            elif op == '×':
                result += val  # 🔴 БАГ 3: × = +
            elif op == '÷':
                result /= val  # 🔴 БАГ 1: Нет проверки на 0
            i += 2
        return result

def main():
    root = tk.Tk()
    # 🔴 БАГ 6: При малом разрешении интерфейс ломается
    root.geometry("350x500")  # Жёстко заданный размер
    app = Calculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()