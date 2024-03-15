import tkinter as tk

root = tk.Tk()

root.title("Calculator")

def get_inputs():
    try:
        num1 = float(entry1.get())
        num2 = float(entry2.get())
        print("Numeric Input 1:", num1)
        print("Numeric Input 2:", num2)
        return num1, num2
    except ValueError:
        result_label.config(text="Invalid input. Please enter numeric values.")
        return None, None

entry1 = tk.Entry(root, validate="key")
entry1.pack()

entry2 = tk.Entry(root, validate="key")
entry2.pack()

result_label = tk.Label(root, text="")
result_label.pack()

def addition():
    num1, num2 = get_inputs()
    if num1 is not None and num2 is not None:
        result = num1 + num2
        result_label.config(text="{:.2f}".format(result))

def subtraction():
    num1, num2 = get_inputs()
    if num1 is not None and num2 is not None:
        result = num1 - num2
        result_label.config(text="{:.2f}".format(result))

# Addition button
add_button = tk.Button(root, text="Add", command=addition)
add_button.pack()

# Subtraction button
sub_button = tk.Button(root, text="Subtract", command=subtraction)
sub_button.pack()

root.mainloop()
