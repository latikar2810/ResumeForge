import spacy
from skill_aliases import SKILL_ALIASES
from skills import SKILLS

nlp = spacy.load("en_core_web_sm")
def normalize_text(text):

    text = text.lower()

    for alias, actual_skill in SKILL_ALIASES.items():
        text = text.replace(alias.lower(), actual_skill.lower())
    return text
def extract_keywords(text):
    doc = nlp(text)
    keywords = []
    for token in doc:
        if not token.is_stop and not token.is_punct:
            keywords.append(token.text.lower())
    return keywords
import re

import re

def extract_section(resume_text, section_name):

    resume_text = resume_text.replace("\r", "")

    lines = resume_text.split("\n")

    start = -1

    end = len(lines)

    section_headers = [
        "SUMMARY",
        "OBJECTIVE",
        "CAREER OBJECTIVE",
        "EDUCATION",
        "EXPERIENCE",
        "PROJECTS",
        "TECHNICAL SKILLS",
        "SKILLS",
        "CORE CONCEPTS",
        "CERTIFICATIONS",
        "ACHIEVEMENTS",
        "INTERNSHIP",
        "LANGUAGES",
        "HOBBIES"
    ]

    # Find the exact section heading
    for i, line in enumerate(lines):

        if line.strip().upper() == section_name.upper():

            start = i + 1
            break

    if start == -1:
        return ""

    # Find the next section heading
    for j in range(start, len(lines)):

        current = lines[j].strip().upper()

        if current in section_headers:

            end = j
            break

    return "\n".join(lines[start:end]).strip()
def extract_resume_skills(pdf_text):
    matched_skills = []
    pdf_text = normalize_text(pdf_text)
    for skill in SKILLS:
        if skill.lower() in pdf_text.lower():
            matched_skills.append(skill)
    return matched_skills
def extract_required_skills(job_description):
    job_description = job_description.lower()
    required_skills = []
    for skill in SKILLS:
        if skill.lower() in job_description:

            required_skills.append(skill)
    return list(dict.fromkeys(required_skills))
def get_missing_skills(required_skills, matched_skills):
    missing_skills = []
    for skill in required_skills:
        if skill not in matched_skills:
            missing_skills.append(skill)
    return missing_skills
def calculate_ats(required_skills, matched_skills):

    matched_required_skills = []

    for skill in required_skills:
        if skill in matched_skills:
            matched_required_skills.append(skill)

    if len(required_skills) > 0:
        return (len(matched_required_skills) / len(required_skills)) * 100
    return round(score, 2)
def get_resume_rating(score):
    if score >= 90:
        return "Excellent ⭐⭐⭐⭐⭐"
    elif score >= 75:
        return "Good ⭐⭐⭐⭐"
    elif score >= 50:
        return "Average ⭐⭐⭐"
    else:
        return "Needs Improvement ⭐⭐"
def get_suggestions(missing_skills):
    suggestions = []
    if len(missing_skills) > 0:
        for skill in missing_skills:
            suggestions.append(f"Add or learn {skill}")
    else:
        suggestions.append("Excellent! Your resume matches the required technical skills.")
    suggestions.append("Add a professional summary at the top of your resume.")
    suggestions.append("Use strong action verbs like Developed, Designed, Implemented and Optimized.")
    suggestions.append("Quantify your achievements using numbers wherever possible.")
    suggestions.append("Add your GitHub and LinkedIn profile links.")
    suggestions.append("Include relevant certifications.")
    suggestions.append("Keep your resume limited to 1–2 pages.")
    return suggestions
def generate_ai_feedback(
    ats_score,
    matched_skills,
    missing_skills,
    education,
    experience,
    projects,
    certifications
):
    feedback = []
    # Overall score
    if ats_score >= 85:
        feedback.append(
            "Excellent resume! It closely matches the job description."
        )
    elif ats_score >= 60:
        feedback.append(
            "Your resume is a good match, but adding a few missing skills could significantly improve it."
        )
    else:
        feedback.append(
            "Your resume needs improvement to better match the job description."
        )
    # Skills
    if matched_skills:
        feedback.append(
            f"Strong technical skills detected: {', '.join(matched_skills[:5])}."
        )
    if missing_skills:
        feedback.append(
            f"Consider adding these important skills: {', '.join(missing_skills)}."
        )
    # Resume sections
    if not education:
        feedback.append("Add an Education section.")
    if not experience:
        feedback.append("Include internships or work experience.")
    if not projects:
        feedback.append("Add 2-3 projects with technologies used and outcomes.")
    if not certifications:
        feedback.append("Adding certifications will strengthen your profile.")
    feedback.append(
        "Use action verbs such as Developed, Designed, Built and Implemented."
    )
    feedback.append(
        "Include measurable achievements wherever possible."
    )
    return feedback
