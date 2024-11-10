from collections.abc import ItemsView
import json
import pandas as pd
from fpdf import FPDF
from pandas.core.computation import align

class LedgerPDF(FPDF):
    def __init__(self, from_var, school_info, date):
        super().__init__()

        self.from_var = from_var
        self.school_info = school_info
        self.date = date

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
        self.ln()

    def school(self):
        self.set_font("Times", "B", 12)
        self.save_x = self.get_x()
        self.save_y = self.get_y()
        self.cell(200, 5, f"{self.school_info["name"]}", align="C")

        self.set_xy(self.save_x, self.save_y + 5)
        self.set_font("Times", "", 10)
        self.cell(200, 5, "Ledger Account", align="C")

        self.set_xy(self.save_x, self.save_y + 10)
        self.cell(200, 5, f"{self.school_info["address_p1"]}", align="C")

        self.set_xy(self.save_x, self.save_y + 15)
        self.cell(200, 5, f"{self.school_info["address_p2"]}", align="C")

        self.set_xy(self.save_x, self.save_y + 20)
        self.cell(200, 5, f"{self.school_info["mobile_no"]}", align="C")
        self.ln()
        self.cell(200, 5, f"1-1-{list(self.date.replace("-", " ").split())[2]} to {self.date}", align="C")
        self.ln()

    def sales_table(self, data):
        self.save_x = self.get_x()
        self.save_y = self.get_y()

        self.set_font("Times", "", 10)
        self.line(self.save_x, self.save_y, self.save_x + 195, self.save_y)

        self.save_y = self.get_y() + 1
        self.set_xy(self.save_x, self.save_y)

        self.cell(15, 5, "Date", align="C")
        self.cell(70, 5, "Particulars", align="C")
        self.cell(40, 5, "Vch Type", align="C")
        self.cell(20, 5, "Vch No.", align="C")
        self.cell(25, 5, "Debit", align="C")
        self.cell(25, 5, "Credit", align="C")

        self.save_y = self.get_y() + 6
        self.line(self.save_x, self.save_y, self.save_x + 195, self.save_y)
        self.ln()

        for session in data:
            df_var = {
                "date": [],
                "particulars": [],
                "vch_type": [],
                "vch_no": [],
                "amount": []
            }
            debit = []
            credit = []
            for item in data[session]:
                if item == "opening_balance":
                    self.cell(15, 5, str(data[session][item]["date"]), align="C")
                    self.cell(70, 5, "Opening Balance", align="C")
                    self.cell(40, 5, "", align="C")
                    self.cell(20, 5, "", align="C")
                    self.cell(25, 5, str(data[session][item]["debit"]) if data[session][item]["debit"] != 0.0 else "", align="R")
                    self.cell(25, 5, str(data[session][item]["credit"]) if data[session][item]["credit"] != 0.0 else "", align="R")
                    if data[session][item]["debit"] != 0.0:
                        debit.append(data[session][item]["debit"])
                    if data[session][item]["credit"] != 0.0:
                        credit.append(data[session][item]["credit"])
                    self.ln()
                else:
                    df_var["date"].append(data[session][item]["date"])
                    df_var["particulars"].append(data[session][item]["particulars"])
                    df_var["vch_type"].append(data[session][item]["vch_type"])
                    df_var["vch_no"].append(data[session][item]["vch_no"])
                    df_var["amount"].append(data[session][item]["amount"])
            df = pd.DataFrame(df_var)
            for i, rows in df.iterrows():
                self.cell(15, 5, str(rows["date"]), align="C")
                self.cell(70, 5, str(rows["particulars"]), align="C")
                self.cell(40, 5, str(rows["vch_type"]), align="C")
                self.cell(20, 5, str(rows["vch_no"]), align="C")
                self.cell(25, 5, str(rows["amount"]) if rows["vch_type"] == "INVOICE" or rows["vch_type"] == "PURCHASE" or rows["vch_type"] == "PURCHASE" else "", align="R")
                self.cell(25, 5, str(rows["amount"]) if rows["vch_type"] == "Credit Note" or rows["vch_type"] == "Receipt" else "", align="R")
                if rows["vch_type"] == "PURCHASE" or rows["vch_type"] == "PURCHASE RETURN" or rows["vch_type"] == "INVOICE":
                    debit.append(float(rows["amount"]))
                else:
                    credit.append(float(rows["amount"]))


                self.ln()
            self.save_x = self.get_x()
            self.save_y = self.get_y()
            self.line(self.save_x + 145, self.save_y, self.save_x + 195, self.save_y)
            self.set_xy(self.save_x + 145, self.save_y + 1)
            self.cell(25, 5, str(sum(debit)), align="R")
            self.cell(25, 5, str(sum(credit)), align="R")

            self.set_xy(self.save_x, self.save_y + 6)
            self.cell(15, 5, f"{self.date}", align="C")

            self.set_xy(self.save_x + 15, self.save_y + 6)
            self.cell(70, 5, "Closing Balance", align="C")

            self.set_xy(self.save_x + 170, self.save_y + 6)
            self.cell(25, 5, str(abs(sum(debit) - sum(credit))), align="R")
            self.set_xy(self.save_x + 145, self.save_y + 6)
            self.save_y = self.get_y() + 6
            self.line(self.save_x + 145, self.save_y, self.save_x + 195, self.save_y)
            self.set_xy(self.save_x + 145, self.save_y + 1)
            self.cell(25, 5, str(abs(sum(debit) - sum(credit))), align="R")
            self.cell(25, 5, str(abs(sum(debit) - sum(credit))), align="R")
            self.set_xy(self.save_x + 145, self.save_y + 1)
            self.save_y = self.get_y() + 6
            self.line(self.save_x + 145, self.save_y, self.save_x + 195, self.save_y)
            self.set_xy(self.save_x, self.save_y)
            self.ln()




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
    with open("data/school-sales-info/test-school.json") as f:
        data = json.load(f)
    pdf = LedgerPDF(from_data, to_data, "10-11-24")
    pdf.add_page()
    pdf.school()
    pdf.sales_table(data["vch_info"])
    pdf.output("pdfs/ledgertest.pdf")
    print("Ledger Created Successfully")


