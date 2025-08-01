import streamlit as st
from datetime import date
import pandas as pd
import os
from openpyxl import load_workbook

# ---------------- Streamlit Config ----------------
st.set_page_config(page_title="Storage Requirement Form", layout="centered")

st.title("📦 Lead Form")

# ------------------- SECTION 1: Contact Details -------------------
st.header("🟩 Section 1: Contact Details")
contact_roles = ["Owner", "Accountant", "Ops", "Commercial"]
col1, col2 = st.columns(2)

with col1:
    company_name = st.text_input("Company Name", value="", placeholder="Enter company name")
                                # help="Company name fetched from the landing page")
    contact_person = st.text_input("Point of Contact", value="", placeholder="Enter contact person name")
                                #   help="Contact person for this lead-details fetched from landing page")

with col2:
    email = st.text_input("Email", value="", placeholder="Enter email address")
                        #  help="Email address of the contact-details fetched from landing page")
    phone = st.text_input("Phone", value="", placeholder="Enter phone number")
                        #  help="Phone number of the contact-details fetched from landing page")

role = st.multiselect("Role", options=contact_roles, help="Select one or more roles")

if st.button("➕ Add Another Contact"):
    st.info("Functionality to add multiple contacts can be implemented dynamically using session_state or a form loop.")

# ------------------- SECTION 2: Storage Needs -------------------
st.header("✅ Section 2: Storage Needs")

row1_col1, row1_col2 = st.columns(2)
with row1_col1:
    location_constraint = st.selectbox(
        "Do you have any location constraints?",
        options=["No", "Yes"],
        help="Select Yes if you want to restrict locations"
    )
uae_industrial_areas = [
    "Jafza", "Al Quoz", "Al Quasis", "DIP", "DIP1", "DIP2", "DIC", "Ras Al Khor", "Sharjah Industrial Area",
    "Umm Ramool", "Emirates Industrial City", "Ad Dar al Baida", "Al Sulay", "Al Khabaisi", "Jebel Ali",
    "Techno Park", "Al Khawaneej", "Al Muqtta", "Al Sajja", "Dubai Land", "Ajman Industrial Area",
    "Hamriyah Free Zone", "DWC", "Musaffah", "Dubai Production City", "ICAD", "Al Qirawan", "Ash Shifa",
    "Al Ruwayyah", "International City"
]

with row1_col2:
    if location_constraint == "Yes":
        storage_location = st.multiselect(
            "Select location(s) in UAE industrial areas",
            options=uae_industrial_areas,
            help="Choose one or more locations"
        )
    else:
        storage_location = []

commodity_types = [
    "Raw & Finished Food",
    "DG",
    "General Good",
    "Perishable",
    "High Value Items",
    "Equipment & Machinery",
    "Medical & Pharma",
    "Other",
    "Non-DG Chemical"
]

row2_col1, row2_col2 = st.columns(2)
with row2_col1:
    commodity_type = st.selectbox(
        "Commodity Type",
        options=commodity_types,
        help="Select the type of commodity",
        key="commodity_type"
    )
with row2_col2:
    commodity_name = st.text_input(
        "Commodity Name",
        help="Specify the exact commodity name or details"
    )

# Row 3: DG Class (spans full width if visible), Storage Type and Temperature
if st.session_state.get("commodity_type") == "DG":
    st.markdown("""
        <div style="background-color:#ffcccc; border:2px solid red; padding:10px; border-radius:5px;">
        ⚠️ <b>DG selected:</b> Please upload the MSDS document for safety compliance.
        </div>
    """, unsafe_allow_html=True)
    dg_class_selected = st.multiselect(
        "DG Class",
        options=[
            "Class 1 Explosives", "Class 2 Gases", "Class 3 Flammable Liquids", "Class 4 Flammable Solids",
            "Class 5 Oxidizing Substances", "Class 6 Toxic and Infectious Substances", "Class 7 Radioactive Material",
            "Class 8 Corrosives", "Class 9 Miscellaneous Dangerous Goods"
        ],
        help="Select DG hazard classes"
    )
    msds_file = st.file_uploader(
        "Upload MSDS Document", type=["pdf", "docx", "jpg", "png"],
        key="msds_uploader", help="Upload Material Safety Data Sheet for Dangerous Goods"
    )
