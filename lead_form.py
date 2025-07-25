import streamlit as st
from datetime import date

st.set_page_config(page_title="Storage Requirement Form", layout="centered")

st.title("📦 Storage Requirement Form")
# ------------------- SECTION 1: Contact Details -------------------
st.header("🟩 Section 1: Contact Details (Auto-Fetched)")

col1, col2 = st.columns(2)

with col1:
    st.text_input("Company Name", value="Autofetched Co.", disabled=True)
    st.text_input("Point of Contact", value="John Doe", disabled=True)

with col2:
    st.text_input("Email", value="john@autofetched.com", disabled=True)
    st.text_input("Phone", value="+971500000000", disabled=True)

# ------------------- SECTION 2: Storage Details -------------------
# ------------------- SECTION 2: Storage Details -------------------
st.header("🟦 Section 2: Storage Details")

# Row 1: Storage Location (Full Width)
storage_location = st.selectbox("Storage Location", locations)

# Row 2: Commodity Type (Left) | Commodity (Right)
row2_col1, row2_col2 = st.columns(2)
with row2_col1:
    commodity_type = st.selectbox("Commodity Type", commodity_types, key="commodity_type")
with row2_col2:
    commodity = st.text_input("Commodity")

# DG Highlight + MSDS Upload
if commodity_type == "DG":
    st.markdown(
        """
        <style>
        div[data-testid="stSelectbox"][data-key="commodity_type"] > div > div > div {
            background-color: #ff0000 !important;
            border: 2px solid red !important;
            border-radius: 8px;
            color: white !important;
            padding: 0.3rem 0.5rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.subheader("📄 MSDS (Material Safety Data Sheet)")
    st.info("⚠️ DG selected: Please upload the MSDS document for safety compliance.")
    msds_file = st.file_uploader("Upload MSDS Document", type=["pdf", "docx", "jpg", "png"])

# Row 3: Storage Type (Left) | Required Temperature (Right if needed)
row3_col1, row3_col2 = st.columns(2)
with row3_col1:
    storage_type = st.selectbox("Storage Type", storage_types)
with row3_col2:
    required_temperature = None
    if storage_type in ["Frozen", "Chilled Storage"]:
        required_temperature = st.number_input("Required Temperature (°C)", step=0.1)

# Row 4: Package Type (Left)
package_type = st.selectbox("Package Type", package_types)

# Conditional Layout for Package Types
if package_type == "Pallets":
    col_a, col_b = st.columns(2)
    with col_a:
        num_pallets = st.number_input("Number of Pallets", min_value=1, step=1)
    with col_b:
        pallet_type = st.selectbox("Type of Pallet", ["Standard", "Euro"])

    cbm_per_pallet = 1.8 if pallet_type == "Standard" else 1.44
    sqft_per_pallet = 13 if pallet_type == "Standard" else 10.03
    total_cbm = cbm_per_pallet * num_pallets
    total_sqft = sqft_per_pallet * num_pallets
    st.info(f"Approx. Expected Space: **{total_cbm:.2f} CBM** or **{total_sqft:.2f} SQFT**")

elif package_type == "Boxes":
    col_a, col_b = st.columns(2)
    with col_a:
        expected_space = st.number_input("Expected Space for Boxes", min_value=0.0, step=0.1)
    with col_b:
        space_unit = st.selectbox("Select Unit", ["CBM", "SQFT"])

elif package_type == "Oversized/Overweight":
    col_a, col_b = st.columns(2)
    with col_a:
        weight = st.number_input("Weight of Commodity (in KG)", min_value=0.0, step=0.1)
    with col_b:
        weight_unit = st.selectbox("Weight Unit", ["KG", "TON"])

    col_c, col_d = st.columns(2)
    with col_c:
        expected_space = st.number_input("Expected Space", min_value=0.0, step=0.1)
    with col_d:
        space_unit = st.selectbox("Select Unit", ["CBM", "SQFT"])

elif package_type == "Container":
    col_a, col_b = st.columns(2)
    with col_a:
        num_containers = st.number_input("Number of Containers", min_value=1, step=1)
    with col_b:
        container_type = st.selectbox("Container Size", ["40ft", "20ft"])

    cbm_per_container = 70 if container_type == "40ft" else 30
    sqft_per_container = 130 if container_type == "40ft" else 65
    total_cbm = cbm_per_container * num_containers
    total_sqft = sqft_per_container * num_containers
    st.info(f"Approx. Expected Space: **{total_cbm} CBM** or **{total_sqft} SQFT**")

elif package_type == "Bags":
    col_a, col_b = st.columns(2)
    with col_a:
        expected_space = st.number_input("Expected Space", min_value=0.0, step=0.1)
    with col_b:
        space_unit = st.selectbox("Select Unit", ["CBM", "SQFT"])

# COO / Location of Shipment (Left) | Expected Start Date (Right)
row5_col1, row5_col2 = st.columns(2)
with row5_col1:
    shipment_location = st.selectbox("COO / Location of Shipment", coo_options)
with row5_col2:
    expected_start = st.date_input("Expected Start Date", min_value=date.today())

# Upload Packing List
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
if handling_out in ["Loose", "Palletised", "Pieces", "Boxes", "Loading"]:
    st.header("🟥 Section 4: Detailed Handling Requirements")
    sku_count = st.number_input("Number of SKUs", min_value=0)

    if handling_out in ["Loose", "Palletised", "Pieces", "Boxes"]:
        mixed_skus = st.selectbox("Are SKUs in the Pallets Mixed?", ["Yes", "No"])

        if mixed_skus == "Yes":
            # Show the checkbox as checked and disabled (mandatory)
            st.checkbox("Segregation Required", value=True, disabled=True)

    tracking_method = st.selectbox("How is Inventory Tracking Maintained?", ["Lot Number", "Expiry Date", "SKU Value"])


# ------------------- Documents Section -------------------
st.header("📎 Documents from WhatsApp")
documents = st.file_uploader("Upload Documents (Photo ID, Trade License, Emirates ID, VAT)", accept_multiple_files=True)

# ------------------- Submit -------------------
if st.button("Submit Form"):
    st.success("✅ Form submitted successfully!")
