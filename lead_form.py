import streamlit as st
from datetime import date
import pandas as pd
import os
from openpyxl import load_workbook
import io

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
    commodity_type = st.selectbox("Commodity Type", commodity_types, key="commodity_type",help="Select the type of commodity to be stored")
with row2_col2:
    commodity = st.text_input("Commodity", key="commodity_text_input",help="Specify the exact commodity name or details")

# DG-specific warning
if st.session_state["commodity_type"] == "DG":
    st.markdown("""
        <div style="background-color:#ffcccc; border:2px solid red; padding:10px; border-radius:5px;">
        ⚠️ <b>DG selected:</b> Please upload the MSDS document for safety compliance.
        </div>
    """, unsafe_allow_html=True)
    msds_file = st.file_uploader("Upload MSDS Document", type=["pdf","docx","jpg","png"], key="msds_uploader",help="Upload Material Safety Data Sheet for Dangerous Goods")

# Storage Type & Temperature
row3_col1, row3_col2 = st.columns(2)
with row3_col1:
    storage_type = st.selectbox("Storage Type", storage_types,help="Choose the type of enviroment required for the goods")
with row3_col2:
    required_temperature = None
    if storage_type in ["Frozen", "Chilled Storage"]:
        required_temperature = st.number_input("Required Temperature (°C)", step=0.1, help="Specify the required storage temperature in Celsius")

# Package Type & Billing Unit
row4_col1, row4_col2 = st.columns(2)
with row4_col1:
    package_type = st.selectbox("Package Type", package_types,help="Select the packaging type for the goods")
with row4_col2:
    billing_unit = st.selectbox("Billing Unit", billing_units,help="Select the billing unit applicable")

if package_type == "Pallets":
    col_a, col_b,col_c,col_d = st.columns(4)
    with col_a:
        num_pallets = st.number_input("Number of Pallets", min_value=1, step=1,
                                      help="Enter total number of pallets")
    with col_b:
        pallet_type = st.selectbox("Type of Pallet", ["Standard", "Euro"],
                                   help="Select pallet type")
    with col_c:
        expected_space = st.number_input("Expected Space", min_value=0.0, step=0.1,
                                         help="Expected storage space needed")
    with col_d:
        space_unit = st.selectbox("Select Unit", ["CBM", "SQFT","per Pallet","Fixed Unit"],
                                  help="Select the unit for storage space")

    cbm_per_pallet = 1.8 if pallet_type == "Standard" else 1.44
    sqft_per_pallet = 13 if pallet_type == "Standard" else 10.03
    total_cbm = cbm_per_pallet * num_pallets
    total_sqft = sqft_per_pallet * num_pallets
    st.info(f"Approx. Expected Space: **{total_cbm:.2f} CBM** or **{total_sqft:.2f} SQFT**")

elif package_type == "Boxes":
    col_a, col_b = st.columns(2)
    with col_a:
        expected_space = st.number_input("Expected Space for Boxes", min_value=0.0, step=0.1,
                                         help="Expected storage space needed for boxes")
    with col_b:
        space_unit = st.selectbox("Select Unit", ["CBM", "SQFT","per Pallet","Fixed Unit"],
                                  help="Select the unit for storage space")

elif package_type == "Oversized/Overweight":
    col_a, col_b = st.columns(2)
    with col_a:
        weight = st.number_input("Weight of Commodity", min_value=0.0, step=0.1,
                                 help="Enter weight of the commodity in kilograms/ton")
    with col_b:
        weight_unit = st.selectbox("Weight Unit", ["KG", "TON"],
                                   help="Select weight unit")

    col_c, col_d = st.columns(2)
    with col_c:
        expected_space = st.number_input("Expected Space", min_value=0.0, step=0.1,
                                         help="Expected storage space needed")
    with col_d:
        space_unit = st.selectbox("Select Unit", ["CBM", "SQFT","per Pallet","Fixed Unit"],
                                  help="Select the unit for storage space")

elif package_type == "Container":
    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a:
        num_containers = st.number_input("Number of Containers", min_value=1, step=1,
                                         help="Enter number of containers")
    with col_b:
        container_type = st.selectbox("Container Size", ["40ft", "20ft"],
                                      help="Select container size")
    with col_c:
        expected_space = st.number_input("Expected Space", min_value=0.0, step=0.1,
                                         help="Expected storage space needed")
    with col_d:
        space_unit = st.selectbox("Select Unit", ["CBM", "SQFT","per Pallet","Fixed Unit"],
                                  help="Select the unit for storage space")

    cbm_per_container = 70 if container_type == "40ft" else 30
    sqft_per_container = 130 if container_type == "40ft" else 65
    total_cbm = cbm_per_container * num_containers
    total_sqft = sqft_per_container * num_containers
    st.info(f"Approx. Expected Space: **{total_cbm} CBM** or **{total_sqft} SQFT**")

elif package_type == "Bags":
    col_a, col_b = st.columns(2)
    with col_a:
        expected_space = st.number_input("Expected Space", min_value=0.0, step=0.1,
                                         help="Expected storage space needed")
    with col_b:
        space_unit = st.selectbox("Select Unit", ["CBM", "SQFT","per Pallet","Fixed Unit"],
                                  help="Select the unit for storage space")

