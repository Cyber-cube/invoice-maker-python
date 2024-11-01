from operator import index
import tkinter as tk
import pandas as pd
import os.path
import json
from pdfinvoice import PDFInvoice
from autocomplete import AutoComplete

root = tk.Tk()
root.title("Invoice creator")
root.geometry("1000x600")

with open("data/booklist.json") as f:
    booklist_json = json.load(f)

with open("data/global-settings.json") as f:
    global_settings_json = json.load(f)

pdf_types = ["PURCHASE", "PURCHASE RETURN", "INVOICE"]
pdf_types_var = tk.IntVar()
pdf_type = ""

payment_types = ["Credit Note", "Receipt"]
payment_types_var = tk.IntVar()
payment_type = ""

org_name = "KUMAR PUSTAK BHANDAR"

from_details_var = {
    "address_p1": "Damyanti Complex, Kurthual, Pillar No.: 47",
    "address_p2": "NH-83, Patna 804453, (Bihar)",
    "mobile_no": "9905793743",
    "pan": "AYPCK5641H",
    "gstin": "10AYPCK5641H1ZU"
}

to_details_var = {
    "name": "INTELLICA PUBLISHERS (HUF) (D0357)",
    "address_p1": "5/17 2ND FLOOR, KIRTI NAGAR INDUSTRIAL AREA NEAR HP PETROL PUMP",
    "address_p2": "NEW DELHI 1100115",
    "mobile_no": "9818220408"
}
memo_no = global_settings_json["memo_no"]
delivery_info_var = {
    "memo": f"{memo_no:03}",
    "date": "26-09-24",
    "gr/rr_no": "_",
    "delivery_by": "_",
    "bundles": "0"
}

sl_counter = 1

booklist = {
    "Sl": [],
    "Code": [],
    "Title": [],
    "Pub": [],
    "Qty": [],
    "Disc": [],
    "Price": []
}

configuration = {
    "filename": "invoice.pdf"
}

pub_keys = list(booklist_json.keys())
book_name_keys = {i: list(booklist_json[i].keys()) for i in booklist_json}

def change_pdf_type():
    global pdf_type
    pdf_type = pdf_types[pdf_types_var.get()]

def change_payment_type():
    global payment_type
    payment_type = payment_types[payment_types_var.get()]
    if payment_types_var.get() == 1:
        bank_name_label.grid(row=4, column=0)
        bank_name.grid(row=4, column=1)
    elif payment_types_var.get() == 0:
        bank_name_label.place_forget()
        bank_name.place_forget()

def publisher_focusout(event, which_pub):
    global catalog_book_autocomplete
    global book_autocomplete
    try:
        if which_pub == "catalog":
            if catalog_publisher.get().strip() != "":
                catalog_book_autocomplete = AutoComplete(catalog_book, book_name_keys[catalog_publisher.get().lower()])
            else:
                pass
        elif which_pub == "product_input":
            if publisher.get().strip() != "":
                book_autocomplete = AutoComplete(book_name, book_name_keys[publisher.get().lower()])
                if book_name.get().strip() != "":
                    quantity_label.config(text=f"Quantity: {booklist_json[publisher.get().lower()][book_name.get().lower()]["quantity"]}")
            else:
                pass
    except Exception as e:
        pass

def book_name_focusout(event):
    try:
        if publisher.get().strip() != "":
            quantity_label.config(text=f"Quantity: {booklist_json[publisher.get().lower()][book_name.get().lower()]["quantity"]}")
        else:
            pass
    except Exception as e:
        pass

def from_details_callback():
    global org_name
    org_name = from_name.get()
    from_details_var["address_p1"] = from_address_p1.get()
    from_details_var["address_p2"] = from_address_p2.get()
    from_details_var["mobile_no"] = from_mobile_no.get()
    from_details_var["pan"] = from_pan.get()
    from_details_var["gstin"] = from_gstin.get()
    from_status_label.config(text="Data added successfully")


def to_details_callback():
    to_details_var["name"] = to_name.get()
    to_details_var["address_p1"] = to_address_p1.get()
    to_details_var["address_p2"] = to_address_p2.get()
    to_details_var["mobile_no"] = to_mobile_no.get()
    to_status_label.config(text="Data added successfully")

def delivery_info_callback(): 
    delivery_info_var["date"] = date.get()
    delivery_info_var["gr/rr_no"] = gr_rr_no.get()
    delivery_info_var["delivery_by"] = delivery_by.get()
    delivery_info_var["bundles"] = bundles.get()
    delivery_info_status_label.config(text="Data added successfully")

