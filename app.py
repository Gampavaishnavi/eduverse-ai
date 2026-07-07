import streamlit as st
import pandas as pd
import bcrypt
from database import SessionLocal, User, Student
from utils.gemini_integration import chat_with_data, get_student_insight

st.set_page_config(page_title="Eduverse AI", page_icon="🎓", layout="wide")

# Custom CSS for modern look
st.markdown("""
<style>
    .metric-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .badge {
        background-color: #ede9fe;
        color: #4f46e5;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
        font-weight: bold;
    }
    .deadline {
        background-color: #fef2f2;
        color: #991b1b;
        padding: 10px;
        border-left: 4px solid #ef4444;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'username' not in st.session_state:
    st.session_state.username = None

def login():
    st.markdown("<h1 style='text-align: center;'>Eduverse AI Login</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b;'>Student Decision Intelligence Platform</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        username = st.text_input("Username (admin or Student ID)")
        password = st.text_input("Password", type="password")
        if st.button("Sign In", use_container_width=True):
            db = SessionLocal()
            user = db.query(User).filter(User.username == username).first()
            if user:
                try:
                    if bcrypt.checkpw(password.encode(), user.password_hash.encode()):
                        st.session_state.user_role = user.role
                        st.session_state.username = user.username
                        st.rerun()
                    else:
                        st.error("Invalid password.")
                except Exception as e:
                    # Fallback for old plaintext passwords if they didn't run the new seeder
                    if password == user.password_hash:
                        st.session_state.user_role = user.role
                        st.session_state.username = user.username
                        st.rerun()
                    else:
                        st.error("Invalid password.")
            else:
                st.error("Invalid username.")
            db.close()

def faculty_dashboard():
    st.sidebar.title("👨‍🏫 Faculty Panel")
    active_tab = st.sidebar.radio("Navigation", ["📊 Overview", "👥 Student Directory", "🤖 AI Insights"])
    
    st.sidebar.markdown("---")
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update(user_role=None, username=None), use_container_width=True)
    
    st.title("Faculty Dashboard")
    
    db = SessionLocal()
    students = db.query(Student).all()
    
    if active_tab == "📊 Overview":
        st.subheader("Class Performance Metrics")
        col1, col2, col3 = st.columns(3)
        avg_att = sum(s.attendance for s in students) / len(students) if students else 0
        col1.markdown(f"<div class='metric-card'><h3>Total Students</h3><h2>{len(students)}</h2></div>", unsafe_allow_html=True)
        col2.markdown(f"<div class='metric-card'><h3>Avg Attendance</h3><h2>{avg_att:.1f}%</h2></div>", unsafe_allow_html=True)
        high_risk = sum(1 for s in students if s.risk_category == 'High')
        col3.markdown(f"<div class='metric-card'><h3>High Risk Students</h3><h2 style='color:red;'>{high_risk}</h2></div>", unsafe_allow_html=True)
        
        st.subheader("Exam Trajectories")
        df = pd.DataFrame([{"ID": s.student_id, "Midterm": s.mid_exam, "Final": s.final_exam} for s in students])
        if not df.empty:
            st.line_chart(df.set_index("ID"))

    elif active_tab == "👥 Student Directory":
        st.subheader("Student Directory")
        st.dataframe(pd.DataFrame([{
            "ID": s.student_id,
            "Name": s.name,
            "Attendance": s.attendance,
            "Midterm": s.mid_exam,
            "Final": s.final_exam,
            "Risk": s.risk_category
        } for s in students]))
        
        st.markdown("### Quick Actions")
        sel_student = st.selectbox("Select Student to Mark Attendance", [s.student_id for s in students])
        col1, col2 = st.columns(2)
        if col1.button("✅ Mark Present"):
            s = db.query(Student).filter(Student.student_id == sel_student).first()
            s.attendance = min(100, s.attendance + 1.5)
            db.commit()
            st.success(f"Marked {s.name} present! Attendance is now {s.attendance:.1f}%")
        if col2.button("❌ Mark Absent"):
            s = db.query(Student).filter(Student.student_id == sel_student).first()
            s.attendance = max(0, s.attendance - 1.5)
            db.commit()
            st.success(f"Marked {s.name} absent! Attendance is now {s.attendance:.1f}%")

    elif active_tab == "🤖 AI Insights":
        st.subheader("Gemini AI Engine")
        query = st.text_input("Ask a question about the class:")
        if st.button("Generate Insight"):
            avg_att = sum(s.attendance for s in students) / len(students) if students else 0
            summary = f"Total students: {len(students)}. Avg Attendance: {avg_att:.1f}%."
            with st.spinner("Processing..."):
                resp = chat_with_data(query, summary)
            st.info(resp)
            
    db.close()

def student_dashboard():
    db = SessionLocal()
    student = db.query(Student).filter(Student.student_id == st.session_state.username).first()
    
    st.sidebar.title("🎓 Student Portal")
    if student:
        st.sidebar.markdown(f"**{student.name}**")
        
    active_tab = st.sidebar.radio("Navigation", ["📈 Overview", "📅 Timetable & Tasks", "🤖 AI Study Plan"])
    
    st.sidebar.markdown("---")
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update(user_role=None, username=None), use_container_width=True)
    
    if not student:
        st.error("Student profile not found.")
        db.close()
        return
        
    st.title(f"Welcome back, {student.name}!")
    st.markdown(f"**ID:** {student.student_id} | **Dept:** {student.department} | **Sem:** {student.semester}")
    st.divider()
    
    if active_tab == "📈 Overview":
        col1, col2, col3 = st.columns(3)
        col1.markdown(f"<div class='metric-card'><h3>Attendance</h3><h2>{student.attendance}%</h2></div>", unsafe_allow_html=True)
        col2.markdown(f"<div class='metric-card'><h3>Assignments</h3><h2>{student.assignment_score}/100</h2></div>", unsafe_allow_html=True)
        col3.markdown(f"<div class='metric-card'><h3>Current GPA</h3><h2>{student.previous_gpa}</h2></div>", unsafe_allow_html=True)
        
        st.subheader("Achievements")
        if student.attendance > 90:
            st.markdown("<div class='badge'>🌟 Attendance Star: 90%+ Attendance</div>", unsafe_allow_html=True)
        if student.final_exam > 85:
            st.markdown("<div class='badge'>🚀 High Achiever: Top marks in Finals</div>", unsafe_allow_html=True)
            
        st.subheader("Your Exam Performance Trajectory")
        df = pd.DataFrame([
            {"Exam": "Midterm", "Score": student.mid_exam}, 
            {"Exam": "Final", "Score": student.final_exam}
        ])
        st.line_chart(df.set_index("Exam"))

    elif active_tab == "📅 Timetable & Tasks":
        st.subheader("Upcoming Deadlines")
        st.markdown("<div class='deadline'><b>Tomorrow:</b> Machine Learning Quiz 3</div>", unsafe_allow_html=True)
        st.markdown("<div class='deadline'><b>Friday:</b> Data Structures Assignment Due</div>", unsafe_allow_html=True)
        st.markdown("<div class='deadline' style='border-color:#f59e0b; background:#fef3c7; color:#b45309;'><b>Next Week:</b> Midterm Exams Begin</div>", unsafe_allow_html=True)

    elif active_tab == "🤖 AI Study Plan":
        st.subheader("Personalized Study Plan by Gemini AI")
        if st.button("Generate My Plan"):
            with st.spinner("Analyzing your academic profile..."):
                s_dict = {"Student_ID": student.student_id, "Attendance": student.attendance, "Risk_Category": student.risk_category or "Low"}
                resp = get_student_insight(s_dict)
            st.info(resp)
            
    db.close()

if st.session_state.user_role == 'faculty':
    faculty_dashboard()
elif st.session_state.user_role == 'student':
    student_dashboard()
else:
    login()
