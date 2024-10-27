from fpdf import FPDF

class PDFInvoice(FPDF):
    def __init__(self, org_name, pdf_type):
        super().__init__()

        self.org_name = org_name
        self.pdf_type = pdf_type

        self.save_x = 0
        self.save_y = 0

    def header(self) -> None:
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
        self.cell(95, 3, f"Memo# {delivery_info["memo"]}       Date: {delivery_info["date"]}", border=1)
        self.set_xy(self.save_x + 100, self.save_y + 3)
        self.cell(95, 5, f"GR/RR No.: {delivery_info["gr/rr_no"]}", border=1)
        self.set_xy(self.save_x + 100, self.save_y + 8)
        self.cell(95, 5, f"Delivery By: {delivery_info["delivery_by"]}                                                  Bundles: {delivery_info["bundles"]}", border=1)
        self.set_xy(self.save_x + 100, self.save_y + 13)
        self.cell(95, 11, "", border=1)
        self.set_xy(self.save_x, self.save_y + 24)
        self.ln(5)

    def product_table(self, df):
        self.set_xy(self.save_x, self.save_y + 24)

        self.set_font("Times", "", 9) 
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
        total_qty = df["Qty"].sum()
        total_amount = df["Amount"].sum()
        self.cell(10, 5, "", border=1)
        self.cell(15, 5, "", border=1)
        self.cell(80, 5, "", border=1)
        self.cell(20, 5, "", border=1)
        self.cell(15, 5, str(total_qty), border=1, align="R")
        self.cell(15, 5, "", border=1, align="R")
        self.cell(15, 5, "", border=1, align="R")
        self.cell(25, 5, str(total_amount), border=1, align="R")
