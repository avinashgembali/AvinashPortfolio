import os
from google import genai
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

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
Avinash is a B.Tech CSE graduate and software developer intern, currently available for full-time roles."""
    },
    {
        "id": "professional_summary",
        "text": """Professional Summary:
Full-stack developer experienced in MERN and MEAN stack development, with production experience building scalable backend systems and APIs. Skilled in Node.js, Express.js, MongoDB, React, and Angular, with expertise in performance optimization, RBAC implementation, and RESTful API development."""
    },
    {
        "id": "education",
        "text": """Education:
- B.Tech in Computer Science and Engineering (CSE) at Anil Neerukonda Institute of Technology And Sciences (ANITS), Tagarapuvalasa, Vishakapatnam. CGPA: 9.32. Duration: 2022-2026.
- Intermediate M.P.C (Maths, Physics, Chemistry) at Sri Chaitanya Junior College, Marikavalasa, Vishakapatnam. Percentage: 97%. Duration: 2020-2022."""
    },
    {
        "id": "experience_duration",
        "text": """Work Experience Duration:
Avinash has approximately 11-12 months of professional work experience as a Software Developer Intern at InnCircles, starting July 2025 (as of June 2026). He is a B.Tech CSE graduate from ANITS (Oct 2022 – April 2026) and is currently available for full-time roles. He is considered a fresher/entry-level developer with strong hands-on production experience."""
    },
    {
        "id": "internship",
        "text": """Internship / Work Experience:
Company: InnCircles
Role: Software Developer Intern (Onsite)
Duration: July 2025 - Present (11-12 months as of June 2026)
- Engineered production-level backend systems using MEAN and MERN stacks, designing database models and implementing complex workflows for an enterprise construction management platform serving construction and real estate clients.
- Optimized API performance by developing efficient Excel data processing pipelines, reducing response times from approximately 20 seconds to 5-6 seconds and improving throughput by 70-75%.
- Authored unit test cases using JUnit, increasing code coverage across critical service modules and ensuring the correctness and reliability of API logic in production environments.
- Implemented Role-Based Access Control (RBAC) to manage user permissions and restrict module access based on assigned roles, strengthening platform security and authorization management.
- Collaborated within agile development teams using Jira and Bitbucket for sprint planning, task tracking, code reviews, and version-controlled software development."""
    },
    {
        "id": "project_helper_management",
        "text": """Project: Helper Management System
Tech Stack: MEAN Stack (MongoDB, Express, Angular, Node.js)
Date: July 2025
- Built a full-stack helper management system with CRUD operations, role-based workflows, and RESTful APIs.
- Implemented QR code generation allowing helpers' details to be accessed via QR scanning with dynamic form-based data handling."""
    },
    {
        "id": "project_batbazaar",
        "text": """Project: BatBazaar
Tech Stack: MERN Stack (MongoDB, Express, React, Node.js, Razorpay, Cloudinary, Gemini AI)
Date: March 2025
- Built and deployed a full-stack e-commerce platform with Razorpay payment integration, real-time inventory tracking, order management, and role-based functionalities for customers and administrators.
- Integrated a Google Gemini AI-powered chatbot to provide natural language cricket bat recommendations and dynamically apply product filters through a conversational interface.
- Designed and implemented an Admin Dashboard for inventory management, stock updates, order tracking, and delivery status monitoring to streamline operational workflows."""
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
Avinash Gembali is a full-stack developer and B.Tech CSE graduate from ANITS Vishakapatnam with an excellent 9.32 CGPA (Oct 2022 – April 2026). He has approximately 11-12 months of professional experience as a Software Developer Intern at InnCircles, contributing to production-level construction management software. He is skilled in full-stack development using both MEAN and MERN stacks, with expertise in performance optimization, RBAC implementation, and RESTful API development. He is a quick learner who can adapt to new technologies including Spring Boot, AI/ML, cloud platforms, and more. He has built multiple projects including BatBazaar (MERN e-commerce with Razorpay payment integration, Cloudinary, Gemini AI chatbot, and Admin Dashboard) and a Helper Management System with QR code generation. He has solved 300+ LeetCode problems and holds an NPTEL Java certification. He is currently available for full-time roles."""
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
