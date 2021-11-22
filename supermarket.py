import tkinter.ttk
from tkinter import font, messagebox
from tkinter import filedialog as fd

import MySQLdb
from mysql.connector import connect
import PIL.Image, PIL.ImageTk
from tkinter import *
from tkinter.scrolledtext import ScrolledText


main_page = Tk()
main_page.geometry("1920x1080")
home_page = Frame(main_page, height=700)
font_style = font.Font(family='Helvetica', size=16)



def database_login():
    user_name = username_entry.get()
    pass_word = password_entry.get()
    connect_database(user_name, pass_word, radio_value)

def select_image():
    filetypes = (
        ("image/jpg", "*.jpg"),
        ("image/png", "*.png")
    )
    file = fd.askopenfilename(title="Open a file", initialdir="/", filetypes=filetypes)
    image_pic_var.set(f'{file}')

def store_database():
    db = connect(host="localhost", username="root", password="11111", db="items")
    cursor = db.cursor()
    image_url = (image_pic_var.get()).split("/")[-1]
    cursor.execute(f"INSERT INTO items.food(Name, Price, image)VALUES('mab', 6, 'yes.png')")

def admin_panel():
    home_page.place_forget()
    Admin_page.place_forget()
    page = Frame(main_page)
    add_item_label = Label(page, text="ADD ITEM", font=font_style)
    add_item_label.pack()
    space_label = Label(page, text=" ", font=font_style)
    space_label.pack()
    global image_name_var
    image_name_var = StringVar()
    image_name_var.set("Name of item")
    item_name_label = Label(page, text="Item name", font=font_style)
    item_name_label.pack()
    image_name = Entry(page, fg="gray", font=font_style, textvariable=image_name_var)
    image_name.pack()
    space_label = Label(page, text=" ", font=font_style)
    space_label.pack()
    global image_pic_var
    image_pic_var = StringVar()
    image_pic_var.set("Click on button to add an image")
    item_image_label = Label(page, text="Item Image", font=font_style)
    item_image_label.pack()
    image_pic = Entry(page,  font=font_style, fg="gray", textvariable=image_pic_var, width=50)
    image_pic.pack()
    space_label = Label(page, text=" ", font=font_style)
    space_label.pack()
    global item_price_var
    item_price_var = DoubleVar()
    item_price_var.set(0.0)
    item_price_label = Label(page, text="Item Price", font=font_style)
    item_price_label.pack()
    item_price_entry = Entry(page, font=font_style, fg="gray", textvariable=item_price_var)
    item_price_entry.pack()
    space_label = Label(page, text=" ", font=font_style)
    space_label.pack()
    add_button = Button(page, text="Add Image", font=font_style, bg="blue", fg="white", command=select_image)
    add_button.pack(side="left")
    save_button = Button(page, text="Save", font=font_style, bg="blue", fg="white", command=store_database)
    save_button.pack(side="right")
    page.place(anchor="c", rely=0.5, relx=0.5)

def connect_database(username, password, role):
    if role == "Staff":
        db = connect(host="localhost", username="root", password="11111", db="staffs")
        cursor = db.cursor(buffered=True)
        #file = open("file.sql", "r")
        show_databases = "show databases"
        describe_table = "describe users_table"
        name = "select Names, Password from users_table"
        cursor.execute(show_databases)
        cursor.execute(describe_table)
        cursor.execute(name)
        myresult = cursor.fetchall()
        list_users = {}
        for x, y in myresult:
            list_users[x.lower()] = y

        if username.lower() in list_users.keys():
            if password == list_users[username.lower()]:
                billing_page()
            else:
                messagebox.showerror("Error", "Incorrect Password!!!")
        else:
            messagebox.showerror("Error", "Incorrect Username!!!")

    elif role == "Admin":
        try:
            db = connect(host="localhost", username=username, password=password, db="staffs")
            if db:
                admin_panel()
        except MySQLdb.DatabaseError:
            messagebox.showerror("Error", "Incorrect Username or Password")