def add_to_booklist():
    if publisher.get().strip() == "" or book_name.get().strip() == "" or discount.get().strip() == "" or quantity.get().strip() == "":
        product_input_status.config(text="Something is not filled")
        print(booklist)
    else:
        global sl_counter
        global booklist_json
        booklist["Sl"].append(sl_counter)
        booklist["Code"].append(booklist_json[publisher.get().lower()][book_name.get().lower()]["code"])
        booklist["Title"].append(book_name.get())
        booklist["Pub"].append(publisher.get())
        booklist["Qty"].append(int(quantity.get()))
        booklist["Disc"].append(float(discount.get()))
        booklist["Price"].append(booklist_json[publisher.get().lower()][book_name.get().lower()]["price"])
    
        sl_counter += 1
        booklist_json[publisher.get().lower()][book_name.get().lower()]["quantity"] = booklist_json[publisher.get().lower()][book_name.get().lower()]["quantity"] - int(quantity.get())
            
        quantity_label.config(text="Quantity:")
        book_name.delete(0, tk.END)
        quantity.delete(0, tk.END)
        discount.delete(0, tk.END)
        publisher.delete(0, tk.END)
        
        current_sl_label.config(text=f"Current Sl No.: {sl_counter}")
        product_input_status.config(text="")
        
        with open("data/booklist.json", "w") as f:
            json.dump(booklist_json, f, indent=2)

def set_configuration():
    configuration["filename"] = f"{filename.get()}.pdf"
    customisatiion_status_label.config(text="Data added successfully")

def add_to_catalog():
    global pub_keys
    global book_name_keys
    global catalog_publisher_autocomplete
    global catalog_book_autocomplete
    global booklist_json
    publisher_func = catalog_publisher.get().lower()
    book_name_func = catalog_book.get().lower()
    price_func = 0.0
    code_func = ""
    quantity_func = 0
    if catalog_price.get().strip() != "":
        price_func = float(catalog_price.get())
    else:
        price_func = booklist_json[publisher_func][book_name_func]["price"]

    if catalog_code.get().strip() != "":
        code_func = catalog_code.get()
    else:
        code_func = booklist_json[publisher_func][book_name_func]["code"]

    if catalog_quantity.get().strip() != "":
        quantity_func = int(catalog_quantity.get())
    else:
        quantity_func = booklist_json[publisher_func][book_name_func]["quantity"]

    booklist_json[publisher_func] = {
        book_name_func: {
            "price": price_func,
            "code": code_func,
            "quantity": quantity_func
        }
    }

    pub_keys = list(booklist_json.keys())
    book_name_keys = {i: list(booklist_json[i].keys()) for i in booklist_json}

    catalog_publisher_autocomplete = AutoComplete(catalog_publisher, pub_keys)
    catalog_book_autocomplete = AutoComplete(catalog_book, book_name_keys)

    if publisher.get().strip() != "" and book_name.get().strip() != "":
        quantity_label.config(text=f"Quantity: {int(catalog_quantity.get())}")

    catalog_publisher.delete(0, tk.END)
    catalog_book.delete(0, tk.END)
    catalog_price.delete(0, tk.END)
    catalog_code.delete(0, tk.END)
    catalog_quantity.delete(0, tk.END)
    with open("data/booklist.json", "w") as f:
        json.dump(booklist_json, f, indent=2)

def add_payment():
    global memo_no
    with open(f"data/school-sales-info/{school_name.get().replace(" ", "-").lower()}.json") as f:
        school_sales_info = json.load(f)
    school_sales_info[memo_no] = {
        "payment_date": payment_date.get(),
        "particulars": bank_name.get() if payment_types_var.get() == 1 else "Sales",
        "vch_type": payment_type,
        "amount": float(payment_amount.get())
    }
    school_sales_info["debit"] -= float(payment_amount.get())
    if school_sales_info["debit"] < 0:
        school_sales_info["credit"] += abs(school_sales_info["debit"])
        school_sales_info["debit"] = 0.0
    memo_no += 1
    payment_memo_no_label.config(text=f"Memo#: {memo_no:03}")
    memo_label.config(text=f"Memo#: {memo_no:03}")
    with open(f"data/school-sales-info/{school_name.get().replace(" ", "-").lower()}.json", "w") as f:
        json.dump(school_sales_info, f, indent=2)
    school_name.delete(0, tk.END)
    payment_date.delete(0, tk.END)
    bank_name.delete(0, tk.END)
    bank_name.place_forget()
    bank_name_label.place_forget()
    payment_amount.delete(0, tk.END)

