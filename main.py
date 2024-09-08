from tkinter import *
from tkinter import messagebox
from mojang import Client

authGui = Tk()
authGui.title("Username Sniper")
authGui.geometry('400x300')
authGui.resizable(False, False)

def attempt_Login():
    username = authUser.get()
    password = authPass.get()

    try:
        client = Client(username, password)
        user_profile = client.get_profile()

        print("Authenticated as:", user_profile.name)
        messagebox.showinfo("Login Status", "Login Successful")

        open_new_window(client, user_profile)



    except Exception as e:
        messagebox.showerror("Login Status", "Login Failed")

def open_new_window(client, user_profile):
    client.get_profile()
    authGui.destroy()
    usernameGui = Tk()
    usernameGui.title(f"Authenticated as: {user_profile.name}")
    usernameGui.geometry('417x231')
    usernameGui.resizable(False, False)

    console_frame = Frame(usernameGui)
    console_frame.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=11)
    console_frame.grid(column=0, row=1, columnspan=2)

    console_text = Text(console_frame, height=8, width=40, wrap='word', state='disabled',)
    console_text.pack(side=LEFT, fill=BOTH)

    scrollbar = Scrollbar(console_frame, command=console_text.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    console_text.config(yscrollcommand=scrollbar.set)

    def log_to_console(message):
        console_text.config(state='normal')
        console_text.insert(END, message + '\n')
        console_text.config(state='disabled')
        console_text.yview(END)

    def performCheck():
        targetUser = usernameBox.get()
        result = client.is_username_available(targetUser)

        if result:
            log_to_console(f"{targetUser} is available")
            return True
        else:
            log_to_console(f"{targetUser} is not available")
            return False

    def snipeyTime():
        targetUser = usernameBox.get()
        if performCheck():
            log_to_console(f"Attempting to change username to {targetUser}...")
            try:
                response = client.change_username(targetUser)
                if response.get('success'):
                    log_to_console(f"{targetUser} has been sniped")
                else:
                    log_to_console(f"{targetUser} failed to snipe: {response.get('error', 'Unknown Error')}")
            except Exception as e:
                log_to_console(f"ERROR {e}")
        else:
            log_to_console(f"Attempting to snipe username again...")
            usernameBox.after(1000, snipeyTime)

    top_frame = Frame(usernameGui)
    top_frame.grid(row=0, column=0, padx=10, pady=10)

    usernamePrompt = Label(top_frame, text="Username:",font=("Arial", 16, "bold"))
    usernamePrompt.grid(column=0, row=0)

    usernameBox = Entry(top_frame, font=("Arial", 16, "bold"), width=15)
    usernameBox.grid(column=1, row=0)

    usernameCheck = Button(top_frame, text="Check Availability", anchor='center',font=("Arial", 16, "bold"), command=performCheck)
    usernameCheck.grid(column=0, row=1)

    usernameSnipe = Button(top_frame, text="Snipe", anchor='center', font=("Arial", 16, "bold"), width=15, command=snipeyTime)
    usernameSnipe.grid(column=1, row=1)



userPrompt = Label(authGui, text = "Username: ", anchor='center',font=("Arial", 16, "bold"))
(userPrompt.grid(column =0, row=0))

authUser = Entry(authGui, width=20, font=("Arial", 16, "bold"))
authUser.grid(column =0, row=1)

passPrompt = Label(authGui, text = "Password: ", anchor='center',font=("Arial", 16, "bold"))
(passPrompt.grid(column =0, row=2))

authPass = Entry(authGui, width=20, font=("Arial", 16, "bold"), show="*")
authPass.grid(column =0, row=3)

lineBreak = Label(authGui, text="---------------------------------------", font=("Arial", 16, "bold"))
lineBreak.grid(column =0, row=4)

auth = Button(authGui, text="Authenticate", font = ("Arial", 16, "bold"), width=30, height=1, activebackground="green3", disabledforeground="gray15", bg="gray62", command=attempt_Login)
auth.grid(column =0, row=5)

authGui.mainloop()