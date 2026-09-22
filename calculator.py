import tkinter as tk
import ast
import operator


# ==========================================
# SAFE CALCULATOR ENGINE
# ==========================================

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def safe_calculate(expression):

    try:
        tree = ast.parse(expression, mode="eval")
        return evaluate_node(tree.body)

    except ZeroDivisionError:
        raise ValueError("Cannot divide by zero")

    except Exception:
        raise ValueError("Invalid expression")


def evaluate_node(node):

    # Numbers
    if isinstance(node, ast.Constant):

        if isinstance(node.value, (int, float)):
            return node.value

        raise ValueError("Invalid number")

    # Addition, subtraction, multiplication, division
    if isinstance(node, ast.BinOp):

        left = evaluate_node(node.left)
        right = evaluate_node(node.right)

        operation = OPERATORS.get(type(node.op))

        if operation is None:
            raise ValueError("Invalid operator")

        return operation(left, right)

    # Positive / negative numbers
    if isinstance(node, ast.UnaryOp):

        if isinstance(node.op, ast.USub):
            return -evaluate_node(node.operand)

        if isinstance(node.op, ast.UAdd):
            return evaluate_node(node.operand)

    raise ValueError("Invalid expression")


# ==========================================
# WINDOW
# ==========================================

window = tk.Tk()

window.title("Python Calculator")

window.geometry("720x650")

window.resizable(False, False)

window.configure(bg="#0f0f0f")


# ==========================================
# MAIN FRAME
# ==========================================

main_frame = tk.Frame(
    window,
    bg="#0f0f0f"
)

main_frame.pack(
    expand=True,
    fill="both",
    padx=15,
    pady=15
)


# ==========================================
# CALCULATOR FRAME
# ==========================================

calculator_frame = tk.Frame(
    main_frame,
    bg="#0f0f0f"
)

calculator_frame.pack(
    side="left",
    expand=True,
    fill="both"
)


# ==========================================
# DISPLAY
# ==========================================

display = tk.Entry(
    calculator_frame,
    font=("Arial", 34),
    bg="#181818",
    fg="white",
    insertbackground="white",
    justify="right",
    borderwidth=0
)

display.pack(
    fill="x",
    ipady=25,
    padx=5,
    pady=(10, 20)
)

# Give keyboard focus to display
display.focus_set()


# ==========================================
# CALCULATOR FUNCTIONS
# ==========================================

def insert_value(value):

    display.insert(
        tk.END,
        value
    )


def clear():

    display.delete(
        0,
        tk.END
    )


def delete():

    current = display.get()

    display.delete(
        0,
        tk.END
    )

    display.insert(
        0,
        current[:-1]
    )


def calculate():

    expression = display.get()

    if not expression:
        return

    try:

        result = safe_calculate(expression)

        if isinstance(result, float) and result.is_integer():
            result = int(result)

        display.delete(
            0,
            tk.END
        )

        display.insert(
            0,
            str(result)
        )

        add_history(
            expression,
            result
        )

    except ValueError as error:

        display.delete(
            0,
            tk.END
        )

        display.insert(
            0,
            str(error)
        )


def percentage():

    try:

        value = float(display.get())

        result = value / 100

        if result.is_integer():
            result = int(result)

        display.delete(
            0,
            tk.END
        )

        display.insert(
            0,
            str(result)
        )

    except:

        display.delete(
            0,
            tk.END
        )

        display.insert(
            0,
            "Error"
        )


def plus_minus():

    try:

        value = float(display.get())

        value = -value

        if value.is_integer():
            value = int(value)

        display.delete(
            0,
            tk.END
        )

        display.insert(
            0,
            str(value)
        )

    except:

        display.delete(
            0,
            tk.END
        )

        display.insert(
            0,
            "Error"
        )


# ==========================================
# HISTORY
# ==========================================

def add_history(expression, result):

    history.insert(
        tk.END,
        f"{expression} = {result}"
    )