def check_education(resume_text):

    resume_text = resume_text.lower()

    education_keywords = [
        "education",
        "b.tech", "btech", "b.e", "be",
        "m.tech", "mtech",
        "bachelor", "master",
        "bca", "mca",
        "b.sc", "m.sc",
        "bcom", "mcom",
        "college",
        "university",
        "degree",
        "cgpa",
        "sgpa"
    ]

    return any(keyword in resume_text for keyword in education_keywords)
def check_projects(resume_text):

    resume_text = resume_text.lower()

    project_keywords = [
        "projects",
        "project",
        "academic project",
        "personal project",
        "major project",
        "minor project"
    ]

    return any(keyword in resume_text for keyword in project_keywords)
def check_experience(resume_text):

    resume_text = resume_text.lower()

    experience_keywords = [
        "experience",
        "work experience",
        "internship",
        "intern",
        "software engineer",
        "developer",
        "trainee",
        "worked as"
    ]

    return any(keyword in resume_text for keyword in experience_keywords)
def check_certifications(resume_text):

    resume_text = resume_text.lower()

    certification_keywords = [
        "certification",
        "certifications",
        "certificate",
        "certified",
        "coursera",
        "udemy",
        "nptel",
        "infosys springboard",
        "oracle",
        "aws"
    ]

    return any(keyword in resume_text for keyword in certification_keywords)
def calculate_resume_strength(
    ats_score,
    matched_skills,
    required_skills,
    education,
    experience,
    projects,
    certifications
):

    # Technical Skills Score
    if len(required_skills) > 0:
        technical_score = int(
            (len(matched_skills) / len(required_skills)) * 100
        )

        if technical_score > 100:
            technical_score = 100

    else:
        technical_score = 100

    # Section Scores
    education_score = 100 if education else 0

    experience_score = 100 if experience else 0

    projects_score = 100 if projects else 0

    certifications_score = 100 if certifications else 0

    return {
        "technical": technical_score,
        "education": education_score,
        "experience": experience_score,
        "projects": projects_score,
        "certifications": certifications_score
    }
def calculate_score_breakdown(
    matched_skills,
    required_skills,
    education,
    experience,
    projects,
    certifications
):

    # Skills (40 Marks)
    if len(required_skills) > 0:
        skills_score = round(
            (len(matched_skills) / len(required_skills)) * 40
        )
    else:
        skills_score = 40

    skills_score = min(skills_score, 40)

    # Projects (20 Marks)
    projects_score = 20 if projects else 0

    # Education (15 Marks)
    education_score = 15 if education else 0

    # Experience (15 Marks)
    experience_score = 15 if experience else 0

    # Certifications (10 Marks)
    certifications_score = 10 if certifications else 0

    total = (
        skills_score +
        projects_score +
        education_score +
        experience_score +
        certifications_score
    )

    return {
        "skills": skills_score,
        "projects": projects_score,
        "education": education_score,
        "experience": experience_score,
        "certifications": certifications_score,
        "total": total
    }

def get_rating(score):

    if score >= 85:
        return "Excellent"

    elif score >= 70:
        return "Good"

    elif score >= 50:
        return "Average"

    else:
        return "Needs Improvement"


def get_stars(score):

    if score >= 85:
        return "★★★★★"

    elif score >= 70:
        return "★★★★☆"

    elif score >= 50:
        return "★★★☆☆"

    elif score >= 30:
        return "★★☆☆☆"

    else:
        return "★☆☆☆☆"

def analyze_resume_sections(
    resume_text,
    education,
    experience,
    projects,
    certifications,
    matched_skills
):

    analysis = {}

    # ------------------------
    # Education
    # ------------------------

    if education:
        score = 90
    else:
        score = 20

    analysis["education"] = {
        "score": score,
        "rating": get_rating(score),
        "stars": get_stars(score)
    }

    # ------------------------
    # Experience
    # ------------------------

    if experience:

        exp_text = extract_section(
            resume_text,
            "experience"
        )

        if len(exp_text.split()) > 50:
            score = 90
        elif len(exp_text.split()) > 20:
            score = 70
        else:
            score = 50

    else:
        score = 20

    analysis["experience"] = {
        "score": score,
        "rating": get_rating(score),
        "stars": get_stars(score)
    }

    # ------------------------
    # Projects
    # ------------------------

    if projects:

        project = analyze_projects(resume_text)

        score = project["score"]

    else:

        score = 20

    analysis["projects"] = {
        "score": score,
        "rating": get_rating(score),
        "stars": get_stars(score)
    }

    # ------------------------
    # Skills
    # ------------------------

    if len(matched_skills) >= 12:
        score = 95
    elif len(matched_skills) >= 8:
        score = 80
    elif len(matched_skills) >= 5:
        score = 65
    else:
        score = 40

    analysis["skills"] = {
        "score": score,
        "rating": get_rating(score),
        "stars": get_stars(score)
    }

    # ------------------------
    # Certifications
    # ------------------------

    if certifications:
        score = 85
    else:
        score = 30

    analysis["certifications"] = {
        "score": score,
        "rating": get_rating(score),
        "stars": get_stars(score)
    }

    return analysis