else:
    dg_class_selected = []
    msds_file = None

# Storage Type dropdown with specified options
row3_col1, row3_col2 = st.columns(2)
with row3_col1:
    storage_type = st.selectbox(
        "Storage Type",
        options=["NON AC", "AC", "Chiller", "Freezer", "Open Yard", "Other"],
        help="Choose the type of storage environment"
    )
with row3_col2:
    required_temperature = None
    if storage_type in ["AC", "Chiller", "Freezer", "Other"]:
        required_temperature = st.text_input(
            "Specific Temperature (°C)",
            help="Enter the required storage temperature"
        )

# Row 4: Cargo Location
row4_col1, _ = st.columns([1, 1])
with row4_col1:
    cargo_location = st.selectbox(
        "Where is the cargo now?",
        options=["Mainland", "Freezone", "On the way to UAE", "Another WH", "Cargo in Procurement Stage"],
        help="Select current cargo location"
    )
# Row 5: Cargo location comment (full width)
cargo_location_comment = st.text_area(
    "Comments about cargo location",
    help="Provide any additional details"
)

# Row 6: Risk Factor
if st.checkbox("❗ Any known risk factor with the commodity?", key="risk_checkbox"):
    st.markdown(
        '<p style="color: red;"><b>Risk Factor Comments</b></p>',
        unsafe_allow_html=True
    )
    risk_factor_comment = st.text_area(
        "Describe the risk factor(s)",
        help="Provide details of the risk factors",
        key="risk_comment"
    )
    risk_factor = "Yes"
else:
    risk_factor = "No"
    risk_factor_comment = ""

# Row 7: Expected Start Date
row7_col1, _ = st.columns([1, 1])
with row7_col1:
    expected_start = st.date_input(
        "Expected Start Date",
        min_value=date.today(),
        help="Select expected start date"
    )
# ------------------- SECTION 3: Space Assesment -------------------
st.header("✅ Section 3: Space Assessment")

# --- Package Type Selection ---
package_types = ["Crates", "Boxes", "Bags", "Oversized/Overweight", "Pallets", "Other"]
space_units = ["CBM", "SQFT", "Pallets", "Not Sure"]

# --- Row 1: Package Type & Space Unit ---
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    selected_package_types = st.multiselect(
        "Package Type(s)",
        options=package_types,
        help="Select all applicable package types"
    )

with row1_col2:
    space_unit = st.selectbox(
        "Space Unit",
        options=space_units,
        help="Choose unit of space measurement"
    )

# --- Number of Packages ---
num_packages_dict = {}
for package in selected_package_types:
    num_packages_dict[package] = st.text_input(
        f"Number of {package}",
        help=f"Enter the number of {package.lower()}",
        key=f"num_{package.lower().replace('/', '_')}"
    )

# --- Row 2: Show only if detailed info required ---
space_types = ["Crates", "Bags", "Oversized/Overweight", "Pallets"]
if any(pt in selected_package_types for pt in space_types):
    st.subheader("📏 Detailed Space Requirements")

    col1, col2, col3 = st.columns(3)

    with col1:
        average_weight = st.text_input(
            "Average Weight (kg)",
            help="Enter average weight of the packages"
        )

    with col2:
        dimensions = st.text_input(
            "Dimensions (L x W x H in cm)",
            help="Enter typical dimensions of packages"
        ) 

    with col3:
        approx_space = st.text_input(
            "Approximate Space Required",
            help="Rough estimate of total space needed"
        )