def get_prices(item):
    db = connect(host="localhost", username="root", password="11111", db="items")
    cursor = db.cursor()
    cursor.execute("select Name, Price from food")
    prices = {}
    myfetch = cursor.fetchall()
    for x, y in myfetch:
        prices[x] = y
    if item.lower() in prices.keys():
        return prices[item.lower()]

def checkout():
    balance = entry_paid_var.get() - entry_amount_var.get()
    entry_balance_var.set(balance)


def reset():
    for num in range(0, 5):
        exp = f"var_check{num}.get() == 0.0"
        if eval(exp):
            exec(f"var_check{num}.set(0.0)")
            exec("purchases.delete('1.0', END)")
            item_title = Label(purchases, text="Items          ", font=font_style)
            price_title = Label(purchases, text="      Quantity", font=font_style)
            cost_title = Label(purchases, text="Cost            ", font=font_style)
            space_out1 = Label(purchases, text="                  |           ", font=font_style)
            space_out2 = Label(purchases, text="                 |          ", font=font_style)
            purchases.window_create("end", window=item_title)
            purchases.window_create("end", window=space_out1)
            purchases.window_create("end", window=price_title)
            purchases.window_create("end", window=space_out2)
            purchases.window_create("end", window=cost_title)
        else:
            pass


def add():
    exec("global new_quantity")
    exec("new_quantity = 0")
    
    for num in range(0, 5):
        exp = f"var_check{num}.get() != 0.0"
        if eval(exp):
            exec(f"item_price = get_prices(lb{num}['text'])")
            exec(f"quantity = float(item_price) * (var_check{num}).get()")
            exec(f"txt = lb{num}['text'] +  '                            |                   x' + str(var_check{num}.get()) +   '                      |             ' + str(quantity)")
            exec("purchases.insert(INSERT, txt)")
            purchases.insert(INSERT, '\n')
            exec("new_quantity += quantity")
            exec(f"var_check{num}.set(0.0)")
        else:
            pass

    purchases.configure(state="disabled")
    exec("entry_amount_var.set(new_quantity)")