def calculate_resume_success(
    ats_score,
    job_fit,
    resume_health,
    completeness_score,
    section_analysis
):

    total = (
        ats_score * 0.35 +
        job_fit["score"] * 0.25 +
        resume_health["score"] * 0.15 +
        completeness_score * 0.10 +
        (
            section_analysis["education"]["score"] +
            section_analysis["experience"]["score"] +
            section_analysis["projects"]["score"] +
            section_analysis["skills"]["score"] +
            section_analysis["certifications"]["score"]
        ) / 5 * 0.15
    )

    total = round(total)

    if total >= 90:
        recruiter_interest = "Very High"
        stars = "★★★★★"

    elif total >= 75:
        recruiter_interest = "High"
        stars = "★★★★☆"

    elif total >= 60:
        recruiter_interest = "Moderate"
        stars = "★★★☆☆"

    elif total >= 40:
        recruiter_interest = "Low"
        stars = "★★☆☆☆"

    else:
        recruiter_interest = "Very Low"
        stars = "★☆☆☆☆"

    strengths = []

    if ats_score >= 80:
        strengths.append("Excellent ATS Score")

    if job_fit["score"] >= 80:
        strengths.append("Strong Job Match")

    if resume_health["score"] >= 80:
        strengths.append("Healthy Resume Structure")

    if completeness_score >= 80:
        strengths.append("Complete Resume")

    improvements = []

    if ats_score < 80:
        improvements.append("Improve ATS Score")

    if completeness_score < 80:
        improvements.append("Complete Missing Sections")

    if resume_health["score"] < 80:
        improvements.append("Improve Resume Quality")

    return {
        "score": total,
        "stars": stars,
        "interest": recruiter_interest,
        "strengths": strengths,
        "improvements": improvements
    }

def generate_recruiter_review(
    ats_score,
    matched_skills,
    missing_skills,
    education,
    experience,
    projects,
    certifications
):
    review = "Overall Assessment:\n\n"

    if ats_score >= 85:
        review += "Your resume is an excellent match for this role. "

    elif ats_score >= 70:
        review += "Your resume is a good match but still has room for improvement. "

    else:
        review += "Your resume requires improvements before it becomes competitive for this role. "

    if matched_skills:
        review += (
            f"It demonstrates strong knowledge of {', '.join(matched_skills[:5])}. "
        )
    if missing_skills:
        review += (
            f"However, important skills such as {', '.join(missing_skills)} are missing. "
        )
    if not experience:
        review += "Adding internships or professional experience would strengthen your profile. "
    if not projects:
        review += "Include 2-3 practical projects showcasing your technical skills. "
    if not certifications:
        review += "Relevant certifications can further improve recruiter confidence. "
    review += (
        "Use measurable achievements and action verbs to make your resume more impactful."
    )
    return review
import re
def check_email(resume_text):

    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

    return bool(re.search(email_pattern, resume_text))
def check_phone(resume_text):

    phone_pattern = r"(\+91[- ]?)?[6-9]\d{9}"

    return bool(re.search(phone_pattern, resume_text))
def check_github(resume_text):

    github_keywords = [
        "github.com",
        "github"
    ]
    resume_text = resume_text.lower()
    for word in github_keywords:

        if word in resume_text:
            return True

    return False
