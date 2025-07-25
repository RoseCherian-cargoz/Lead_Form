import streamlit as st
from datetime import date

st.set_page_config(page_title="Storage Requirement Form", layout="centered")

st.title("📦 Storage Requirement Form")

# ------------------- SECTION 1: Contact Details -------------------
st.header("🟩 Section 1: Contact Details (Auto-Fetched)")
st.text_input("Company Name", value="Autofetched Co.", disabled=True)
st.text_input("Point of Contact", value="John Doe", disabled=True)
st.text_input("Email", value="john@autofetched.com", disabled=True)
st.text_input("Phone", value="+971500000000", disabled=True)

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
units = ["CBM", "SQFT", "SQM","Pallete","Fixed Unit"]
coo_options = ["Mainland", "Freezone", "On the way to UAE", "Another Warehouse"]

storage_location = st.selectbox("Storage Location", locations)
commodity_type = st.selectbox("Commodity Type", commodity_types)

# If DG is selected → Highlight + Show MSDS upload
if commodity_type == "DG":
    st.markdown(
        """
        <style>
        /* Target the commodity_type selectbox input area fully */
        div[data-testid="stSelectbox"][data-key="commodity_type"] > div[role="combobox"] > div:first-child {
            background-color: #ffcccc !important;  /* Light red/pink */
            border: 2px solid red !important;      /* Red border */
            border-radius: 8px;
            padding: 0.25rem 0.5rem;                /* Add some padding for better fill */
        }
        </style>
        """,
        unsafe_allow_html=True
    )


    # Show MSDS Section
    st.subheader("📄 MSDS (Material Safety Data Sheet)")
    st.info("⚠️ DG selected: Please upload the MSDS document for safety compliance.")
    
    msds_file = st.file_uploader("Upload MSDS Document", type=["pdf", "docx", "jpg", "png"])

commodity = st.text_input("Commodity")
storage_type = st.selectbox("Storage Type", storage_types)

# If Frozen or Chilled Storage is selected, show temperature field
required_temperature = None
if storage_type in ["Frozen", "Chilled Storage"]:
    required_temperature = st.number_input("Required Temperature (°C)", step=0.1)

package_type = st.selectbox("Package Type", package_types)
unit = st.selectbox("Measurement Unit", units)

# Conditional Fields for Package Type
if package_type == "Boxes" or package_type == "Bags":
    expected_space = st.number_input(f"Expected Space for {package_type}", min_value=0.0, step=0.1)
    space_unit = st.selectbox("Select Unit", ["CBM", "SQFT"])

elif package_type == "Oversized/Overweight":
    weight = st.number_input("Weight of Commodity (in KG)", min_value=0.0, step=0.1)
    weight_unit = st.selectbox("Weight Unit", ["KG", "TON"])
    expected_space = st.number_input("Expected Space", min_value=0.0, step=0.1)
    space_unit = st.selectbox("Select Unit", ["CBM", "SQFT"])

elif package_type == "Container":
    container_type = st.selectbox("Container Size", ["40ft", "20ft"])
    num_containers = st.number_input("Number of Containers", min_value=1, step=1)
    
    if container_type == "40ft":
        cbm_per_container = 70
        sqft_per_container = 130
    else:  # 20ft
        cbm_per_container = 30
        sqft_per_container = 65

    total_cbm = cbm_per_container * num_containers
    total_sqft = sqft_per_container * num_containers

    st.info(f"Approx. Expected Space: **{total_cbm} CBM** or **{total_sqft} SQFT**")

elif package_type == "Pallets":
    pallet_type = st.selectbox("Type of Pallet", ["Standard", "Euro"])
    num_pallets = st.number_input("Number of Pallets", min_value=1, step=1)

    if pallet_type == "Standard":
        cbm_per_pallet = 1.8
        sqft_per_pallet = 13
    else:  # Euro
        cbm_per_pallet = 1.44
        sqft_per_pallet = 10.03

    total_cbm = cbm_per_pallet * num_pallets
    total_sqft = sqft_per_pallet * num_pallets

    st.info(f"Approx. Expected Space: **{total_cbm:.2f} CBM** or **{total_sqft:.2f} SQFT**")

elif package_type == "Other":
    other_commodity = st.text_input("Enter Commodity Type")
    expected_space = st.number_input("Expected Space", min_value=0.0, step=0.1)
    space_unit = st.selectbox("Select Unit", ["CBM", "SQFT"])

shipment_location = st.selectbox("COO / Location of Shipment", coo_options)
expected_start = st.date_input("Expected Start Date", min_value=date.today())
packing_list = st.file_uploader("Upload Packing List (from WhatsApp)", type=["pdf", "doc", "jpg", "png"])

# ------------------- SECTION 3: Handling Requirements -------------------
st.header("🟧 Section 3: Handling Requirements")

handling_in = st.selectbox("Handling In", ["Loose", "Pallets", "Not Required","Offloading"])
handling_out = st.selectbox("Handling Out", ["Loose", "Pallets", "Not Required", "Pieces","Loading","Boxes"])

# Inventory Tracking Display
if handling_out == "Pallets":
    st.info("Inventory will be tracked by: Pallets")
elif handling_out == "Loose":
    st.info("Inventory will be tracked by: Boxes")
elif handling_out == "Pieces":
    st.info("Inventory will be tracked by: Pallets")

# ------------------- SECTION 4: Detailed Handling Requirements -------------------
if handling_out in ["Loose", "Pallets", "Pieces", "Boxes", "Loading"]:
    st.header("🟥 Section 4: Detailed Handling Requirements")
    sku_count = st.number_input("Number of SKUs", min_value=0)

    # Show "Are SKUs in the Pallets Mixed?" only for these handling_out values
    if handling_out in ["Loose", "Palletised", "Pieces", "Boxes"]:
        mixed_skus = st.selectbox("Are SKUs in the Pallets Mixed?", ["Yes", "No"])

    tracking_method = st.selectbox("How is Inventory Tracking Maintained?", ["Lot Number", "Expiry Date", "SKU Value"])

# ------------------- Documents Section -------------------
st.header("📎 Documents from WhatsApp")
documents = st.file_uploader("Upload Documents (Photo ID, Trade License, Emirates ID, VAT)", accept_multiple_files=True)

# ------------------- Submit -------------------
if st.button("Submit Form"):
    st.success("✅ Form submitted successfully!")