def billing_page():
    home_page.place_forget()
    Staff_page.place_forget()
    billing_page_frame = Frame(main_page, width=1920, height=1080)
    billing_page_frame.place(x=0, y=0)
    global items
    items = []
    global new_list
    new_list = []
    global purchases
    purchases = ScrolledText(billing_page_frame, width=60, height=15, font=font_style)
    purchases.place(x=760, y=70)
    item_title = Label(purchases, text="Items          ", font=font_style)
    price_title = Label(purchases, text="      Quantity", font=font_style)
    cost_title = Label(purchases, text="Cost            ", font=font_style)
    space_out1 = Label(purchases, text="                  |           ", font=font_style)
    space_out2 = Label(purchases, text="                 |          ", font=font_style)
    purchases.window_create("end", window=item_title)
    purchases.window_create("end", window=space_out1)
    purchases.window_create("end", window=price_title)
    purchases.window_create("end", window=space_out2)
    purchases.window_create("end", window=cost_title)

    total_amount = Label(billing_page_frame, text="Total", font=font_style)
    total_amount.place(x=760, y=480)
    global entry_amount_var
    entry_amount_var = DoubleVar()
    entry_amount = Entry(billing_page_frame, textvariable=entry_amount_var, font=font_style)
    entry_amount.place(x=880, y=480)

    amount_paid = Label(billing_page_frame, text="Paid", font=font_style)
    amount_paid.place(x=760, y=560)
    global entry_paid_var
    entry_paid_var = DoubleVar()
    entry_paid = Entry(billing_page_frame, textvariable=entry_paid_var, font=font_style)
    entry_paid.place(x=880, y=560)

    amount_balance = Label(billing_page_frame, text="Balance", font=font_style)
    amount_balance.place(x=760, y=640)
    global entry_balance_var
    entry_balance_var = DoubleVar()
    entry_balance = Entry(billing_page_frame, textvariable=entry_balance_var, font=font_style)
    entry_balance.place(x=880, y=640)

    checkout_btn = Button(billing_page_frame, text="Checkout", font=font_style, bg="blue", fg="white", command=checkout)
    checkout_btn.place(x=930, y=690)

    food_tab_button = Menubutton(billing_page_frame, text="FOOD", relief=SUNKEN, font=font_style, fg="white", bg="blue", state="disabled")
    clothes_tab_button = Menubutton(billing_page_frame, text="CLOTHES", relief=RAISED, font=font_style, fg="white", bg="blue")
    food_tab_list = Menu(food_tab_button, tearoff=0)
    food_tab_button["menu"] = food_tab_list
    food_tab_button.place(x=10, y=0)
    clothes_tab_list = Menu(clothes_tab_button, tearoff=0)
    clothes_tab_button["menu"] = clothes_tab_list
    clothes_tab_button.place(x=80, y=0)
    item_list = {}
    db = connect(host="localhost", username="root", password="11111", db="items")
    cursor = db.cursor()
    cursor.execute("select image, Name from food")
    myresult = cursor.fetchall()
    for x, y in myresult:
        item_list[x] = y

    mylist = ScrolledText(billing_page_frame, width=80, height=35)
    mylist.images = []
    global last_item
    image0 = PIL.Image.open("images/apple.png")
    img0 = PIL.ImageTk.PhotoImage(image0.resize((90, 90), PIL.Image.ANTIALIAS))
    mylist.image_create(INSERT, padx=5, pady=5, image=img0)
    mylist.images.append(img0)
    global var_check0, lb0
    var_check0 = DoubleVar()
    check0 = Entry(mylist, textvariable=var_check0, width=25)
    items.append(var_check0)
    lb0 = Label(mylist, text="Apple")
    mylist.window_create("end", window=lb0)
    mylist.window_create('end', window=check0)
    image1 = PIL.Image.open("images/sugar.jpg")
    img1 = PIL.ImageTk.PhotoImage(image1.resize((90, 90), PIL.Image.ANTIALIAS))
    mylist.image_create(INSERT, padx=5, pady=5, image=img1)
    mylist.images.append(img1)
    global var_check1, lb1
    var_check1 = DoubleVar()
    check1 = Entry(mylist, textvariable=var_check1, width=25)
    items.append(var_check1)
    lb1 = Label(mylist, text="Sugar")
    mylist.window_create("end", window=lb1)
    mylist.window_create('end', window=check1)
    global var_check2, lb2
    image2 = PIL.Image.open("images/milk1.jpg")
    img2 = PIL.ImageTk.PhotoImage(image2.resize((90, 90), PIL.Image.ANTIALIAS))
    mylist.image_create(INSERT, padx=5, pady=5, image=img2)
    mylist.images.append(img2)
    var_check2 = DoubleVar()
    check2 = Entry(mylist, textvariable=var_check2, width=25)
    items.append(var_check2)
    lb2 = Label(mylist, text="Milk")
    mylist.window_create("end", window=lb2)
    mylist.window_create('end', window=check2)
    image3 = PIL.Image.open("images/margarine.jpg")
    img3 = PIL.ImageTk.PhotoImage(image3.resize((90, 90), PIL.Image.ANTIALIAS))
    mylist.image_create(INSERT, padx=5, pady=5, image=img3)
    mylist.images.append(img3)
    global var_check3, lb3
    var_check3 = DoubleVar()
    check3 = Entry(mylist, textvariable=var_check3, width=25)
    items.append(var_check3)
    lb3 = Label(mylist, text="Margarine")
    mylist.window_create("end", window=lb3)
    mylist.window_create('end', window=check3)
    image4 = PIL.Image.open("images/yogurt.jpg")
    img4 = PIL.ImageTk.PhotoImage(image4.resize((90, 90), PIL.Image.ANTIALIAS))
    mylist.image_create(INSERT, padx=5, pady=5, image=img4)
    mylist.images.append(img4)
    global var_check4, lb4
    var_check4 = DoubleVar()
    check4 = Entry(mylist, textvariable=var_check4, width=25)
    items.append(var_check4)
    lb4 = Label(mylist, text="Yogurt")
    mylist.window_create("end", window=lb4)
    mylist.window_create('end', window=check4)
    mylist.place(x=10, y=100)
    bt = Button(billing_page_frame, text="Add", command=add, width=10, font=font_style, bg="blue", fg="white")
    bt.place(x=30, y=700)
    bt_reset = Button(billing_page_frame, text="Reset", command=reset, width=10, font=font_style, bg="blue", fg="white")
    bt_reset.place(x=190, y=700)
    mylist.configure(state="disabled")