def create_pdf():
    global booklist
    global sl_counter
    global delivery_info_var
    global memo_no
    global global_settings_json
    pdf = PDFInvoice(org_name, pdf_type)
    df = pd.DataFrame(booklist)

    df["Amount"] = (df["Qty"] * df["Price"]) - ((df["Disc"] * (df["Qty"] * df["Price"])) / 100)

    if os.path.exists(f"data/school-sales-info/{to_details_var["name"].replace(" ", "-").lower()}.json"):
        with open(f"data/school-sales-info/{to_details_var["name"].replace(" ", "-").lower()}.json") as f:
            school_sales_info = json.load(f)
        school_sales_info["debit"] += df["Amount"].sum()
        school_sales_info[memo_no] = {
            "particulars": "Sales",
            "vch_type": pdf_type,
            "type": "debit",
            "amount": df["Amount"].sum()
        }
        with open(f"school-sales-info/{to_details_var["name"].replace(" ", "-").lower()}.json", "w") as f:
            json.dump(school_sales_info, f, indent=2)
    else:
        open(f"data/school-sales-info/{to_details_var["name"].replace(" ", "-").lower()}.json", "x").close()

        with open(f"data/school-sales-info/{to_details_var["name"].replace(" ", "-").lower()}.json", "w") as f:
            json.dump({}, f, indent=2)

        with open(f"data/school-sales-info/{to_details_var["name"].replace(" ", "-").lower()}.json") as f:
            school_sales_info = json.load(f)

        school_sales_info["from"] = {i: from_details_var[i] for i in from_details_var}
        school_sales_info["school_info"] = {i: to_details_var[i] for i in to_details_var}
        school_sales_info["credit"] = 00.0
        school_sales_info["debit"] = df["Amount"].sum()
        school_sales_info[memo_no] = {
            "particulars": "Sales",
            "vch_type": pdf_type,
            "type": "debit",
            "amount": df["Amount"].sum()
        }
        with open(f"data/school-sales-info/{to_details_var["name"].replace(" ", "-").lower()}.json", "w") as f:
            json.dump(school_sales_info, f, indent=2)

    chunk_size = 32
    for i in range(0, len(df), chunk_size):
        pdf.add_page()
        pdf.from_details(from_details_var)
        pdf.to_details(to_details_var, delivery_info_var)
        pdf.product_table(df.iloc[i:i + chunk_size])
        pdf.output(f"pdfs/{configuration["filename"]}")
        for j in booklist:
            booklist[j] = []
        sl_counter = 1
        global_settings_json["memo_no"] += 1
        memo_no = global_settings_json["memo_no"]
        delivery_info_var["memo"] = f"{memo_no:03}"

        current_sl_label.config(text=f"Current Sl No.: {sl_counter}")
        memo_label.config(text=f"Memo#: {memo_no:03}")
        payment_memo_no_label.config(text=f"Memo#: {memo_no:03}")
        from_status_label.config(text="")
        to_status_label.config(text="")
        delivery_info_status_label.config(text="")
        customisatiion_status_label.config(text="")
        with open("data/global-settings.json", "w") as f:
            json.dump(global_settings_json, f, indent=2)
        print("Invoice created successfully!")

# from details frame
from_details = tk.Frame(root, width=250, height=200, bd=5, relief="solid")
from_details.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# from name
from_name_label = tk.Label(from_details, text="From: ")
from_name_label.grid(row=0, column=0)
from_name = tk.Entry(from_details)
from_name.grid(row=0, column=1)

# Address
from_address_p1_label = tk.Label(from_details, text="Address: ")
from_address_p1_label.grid(row=1, column=0)
from_address_p1 = tk.Entry(from_details)
from_address_p1.grid(row=1, column=1)

from_address_p2_label = tk.Label(from_details, text="Address (2nd Part): ")
from_address_p2_label.grid(row=2, column=0)
from_address_p2 = tk.Entry(from_details)
from_address_p2.grid(row=2, column=1)

# mobile no
from_mobile_no_label = tk.Label(from_details, text="Mobile No.: ")
from_mobile_no_label.grid(row=3, column=0)
from_mobile_no = tk.Entry(from_details)
from_mobile_no.grid(row=3, column=1)

# PAN
from_pan_label = tk.Label(from_details, text="PAN: ")
from_pan_label.grid(row=4, column=0)
from_pan = tk.Entry(from_details)
from_pan.grid(row=4, column=1)

# GSTIN
from_gstin_label = tk.Label(from_details, text="GSTIN: ")
from_gstin_label.grid(row=5, column=0)
from_gstin = tk.Entry(from_details)
from_gstin.grid(row=5, column=1)

# Label Status
from_status_label = tk.Label(from_details, text="")
from_status_label.grid(row=6, column=0)

