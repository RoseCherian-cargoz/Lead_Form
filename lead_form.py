import streamlit as st
from datetime import date

st.set_page_config(page_title="Storage Requirement Form", layout="centered")

st.title("📦 Lead Form")
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
billing_unit = ["CBM", "SQFT", "SQM", "Per Pallet", "Fixed Unit"]
coo_options = ["Mainland", "Freezone", "On the way to UAE", "Another Warehouse"]

# Row 1: Storage Location (Full Width)
storage_location = st.selectbox("Storage Location", locations)

# # Row 2: Commodity Type (Left) | Commodity (Right)
# row2_col1, row2_col2 = st.columns(2)
# with row2_col1:
#     # Wrap Commodity Type in a container for unique targeting
#     st.markdown('<div id="commodity-type-container">', unsafe_allow_html=True)
#     commodity_type = st.selectbox("Commodity Type", commodity_types, key="commodity_type")
#     st.markdown('</div>', unsafe_allow_html=True)

# with row2_col2:
#     commodity = st.text_input("Commodity")

# DG Highlight + MSDS Upload
# Row 2: Commodity Type (Left) | Commodity (Right)
row2_col1, row2_col2 = st.columns(2)

# --- COMMODITY TYPE (Left Column) ---
with row2_col1:
    if "commodity_type" not in st.session_state:
        st.session_state["commodity_type"] = commodity_types[0]

    # Custom-styled container around the selectbox
    if st.session_state["commodity_type"] == "DG":
        st.markdown(
            """
            <style>
            div[data-testid="stSelectbox"] {
                background-color: #ffe6e6;
                border: 2px solid red;
                border-radius: 8px;
                padding: 5px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

    commodity_type = st.selectbox("Commodity Type", commodity_types, key="commodity_type")

# --- COMMODITY INPUT (Right Column) ---
with row2_col2:
    commodity = st.text_input("Commodity", key="commodity_text_input")

# --- DG-SPECIFIC FIELDS ---
if commodity_type == "DG":
    # MSDS warning with fully red styling
    st.markdown(
        """
        <div style="
            background-color: #ffcccc;
            color: #a94442;
            border: 2px solid red;
            padding: 16px;
            border-radius: 8px;
            font-weight: bold;
            margin-top: 10px;">
            ⚠️ <strong>DG selected:</strong> Please upload the MSDS document for safety compliance.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("📄 MSDS (Material Safety Data Sheet)")
    msds_file = st.file_uploader(
        "Upload MSDS Document", type=["pdf", "docx", "jpg", "png"], key="msds_uploader"
    )
with row2_col2:
    # commodity = st.text_input("Commodity", key="commodity_text_input")

# Row 3: Storage Type (Left) | Required Temperature (Right if needed)
row3_col1, row3_col2 = st.columns(2)
with row3_col1:
    storage_type = st.selectbox("Storage Type", storage_types)
with row3_col2:
    required_temperature = None
    if storage_type in ["Frozen", "Chilled Storage"]:
        required_temperature = st.number_input("Required Temperature (°C)", step=0.1)

# Row 4: Package Type (Left) | Billing Type (Right)
row4_col1, row4_col2 = st.columns(2)
with row4_col1:
    package_type = st.selectbox("Package Type", package_types)
with row4_col2:
    billing_unit = st.selectbox("Billing Unit", billing_unit)

# Conditional Layout for Package Types
if package_type == "Pallets":
    col_a, col_b,col_c,col_d = st.columns(4)
    with col_a:
        num_pallets = st.number_input("Number of Pallets", min_value=1, step=1)
    with col_b:
        pallet_type = st.selectbox("Type of Pallet", ["Standard", "Euro"])
    with col_c:
        expected_space = st.number_input("Expected Space", min_value=0.0, step=0.1)
    with col_d:
        space_unit = st.selectbox("Select Unit", ["CBM", "SQFT","per Pallet","Fixed Unit"])

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
        space_unit = st.selectbox("Select Unit", ["CBM", "SQFT","per Pallet","Fixed Unit"])

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
        space_unit = st.selectbox("Select Unit", ["CBM", "SQFT","per Pallet","Fixed Unit"])

elif package_type == "Container":
    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a:
        num_containers = st.number_input("Number of Containers", min_value=1, step=1)
    with col_b:
        container_type = st.selectbox("Container Size", ["40ft", "20ft"])
    with col_c:
        expected_space = st.number_input("Expected Space", min_value=0.0, step=0.1)
    with col_d:
        space_unit = st.selectbox("Select Unit", ["CBM", "SQFT","per Pallet","Fixed Unit"])

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
        space_unit = st.selectbox("Select Unit", ["CBM", "SQFT","per Pallet","Fixed Unit"])

# COO / Location of Shipment (Left) | Expected Start Date (Right)
# COO / Location of Shipment and Expected Start Date (Stacked on Left)
col_left, col_right = st.columns([1, 3])  # Left for fields, Right for spacing
with col_left:
    shipment_location = st.selectbox("COO / Location of Shipment", coo_options)
    expected_start = st.date_input("Expected Start Date", min_value=date.today())

# Upload Packing List
packing_list = st.file_uploader("Upload Packing List (from WhatsApp)", type=["pdf", "doc", "jpg", "png"])


# ------------------- SECTION 3: Handling Requirements -------------------
st.header("🟧 Section 3: Handling Requirements")

col_1,col_2=st.columns(2)
with col_1:
    handling_in = st.selectbox("Handling In", ["Loose", "Pallets", "Not Required","Offloading"])
with col_2:
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