def Staff_login():
    home_page.place_forget()
    global Staff_page
    Staff_page = Frame(main_page)
    login_label = Label(Staff_page, text="STAFF LOGIN PAGE", font=font_style)
    login_label.pack()
    line = Canvas(Staff_page)
    line.create_line(120, 10, 250, 10)
    line.pack()
    username_label = Label(Staff_page, text="Username", font=font_style)
    global username_entry
    username_entry = Entry(Staff_page, font=font_style)
    username_label.place(x=80, y=80)
    global password_entry
    username_entry.place(x=80, y=120)
    password_label = Label(Staff_page, text="Password", font=font_style)
    password_entry = Entry(Staff_page, font=font_style, show="x")
    password_label.place(x=80, y=150)
    password_entry.place(x=80, y=180)
    login_btn = Button(Staff_page, text="Login", relief="flat", bg="blue", fg="white", font=font_style, command=database_login)
    login_btn.place(x=150, y=230)
    Staff_page.place(anchor='c', relx=0.5, rely=0.5)

def Admin_login():
    home_page.place_forget()
    global Admin_page
    Admin_page = Frame(main_page)
    login_label = Label(Admin_page, text="ADMIN LOGIN PAGE", font=font_style)
    login_label.pack()
    line = Canvas(Admin_page)
    line.create_line(120, 10, 250, 10)
    line.pack()
    username_label = Label(Admin_page, text="Username", font=font_style)
    global username_entry
    username_entry = Entry(Admin_page, font=font_style)
    username_label.place(x=80, y=80)
    username_entry.place(x=80, y=120)
    password_label = Label(Admin_page, text="Password", font=font_style)
    global password_entry
    password_entry = Entry(Admin_page, font=font_style, show="x")
    password_label.place(x=80, y=150)
    password_entry.place(x=80, y=180)
    login_btn = Button(Admin_page, text="Login", relief="flat", bg="blue", fg="white", font=font_style, command=database_login)
    login_btn.place(x=150, y=230)
    Admin_page.place(anchor='c', relx=0.5, rely=0.5)


def change_home():
    global radio_value
    radio_value = home_page_radio.get()
    if radio_value == "Staff":

        Staff_login()
    else:
        Admin_login()


welcome_label = Label(home_page, text="WELCOME TO THE SUPERMARKET", font=font_style)
welcome_label.pack()
line = Canvas(home_page)
line.create_line(70, 20, 300, 20)
line.pack(side=TOP)
home_page_radio = StringVar()
radio_btn1 = Radiobutton(home_page, text="Staff", variable=home_page_radio, value="Staff", font=font_style)
radio_btn2 = Radiobutton(home_page, text="Admin", variable=home_page_radio, value="Admin", font=font_style)
radio_btn1.place(x=150, y=130)
radio_btn2.place(x=150, y=180)

continue_btn = Button(home_page, relief="flat", text="Continue", bg="blue", fg="white", font=font_style, borderwidth=5, command=change_home)
continue_btn.place(x=150, y=250)
home_page.place(anchor='c', relx=0.5, rely=0.5)
main_page.mainloop()


