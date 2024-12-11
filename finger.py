import random
from tkinter import *
from tkinter import ttk, filedialog
from twilio.rest import Client

# Dynamic account database: Each account stores phone number and fingerprint path.
account_database = {}
current_user = {}
generated_otp = None  # Store the OTP for verification

# Twilio credentials (replace with your actual credentials)
TWILIO_SID = "ACecc81d875209774176a9d315fd713644"
TWILIO_AUTH_TOKEN = "06684add3f845b5084b05477bde17e3c"
TWILIO_PHONE_NUMBER = "+12569527829"  # Replace with your Twilio number


# Function to send OTP
def send_otp(phone_number):
    global generated_otp
    generated_otp = random.randint(100000, 999999)
    print(f"Generated OTP (debugging): {generated_otp}")  # Debugging
    try:
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=f"Your ATM OTP is: {generated_otp}",
            from_= +12569527829,
            to=+919342495378
        )
    except Exception as e:
        print(f"Failed to send OTP: {e}")


# Function to proceed to the next window
def show_window(window_to_open, current_window=None):
    if current_window:
        current_window.destroy()
    window_to_open()


# Page 1: Bank Selection
def bank_selection_page():
    def proceed_to_registration():
        show_window(registration_page, bank_window)

    bank_window = Tk()#label,icons and text
    bank_window.title("Bank Selection")
    bank_window.geometry('739x415')
    bank_window.configure(bg="SkyBlue1")

    Label(bank_window, text="Please Select Your Bank", font=("Times New Roman", 30)).grid(row=0, column=0, pady=10)
    bank_names = [
        "Indian Overseas Bank",
        "Bank Of India",
        "Central Bank of India",
        "Punjab National Bank",
        "Oriental Bank of Commerce",
        "Bhartiya Mahila Bank",
        "State Bank of India",
        "Andhra Bank"
    ]

    for i, bank_name in enumerate(bank_names, start=1):
        Checkbutton(bank_window, text=bank_name, font=("Times New Roman", 10)).grid(row=i, sticky=W, padx=20)

    Button(bank_window, text="Proceed", font=("Arial", 12), bg="green", fg="white", command=proceed_to_registration).grid(row=10, pady=20)
    bank_window.mainloop()


# Page 2: Registration Page
def registration_page():
    def register_account():
        account_number = account_entry.get().strip()
        phone_number = phone_entry.get().strip()

        if account_number and phone_number and uploaded_fingerprint_path:
            if account_number not in account_database:
                account_database[account_number] = {
                    "phone": phone_number,
                    "fingerprint": uploaded_fingerprint_path
                }
                lbl_status.config(text="Account registered successfully!", fg="green")
            else:
                lbl_status.config(text="Account number already exists.", fg="red")
        else:
            lbl_status.config(text="Please fill in all fields and upload fingerprint.", fg="red")

    def upload_fingerprint():
        nonlocal uploaded_fingerprint_path
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if file_path:
            uploaded_fingerprint_path = file_path
            lbl_fingerprint_status.config(text="Fingerprint uploaded!", fg="green")
        else:
            lbl_fingerprint_status.config(text="Fingerprint upload canceled.", fg="red")

    uploaded_fingerprint_path = None
    reg_window = Tk()#label,icons and text
    reg_window.title("Register Account")
    reg_window.geometry('500x500')
    reg_window.configure(bg="lightblue")

    Label(reg_window, text="Register Account", font=("Arial", 14), bg="lightblue").pack(pady=10)

    Label(reg_window, text="Enter Account Number:", font=("Arial", 12), bg="lightblue").pack()
    account_entry = Entry(reg_window, font=("Arial", 12)) #regitered details after used
    account_entry.pack(pady=5)# padding 

    Label(reg_window, text="Enter Phone Number:", font=("Arial", 12), bg="lightblue").pack()
    phone_entry = Entry(reg_window, font=("Arial", 12))
    phone_entry.pack(pady=5)

    Label(reg_window, text="Upload Fingerprint:", font=("Arial", 12), bg="lightblue").pack()
    Button(reg_window, text="Upload Fingerprint", font=("Arial", 12), command=upload_fingerprint).pack(pady=10)
    lbl_fingerprint_status = Label(reg_window, text="", font=("Arial", 10), bg="lightblue")
    lbl_fingerprint_status.pack(pady=5)

    Button(reg_window, text="Register", font=("Arial", 12), bg="green", fg="white", command=register_account).pack(pady=10)
    lbl_status = Label(reg_window, text="", font=("Arial", 10), bg="lightblue")
    lbl_status.pack(pady=10)

    Button(reg_window, text="Go to Login", font=("Arial", 12), bg="blue", fg="white", command=lambda: show_window(login_page, reg_window)).pack(pady=10)

    reg_window.mainloop()


