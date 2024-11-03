from fpdf import FPDF

class LedgerPDF(FPDF):
    def __init__(self, from_var, school_info):
        super().__init__()

        self.from_var = from_var
        self.school_info = school_info

        self.save_x = 0
        self.save_y = 0
    def header(self):
        self.set_font("Times", "B", 12)
        self.save_x = self.get_x()
        self.save_y = self.get_y()
        self.cell(200, 5, f"{self.from_var["name"]}", align="C")

        self.set_xy(self.save_x, self.save_y + 5)
        self.set_font("Times", "", 10)
        self.cell(200, 5, f"{self.from_var["address_p1"]}", align="C")

        self.set_xy(self.save_x, self.save_y + 10)
        self.cell(200, 5, f"{self.from_var["address_p2"]}", align="C")
        self.set_font("Times", "U", 10)
        self.set_xy(self.save_x, self.save_y + 15)
        self.cell(200, 5, f"Ph No.: +91 {self.from_var["mobile_no"]}", align="C")


if __name__ == "__main__":
    from_data = {
        "name": "Test",
        "address_p1": "Idieuoxhsjeiwhbxkdh",
        "address_p2": "iwofuksixbeuxvajvdrigd",
        "mobile_no": "7493684523",
    }
    to_data = {
        "name": "Test2",
        "address_p1": "Kdheofhsihrishefhwfeisbdue",
        "address_p2": "odhekfiehdwudisdfheoxivwdeksj",
        "mobile_no": "7492527493628"
    }
    pdf = LedgerPDF(from_data, to_data)
    pdf.output("pdfs/ledgertest.pdf")
    print("Ledger Created Successfully")