# set button
from_details_button = tk.Button(from_details, text="Set", command=from_details_callback)
from_details_button.grid(row=6, column=1)


# To details frame
to_details = tk.Frame(root, width=250, height=200, bd=5, relief="solid")
to_details.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# from name
to_name_label = tk.Label(to_details, text="To: ")
to_name_label.grid(row=0, column=0)
to_name = tk.Entry(to_details)
to_name.grid(row=0, column=1)

# Address
to_address_p1_label = tk.Label(to_details, text="Address: ")
to_address_p1_label.grid(row=1, column=0)
to_address_p1 = tk.Entry(to_details)
to_address_p1.grid(row=1, column=1)

to_address_p2_label = tk.Label(to_details, text="Address (2nd Part): ")
to_address_p2_label.grid(row=2, column=0)
to_address_p2 = tk.Entry(to_details)
to_address_p2.grid(row=2, column=1)

# mobile no
to_mobile_no_label = tk.Label(to_details, text="Mobile No.: ")
to_mobile_no_label.grid(row=3, column=0)
to_mobile_no = tk.Entry(to_details)
to_mobile_no.grid(row=3, column=1)

# Label Status
to_status_label = tk.Label(to_details, text="")
to_status_label.grid(row=4, column=0)

# set button
to_details_button = tk.Button(to_details, text="Set", command=to_details_callback)
to_details_button.grid(row=4, column=1)


# Delivery Info
delivery_info = tk.Frame(root, width=250, height=200, bd=5, relief="solid")
delivery_info.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

# Memo Label
memo_label = tk.Label(delivery_info, text=f"Memo#: {memo_no:03}")
memo_label.grid(row=0, column=0)

# Date
date_label = tk.Label(delivery_info, text="Date:")
date_label.grid(row=1, column=0)
date = tk.Entry(delivery_info)
date.grid(row=1, column=1)

# GR/RR No.
gr_rr_no_label = tk.Label(delivery_info, text="GR/RR No.:")
gr_rr_no_label.grid(row=2, column=0)
gr_rr_no = tk.Entry(delivery_info)
gr_rr_no.grid(row=2, column=1)

# Delivery by
delivery_by_label = tk.Label(delivery_info, text="Delivery By:")
delivery_by_label.grid(row=3, column=0)
delivery_by = tk.Entry(delivery_info)
delivery_by.grid(row=3, column=1)

# Bundles
bundles_label = tk.Label(delivery_info, text="Bundles:")
bundles_label.grid(row=4, column=0)
bundles = tk.Entry(delivery_info)
bundles.grid(row=4, column=1)

# Label Status
delivery_info_status_label = tk.Label(delivery_info, text="")
delivery_info_status_label.grid(row=5, column=0)

# set button
delivery_info_button = tk.Button(delivery_info, text="Set", command=delivery_info_callback)
delivery_info_button.grid(row=5, column=1)


# Product Input
product_input = tk.Frame(root, width=250, height=200, bd=5, relief="solid")
product_input.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# PUB
publisher_label = tk.Label(product_input, text="Publisher:")
publisher_label.grid(row=0, column=0)
publisher = tk.Entry(product_input)
publisher.grid(row=0, column=1)

publisher.bind("<FocusOut>", lambda event: publisher_focusout(event, "product_input"))
publisher_autocomplete = AutoComplete(publisher, pub_keys)

# Book name
book_name_label = tk.Label(product_input, text="Book name:")
book_name_label.grid(row=1, column=0)
book_name = tk.Entry(product_input)
book_name.grid(row=1, column=1)

book_name.bind("<FocusOut>", lambda event: book_name_focusout(event))

if publisher.get().strip() != "":
    book_autocomplete = AutoComplete(book_name, book_name_keys[publisher.get().lower()])

# Quantity
quantity_label = tk.Label(product_input, text="Quantity:")
quantity_label.grid(row=2, column=0)
quantity = tk.Entry(product_input)
quantity.grid(row=2, column=1)

if publisher.get().strip() != "" and book_name.get().strip() != "":
    quantity_label.config(text=f"Quantity: {booklist_json[publisher.get().lower()][book_name.get().lower()]["quantity"]}")

# Discount
discount_label = tk.Label(product_input, text="Discount:")
discount_label.grid(row=3, column=0)
discount = tk.Entry(product_input)
discount.grid(row=3, column=1)


# Current Sl
current_sl_label = tk.Label(product_input, text=f"Current Sl No.: {sl_counter}")
current_sl_label.grid(row=4, column=0)

# Add to list
add_to_booklist_button = tk.Button(product_input, text="Add to Booklist", command=add_to_booklist)
add_to_booklist_button.grid(row=4, column=1)

