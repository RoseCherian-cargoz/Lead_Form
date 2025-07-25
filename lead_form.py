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
commodity = st.text_input("Commodity")
commodity_type = st.selectbox("Commodity Type", commodity_types)
storage_type = st.selectbox("Storage Type", storage_types)
package_type = st.selectbox("Package Type", package_types)
unit = st.selectbox("Measurement Unit", units)

# Conditional Fields for Package Type
if package_type == "Loose":
    loose_items = st.number_input("Number of Loose Items", min_value=0)
elif package_type == "Palletised":
    num_pallets = st.number_input("Number of Pallets", min_value=0)
    dimensions_pallet = st.text_input("Dimensions of Commodity (Palletised)")
elif package_type == "Oversized/Overweight":
    weight = st.text_input("Weight of Commodity")
    dimensions_oversize = st.text_input("Dimensions of Commodity (Oversized)")
elif package_type == "Container":
    container_size = st.text_input("Size of Container")
    dimensions_container = st.text_input("Dimensions of Commodity (Container)")

shipment_location = st.selectbox("COO / Location of Shipment", coo_options)
expected_start = st.date_input("Expected Start Date", min_value=date.today())
packing_list = st.file_uploader("Upload Packing List (from WhatsApp)", type=["pdf", "doc", "jpg", "png"])

# ------------------- SECTION 3: Handling Requirements -------------------
st.header("🟧 Section 3: Handling Requirements")

handling_in = st.selectbox("Handling In", ["Loose", "Palletised", "Not Required"])
handling_out = st.selectbox("Handling Out", ["Loose", "Palletised", "Not Required", "Pieces"])

if handling_in in ["Loose", "Palletised"]:
    segregation_required = st.selectbox("Segregation Required?", ["Yes", "No"])

# Inventory Tracking Display
if handling_out == "Palletised":
    st.info("Inventory will be tracked by: Pallets")
elif handling_out == "Loose":
    st.info("Inventory will be tracked by: Boxes")
elif handling_out == "Pieces":
    st.info("Inventory will be tracked by: Pallets")

# ------------------- SECTION 4: Detailed Handling Requirements -------------------
if handling_out != "Not Required":
    st.header("🟥 Section 4: Detailed Handling Requirements")
    sku_count = st.number_input("Number of SKUs", min_value=0)
    if handling_out == "Palletised":
        mixed_skus = st.selectbox("Are SKUs in the Pallets Mixed?", ["Yes", "No"])
    tracking_method = st.selectbox("How is Inventory Tracking Maintained?", ["Lot Number", "Expiry Date", "SKU Value"])

# ------------------- Documents Section -------------------
st.header("📎 Documents from WhatsApp")
documents = st.file_uploader("Upload Documents (Photo ID, Trade License, Emirates ID, VAT)", accept_multiple_files=True)

# ------------------- Submit -------------------
if st.button("Submit Form"):
    st.success("✅ Form submitted successfully!")

