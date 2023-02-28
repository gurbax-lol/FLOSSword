from tkinter import Tk, Canvas, PhotoImage, Label, Button, Entry, E, W, messagebox
from datetime import datetime
from random import randint, choice, shuffle
from pyperclip import copy
from json import dump, load


# TODO: Add functionality to save multiple logins for the same website
# TODO: Add functionality to display multiple logins for the same website
# TODO: Make it so that when the program crashes it does not delete everything


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    number_of_letters = randint(8, 10)
    number_of_symbols = randint(2, 4)
    number_of_numbers = randint(2, 4)

    password_list = [choice(letters) for _ in range(number_of_letters)]
    password_list += [choice(symbols) for _ in range(number_of_symbols)]
    password_list += [choice(numbers) for _ in range(number_of_numbers)]

    shuffle(password_list)
    password = "".join(password_list)
    password_entry.delete(0, "end")
    password_entry.insert(0, password)
    copy(password)
    conformation_label.config(text="Copied")
    window.after(5000, clear_confirmation_label)


# ---------------------------- SAVE + FIND PASSWORD ------------------------------- #
update_password = False


def save_password():
    # Grab data
    website = website_entry.get().lower()
    email = email_entry.get()
    password = password_entry.get()
    # Validate data
    if website == "" or email == "" or password == "":
        messagebox.showwarning(title="Oops...", message="Please don't leave any fields empty!")
    else:
        # Save it to the DO_NOT_DELETE_data.json file
        now = datetime.now()
        date = now.strftime('%B %d, %Y')
        time = now.strftime('%H:%M:%S')
        new_data = {
            website: {
                "email": email,
                "password": password,
                "date": date,
                "time": time
            }
        }
        try:  # Open a DO_NOT_DELETE_data.json file
            with open(file="DO_NOT_DELETE_data.json", mode="r") as file:
                data = load(file)  # Read its contents and assign them to the data variable
        except FileNotFoundError:  # If the file does not exist,
            with open(file="DO_NOT_DELETE_data.json", mode="w") as file:
                dump(obj=new_data, fp=file, indent=4)  # create one and save new_data into it
        else:  # If it does exist,
            with open(file="DO_NOT_DELETE_data.json", mode="w") as file:
                if website in data and email == data[website]["email"]:
                    global update_password
                    update_password = messagebox.askyesno(title="Update password?",
                                                          message=f"A password for {email} on {website} "
                                                                  f"already exists.\nDo you want to update it?")
                    if update_password:
                        data.update(new_data)  # Update the data loaded from the try block above
                        dump(obj=data, fp=file, indent=4)  # Save it into the file
                    else:
                        dump(obj=data, fp=file, indent=4)  # Save data with no changes to the file
                        copy(data[website]["password"])  # Copy old password
                elif website in data:
                    data.append(new_data)  # Update the data loaded from the try block above
                    dump(obj=data, fp=file, indent=4)  # Save it into the file
                else:
                    data.update(new_data)  # Update the data loaded from the try block above
                    dump(obj=data, fp=file, indent=4)  # Save it into the file
        finally:  # Clear data in the UI
            website_entry.delete(0, 'end')
            password_entry.delete(0, 'end')
            website_entry.focus()
            if update_password:
                conformation_label.config(text="Done")
            else:
                conformation_label.config(text="Copied")
            window.after(5000, clear_confirmation_label)


def find_password():
    website = website_entry.get()
    try:  # Open a DO_NOT_DELETE_data.json file and save existing data
        with open(file="DO_NOT_DELETE_data.json", mode="r") as file:
            data = load(file)  # Read
    except FileNotFoundError:  # If it does not exist, say message
        messagebox.showinfo(title="Welcome!", message="You haven't saved any passwords yet. "
                                                      "You can use this button to search for passwords "
                                                      "that you have saved.")
    else:
        if website in data:
            # if multiple instances of website in data:
            # check if user email matches any
                # if yes, copy pass of that email
                # else show user list of emails, and ask them to type in the previous screen
            # else
            email = data[website]["email"]
            password = data[website]["password"]
            date = data[website]["date"]
            messagebox.showinfo(title=f"{website} Password Copied", message=f"Email / Username: {email}\n"
                                                                            f"Password: {password}\n"
            # Todo: Save this as Feb 2, 2019 
                                                                            f"Saved on: {date}")
            copy(password)
        else:
            messagebox.showinfo(title=f"{website} Login Details", message=f"No passwords saved for {website}")
    finally:
        website_entry.delete(0, 'end')
        website_entry.focus()