# Page 3: Login Page
def login_page():
    def login():
        phone_number = phone_entry.get().strip()  # Get the entered phone number
        if phone_number and uploaded_fingerprint_path:  # Check if phone number and fingerprint are provided
            for account_number, details in account_database.items():
                if details["phone"] == phone_number:  # Match phone number
                    if uploaded_fingerprint_path == details["fingerprint"]:  # Match fingerprint
                        current_user["account"] = account_number
                        current_user["phone"] = phone_number
                        lbl_status.config(text="Login successful!", fg="green")
                        show_window(fingerprint_page, login_window)  # Proceed to the next page
                        return
                    else:
                        lbl_status.config(text="Fingerprint mismatch. Access denied.", fg="red")
                        return
            lbl_status.config(text="Phone number not found.", fg="red")
        else:
            lbl_status.config(text="Phone number or fingerprint not provided.", fg="red")

    def upload_fingerprint():
        nonlocal uploaded_fingerprint_path
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if file_path:
            uploaded_fingerprint_path = file_path
            lbl_fingerprint_status.config(text="Fingerprint uploaded for login!", fg="green")
        else:
            lbl_fingerprint_status.config(text="Fingerprint upload canceled.", fg="red")

    uploaded_fingerprint_path = None
    login_window = Tk()
    login_window.title("Login")
    login_window.geometry('500x500')
    login_window.configure(bg="lightblue")

    Label(login_window, text="Login", font=("Arial", 14), bg="lightblue").pack(pady=10)

    Label(login_window, text="Enter Phone Number:", font=("Arial", 12), bg="lightblue").pack()  # Updated to phone number
    phone_entry = Entry(login_window, font=("Arial", 12))
    phone_entry.pack(pady=5)

    Label(login_window, text="Upload Fingerprint:", font=("Arial", 12), bg="lightblue").pack()
    Button(login_window, text="Upload Fingerprint", font=("Arial", 12), command=upload_fingerprint).pack(pady=10)
    lbl_fingerprint_status = Label(login_window, text="", font=("Arial", 10), bg="lightblue")
    lbl_fingerprint_status.pack(pady=5)

    Button(login_window, text="Login", font=("Arial", 12), bg="blue", fg="white", command=login).pack(pady=10)
    lbl_status = Label(login_window, text="", font=("Arial", 10), bg="lightblue")
    lbl_status.pack(pady=10)

    login_window.mainloop()