def analyze_projects(resume_text):

    import re

    # ------------------------------------
    # Extract ONLY the Projects Section
    # ------------------------------------
    # ------------------------------------


    projects_text = resume_text

    
    

    # ------------------------------------
    # Detect Project Titles
    # ------------------------------------

    lines = projects_text.split("\n")
    project_keywords = [

        "movie recommendation",

        "citizen tool",

        "sentiment analysis",

        "portfolio",

        "resume analyzer",

        "chatbot",

        "management system",

        "prediction",

        "classification"

    ]

    project_titles = []

    for keyword in project_keywords:

        if keyword in resume_text.lower():

            project_titles.append(keyword)

    

    # ------------------------------------
    # Technologies
    # ------------------------------------

    technologies = [

        "Python",
        "Java",
        "JavaScript",
        "HTML",
        "CSS",
        "React",
        "Node.js",
        "Express",
        "Express.js",
        "Flask",
        "Django",
        "SQL",
        "MySQL",
        "SQLite",
        "MongoDB",
        "PostgreSQL",
        "Bootstrap",
        "Git",
        "GitHub",
        "Machine Learning",
        "Deep Learning",
        "NLP",
        "Pandas",
        "NumPy",
        "Scikit-Learn",
        "TensorFlow",
        "REST API"

    ]

    found_technologies = []

    lower_projects = resume_text.lower()

    for tech in technologies:

        if tech.lower() in lower_projects:
            found_technologies.append(tech)

    # ------------------------------------
    # Action Verbs
    # ------------------------------------

    verbs = [

        "Developed",
        "Implemented",
        "Built",
        "Applied",
        "Generated",
        "Utilized",
        "Created",
        "Designed",
        "Optimized",
        "Integrated",
        "Engineered",
        "Deployed"

    ]

    found_verbs = []

    for verb in verbs:

        if verb.lower() in lower_projects:
            found_verbs.append(verb)

    # ------------------------------------
    # GitHub
    # ------------------------------------

    github = (
        "github.com" in lower_projects
    )

    # ------------------------------------
    # Deployment
    # ------------------------------------

    deployment_sites = [

        "vercel",
        "render",
        "netlify",
        "railway",
        "heroku",
        "firebase",
        "github.io"

    ]

    deployment = any(site in lower_projects for site in deployment_sites)

    # ------------------------------------
    # Score
    # ------------------------------------

    score = 0

    score += min(len(project_titles) * 10, 30)

    score += min(len(found_technologies) * 3, 30)

    score += min(len(found_verbs) * 3, 20)

    if github:
        score += 10

    if deployment:
        score += 10

    score = min(score, 100)

    # ------------------------------------
    # Suggestions
    # ------------------------------------

    suggestions = []

    if len(project_titles) < 2:
        suggestions.append("Add at least two quality projects.")

    if len(found_technologies) < 5:
        suggestions.append("Mention technologies used in every project.")

    if not github:
        suggestions.append("Add GitHub repository links.")

    if not deployment:
        suggestions.append("Deploy projects using Vercel, Render or Netlify.")

    if len(found_verbs) < 4:
        suggestions.append("Use more action verbs in project descriptions.")

    return {

        "project_count": len(project_titles),

        "technologies": found_technologies,

        "action_verbs": found_verbs,

        "github": github,

        "deployment": deployment,

        "score": score,

        "suggestions": suggestions

    }
    print("========== PROJECT SECTION ==========")
    print(projects_text)
    print("=====================================")
import re
def calculate_job_fit(
    ats_score,
    completeness_score,
    technical_strength,
    matched_skills,
    required_skills
):
    # Skill Match Percentage
    if len(required_skills) > 0:
        skill_match = (
            len(matched_skills) / len(required_skills)
        ) * 100
    else:
        skill_match = 100

    job_fit = (
        ats_score * 0.40 +
        completeness_score * 0.20 +
        technical_strength * 0.20 +
        skill_match * 0.20
    )

    job_fit = round(job_fit, 2)

    if job_fit >= 85:
        verdict = "Excellent Match ⭐⭐⭐⭐⭐"
    elif job_fit >= 70:
        verdict = "Good Match ⭐⭐⭐⭐"
    elif job_fit >= 55:
        verdict = "Average Match ⭐⭐⭐"
    else:
        verdict = "Needs Improvement ⭐⭐"

    return {
        "score": job_fit,
        "verdict": verdict
    }
def calculate_resume_health(
    email,
    phone,
    github,
    education,
    experience,
    projects,
    certifications,
    resume_text
):

    linkedin = (
        "linkedin.com" in resume_text.lower()
        or "linkedin" in resume_text.lower()
    )

    achievements = any(word in resume_text.lower() for word in [
        "achievement",
        "achievements",
        "award",
        "awards",
        "winner",
        "rank",
        "hackathon"
    ])

    total = 9

    found = sum([
        email,
        phone,
        github,
        linkedin,
        education,
        experience,
        projects,
        certifications,
        achievements
    ])

    score = round((found / total) * 100, 2)

    return {
        "score": score,
        "linkedin": linkedin,
        "achievements": achievements
    }
