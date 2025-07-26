import streamlit as st
from datetime import date
import pandas as pd
import os
from openpyxl import load_workbook

# ---------------- Streamlit Config ----------------
st.set_page_config(page_title="Storage Requirement Form", layout="centered")

st.title("📦 Lead Form")

# ------------------- SECTION 1: Contact Details -------------------
st.header("🟩 Section 1: Contact Details (Auto-Fetched)")

col1, col2 = st.columns(2)

with col1:
    company_name = st.text_input("Company Name", value="", placeholder="Enter company name",
                                help="Company name fetched from the landing page")
    contact_person = st.text_input("Point of Contact", value="", placeholder="Enter contact person name",
                                  help="Contact person for this lead-details fetched from landing page")

with col2:
    email = st.text_input("Email", value="", placeholder="Enter email address",
                         help="Email address of the contact-details fetched from landing page")
    phone = st.text_input("Phone", value="", placeholder="Enter phone number",
                         help="Phone number of the contact-details fetched from landing page")

# ------------------- SECTION 2: Storage Details -------------------
st.header("🟦 Section 2: Storage Details")

locations = [
    "Jafza", "Al Quoz", "Al Quasis", "DIP", "DIP1", "DIP2", "DIC", "Ras Al Khor", "Sharjah Industrial Area",
    "Umm Ramool", "Emirates Industrial City", "Ad Dar al Baida", "Al Sulay", "Al Khabaisi", "Jebel Ali",
    "Techno Park", "Al Khawaneej", "Al Muqtta", "Al Sajja", "Dubai Land", "Ajman Industrial Area",
    "Hamriyah Free Zone", "DWC", "Musaffah", "Dubai Production City", "ICAD", "Al Qirawan", "Ash Shifa",
    "Al Ruwayyah", "International City"
]

commodity_types = [
    "Food", "DG", "General Goods", "Perishable Artwork", "Equipment", "Machinery", "Medical", "Pharma", "Other"
]

storage_types = ["Non Air Conditioned", "Ambient", "Chilled Storage", "Frozen","Open Yard"]
package_types = ["Pallets", "Boxes", "Oversized/Overweight", "Container","Bags"]
billing_units = ["CBM", "SQFT", "SQM", "Per Pallet", "Fixed Unit"]
coo_options = ["Mainland", "Freezone", "On the way to UAE", "Another Warehouse"]

# Row 1: Storage Location (Full Width)
storage_location = st.multiselect("Storage Location", locations, help="Select the storage location/locations for the goods")

# Row 2: Commodity Type (Left) | Commodity (Right)
row2_col1, row2_col2 = st.columns(2)
with row2_col1:
    commodity_type = st.selectbox("Commodity Type", commodity_types, key="commodity_type")
with row2_col2:
    commodity = st.text_input("Commodity", key="commodity_text_input")

# DG-specific warning
if st.session_state["commodity_type"] == "DG":
    st.markdown("""
        <div style="background-color:#ffcccc; border:2px solid red; padding:10px; border-radius:5px;">
        ⚠️ <b>DG selected:</b> Please upload the MSDS document for safety compliance.
        </div>
    """, unsafe_allow_html=True)
    msds_file = st.file_uploader("Upload MSDS Document", type=["pdf","docx","jpg","png"], key="msds_uploader")

# Storage Type & Temperature
row3_col1, row3_col2 = st.columns(2)
with row3_col1:
    storage_type = st.selectbox("Storage Type", storage_types)
with row3_col2:
    required_temperature = None
    if storage_type in ["Frozen", "Chilled Storage"]:
        required_temperature = st.number_input("Required Temperature (°C)", step=0.1)

# Package Type & Billing Unit
row4_col1, row4_col2 = st.columns(2)
with row4_col1:
    package_type = st.selectbox("Package Type", package_types)
with row4_col2:
    billing_unit = st.selectbox("Billing Unit", billing_units)

# COO and Expected Start Date
col_left, col_right = st.columns([1, 3])
with col_left:
    shipment_location = st.selectbox("COO / Location of Shipment", coo_options)
    expected_start = st.date_input("Expected Start Date", min_value=date.today())

packing_list = st.file_uploader("Upload Packing List (from WhatsApp)", type=["pdf","doc","jpg","png"])