#------Packing list--------
packing_list = st.file_uploader("Upload Packing List (from WhatsApp)", type=["pdf","doc","jpg","png"],help="Upload packing list document")

# --- Handling In/Out ---
col_in, col_out = st.columns(2)

with col_in:
    handling_in = st.radio(
        "Handling In Required?",
        options=["Yes", "No"],
        horizontal=True,
        key="handling_in"
    )

with col_out:
    handling_out = st.radio(
        "Handling Out Required?",
        options=["Yes", "No"],
        horizontal=True,
        key="handling_out"
    )

# --- Conditional Warning ---
if handling_in == "Yes" and handling_out == "No":
    st.markdown("""
        <div style="background-color:#fff3cd; border-left:6px solid #ffa500; padding:10px; border-radius:4px;">
        ❗ <strong>Warning:</strong> Without <b>Handling Out</b>, we cannot track your inventory. 
        If tracking is important, warehouse must assist with Handling Out.
        </div>
    """, unsafe_allow_html=True)

# You can now use `handling_out` to conditionally display Section 4
if handling_out == "Yes":
    st.markdown("✅ Proceed to Section 4")

#---------------Section 4 - Inventory and Tracking--------------
st.header("✅ Section 4: Inventory & Tracking")

# --- Handling Types ---
col1, col2 = st.columns(2)

with col1:
    handling_in_type = st.selectbox(
        "Handling In Type",
        ["Loose", "Palletized"],
        key="handling_in_type"
    )

with col2:
    handling_out_type = st.selectbox(
        "Handling Out Type",
        ["Loose", "Palletized", "Pieces"],
        key="handling_out_type"
    )

# --- SKU Logic Branches ---
sku_count = None
segregation = None
seg_charges_note = ""
inventory_charge_warning = ""

# Conditions where SKU question must be asked
if (handling_in_type == "Loose" and handling_out_type == "Loose") or \
   (handling_in_type == "Palletized" and handling_out_type in ["Loose", "Palletized"]):

    st.subheader("🧩 SKU Details")
    # Initialize defaults first
 # Initialize defaults first
    mixed_skus = "No"
    segregation = "No"
    if handling_in_type == "Palletized" and handling_out_type in ["Loose", "Palletized"]:
        mixed_skus = st.selectbox(
            "Are SKUs mixed per pallet?",
            ["Yes", "No"],
            key="mixed_skus"
        )

        if mixed_skus == "Yes":
            segregation = st.selectbox(
                "Do you need segregation?",
                ["Yes", "No"],
                key="need_segregation"
            )

            if segregation == "Yes":
                st.markdown("""
                    <div style="background-color:#fff3cd; border-left:6px solid #ffc107; padding:10px; border-radius:4px;">
                    ⚠️ <strong>Segregation Charges apply</strong>
                    </div>
                """, unsafe_allow_html=True)

    sku_count = st.number_input(
        "Number of SKUs",
        min_value=1,
        step=1
    )

# --- Inventory Charges Warning ---
# Show warning if SKU count > 5 and user inputs small volume

if sku_count and sku_count > 5:
    col_cbm, col_pallets = st.columns(2)

    with col_cbm:
        try:
            cbm = float(st.text_input("Total CBM", placeholder="e.g., 4.5"))
        except:
            cbm = 0.0

    with col_pallets:
        try:
            pallet_qty = int(st.text_input("Total Pallets", placeholder="e.g., 2"))
        except:
            pallet_qty = 0

    if pallet_qty < 3 or cbm < 5:
        st.markdown("""
            <div style="background-color:#f8d7da; border-left:6px solid #dc3545; padding:10px; border-radius:4px;">
            ❗ <strong>Inventory charges will apply.</strong> The partner will provide the cost.
            </div>
        """, unsafe_allow_html=True)