# COO and Expected Start Date
col_left, col_right = st.columns([1, 3])
with col_left:
    shipment_location = st.selectbox("COO / Location of Shipment", coo_options,help="Country of origin or location of shipment")
    expected_start = st.date_input("Expected Start Date", min_value=date.today(),help="Enter the expected start date for storage")

packing_list = st.file_uploader("Upload Packing List (from WhatsApp)", type=["pdf","doc","jpg","png"],help="Upload packing list document")

# ------------------- SECTION 3: Handling Requirements -------------------
st.header("🟧 Section 3: Handling Requirements")
col_1,col_2=st.columns(2)
with col_1:
    handling_in = st.selectbox("Handling In", ["Loose","Pallets","Not Required","Offloading"],help="Select how goods are handled on arrival")
with col_2:
    handling_out = st.selectbox("Handling Out", ["Loose","Pallets","Not Required","Pieces","Loading","Boxes"],help="Select how goods are handled when dispatched")

if handling_out == "Pallets":
    st.info("Inventory will be tracked by: Pallets")
elif handling_out == "Loose":
    st.info("Inventory will be tracked by: Boxes")
elif handling_out == "Pieces":
    st.info("Inventory will be tracked by: Pallets")

# ------------------- SECTION 4: Detailed Handling Requirements -------------------
if handling_out in ["Loose","Palletised","Pieces","Boxes","Loading"]:
    st.header("🟥 Section 4: Detailed Handling Requirements")
    sku_count = st.number_input("Number of SKUs", min_value=0,help="Enter the number of Stock Keeping Units (SKUs)")
    mixed_skus = st.selectbox("Are SKUs in the Pallets Mixed?", ["Yes","No"])
    if mixed_skus == "Yes":
        st.checkbox("Segregation Required", value=True, disabled=True,help="Segregation is required due to mixed SKUs")
    tracking_method = st.selectbox("How is Inventory Tracking Maintained?", ["Lot Number","Expiry Date","SKU Value"],help="Select inventory tracking method")

# ------------------- Documents Section -------------------
st.header("📎 Documents from WhatsApp")
documents = st.file_uploader("Upload Documents", accept_multiple_files=True,help="Required Documents:\n1. Emirates ID\n2. VAT Certificate\n3. Trade License")
#-----------------------------------------------------------------------------------------

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SPREADSHEET_ID = '1vAA_G-GhJFvz_z8e22PpvXNV8KEWgMsSZIErKxJNEL8'  # only the ID
SHEET_NAME = 'Sheet1'  # exact name of the sheet tab

SCOPES = ['https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive"]

# Use service account info from Streamlit secrets to create credentials
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=SCOPES
)

drive_service = build('drive', 'v3', credentials=credentials)
service = build('sheets', 'v4', credentials=credentials)

#Document Upload-------------------------------
def upload_file_to_drive(file, folder_id=None):
    file_io = io.BytesIO(file.getbuffer())
    file_metadata = {'name': file.name}
    if folder_id:
        file_metadata['parents'] = [folder_id]
    media = MediaIoBaseUpload(file_io, mimetype=file.type, resumable=True)

    uploaded_file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    drive_service.permissions().create(
        fileId=uploaded_file['id'],
        body={'type': 'anyone', 'role': 'reader'}
    ).execute()

    return f"https://drive.google.com/file/d/{uploaded_file['id']}/view?usp=sharing"

# ------------------- Save to Excel -------------------

def append_to_google_sheet(data: dict):
    sheet = service.spreadsheets()

    # Define the header row (field names exactly as your sheet columns)
    header = [
        "Company Name",
        "Point of Contact",
        "Email",
        "Phone",
        "Storage Location",
        "Commodity Type",
        "Commodity",
        "MSDS Uploaded",
        "Storage Type",
        "Required Temperature (°C)",
        "Package Type",
        "Billing Unit",
        "Shipment Location",
        "Expected Start Date",
        "Handling In",
        "Handling Out",
        "Number of SKUs",
        "Mixed SKUs",
        "Segregation Required",
        "Tracking Method",
        "Packing List Uploaded",
        "Documents Uploaded"
    ]

    # First, read the first row to check if header exists
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_NAME}!1:1"
    ).execute()

    existing_header = result.get('values', [])

    # If header row is empty, write it
    if not existing_header:
        sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME}!1:1",
            valueInputOption='RAW',
            body={'values': [header]}
        ).execute()

    # Prepare data row values in the same order as header
    values = [[
        data.get(field, "") for field in header
    ]]

    # Append data below header row
    body = {'values': values}
    append_result = sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_NAME}!A2",  # start appending from second row
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body=body
    ).execute()

    return append_result


# ------------------- Submit Button -------------------
if st.button("Submit Form"):
    segregation_required = "Yes" if mixed_skus == "Yes" else "No"
    packing_list_link = upload_file_to_drive(packing_list) if packing_list else ""
    documents_links = []
    if documents:
        for doc in documents:
            documents_links.append(upload_file_to_drive(doc))
    msds_link = upload_file_to_drive(msds_file) if commodity_type == "DG" and msds_file else ""

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
        "Documents Uploaded": len(documents) if documents else 0,
        "Packing List Uploaded": packing_list_link,
        "Documents Uploaded": ", ".join(documents_links)
    }

    # Append data to Google Sheet
    append_result = append_to_google_sheet(summary)

    st.success("✅ Form submitted successfully and data saved to Google Sheets!")
    st.json(summary)