# ------------------- SECTION 3: Handling Requirements -------------------
st.header("🟧 Section 3: Handling Requirements")
col_1,col_2=st.columns(2)
with col_1:
    handling_in = st.selectbox("Handling In", ["Loose","Pallets","Not Required","Offloading"])
with col_2:
    handling_out = st.selectbox("Handling Out", ["Loose","Pallets","Not Required","Pieces","Loading","Boxes"])

if handling_out == "Pallets":
    st.info("Inventory will be tracked by: Pallets")
elif handling_out == "Loose":
    st.info("Inventory will be tracked by: Boxes")
elif handling_out == "Pieces":
    st.info("Inventory will be tracked by: Pallets")

# ------------------- SECTION 4: Detailed Handling Requirements -------------------
if handling_out in ["Loose","Palletised","Pieces","Boxes","Loading"]:
    st.header("🟥 Section 4: Detailed Handling Requirements")
    sku_count = st.number_input("Number of SKUs", min_value=0)
    mixed_skus = st.selectbox("Are SKUs in the Pallets Mixed?", ["Yes","No"])
    if mixed_skus == "Yes":
        st.checkbox("Segregation Required", value=True, disabled=True)
    tracking_method = st.selectbox("How is Inventory Tracking Maintained?", ["Lot Number","Expiry Date","SKU Value"])

# ------------------- Documents Section -------------------
st.header("📎 Documents from WhatsApp")
documents = st.file_uploader("Upload Documents", accept_multiple_files=True)

# ------------------- Save to Excel -------------------
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Constants
SERVICE_ACCOUNT_FILE = 'C:\Users\rose\Downloads\lead-form-467108-9259f04dba08.json'  # update this path
SPREADSHEET_ID = 'https://docs.google.com/spreadsheets/d/1vAA_G-GhJFvz_z8e22PpvXNV8KEWgMsSZIErKxJNEL8/edit?gid=0#gid=0'  # from the sheet URL
SHEET_NAME = 'Lead Requirements Sheet'  # or your sheet tab name

# Authenticate Google Sheets API client
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('sheets', 'v4', credentials=credentials)

def append_to_google_sheet(data: dict):
    sheet = service.spreadsheets()
    # Order fields exactly as your Google Sheet columns
    values = [[
        data["Company Name"],
        data["Point of Contact"],
        data["Email"],
        data["Phone"],
        data["Storage Location"],
        data["Commodity Type"],
        data["Commodity"],
        data["MSDS Uploaded"],
        data["Storage Type"],
        data["Required Temperature (°C)"],
        data["Package Type"],
        data["Billing Unit"],
        data["Shipment Location"],
        data["Expected Start Date"],
        data["Handling In"],
        data["Handling Out"],
        data["Number of SKUs"],
        data["Mixed SKUs"],
        data["Segregation Required"],
        data["Tracking Method"],
        data["Packing List Uploaded"],
        data["Documents Uploaded"]
    ]]
    body = {'values': values}
    result = sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f'{SHEET_NAME}!A1',
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body=body
    ).execute()
    return result


# ------------------- Submit Button -------------------
if st.button("Submit Form"):
    segregation_required = "Yes" if mixed_skus == "Yes" else "No"

    summary = {
        "Company Name": company_name,
        "Point of Contact": contact_person,
        "Email": email,
        "Phone": phone,
        "Storage Location": ", ".join(storage_location),
        "Commodity Type": commodity_type,
        "Commodity": commodity,
        "MSDS Uploaded": "Yes" if commodity_type=="DG" and msds_file else "No",
        "Storage Type": storage_type,
        "Required Temperature (°C)": required_temperature if required_temperature else "N/A",
        "Package Type": package_type,
        "Billing Unit": billing_unit,
        "Shipment Location": shipment_location,
        "Expected Start Date": expected_start.strftime("%Y-%m-%d"),
        "Handling In": handling_in,
        "Handling Out": handling_out,
        "Number of SKUs": sku_count if 'sku_count' in locals() else "N/A",
        "Mixed SKUs": mixed_skus,
        "Segregation Required": segregation_required,
        "Tracking Method": tracking_method,
        "Packing List Uploaded": "Yes" if packing_list else "No",
        "Documents Uploaded": len(documents) if documents else 0
    }

    # Append data to Google Sheet
    append_result = append_to_google_sheet(summary)

    st.success("✅ Form submitted successfully and data saved to Google Sheets!")
    st.json(summary)