# Status
product_input_status = tk.Label(product_input, text="")
product_input_status.grid(row=5, column=0)

# Create PDF
create_pdf_button = tk.Button(product_input, text="Create PDF", command=create_pdf)
create_pdf_button.grid(row=5, column=1)


# Customisatiion 
customisatiion = tk.Frame(root, width=250, height=200, bd=5, relief="solid")
customisatiion.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

# Filenams
filename_label = tk.Label(customisatiion, text="Filename:")
filename_label.grid(row=0, column=0)
filename = tk.Entry(customisatiion)
filename.grid(row=0, column=1)

# Select PDF Type
for i in range(len(pdf_types)):
    pdf_types_option_radiobutton = tk.Radiobutton(customisatiion, text=pdf_types[i], variable=pdf_types_var, value=i, command=change_pdf_type)
    pdf_types_option_radiobutton.grid(row=1 + i, column=0)

# Label Status
customisatiion_status_label = tk.Label(customisatiion, text="")
customisatiion_status_label.grid(row=4, column=0)

# Set Configuration
set_config_button = tk.Button(customisatiion, text="Set Configuration", command=set_configuration)
set_config_button.grid(row=2, column=1)

# Add to Catalog
catalog = tk.Frame(root, width=250, height=200, bd=5, relief="solid")
catalog.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

# Publisher name
catalog_publisher_label = tk.Label(catalog, text="Publisher:")
catalog_publisher_label.grid(row=0, column=0)
catalog_publisher = tk.Entry(catalog)
catalog_publisher.grid(row=0, column=1)

catalog_publisher.bind("<FocusOut>", lambda event: publisher_focusout(event, "catalog"))

catalog_publisher_autocomplete = AutoComplete(catalog_publisher, pub_keys)

# Book name
catalog_book_label = tk.Label(catalog, text="Book Name:")
catalog_book_label.grid(row=1, column=0)
catalog_book = tk.Entry(catalog)
catalog_book.grid(row=1, column=1)

if catalog_publisher.get().strip() != "":
    catalog_book_autocomplete = AutoComplete(catalog_book, book_name_keys[catalog_publisher.get().lower()])

# Code
catalog_code_label = tk.Label(catalog, text="Code:")
catalog_code_label.grid(row=2, column=0)
catalog_code = tk.Entry(catalog)
catalog_code.grid(row=2, column=1)

# Price
catalog_price_label = tk.Label(catalog, text="Price:")
catalog_price_label.grid(row=3, column=0)
catalog_price = tk.Entry(catalog)
catalog_price.grid(row=3, column=1)

# Quantity
catalog_quantity_label = tk.Label(catalog, text="Quantity:")
catalog_quantity_label.grid(row=4, column=0)
catalog_quantity = tk.Entry(catalog)
catalog_quantity.grid(row=4, column=1)

# Add to catalog
add_to_catalog_button = tk.Button(catalog, text="Add to catalog", command=add_to_catalog)
add_to_catalog_button.grid(row=5, column=1)

# Add Payment
payment = tk.Frame(root, width=250, height=200, bd=5, relief="solid")
payment.grid(row=2, column=0, padx= 10, pady=10, sticky="nsew")

# School Name
school_name_label = tk.Label(payment, text="School Name:")
school_name_label.grid(row=0, column=0)
school_name = tk.Entry(payment)
school_name.grid(row=0, column=1)

# Payment Date
payment_date_label = tk.Label(payment, text="Payment Date:")
payment_date_label.grid(row=1, column=0)
payment_date = tk.Entry(payment)
payment_date.grid(row=1, column=1)

# Payment type
for i in range(len(payment_types)):
    payment_types_radiobutton = tk.Radiobutton(payment, text=payment_types[i], variable=payment_types_var, value=i, command=change_payment_type)
    payment_types_radiobutton.grid(row=2+i, column=0)

# Bank Name (If Receipt)
bank_name_label = tk.Label(payment, text="Bank Name:")
bank_name = tk.Entry(payment)

# amount
payment_amount_label = tk.Label(payment, text="Payment Amount:")
payment_amount_label.grid(row=6, column=0)
payment_amount = tk.Entry(payment)
payment_amount.grid(row=6, column=1)

# Memo No.
payment_memo_no_label = tk.Label(payment, text=f"Memo#: {memo_no:03}")
payment_memo_no_label.grid(row=7, column=0)

# Add Payment button
add_payment_button = tk.Button(payment, text="Add Payment", command=add_payment)
add_payment_button.grid(row=7, column=1)

tk.mainloop()
