import tkinter as tk 

root = tk.Tk()

root.title("Calculator")

def get_inputs():
    try:
        num1 = float(entry1.get())
        num2 = float(entry2.get())
        print("Numeric Input 1:", num1)
        print("Numeric Input 2:", num2)
    except ValueError:
        print("Invalid input. Please enter numeric values.")

entry1 = tk.Entry(root, validate="key")
entry1.pack()

entry2 = tk.Entry(root, validate="key")
entry2.pack()

# Create a button to get the inputs

button = tk.Button(root, text="Get Inputs", command=get_inputs)
button.pack()


# Addition button 
button = tk.Button(root, text="Add", command=addition)
button.pack()

# Subtraction

root.mainloop()