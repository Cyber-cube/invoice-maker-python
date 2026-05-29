from fpdf import FPDF

class PDFInvoice(FPDF):
    def __init__(self, org_name, pdf_type):
        super().__init__()

        self.org_name = org_name
        self.pdf_type = pdf_type

        self.save_x = 0
        self.save_y = 0

    def header(self) -> None:
        # self.add_font("NotoFont", "B", "fonts/Noto_Serif_Devanagari/NotoSerifDevanagari-VariableFont_wdth,wght.ttf")
        self.add_font("NotoFont", "", "fonts/Noto_Serif_Devanagari/NotoSerifDevanagari-VariableFont_wdth,wght.ttf")
        self.set_font("Times", "B", 12)
        self.cell(200, 10, f"{self.pdf_type}", align="C" )
        self.ln()
        self.set_font("Times", "B", 23)
        self.cell(200, 10, self.org_name, align="C")
        self.ln()
        self.set_font("Times", "B", 11)
        self.cell(200, 10, "(All Kinds of Books Whole Sellers & Suppliers)", align="C")
        self.ln()

    def from_details(self, from_details_var):
        self.set_font("Times", "", 10)
        self.cell(100, 10, f"{from_details_var["address_p1"]}", align="L")
        self.ln()
        self.cell(100, 10, f"{from_details_var["address_p2"]}", align="L")
        self.ln()
        self.cell(100, 10, f"Mobile: {from_details_var["mobile_no"]}", align="L")
        self.ln()
        self.cell(100, 10, f"PAN: {from_details_var["pan"]} | GSTIN: {from_details_var["gstin"]}", align="L")
        self.ln()
    
    def to_details(self, to_details_var, delivery_info):
        self.set_font("Times", "", 10)
        self.save_x = self.get_x()
        self.save_y = self.get_y()

        self.multi_cell(100, 3, f"""
        To, {to_details_var["name"]} \n
        {to_details_var["address_p1"]} \n
        {to_details_var["address_p2"]}, Ph: {to_details_var["mobile_no"]}
        """, align="L", border=1)

        self.set_xy(self.save_x + 100, self.save_y)
        if self.pdf_type == "PURCHASE RETURN":
            self.cell(95, 3, f"Credit Note No.# {delivery_info["memo"]}       Date: {delivery_info["date"]}", border=1)
        else:
            self.cell(95, 3, f"Memo# {delivery_info["memo"]}       Date: {delivery_info["date"]}", border=1)
        self.set_xy(self.save_x + 100, self.save_y + 3)
        self.cell(95, 5, f"GR/RR No.: {delivery_info["gr/rr_no"]}", border=1)
        self.set_xy(self.save_x + 100, self.save_y + 8)
        self.cell(95, 5, "", border=1)
        self.set_xy(self.save_x + 100, self.save_y + 8)
        self.cell(60, 5, f"Delivery By: {delivery_info["delivery_by"]}")
        self.cell(35, 5, f"Bundles: {delivery_info["bundles"]}")
        self.set_xy(self.save_x + 100, self.save_y + 13)
        self.cell(95, 11, "", border=1)
        self.set_xy(self.save_x, self.save_y + 24)
        self.ln(5)

    def product_table(self, df, totalAmount, totalQty, setTotal):
        self.set_xy(self.save_x, self.save_y + 24)

        self.set_font("NotoFont", "", 9) 
        self.cell(10, 5, "Sl", border=1)
        self.cell(15, 5, "Code", border=1)
        self.cell(80, 5, "Title", border=1)
        self.cell(20, 5, "PUB", border=1)
        self.cell(15, 5, "Qty", border=1, align="R")
        self.cell(15, 5, "Price", border=1, align="R")
        self.cell(15, 5, "Disc", border=1, align="R")
        self.cell(25, 5, "Amount", border=1, align="R")
        self.ln()

        for i, rows in df.iterrows():
            self.cell(10, 5, str(rows["Sl"]), border=1)
            self.cell(15, 5, str(rows["Code"]), border=1)
            self.cell(80, 5, str(rows["Title"]), border=1)
            self.cell(20, 5, str(rows["Pub"]), border=1)
            self.cell(15, 5, str(rows["Qty"]), border=1, align="R")
            self.cell(15, 5, str(rows["Price"]), border=1, align="R")
            self.cell(15, 5, str(rows["Disc"]), border=1, align="R")
            self.cell(25, 5, str(rows["Amount"]), border=1, align="R")
            self.ln()
        if setTotal:
            total_qty = totalQty
            total_amount = totalAmount
            self.cell(10, 5, "", border=1)
            self.cell(15, 5, "", border=1)
            self.cell(80, 5, "", border=1)
            self.cell(20, 5, "", border=1)
            self.cell(15, 5, str(total_qty), border=1, align="R")
            self.cell(15, 5, "", border=1, align="R")
            self.cell(15, 5, "", border=1, align="R")
            self.cell(25, 5, str(total_amount), border=1, align="R")
    
    def footer(self):
    
        self.set_font("Times", "B", 8)
        self.set_xy(175, -30)
        self.cell(20, 5, f"For {self.org_name}", align="C")
        self.set_xy(175, -10)
        self.cell(20, 5, "Auth. Signatory", align="C")
        self.set_font("Times", "B")
        self.set_xy(5, -10)
        self.cell(30, 5, "Books once sold cannot be exchanged or returned.")


if __name__ == "__main__":
    pdf = PDFInvoice("Saoumya Book Point", "Invoice")
    pdf.add_page()
    org_name = "SAOUMYA BOOK POINT"

    from_details_var = {
        "address_p1": "Transport Nagar, Patna - 800026",
        "address_p2": "Near Mico Company, G.T. Road, Sasaram - 821115",
        "mobile_no": "8294472040, 9631010694",
        "pan": "AZDPM2348H",
        "gstin": ""
    }

    to_details_var = {
        "name": "INTELLICA PUBLISHERS (HUF) (D0357)",
        "address_p1": "5/17 2ND FLOOR, KIRTI NAGAR INDUSTRIAL AREA NEAR HP PETROL PUMP",
        "address_p2": "NEW DELHI 1100115",
        "mobile_no": "9818220408"
    }

    delivery_info = {
        "memo": "#036",
        "date": "19/03/2026",
        "gr/rr_no": "0202",
        "delivery_by": "meow",
        "bundles": "10"
    }

    pdf.header()
    pdf.from_details(from_details_var)
    pdf.to_details(to_details_var, delivery_info)
    pdf.output("pdfs/mmmmm.pdf")
    