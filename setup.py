import os.path
import json

# Setup Wizard
print("Welcome to the Setup Wizard\n Only run this file when you are setting up the program for the first time or you want to update the program's details")
print("Now, follow the instructions")
org_name = input("What's your organisation name ? \n").upper()
address_p1 = input("Enter the first part of your company's address \n")
address_p2 = input("Enter the second part of your company's address \n")
mobile_no = input("Enter the number associated with your company \n")
pan = input("Enter your company's PAN \n")
gstin = input("Enter your company's GST number \n")

if os.path.exists("/data/global-settings.json"):
    while True:
        decision = input("Do you want to reset the configuration file (including the memo no, credit note no, etc.) ?\n Enter Yes to reset and remake the configuration file. Enter No to update the configuration file without resetting it. \n")
    
        if decision == "Yes":
            print("Resetting and changing configuration")
            with open("data/global-settings.json") as f:
                settings = json.load(f)

            settings["org_name"] = org_name
            settings["address_p1"] = address_p1
            settings["address_p2"] = address_p2
            settings["mobile_no"] = mobile_no
            settings["pan"] = pan
            settings["gstin"] = gstin
            settings["memo_no"] = 1
            settings["payment_memo_no"] = 1
            settings["credit_note_no"] = 1

            with open("data/global-settings.json", "w") as f:
                json.dump(settings, f, indent=2)
            print("Successfully resetted and changed the configuration")
            break
        elif decision == "No":
            print("Updating configuration file")
            with open("data/global-settings.json") as f:
                settings = json.load(f)

            settings["org_name"] = org_name
            settings["address_p1"] = address_p1
            settings["address_p2"] = address_p2
            settings["mobile_no"] = mobile_no
            settings["pan"] = pan
            settings["gstin"] = gstin

            with open("data/global-settings.json", "w") as f:
                json.dump(settings, f, indent=2)
            print("Successfully updated the configuration")
            break
        else:
            print("Wrong input")
else:
    print("Creating the required files")
    os.makedirs("data", exist_ok=True)
    open("data/global-settings.json", "x").close() 
    with open("data/global-settings.json", "w") as f:
        json.dump({}, f, indent=2)

    with open("data/global-settings.json") as f:
        settings = json.load(f)

    settings["org_name"] = org_name
    settings["address_p1"] = address_p1
    settings["address_p2"] = address_p2
    settings["mobile_no"] = mobile_no
    settings["pan"] = pan
    settings["gstin"] = gstin
    settings["memo_no"] = 1
    settings["payment_memo_no"] = 1
    settings["credit_note_no"] = 1

    with open("data/global-settings.json", "w") as f:
        json.dump(settings, f, indent=2)

    open("data/booklist.json", "x").close() 
    with open("data/booklist.json", "w") as f:
        json.dump({}, f, indent=2)

    os.makedirs("data/school-sales-info", exist_ok=True)
    os.makedirs("pdfs/", exist_ok=True)
    print("Setup done! Now you can run the program")
