from flask import Flask, render_template, request, send_file
from pdf_generator import generate_pdf
import os
import fitz

from utils import (
    extract_resume_skills,
    extract_required_skills,
    get_missing_skills,
    calculate_ats,
    get_resume_rating,
    get_suggestions,
    extract_keywords,
    check_education,
    check_projects,
    check_experience,
    check_certifications,
    check_email,
    check_phone,
    check_github,
    generate_ai_feedback,
    generate_recruiter_review,
    analyze_projects,
    calculate_resume_strength,
    extract_section,
    calculate_job_fit,
    calculate_resume_health,
    calculate_score_breakdown,
    analyze_resume_sections,
    calculate_resume_success,
    
)
from interview_questions import generate_questions
app = Flask(__name__)

latest_result = {}


# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Analyze Resume
@app.route("/analyze", methods=["POST"])
def analyze():

    resume = request.files["resume"]
    job_description = request.form["job_description"]

    keywords = extract_keywords(job_description)

    upload_folder = os.path.join("static", "uploads")
    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, resume.filename)

    resume.save(file_path)

    doc = fitz.open(file_path)

    pdf_text = ""

    for page in doc:
        pdf_text += page.get_text()

    doc.close()
    print(repr(pdf_text))
    print("========== FULL PDF TEXT ==========")
    print(pdf_text)
    print("===================================")

    
    print("========== RESUME TEXT ==========")
    print(pdf_text)
    print("=================================")
    print("Total Length:", len(pdf_text))

    # ----------------------------
    # Skill Analysis
    # ----------------------------

    matched_skills = extract_resume_skills(pdf_text)

    required_skills = extract_required_skills(job_description)

    missing_skills = get_missing_skills(
        required_skills,
        matched_skills
    )


    ats_score = calculate_ats(
        required_skills,
        matched_skills
    )


    matched_required = []

    for skill in required_skills:
        if skill in matched_skills:
            matched_required.append(skill)


    resume_rating = get_resume_rating(ats_score)

    suggestions = get_suggestions(missing_skills)


    interview_questions = generate_questions(
        matched_skills
    )


    # ----------------------------
    # Resume Section Detection
    # ----------------------------

    education = check_education(pdf_text)

    experience = check_experience(pdf_text)

    projects = check_projects(pdf_text)

    certifications = check_certifications(pdf_text)

    email = check_email(pdf_text)

    phone = check_phone(pdf_text)

    github = check_github(pdf_text)


    project_analysis = analyze_projects(pdf_text)
    print("PROJECT ANALYSIS")
    print(project_analysis)


    total_sections = 7

    found_sections = 0


    if email:
        found_sections += 1

    if phone:
        found_sections += 1

    if github:
        found_sections += 1

    if education:
        found_sections += 1

    if experience:
        found_sections += 1

    if projects:
        found_sections += 1

    if certifications:
        found_sections += 1


    completeness_score = round(
        (found_sections / total_sections) * 100,
        2
    )
        # ----------------------------
    # AI Feedback
    # ----------------------------

    ai_feedback = generate_ai_feedback(
        ats_score,
        matched_skills,
        missing_skills,
        education,
        experience,
        projects,
        certifications
    )


    recruiter_review = generate_recruiter_review(
        ats_score,
        matched_skills,
        missing_skills,
        education,
        experience,
        projects,
        certifications
    )


    strength = calculate_resume_strength(
        ats_score,
        matched_skills,
        required_skills,
        education,
        experience,
        projects,
        certifications,
    )
    score_breakdown = calculate_score_breakdown(
        matched_skills,
        required_skills,
        education,
        experience,
        projects,
        certifications,

    )
    section_analysis = analyze_resume_sections(
        pdf_text,
        education,
        experience,
        projects,
        certifications,
        matched_skills
    )


    job_fit = calculate_job_fit(
    ats_score,
    completeness_score,
    strength["technical"],
    matched_skills,
    required_skills
    )

    resume_health = calculate_resume_health(
    email,
    phone,
    github,
    education,
    experience,
    projects,
    certifications,
    pdf_text
    )
    resume_success = calculate_resume_success(
        ats_score,
        job_fit,
        resume_health,
        completeness_score,
        section_analysis
    )


    # ----------------------------
    # Store Results
    # ----------------------------

    global latest_result

    latest_result = {

        "ats_score": ats_score,

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,

        "resume_rating": resume_rating,

        "suggestions": suggestions,

        "interview_questions": interview_questions,

        "education": education,

        "experience": experience,

        "projects": projects,

        "certifications": certifications,

        "email": email,

        "phone": phone,

        "github": github,

        "completeness_score": completeness_score,

        "ai_feedback": ai_feedback,

        "recruiter_review": recruiter_review,

        "strength": strength,

        "score_breakdown": score_breakdown,

        "section_analysis": section_analysis,
        "resume_success": resume_success,

        "project_analysis": project_analysis,

        "keywords": keywords,

        "job_fit": job_fit,

        "resume_health": resume_health,
    }

    print(project_analysis) 
    print("Resume Success:", resume_success)
    return render_template(

    "result.html",

    # ATS
    ats_score=round(ats_score, 2),
    resume_rating=resume_rating,

    # Skills
    matched_skills=matched_skills,
    required_skills=required_skills,
    missing_skills=missing_skills,

    matched_count=len(matched_skills),
    missing_count=len(missing_skills),
    required_count=len(required_skills),

    matched_required=matched_required,

    formula=f"({len(matched_required)} / {len(required_skills)}) × 100",

    # Suggestions
    suggestions=suggestions,
    ai_feedback=ai_feedback,

    # Resume Sections
    education=education,
    experience=experience,
    projects=projects,
    certifications=certifications,

    # Resume Strength
    strength=strength,

    score_breakdown=score_breakdown,
    section_analysis=section_analysis,
    resume_success=resume_success,

    # Recruiter Review
    recruiter_review=recruiter_review,

    # Interview Questions
    interview_questions=interview_questions,

    # Contact Details
    email=email,
    phone=phone,
    github=github,

    # Resume Completeness
    completeness_score=completeness_score,

    # Project Analysis
    project_analysis=project_analysis,

    job_fit=job_fit,

    resume_health=resume_health,
)



# ----------------------------
# Download PDF
# ----------------------------

@app.route("/download")
def download():

    filename = "Resume_Report.pdf"

    generate_pdf(
        filename,
        latest_result["ats_score"],
        latest_result["resume_rating"],
        latest_result["matched_skills"],
        latest_result["missing_skills"],
        latest_result["suggestions"]
    )

    return send_file(
        filename,
        as_attachment=True
    )


# ----------------------------
# Run Application
# ----------------------------

if __name__ == "__main__":

    app.run(debug=True)