# ------------------- Documents Section -------------------
st.header("📎 Documents from WhatsApp")
documents = st.file_uploader("Upload Documents", accept_multiple_files=True,help="Required Documents:\n1. Emirates ID\n2. VAT Certificate\n3. Trade License")
#-----------------------------------------------------------------------------------------

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseUpload
import io

from googleapiclient.errors import HttpError


SPREADSHEET_ID = '1vAA_G-GhJFvz_z8e22PpvXNV8KEWgMsSZIErKxJNEL8'  # only the ID
SHEET_NAME = 'data'  # exact name of the sheet tab

SCOPES = ['https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive"]

# Use service account info from Streamlit secrets to create credentials
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=SCOPES
)

drive_service = build('drive', 'v3', credentials=credentials)
service = build('sheets', 'v4', credentials=credentials)

#Document Upload-------------------------------
from googleapiclient.errors import HttpError

SHARED_DRIVE_FOLDER_ID = '0AJ2EMdEDYgIcUk9PVA'  # update this

def upload_file_to_drive(file, folder_id=SHARED_DRIVE_FOLDER_ID):
    file_io = io.BytesIO(file.getbuffer())
    file_metadata = {'name': file.name, 'parents': [folder_id]}
    mime_type = file.type if file.type else "application/octet-stream"
    media = MediaIoBaseUpload(file_io, mimetype=mime_type, resumable=True)

    uploaded_file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id',
        supportsAllDrives=True  # IMPORTANT for shared drives
    ).execute()

    drive_service.permissions().create(
        fileId=uploaded_file['id'],
        body={'type': 'anyone', 'role': 'reader'},
        supportsAllDrives=True  # IMPORTANT
    ).execute()

    return f"https://drive.google.com/file/d/{uploaded_file['id']}/view?usp=sharing"

# ------------------- Save to Excel -------------------

def append_to_google_sheet(data: dict):
    try:
        sheet = service.spreadsheets()

        header = [
            "Company Name",
            "Point of Contact",
            "Email",
            "Phone",
            "Role",
            "Location Constraints",
            "Selected Location",
            "Commodity Type",
            "Commodity Name",
            "DG Class",
            "MSDS Uploaded",
            "Storage Type",
            "Specific Temperature (°C)",
            "Where is the Cargo now",
            "Comments on cargo location",
            "Known Risk Factor [Yes/No]",
            "Risk Factor Comments",
            "Expected Start Date",
            "Package Type(s)",
            "Space Unit",
            "Number of Crates (if selectd)",
            "Number of Boxes (if selectd)",
            "Number of Bags (if selectd)",
            "Number of Oversized/Overweight (if selectd)",
            "Number of Pallets (if selectd)",
            "Number of Other (if selectd)",
            "Avg Weight (KG)",
            "Dimensions (L X W X H in cm)",
            "Approximate Space Required",
            "Packing List File (link)",
            "Handling In Required [Yes/No]",
            "Handling Out Required [Yes/No]",
            "Handling In Type [Loose/Palletised]",
            "Handling Out Type [Loose/Palletised/Pieces]",
            "Mixed SKUs",
            "Segregation Required",
            "No of SKU's",
            "Total CBM",
            "Total Palletes",
            "Inventory Charge [Yes/No]",
            "Documents Uploaded"
        ]

        # Check if header exists
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=SHEET_NAME
        ).execute()

        existing_header = result.get('values', [])

        # If header is missing, insert it
        if not existing_header:
            sheet.values().update(
                spreadsheetId=SPREADSHEET_ID,
                range=f"{SHEET_NAME}!A1",
                valueInputOption='RAW',
                body={'values': [header]}
            ).execute()

        # Prepare row in header order
        values = [[data.get(col, "") for col in header]]

        # Append data
        append_result = sheet.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME}!A1",  # use just the sheet name
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body={'values': values}
        ).execute()

        return append_result

    except Exception as e:
        st.error(f"Error while writing to Google Sheet: {e}")
        import traceback
        st.text(traceback.format_exc())
        st.stop()

