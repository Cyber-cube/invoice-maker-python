from fpdf import FPDF
from num2words import num2words

class PaymentSlip(FPDF):
    def __init__(self, org_name):
        super().__init__()

        self.org_name = org_name

        self.save_x = 0
        self.save_y = 0

    def header(self) -> None:
        self.add_font("NotoFont", "B", "fonts/Noto_Serif_Devanagari/NotoSerifDevanagari-VariableFont_wdth,wght.ttf")
        self.add_font("NotoFont", "", "fonts/Noto_Serif_Devanagari/NotoSerifDevanagari-VariableFont_wdth,wght.ttf")
        self.set_font("Times", "B", 12)
        self.cell(200, 10, "Money Receipt", align="C" )
        self.ln()
        self.set_font("Times", "B", 23)
        self.cell(200, 10, self.org_name, align="C")
        self.ln()
        self.set_font("Times", "B", 11)
        self.cell(200, 10, "(All Kinds of Books Whole Sellers & Suppliers)", align="C")
        self.ln()

    def add_info(self, details):
        self.save_x = self.get_x()
        self.save_y = self.get_y()

        self.cell(None, None, f"Memo No: {details["memo_no"]}", align="L")
        self.cell(0, None, f"Date: {details["receipt_date"]}", align="R")
        self.ln(self.font_size + 8)

        self.set_font("NotoFont", "", 10)
        self.cell(None, None, "Received with thanks from:")
        self.cell(0, None, details["school_name"], "B")
        self.ln(self.font_size + 8)

        self.cell(None, None, "Amount in a word:")
        self.cell(0, None, f"{num2words(details["amount"], lang="en_IN")}", "B")
        self.ln(self.font_size + 8)

        self.cell(None, None, "By Cash/Cheque:")
        self.cell(80, None, details["mode"], "B")
        self.cell(None, None, "Bank")
        self.cell(40, None, details["bank"], "B")
        self.cell(None, None, "Date")
        self.cell(0, None, details["transaction_date"], "B")
        self.ln(self.font_size + 8)

        self.set_font("NotoFont", "", 11)
        self.cell(None, None, "Amount")
        self.set_xy(self.get_x(), self.get_y() - 2)
        self.multi_cell(50, None, f"₹{details["amount"]}", True, padding=2)
        
        self.ln(self.font_size + 15)
        self.cell(0, None, "Authorized Signature", align="R")



if __name__ == "__main__":
    details = {
        "memo_no": 1,
        "receipt_date": "23-01-2026",
        "school_name": "meow",
        "amount": 4677,
        "mode": "Cheque",
        "bank": "Test Bank",
        "transaction_date": "20-01-2026"
    }
    pdf = PaymentSlip("Saoumya Book Point")
    pdf.add_page()
    pdf.add_info(details)
    pdf.output("pdfs/test.pdf")