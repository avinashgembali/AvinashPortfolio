import os
from datetime import date
from google import genai
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


def _experience_duration() -> str:
    start = date(2025, 7, 1)
    today = date.today()
    months = (today.year - start.year) * 12 + (today.month - start.month)
    if months < 12:
        return f"approximately {months} month{'s' if months != 1 else ''}"
    years = months // 12
    rem = months % 12
    if rem == 0:
        return f"approximately {years} year{'s' if years != 1 else ''}"
    return f"approximately {years} year{'s' if years != 1 else ''} and {rem} month{'s' if rem != 1 else ''}"


_exp = _experience_duration()

gemini_client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY"),
    http_options={"api_version": "v1"},
)

CHUNKS = [
    {
        "id": "personal_info",
        "text": """Personal Information:
Name: Avinash Gembali
Email: avinashgembali13@gmail.com
Phone: 9052244239
Avinash is a B.Tech CSE graduate and Full Stack Developer currently working as a Product Developer at InnCircles."""
    },
    {
        "id": "professional_summary",
        "text": """Professional Summary:
Full Stack Developer with hands-on experience building scalable enterprise applications using MERN and MEAN stacks. Improved backend API performance by 70%+, implemented RBAC-based security systems, and developed AI-powered applications leveraging Gemini AI. Strong foundation in DSA with 300+ LeetCode problems solved."""
    },
    {
        "id": "education",
        "text": """Education:
- B.Tech in Computer Science and Engineering (CSE) at Anil Neerukonda Institute of Technology And Sciences (ANITS), Tagarapuvalasa, Vishakapatnam. CGPA: 9.32. Duration: 2022-2026.
- Intermediate M.P.C (Maths, Physics, Chemistry) at Sri Chaitanya Junior College, Marikavalasa, Vishakapatnam. Percentage: 97%. Duration: 2020-2022."""
    },
    {
        "id": "experience_duration",
        "text": f"""Work Experience Duration:
Avinash has {_exp} of total professional experience at InnCircles. He first joined as a Software Developer Intern (July 2025 – July 2026) and was then converted to a full-time Product Developer role from August 2026 onwards. He is a B.Tech CSE graduate from ANITS (Oct 2022 – April 2026)."""
    },
    {
        "id": "internship",
        "text": """Internship:
Company: InnCircles
Role: Software Developer Intern (Onsite)
Duration: July 2025 – July 2026 (12 months)
- Engineered production-level backend systems using MEAN and MERN stacks, designing database models and implementing complex workflows for an enterprise construction management platform serving 1000+ users.
- Optimized API performance by developing efficient Excel data processing pipelines, reducing response times from approximately 20 seconds to 5-6 seconds and improving throughput by 70-75%.
- Authored 25+ unit test cases using JUnit, increasing code coverage across critical service modules and ensuring the correctness and reliability of API logic in production environments.
- Implemented Role-Based Access Control (RBAC) across 3 user roles to manage permissions and restrict module access based on assigned responsibilities, strengthening platform security and authorization management.
- Collaborated within a 50-member agile development team using Jira and Bitbucket for sprint planning, task tracking, code reviews, and version-controlled software development."""
    },
    {
        "id": "full_time_role",
        "text": f"""Full-Time Employment:
Company: InnCircles
Role: Product Developer (Onsite)
Duration: August 2026 – Present ({_exp} total experience at InnCircles including internship)
Avinash was converted from a Software Developer Intern to a full-time Product Developer at InnCircles starting August 2026, recognising his contributions during the internship."""
    },
    {
        "id": "project_helper_management",
        "text": """Project: Helper Management System
Tech Stack: MEAN Stack (MongoDB, Express, Angular, Node.js)
- Developed a full-stack helper management system featuring CRUD operations, role-based workflows, and 10+ REST APIs, demonstrating end-to-end ownership across frontend and backend development.
- Integrated dynamic QR code generation to enable instant access to helper profiles through QR scanning, while implementing form-based data handling and validation for improved data accuracy."""
    },
    {
        "id": "project_batbazaar",
        "text": """Project: BatBazaar
Tech Stack: MERN Stack (MongoDB, Express, React, Node.js, Razorpay, Cloudinary, Gemini AI)
- Built and deployed a full-stack e-commerce platform with 15+ REST APIs, Razorpay payment integration, real-time inventory tracking, order management, and role-based functionalities for customers and administrators.
- Integrated a Google Gemini AI-powered chatbot to provide natural language cricket bat recommendations and dynamically apply product filters across 50+ products through a conversational interface.
- Designed and implemented a 5+ module Admin Dashboard for inventory management, stock updates, order tracking, and delivery status monitoring to streamline operational workflows."""
    },
    {
        "id": "technical_skills",
        "text": """Technical Skills:
Languages: Java, Python, C, HTML/CSS, JavaScript
Frameworks and Libraries: React, Express, Angular, Node.js
Developer Tools: Git, Jira, Bitbucket, VS Code, IntelliJ IDEA
Databases: MongoDB, SQL
Core Concepts: Data Structures & Algorithms, REST APIs, RBAC, Unit Testing, Agile Methodology
Avinash is proficient in both MEAN stack (MongoDB, Express, Angular, Node.js) and MERN stack (MongoDB, Express, React, Node.js)."""
    },
    {
        "id": "achievements",
        "text": """Achievements and Certifications:
- LeetCode: Solved 300+ problems covering data structures and algorithms.
- NPTEL Certification: Programming in Java."""
    },
    {
        "id": "adaptability",
        "text": """Adaptability and Learning Ability:
Avinash is a quick learner who can adapt to new technologies rapidly. His strong foundation in computer science fundamentals (Data Structures, Algorithms, DBMS, Operating Systems) along with a 9.32 CGPA enables him to pick up any new framework, language, or technology stack quickly. While his primary expertise is in the MEAN and MERN stacks, he is fully open and willing to work with other technologies such as Spring Boot, Django, Flutter, AI/ML frameworks, cloud platforms (AWS, GCP, Azure), DevOps tools, or any other tech stack required by the role. He has already demonstrated this adaptability by learning and working with multiple stacks simultaneously during his internship. Avinash believes in learning by doing and is always excited to explore new tools and technologies."""
    },
    {
        "id": "openness_to_technologies",
        "text": """Openness to New Technologies:
If asked about technologies not listed in Avinash's resume — such as Spring Boot, Kotlin, Go, Rust, AI/ML, deep learning, cloud computing (AWS, Azure, GCP), DevOps, Docker, Kubernetes, GraphQL, or any other stack — Avinash is open to learning and working with them. He has a solid programming foundation in Java, Python, and JavaScript, and a track record of quickly becoming productive in new environments. He would be able to get up to speed with any technology stack given a reasonable ramp-up period. His quick learning ability and strong CS fundamentals make him a versatile developer."""
    },
    {
        "id": "summary",
        "text": """Summary about Avinash Gembali:
Avinash Gembali is a Full Stack Developer and B.Tech CSE graduate from ANITS Vishakapatnam with a 9.32 CGPA (Oct 2022 – April 2026). He started as a Software Developer Intern at InnCircles in July 2025 and was converted to a full-time Product Developer role in August 2026. He has built production-level systems for a construction management platform serving 1000+ users, improved backend API performance by 70%+, authored 25+ unit test cases, implemented RBAC across 3 user roles, and collaborated in a 50-member agile team. He built BatBazaar (MERN e-commerce with 15+ REST APIs, Razorpay, Cloudinary, Gemini AI chatbot, 5+ module Admin Dashboard) and a Helper Management System (MEAN stack with 10+ REST APIs and QR code generation). He has solved 300+ LeetCode problems and holds an NPTEL Java certification."""
    },
]


def embed_text(text: str) -> list:
    response = gemini_client.models.embed_content(
        model="gemini-embedding-2",
        contents=text,
    )
    return list(response.embeddings[0].values)


def ingest():
    mongo = MongoClient(os.getenv("MONGODB_URI"))
    db = mongo["portfolio"]
    collection = db["resume_chunks"]

    collection.drop()
    print("Dropped existing collection.")

    docs = []
    print(f"Embedding {len(CHUNKS)} chunks...")

    for chunk in CHUNKS:
        embedding = embed_text(chunk["text"])
        docs.append({
            "_id": chunk["id"],
            "text": chunk["text"],
            "embedding": embedding,
        })
        print(f"  embedded: {chunk['id']}")

    collection.insert_many(docs)
    print(f"\nIngested {len(docs)} chunks into MongoDB Atlas.")
    print("Database: portfolio | Collection: resume_chunks")
    print("\nNEXT STEP: Recreate the Vector Search index in Atlas UI if you dropped the collection.")

    mongo.close()


if __name__ == "__main__":
    ingest()