# Page 4: Fingerprint and OTP Verification
def fingerprint_page():
    def upload_fingerprint():
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if file_path:
            lbl_status.config(text=f"Fingerprint uploaded: {file_path}", fg="green")
            send_otp(current_user["phone"])
        else:
            lbl_status.config(text="Fingerprint upload canceled.", fg="red")

    def verify_otp():
        entered_otp = otp_entry.get().strip()
        if entered_otp and int(entered_otp) == generated_otp:
            lbl_status.config(text="OTP verified! Proceeding to ATM services.", fg="green")
            show_window(atm_process_page, fingerprint_window)
        else:
            lbl_status.config(text="Incorrect OTP. Please try again.", fg="red")

    fingerprint_window = Tk()
    fingerprint_window.title("Fingerprint and OTP Verification")
    fingerprint_window.geometry('500x400')
    fingerprint_window.configure(bg="purple1")

    Label(fingerprint_window, text="Upload Your Fingerprint", font=("Arial", 14), bg="purple1", fg="white").pack(pady=10)
    Button(fingerprint_window, text="Upload Fingerprint", font=("Arial", 12), command=upload_fingerprint).pack(pady=10)

    Label(fingerprint_window, text="Enter OTP:", font=("Arial", 12), bg="purple1", fg="white").pack(pady=10)
    otp_entry = Entry(fingerprint_window, font=("Arial", 12))
    otp_entry.pack(pady=5)

    Button(fingerprint_window, text="Verify OTP", font=("Arial", 12), command=verify_otp).pack(pady=10)
    lbl_status = Label(fingerprint_window, text="", font=("Arial", 10), bg="purple1", fg="white")
    lbl_status.pack(pady=10)

    fingerprint_window.mainloop()


# Page 5: ATM Process
def atm_process_page():
    current_user['balance'] = current_user.get('balance', 500)  # Default balance

    def withdrawal():
        def process_withdrawal():
            amount = int(amount_entry.get().strip())
            if 0 < amount <= current_user['balance']:
                current_user['balance'] -= amount
                lbl_status.config(text=f"₹{amount} withdrawn successfully! Remaining Balance: ₹{current_user['balance']}", fg="green")
            else:
                lbl_status.config(text="Insufficient balance or invalid amount.", fg="red")

        withdrawal_window = Toplevel(atm_window)
        withdrawal_window.title("Withdrawal")
        withdrawal_window.geometry('400x200')
        Label(withdrawal_window, text="Enter amount to withdraw:", font=("Arial", 12)).pack(pady=10)
        amount_entry = Entry(withdrawal_window, font=("Arial", 12))
        amount_entry.pack(pady=10)
        Button(withdrawal_window, text="Withdraw", font=("Arial", 12), command=process_withdrawal).pack(pady=10)
        lbl_status = Label(withdrawal_window, text="", font=("Arial", 10))
        lbl_status.pack(pady=10)

    def deposit():
        def process_deposit():
            amount = int(amount_entry.get().strip())
            if amount > 0:
                current_user['balance'] += amount
                lbl_status.config(text=f"₹{amount} deposited successfully! Total Balance: ₹{current_user['balance']}", fg="green")
            else:
                lbl_status.config(text="Enter a valid amount.", fg="red")

        deposit_window = Toplevel(atm_window)
        deposit_window.title("Deposit")
        deposit_window.geometry('400x200')
        Label(deposit_window, text="Enter amount to deposit:", font=("Arial", 12)).pack(pady=10)
        amount_entry = Entry(deposit_window, font=("Arial", 12))
        amount_entry.pack(pady=10)
        Button(deposit_window, text="Deposit", font=("Arial", 12), command=process_deposit).pack(pady=10)
        lbl_status = Label(deposit_window, text="", font=("Arial", 10))
        lbl_status.pack(pady=10)

    def balance():
        lbl_status.config(text=f"Your current balance is ₹{current_user['balance']}", fg="blue")

    atm_window = Tk()
    atm_window.title("ATM Process")
    atm_window.geometry('500x400')
    atm_window.configure(bg="lightblue")

    Label(atm_window, text="ATM Services", font=("Arial", 18), bg="lightblue", fg="black").pack(pady=10)
    Button(atm_window, text="Withdrawal", font=("Arial", 12), command=withdrawal).pack(pady=10)
    Button(atm_window, text="Deposit", font=("Arial", 12), command=deposit).pack(pady=10)
    Button(atm_window, text="Check Balance", font=("Arial", 12), command=balance).pack(pady=10)
    Button(atm_window, text="Exit", font=("Arial", 12), bg="red", fg="white", command=atm_window.destroy).pack(pady=10)

    lbl_status = Label(atm_window, text="", font=("Arial", 10), bg="lightblue")
    lbl_status.pack(pady=10)

    atm_window.mainloop()


# Start the application with the bank selection page
bank_selection_page()