def clear_history():

    history.delete(
        0,
        tk.END
    )


# ==========================================
# BUTTON FRAME
# ==========================================

button_frame = tk.Frame(
    calculator_frame,
    bg="#0f0f0f"
)

button_frame.pack(
    expand=True,
    fill="both"
)


# ==========================================
# BUTTONS
# ==========================================

buttons = [

    ["AC", "⌫", "%", "÷"],

    ["7", "8", "9", "×"],

    ["4", "5", "6", "−"],

    ["1", "2", "3", "+"],

    ["+/-", "0", ".", "="]

]


# ==========================================
# COLORS
# ==========================================

number_color = "#292929"

operator_color = "#ff9500"

function_color = "#555555"

text_color = "#ffffff"


# ==========================================
# CREATE BUTTONS
# ==========================================

for row_index, row in enumerate(buttons):

    for column_index, value in enumerate(row):

        actual_value = value

        if value == "×":
            actual_value = "*"

        elif value == "÷":
            actual_value = "/"

        elif value == "−":
            actual_value = "-"


        # Determine button action

        if value == "AC":

            command = clear
            button_color = function_color

        elif value == "⌫":

            command = delete
            button_color = function_color

        elif value == "%":

            command = percentage
            button_color = function_color

        elif value == "+/-":

            command = plus_minus
            button_color = function_color

        elif value == "=":

            command = calculate
            button_color = operator_color

        elif value in ["÷", "×", "−", "+"]:

            command = lambda value=actual_value: insert_value(value)
            button_color = operator_color

        else:

            command = lambda value=actual_value: insert_value(value)
            button_color = number_color


        button = tk.Button(

            button_frame,

            text=value,

            font=("Arial", 20, "bold"),

            bg=button_color,

            fg=text_color,

            activebackground="#777777",

            activeforeground="white",

            borderwidth=0,

            command=command
        )

        button.grid(

            row=row_index,

            column=column_index,

            sticky="nsew",

            padx=5,

            pady=5
        )


# ==========================================
# BUTTON SIZING
# ==========================================

for row in range(5):

    button_frame.rowconfigure(
        row,
        weight=1
    )


for column in range(4):

    button_frame.columnconfigure(
        column,
        weight=1
    )


# ==========================================
# HISTORY PANEL
# ==========================================

history_frame = tk.Frame(
    main_frame,
    bg="#181818",
    width=240
)

history_frame.pack(
    side="right",
    fill="y",
    padx=(15, 0)
)

history_frame.pack_propagate(False)


history_title = tk.Label(
    history_frame,
    text="HISTORY",
    font=("Arial", 15, "bold"),
    bg="#181818",
    fg="white"
)

history_title.pack(
    pady=15
)


history = tk.Listbox(
    history_frame,
    font=("Arial", 11),
    bg="#222222",
    fg="white",
    selectbackground="#ff9500",
    borderwidth=0
)

history.pack(
    expand=True,
    fill="both",
    padx=10,
    pady=10
)


clear_history_button = tk.Button(
    history_frame,
    text="Clear History",
    font=("Arial", 11, "bold"),
    bg="#333333",
    fg="white",
    activebackground="#555555",
    borderwidth=0,
    command=clear_history
)

clear_history_button.pack(
    fill="x",
    padx=10,
    pady=10
)


# ==========================================
# KEYBOARD SUPPORT
# ==========================================

def keyboard_input(event):

    key = event.keysym

    # Only handle special keys here.
    # Normal numbers/operators are handled
    # automatically by the Entry widget.

    if key == "Return":

        calculate()

        return "break"

    elif key == "BackSpace":

        delete()

        return "break"

    elif key == "Escape":

        clear()

        return "break"


# Bind only special keyboard keys
window.bind(
    "<Return>",
    keyboard_input
)

window.bind(
    "<BackSpace>",
    keyboard_input
)

window.bind(
    "<Escape>",
    keyboard_input
)


# ==========================================
# START APPLICATION
# ==========================================

window.mainloop()