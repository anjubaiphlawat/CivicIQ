import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ------------------ Sample Complaints ------------------
complaints_data = {
    "Area": ["Village A", "Village B", "Village A", "Village C", "Village B"],
    "Complaint_Text": [
        "Our village well water is dirty and unsafe.",
        "The school toilets are broken and unhygienic.",
        "The main road is full of potholes.",
        "Water supply is inconsistent in our area.",
        "The school playground is damaged."
    ]
}

complaints = pd.DataFrame(complaints_data)

# ------------------ Categories ------------------
categories = {
    "Water": ["water", "well", "drinking"],
    "Sanitation": ["toilet", "sanitation", "hygienic"],
    "Road": ["road", "potholes", "street"],
    "Education": ["school", "playground", "education"]
}

# ------------------ Policies ------------------
policies = {
    "Water": "All villages must have clean drinking water by 2025.",
    "Sanitation": "Every school should have proper sanitation facilities.",
    "Road": "Road maintenance must be done annually in rural areas.",
    "Education": "Schools should maintain safe infrastructure for students."
}

# ------------------ Categorization Function ------------------
def categorize_complaint(text):
    text = text.lower()
    for category, keywords in categories.items():
        for word in keywords:
            if word in text:
                return category
    return "Other"

complaints["Category"] = complaints["Complaint_Text"].apply(categorize_complaint)

# ------------------ Streamlit UI ------------------
st.title("CivicIQ 🧠")
st.subheader("AI for Transparent and Smart Governance")

# ---- Complaint Submission ----
st.header("📢 Submit a Complaint")
area_input = st.text_input("Enter Area / Village Name")
complaint_input = st.text_area("Enter Complaint")

if st.button("Submit Complaint"):
    new_data = pd.DataFrame({
        "Area": [area_input],
        "Complaint_Text": [complaint_input]
    })
    new_data["Category"] = new_data["Complaint_Text"].apply(categorize_complaint)
    complaints = pd.concat([complaints, new_data], ignore_index=True)
    st.success("Complaint submitted successfully!")

# ---- Complaint Chart ----
st.header("📊 Complaint Category Overview")
category_counts = complaints["Category"].value_counts()

fig, ax = plt.subplots()
category_counts.plot(kind="bar", ax=ax)
ax.set_xlabel("Category")
ax.set_ylabel("Number of Complaints")
ax.set_title("Complaints by Category")
st.pyplot(fig)

# ---- Policy Gap Detection ----
st.header("🚨 Policy Implementation Gaps")

gap_results = []

for category, policy_text in policies.items():
    count = category_counts.get(category, 0)
    if count > 0:
        gap_results.append({
            "Policy Area": category,
            "Policy": policy_text,
            "Number of Complaints": count,
            "Status": "⚠ Implementation Gap Detected"
        })

gap_df = pd.DataFrame(gap_results)
st.dataframe(gap_df)

# ---- Show All Complaints ----
st.header("📄 All Complaints")
st.dataframe(complaints)
