from tkinter import *
from tkinter import messagebox
from mojang import Client

authGui = Tk()
authGui.title("Username Sniper")
authGui.geometry('400x300')
authGui.resizable(False, False)

def attemptLogin():
    username = authUser.get()
    password = authPass.get()

    try:
        client = Client(username, password)
        user_profile = client.get_profile()

        print("Authenticated as:", user_profile.name)
        messagebox.showinfo("Login Status", "Login Successful")

        openNewWindow(client, user_profile)



    except Exception as e:
        messagebox.showerror("Login Status", "Login Failed")

def openNewWindow(client, user_profile):
    client.get_profile()
    authGui.destroy()
    usernameGui = Tk()
    usernameGui.title(f"Authenticated as: {user_profile.name}")
    usernameGui.geometry('417x231')
    usernameGui.resizable(False, False)

    consoleFrame = Frame(usernameGui)
    consoleFrame.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=11)
    consoleFrame.grid(column=0, row=1, columnspan=2)

    consoleText = Text(consoleFrame, height=8, width=40, wrap='word', state='disabled',)
    consoleText.pack(side=LEFT, fill=BOTH)

    scrollbar = Scrollbar(consoleFrame, command=consoleText.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    consoleText.config(yscrollcommand=scrollbar.set)

    def logToConsole(message):
        consoleText.config(state='normal')
        consoleText.insert(END, message + '\n')
        consoleText.config(state='disabled')
        consoleText.yview(END)

    def performCheck():
        targetUser = usernameBox.get()
        result = client.is_username_available(targetUser)

        if result:
            logToConsole(f"{targetUser} is available")
            return True
        else:
            logToConsole(f"{targetUser} is not available")
            return False

    def snipeyTime():
        targetUser = usernameBox.get()
        if performCheck():
            logToConsole(f"Attempting to change username to {targetUser}...")
            try:
                response = client.change_username(targetUser)
                if response.get('success'):
                    logToConsole(f"{targetUser} has been sniped")
                else:
                    logToConsole(f"{targetUser} failed to snipe: {response.get('error', 'Unknown Error')}")
            except Exception as e:
                logToConsole(f"ERROR {e}")
        else:
            logToConsole(f"Attempting to snipe username again...")
            usernameBox.after(1000, snipeyTime)

    topFrame = Frame(usernameGui)
    topFrame.grid(row=0, column=0, padx=10, pady=10)

    usernamePrompt = Label(topFrame, text="Username:",font=("Arial", 16, "bold"))
    usernamePrompt.grid(column=0, row=0)

    usernameBox = Entry(topFrame, font=("Arial", 16, "bold"), width=15)
    usernameBox.grid(column=1, row=0)

    usernameCheck = Button(topFrame, text="Check Availability", anchor='center',font=("Arial", 16, "bold"), command=performCheck)
    usernameCheck.grid(column=0, row=1)

    usernameSnipe = Button(topFrame, text="Snipe", anchor='center', font=("Arial", 16, "bold"), width=15, command=snipeyTime)
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

auth = Button(authGui, text="Authenticate", font = ("Arial", 16, "bold"), width=30, height=1, activebackground="green3", disabledforeground="gray15", bg="gray62", command=attemptLogin)
auth.grid(column =0, row=5)

authGui.mainloop()