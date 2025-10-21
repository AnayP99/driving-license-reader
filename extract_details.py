from datetime import datetime
import re
from dateutil.relativedelta import relativedelta

def get_name(text: str):
    match = re.search(r"Name\s+(.*)", text, re.IGNORECASE)
    return match.group(1)

def get_age(text: str):
    match = re.search(r"DOB\s+(\d{2}-\d{2}-\d{4})", text, re.IGNORECASE)
    dob = datetime.strptime(match.group(1), "%d-%m-%Y").date()
    today = datetime.today().date()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

def get_validity(text: str):
    match = re.search(r"Valid\s+Til[lt]?\s+(\d{2}-\d{2}-\d{4})", text, re.IGNORECASE)
    validity = datetime.strptime(match.group(1), "%d-%m-%Y").date()
    today = datetime.today().date()
    if validity < today:
        return {"status": "expired"}
    if validity < (today + relativedelta(months=6)):
        diff = relativedelta(validity, today)
        return {
            "status": "valid",
            "message": f"Expiring in {diff.months} months and {diff.days} days",
        }
    return {"status": "valid"}

def get_license_number(text: str):
    pattern = r"DL\s*No\s*[-]?\s*([A-Z]{2}[\dO]{2}\s*\d{11})\s+DO[I]?\s+(\d{2}-\d{2}-\d{4})"
    match = re.search(pattern, text, re.IGNORECASE)
    license_no =  match.group(1)
    if license_no[2] == "O":
        license_no = license_no[:2] + "0" + license_no[3:]
    issued = datetime.strptime(match.group(2), "%d-%m-%Y").date()
    pattern = r"Issuing\s+Authority\s+([A-Z]{2}\d{2})"
    issuing_authority = re.search(pattern, text, re.IGNORECASE).group(1)
    issued_date_flag = int(license_no[5:9]) == issued.year
    issuing_authority_flag = license_no[:4] == issuing_authority
    return {
        "number": license_no,
        "issued_date_matching": issued_date_flag,
        "issuing_authority_matching": issuing_authority_flag,
    }
