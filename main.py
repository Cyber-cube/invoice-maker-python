import tkinter as tk
import pandas as pd
import json
from pdfinvoice import PDFInvoice

root = tk.Tk()
root.title("Invoice creator")
root.geometry("1000x600")


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
delivery_info_var = {
    "memo": "KP (P)/PR/24-25/0231",
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

def from_details_callback():
    global org_name
    org_name = from_name.get()
    from_details_var["address_p1"] = from_address_p1.get()
    from_details_var["address_p2"] = from_address_p2.get()
    from_details_var["mobile_no"] = from_mobile_no.get()
    from_details_var["pan"] = from_pan.get()
    from_details_var["gstin"] = from_gstin.get()


def to_details_callback():
    to_details_var["name"] = to_name.get()
    to_details_var["address_p1"] = to_address_p1.get()
    to_details_var["address_p2"] = to_address_p2.get()
    to_details_var["mobile_no"] = to_mobile_no.get()

def delivery_info_callback(): 
    delivery_info_var["memo"] = memo_entry.get()
    delivery_info_var["date"] = date.get()
    delivery_info_var["gr/rr_no"] = gr_rr_no.get()
    delivery_info_var["delivery_by"] = delivery_by.get()
    delivery_info_var["bundles"] = bundles.get()

def add_to_booklist():
    global sl_counter
    with open("books.json") as file:
        books = json.load(file)
    booklist["Sl"].append(sl_counter)
    booklist["Code"].append(books[str(book_name.get()).upper()]["Code"])
    booklist["Title"].append(book_name.get())
    booklist["Pub"].append(books[str(book_name.get()).upper()]["Pub"])
    booklist["Qty"].append(int(quantity.get()))
    booklist["Disc"].append(float(discount.get()))
    booklist["Price"].append(books[str(book_name.get()).upper()]["Price"])

    sl_counter += 1

    book_name.delete(0, tk.END)
    quantity.delete(0, tk.END)
    discount.delete(0, tk.END)
    current_sl_label.config(text=f"Current Sl No.: {sl_counter}")

def create_pdf():
    pdf = PDFInvoice(org_name)
    df = pd.DataFrame(booklist)

    df["Amount"] = (df["Qty"] * df["Price"]) - ((df["Disc"] * (df["Qty"] * df["Price"])) / 100)

    chunk_size = 32
    for i in range(0, len(df), chunk_size):
        pdf.add_page()
        pdf.from_details(from_details_var)
        pdf.to_details(to_details_var, delivery_info_var)
        pdf.product_table(df.iloc[i:i + chunk_size])
        pdf.output("invoice.pdf")
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

# set button
to_details_button = tk.Button(to_details, text="Set", command=to_details_callback)
to_details_button.grid(row=4, column=1)


# Delivery Info
delivery_info = tk.Frame(root, width=250, height=200, bd=5, relief="solid")
delivery_info.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

# Memo#
memo_label = tk.Label(delivery_info, text="Memo# :")
memo_label.grid(row=0, column=0)
memo_entry = tk.Entry(delivery_info)
memo_entry.grid(row=0, column=1)

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

# set button
delivery_info_button = tk.Button(delivery_info, text="Set", command=delivery_info_callback)
delivery_info_button.grid(row=5, column=1)


# Product Input
product_input = tk.Frame(root, width=250, height=200, bd=5, relief="solid")
product_input.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# Book name
book_name_label = tk.Label(product_input, text="Book name:")
book_name_label.grid(row=0, column=0)
book_name = tk.Entry(product_input)
book_name.grid(row=0, column=1)

# Quantity
quantity_label = tk.Label(product_input, text="Quantity:")
quantity_label.grid(row=1, column=0)
quantity = tk.Entry(product_input)
quantity.grid(row=1, column=1)

# Discount
discount_label = tk.Label(product_input, text="Discount:")
discount_label.grid(row=2, column=0)
discount = tk.Entry(product_input)
discount.grid(row=2, column=1)

# Current Sl
current_sl_label = tk.Label(product_input, text=f"Current Sl No.: {sl_counter}")
current_sl_label.grid(row=3, column=0)

# Add to list
add_to_booklist_button = tk.Button(product_input, text="Add to Booklist", command=add_to_booklist)
add_to_booklist_button.grid(row=3, column=1)

# Create PDF
create_pdf_button = tk.Button(product_input, text="Create PDF", command=create_pdf)
create_pdf_button.grid(row=4, column=0)

tk.mainloop()