# ------------------- Submit Button -------------------
if st.button("Submit Form"):
    segregation_required = "Yes" if mixed_skus == "Yes" and segregation == "Yes" else "No"
    packing_list_link = upload_file_to_drive(packing_list) if packing_list else "No"
    documents_links = []
    if documents:
        for doc in documents:
            uploaded_link = upload_file_to_drive(doc)
            documents_links.append(uploaded_link)
    
    msds_link = upload_file_to_drive(msds_file) if commodity_type == "DG" and msds_file else "No"

    summary = {
        "Company Name": company_name,
        "Point of Contact": contact_person,
        "Email": email,
        "Phone": phone,
        "Role": ", ".join(role) if isinstance(role, list) else role,
        "Location Constraints": location_constraint,
        "Selected Location": ", ".join(storage_location),
        "Commodity Type": commodity_type,
        "Commodity Name": commodity_name,
        "DG Class": ", ".join(dg_class_selected) if isinstance(dg_class_selected, list) else dg_class_selected,
        "MSDS Uploaded": upload_file_to_drive(msds_file) if msds_file else "No",
        "Storage Type": storage_type,
        "Specific Temperature (°C)": required_temperature if required_temperature else "N/A",
        "Where is the Cargo now": cargo_location,
        "Comments on cargo location": cargo_location_comment,
        "Known Risk Factor [Yes/No]": risk_factor,
        "Risk Factor Comments": risk_factor_comment if risk_factor == "Yes" else "N/A",
        "Expected Start Date": expected_start.strftime("%Y-%m-%d"),
        "Package Type(s)": ", ".join(selected_package_types),
        "Space Unit": space_unit,
        "Number of Crates (if selectd)": num_packages_dict.get("Crates", "N/A"),
        "Number of Boxes (if selectd)": num_packages_dict.get("Boxes", "N/A"),
        "Number of Bags (if selectd)": num_packages_dict.get("Bags", "N/A"),
        "Number of Oversized/Overweight (if selectd)": num_packages_dict.get("Oversized/Overweight", "N/A"),
        "Number of Pallets (if selectd)": num_packages_dict.get("Pallets", "N/A"),
        "Number of Other (if selectd)": num_packages_dict.get("Other", "N/A"),
        "Avg Weight (KG)": average_weight if 'average_weight' in locals() else "N/A",
        "Dimensions (L X W X H in cm)": dimensions if 'dimensions' in locals() else "N/A",
        "Approximate Space Required": approx_space if 'approx_space' in locals() else "N/A",
        "Packing List File (link)": upload_file_to_drive(packing_list) if packing_list else "No",
        "Handling In Required [Yes/No]": handling_in,
        "Handling Out Required [Yes/No]": handling_out,
        "Handling In Type [Loose/Palletised]": handling_in_type,
        "Handling Out Type [Loose/Palletised/Pieces]": handling_out_type,
        "Mixed SKUs": mixed_skus if 'mixed_skus' in locals() else "N/A",
        "Segregation Required": segregation if 'segregation' in locals() else "No",
        "No of SKU's": sku_count if 'sku_count' in locals() else "N/A",
        "Total CBM": cbm if 'cbm' in locals() else "N/A",
        "Total Palletes": pallet_qty if 'pallet_qty' in locals() else "N/A",
        "Inventory Charge [Yes/No]": "Yes" if sku_count and sku_count > 5 and (cbm < 5 or pallet_qty < 3) else "No",
        "Documents Uploaded": ", ".join([upload_file_to_drive(doc) for doc in documents]) if documents else "No"
    }

    # Append data to Google Sheet
    st.write("Data to append:", summary)
    append_result = append_to_google_sheet(summary)
    st.write("Append result:", append_result)
    # append_result = append_to_google_sheet(summary)

    st.success("✅ Form submitted successfully and data saved to Google Sheets!")
    st.json(summary)