# ---------------------------- UI SETUP ------------------------------- #

DEFAULT_EMAIL = "demo@example.com"
NAVY_BLUE = "#020D1E"
BLACK = "#222831"
GREY = "#EEEEEE"
WHITE = "#FFFFFF"
# TODO: Load external font, paired with logo font
LARGE_FONT = ("Arial Narrow", 12, "bold")
SMALL_FONT = ("Arial Narrow", 12, "normal")
BUTTON_FONT = ("Arial Narrow", 9, "normal")


def on_enter(event):
    event.widget["background"] = WHITE


def on_leave(event):
    event.widget["background"] = GREY


def clear_confirmation_label():
    conformation_label.config(text="")


window = Tk()
window.title("FLOSSword: The Offline Password Manager")
window.iconbitmap(r"images/favicon.ico")
window.config(padx=50, pady=30, bg=NAVY_BLUE)

canvas = Canvas(width=200, height=200, bg=NAVY_BLUE, highlightthickness=0)
logo_img = PhotoImage(file=r"images/logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

website_label = Label(text="Website:", font=LARGE_FONT, bg=NAVY_BLUE, fg=WHITE)
website_label.grid(row=1, column=0, sticky=E)
website_entry = Entry(width=20, fg=BLACK, bg=GREY, font=SMALL_FONT)
website_entry.grid(row=1, column=1, sticky=W, pady=5)
website_entry.focus()
website_entry.bind("<Return>", (lambda event: find_password()))

search_button = Button(text="Search", width=16, command=find_password, font=BUTTON_FONT, bd=0, cursor="hand2")
search_button.grid(row=1, column=2, sticky=E, pady=5)
search_button.bind("<Enter>", on_enter)
search_button.bind("<Leave>", on_leave)

email_label = Label(text="Email / Username:", font=LARGE_FONT, bg=NAVY_BLUE, fg=WHITE)
email_label.grid(row=2, column=0, sticky=E)
email_entry = Entry(width=35, fg=BLACK, bg=GREY, font=SMALL_FONT)
email_entry.grid(row=2, column=1, columnspan=2, pady=5)
# TODO: Autoload the last saved email
email_entry.insert(0, DEFAULT_EMAIL)

password_label = Label(text="Password:", font=LARGE_FONT, bg=NAVY_BLUE, fg=WHITE)
password_label.grid(row=3, column=0, sticky=E)
password_entry = Entry(width=20, fg=BLACK, bg=GREY, font=SMALL_FONT)
password_entry.grid(row=3, column=1, sticky=W, pady=5)
password_entry.bind("<Return>", (lambda event: save_password()))

generate_button = Button(text="Generate", width=16, command=generate_password, font=BUTTON_FONT, bd=0, cursor="hand2")
generate_button.grid(row=3, column=2, sticky=E, pady=5)
generate_button.bind("<Enter>", on_enter)
generate_button.bind("<Leave>", on_leave)

save_button = Button(text="Save", width=36, command=save_password, font=BUTTON_FONT, bd=0, cursor="hand2")
save_button.grid(row=5, column=1, columnspan=2, sticky=W, pady=10)
save_button.bind("<Enter>", on_enter)
save_button.bind("<Leave>", on_leave)

conformation_label = Label(text="", bg=NAVY_BLUE, fg=GREY, font=SMALL_FONT)
conformation_label.grid(row=5, column=2, sticky=E)
window.mainloop()