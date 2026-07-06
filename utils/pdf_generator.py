from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Eduverse AI - Student Report', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_student_report(student_data, ai_insight, output_path="reports/student_report.pdf"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)
    
    pdf.cell(0, 10, f"Student Name: {student_data.get('Student_Name', '')}", 0, 1)
    pdf.cell(0, 10, f"Student ID: {student_data.get('Student_ID', '')}", 0, 1)
    pdf.cell(0, 10, f"Department: {student_data.get('Department', '')}", 0, 1)
    
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, "Academic Performance:", 0, 1)
    pdf.set_font('Arial', '', 12)
    
    pdf.cell(0, 10, f"Attendance: {student_data.get('Attendance', '')}%", 0, 1)
    pdf.cell(0, 10, f"Assignment Score: {student_data.get('Assignment_Score', '')}", 0, 1)
    pdf.cell(0, 10, f"Mid Exam: {student_data.get('Mid_Exam', '')}", 0, 1)
    pdf.cell(0, 10, f"Risk Category: {student_data.get('Risk_Category', '')}", 0, 1)
    
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, "AI Recommendations:", 0, 1)
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, str(ai_insight))
    
    pdf.output(output_path)
    return output_path
