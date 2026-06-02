from fpdf import FPDF
import datetime


class CareerReportPDF(FPDF):
    """Custom PDF Report Generator."""

    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Career Guidance Report', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')


def generate_pdf_report(user_data, recommendations, skill_gaps, output_path="career_report.pdf"):
    """
    Generates a detailed PDF report for the user.
    """
    pdf = CareerReportPDF()
    pdf.add_page()

    # --- User Profile Section ---
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'User Profile', 0, 1)
    pdf.set_font('Arial', '', 10)

    pdf.cell(50, 8, f"Name: {user_data.get('name', 'N/A')}", 0, 1)
    pdf.cell(50, 8, f"Age: {user_data.get('age', 'N/A')}", 0, 1)
    pdf.cell(50, 8, f"Education: {user_data.get('degree', 'N/A')}", 0, 1)
    pdf.cell(50, 8, f"Personality: {user_data.get('personality', 'N/A')}", 0, 1)
    pdf.ln(5)

    # --- Top Recommendations ---
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Top 5 Recommended Careers', 0, 1)
    pdf.set_font('Arial', '', 10)

    for i, rec in enumerate(recommendations, 1):
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 8, f"{i}. {rec['Career']} ({rec['Domain']})", 0, 1)
        pdf.set_font('Arial', '', 9)
        pdf.cell(0, 6, f"Match Score: {rec['Match Score']}%", 0, 1)
        pdf.cell(0, 6, f"Description: {rec['Description']}", 0, 1)

        matched = ", ".join(rec['Matched Skills']) if rec['Matched Skills'] else "None"
        pdf.cell(0, 6, f"Matching Skills: {matched}", 0, 1)
        pdf.ln(3)

    # --- Skill Gap Analysis ---
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Skill Gap Analysis', 0, 1)

    for gap in skill_gaps:
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 8, f"Career: {gap['Career']}", 0, 1)
        pdf.set_font('Arial', '', 9)

        missing = ", ".join(gap['Missing Skills']) if gap['Missing Skills'] else "None"
        pdf.cell(0, 6, f"Missing Skills: {missing}", 0, 1)

        courses = ", ".join(gap['Suggested Courses']) if gap['Suggested Courses'] else "None"
        pdf.cell(0, 6, f"Recommended Courses: {courses}", 0, 1)
        pdf.ln(5)

    # --- Footer ---
    pdf.set_font('Arial', 'I', 8)
    pdf.cell(0, 10, f"Report generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1)

    pdf.output(output_path)
    return output_path