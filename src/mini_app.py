import customtkinter as ctk

app = ctk.CTk()

app.geometry("300x200")
app.title("MiniMap App")

label = ctk.CTkLabel(app, text="Welcome to MiniMap!")
label.pack(pady=20)

button = ctk.CTkButton(app, text="Click Me!", command=lambda: label.configure(text="Button clicked!"))
button.pack(pady=10)

app.mainloop()
