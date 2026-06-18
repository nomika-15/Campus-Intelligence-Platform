import streamlit as st
import joblib
import numpy as np
import shap
from reportlab.pdfgen import canvas
from database import save_student


def generate_pdf(
    student_name,
    college_name,
    department,
    semester,
    probability,
    success_score,
    profile_rating
):

    pdf = canvas.Canvas("student_report.pdf")

    pdf.setTitle("Campus Intelligence Report")

    pdf.drawString(100, 800, "Campus Intelligence Platform Report")

    pdf.drawString(100, 760, f"College: {college_name}")
    pdf.drawString(100, 740, f"Student Name: {student_name}")
    pdf.drawString(100, 720, f"Department: {department}")
    pdf.drawString(100, 700, f"Semester: {semester}")

    pdf.drawString(
        100,
        660,
        f"Placement Probability: {round(probability * 100, 2)}%"
    )

    pdf.drawString(
        100,
        640,
        f"Success Score: {round(success_score, 2)}"
    )

    pdf.drawString(
        100,
        620,
        f"Profile Rating: {profile_rating}"
    )

    pdf.save()


st.set_page_config(
    page_title="Campus Intelligence Platform",
    page_icon="🎓",
    layout="wide"
)

import os

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "models",
    "placement_model.pkl"
)

model = joblib.load(MODEL_PATH)

st.title("🎓 Campus Intelligence Platform")
st.markdown("### AI-Powered Student Placement Prediction System")

st.divider()

st.subheader("👨‍🎓 Student Information")

college_name = st.text_input(
    "College Name",
    placeholder="Enter College Name"
)

student_name = st.text_input(
    "Student Name",
    placeholder="Enter Student Name"
)
department = st.selectbox(
    "Department",
    [
        "AI & Data Science (AIDS)",
        "Computer Science Engineering (CSE)",
        "Information Technology (IT)",
        "Artificial Intelligence & Machine Learning (AIML)",
        "Electronics & Communication Engineering (ECE)",
        "Electrical & Electronics Engineering (EEE)",
        "Mechanical Engineering",
        "Civil Engineering",
        "Biomedical Engineering",
        "Mechatronics Engineering",
        "Aeronautical Engineering",
        "Automobile Engineering",
        "Chemical Engineering",
        "Cyber Security",
        "Data Science",
        "Robotics & Automation",
        "Electronics & Instrumentation Engineering (EIE)",
        "Production Engineering",
        "Agricultural Engineering",
        "Biotechnology"
    ]
)

semester = st.selectbox(
    "Semester",
    ["1", "2", "3", "4", "5", "6", "7", "8"]
)

st.divider()

st.subheader("📋 Academic Details")

col1, col2 = st.columns(2)

with col1:

    cgpa = st.number_input(
        "CGPA",
        min_value=0.0,
        max_value=10.0,
        value=8.0
    )

    attendance = st.number_input(
        "Attendance (%)",
        min_value=0,
        max_value=100,
        value=85
    )

    coding_score = st.number_input(
        "Coding Score",
        min_value=0,
        max_value=100,
        value=75
    )

    aptitude_score = st.number_input(
        "Aptitude Score",
        min_value=0,
        max_value=100,
        value=75
    )

with col2:

    communication_score = st.number_input(
        "Communication Score",
        min_value=0,
        max_value=100,
        value=75
    )

    projects_count = st.number_input(
        "Projects Count",
        min_value=0,
        max_value=10,
        value=2
    )

    internships_count = st.number_input(
        "Internships Count",
        min_value=0,
        max_value=5,
        value=1
    )

    hackathon_count = st.number_input(
        "Hackathon Count",
        min_value=0,
        max_value=10,
        value=1
    )

st.divider()
if st.button("🚀 Predict Placement", use_container_width=True):

    student = np.array([[
        cgpa,
        attendance,
        coding_score,
        aptitude_score,
        communication_score,
        projects_count,
        internships_count,
        hackathon_count
    ]])

    prediction = model.predict(student)[0]
    probability = model.predict_proba(student)[0][1]

    st.divider()
    st.subheader("🧠 AI Explanation")

    if cgpa >= 8:
        st.success("✅ Strong CGPA")

    if coding_score >= 70:
        st.success("✅ Strong Coding Skills")

    if aptitude_score >= 70:
        st.success("✅ Strong Aptitude Skills")

    if communication_score < 70:
        st.warning("⚠ Communication Skills Need Improvement")

    if projects_count < 3:
        st.warning("⚠ Build More Projects")

    if internships_count < 1:
        st.warning("⚠ Complete an Internship")

    success_score = (
        cgpa * 10 +
        coding_score * 0.4 +
        aptitude_score * 0.3 +
        communication_score * 0.1 +
        projects_count * 3 +
        internships_count * 5
    )

    if success_score >= 140:
        profile_rating = "Excellent ⭐"
    elif success_score >= 110:
        profile_rating = "Good 👍"
    elif success_score >= 80:
        profile_rating = "Average ⚡"
    else:
        profile_rating = "Needs Improvement 🔴"

    st.subheader("📊 Prediction Results")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Placement Probability",
            f"{round(probability * 100, 2)}%"
        )

    with col2:
        st.metric(
            "Success Score",
            round(success_score, 2)
        )

    with col3:
        st.metric(
            "Profile Rating",
            profile_rating
        )

    st.divider()

    st.subheader("🧾 Student Summary")

    st.write(f"**College:** {college_name}")
    st.write(f"**Student Name:** {student_name}")
    st.write(f"**Department:** {department}")
    st.write(f"**Semester:** {semester}")

    if prediction == 1:
        st.success("✅ Student is Likely to be Placed")
    else:
        st.error("❌ Student is Not Likely to be Placed")

    save_student(
        student_name,
        college_name,
        department,
        semester,
        round(probability * 100, 2),
        round(success_score, 2),
        profile_rating
    )

    st.divider()
    st.subheader("💡 Recommendations")

    recommendations = []

    if coding_score < 70:
        recommendations.append("Improve Coding Skills")

    if aptitude_score < 70:
        recommendations.append("Practice Aptitude Questions")

    if communication_score < 70:
        recommendations.append("Improve Communication Skills")

    if projects_count < 3:
        recommendations.append("Build More Projects")

    if internships_count < 1:
        recommendations.append("Complete an Internship")

    if len(recommendations) == 0:
        st.success("🎉 Excellent Profile for Placement")
    else:
        for item in recommendations:
            st.warning(item)

    generate_pdf(
        student_name,
        college_name,
        department,
        semester,
        probability,
        success_score,
        profile_rating
    )

    with open("student_report.pdf", "rb") as pdf_file:
        st.download_button(
            label="📄 Download Report",
            data=pdf_file,
            file_name="Campus_Intelligence_Report.pdf",
            mime="application/pdf"
        )
        
