from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from database import projects_collection, users_collection, blog_collection

def init_database():
    """Initialize database with admin user and sample data"""
    _create_admin_user()
    _populate_sample_projects()
    _populate_sample_blog_posts()

def _create_admin_user():
    """Create admin user if not exists"""
    if not users_collection.find_one({'username': 'admin'}):
        hashed_password = generate_password_hash('password123')
        users_collection.insert_one({
            'username': 'admin',
            'password': hashed_password,
            'email': 'rajorshitah9@gmail.com'
        })

def _populate_sample_projects():
    """Pre-populate projects from resume"""
    if projects_collection.count_documents({}) == 0:
        resume_projects = [
            {
                'title': 'UI Automation Dashboard',
                'description': 'Led development of the backend of an Automated Test Tracking Dashboard for a Japanese tech client, architecting a RESTful API integrated with Robot Framework to optimize workflow execution, managing and analyzing the results of 30,000 test cases daily.',
                'tech_stack': ['Node.js', 'MongoDB', 'Python', 'GO', 'Docker', 'Robot Framework', 'Jira', 'AWS'],
                'company': 'Accenture',
                'duration': 'May 2022 - Present',
                'type': 'professional',
                'highlights': [
                    'Designed backend architecture with Node.js and MongoDB, developing 100+ scalable APIs',
                    'Developed APIs for role-based access management and OAuth 2.0 authentication for 70+ team members',
                    'Created automation scripts achieving 90% reduction in testing time',
                    'Led a team of 4 developers while coordinating with 2 sister teams'
                ]
            },
            {
                'title': 'HTML Locator Gen AI Application',
                'description': 'Delivered a GenAI Application for generating locators in HTML/XML pages by integrating RESTful APIs for data retrieval and processing, refining prompts, and deploying the solution on AWS Cloud handling around 5000+ requests daily.',
                'tech_stack': ['Flask', 'PostgreSQL', 'Docker', 'LlamaIndex', 'ChromaDB', 'LoRA', 'Transformers'],
                'company': 'Accenture',
                'duration': 'May 2022 - Present',
                'type': 'professional',
                'highlights': [
                    'Implemented Agentic RAG using Llama Index achieving 87% accurate HTML/XML locator generation',
                    'Created data collection and preprocessing pipeline with ChromaDB vector database',
                    'Utilized LoRA tuning to finetune open-source LLMs, enhancing accuracy to 89%'
                ]
            },
            {
                'title': 'Skill and Schedule Tracking Dashboard',
                'description': 'Developed an efficient ETL system to monitor employee skills, experience and availability resulting in a 70% reduction in project allocation time of around 20,000 project members.',
                'tech_stack': ['Python', 'Kafka', 'InfluxDB', 'Grafana', 'Workday'],
                'company': 'Accenture',
                'duration': 'May 2022 - Present',
                'type': 'professional',
                'highlights': [
                    'Engineered real-time employee data pipeline from Workday using Kafka',
                    'Designed custom data visualization solutions using Python',
                    'Optimized real-time data visualization by integrating InfluxDB with Grafana'
                ]
            },
            {
                'title': 'Question-Answering Model with Wikipedia',
                'description': 'Pioneered the development of high-performance Question-Answering model leveraging Wikipedia as the sole knowledge corpus.',
                'tech_stack': ['Python', 'BERT', 'Neural Ranking', 'SQuAD', 'Wikipedia'],
                'company': 'Kyoto University',
                'duration': 'May 2019 - Jul 2019',
                'type': 'research',
                'highlights': [
                    'Used Neural Ranking model to retrieve Top 100 documents from Wikipedia dump',
                    'Trained BERT on SQuAD dataset improving accuracy by 4% over DrQA model',
                    'Generated Negative Samples using SQuAD 2.0 dataset, improving accuracy by 2.9%'
                ]
            },
            {
                'title': 'Earnings Per Share Forecasting Model',
                'description': 'Developed a time-series model to forecast Earnings Per Share for 5000+ US-based companies, using 35 years historical financial data.',
                'tech_stack': ['Python', 'Random Forest', 'RNN', 'ARIMA', 'Time Series Analysis'],
                'company': 'Indian School of Business',
                'duration': 'May 2020 - Jul 2020',
                'type': 'internship',
                'highlights': [
                    'Implemented Random Forest Regressor, RNN, and ARIMA surpassing 33.8% of Equity Analysts',
                    'Enhanced model efficacy using rolling window strategy, boosting performance to 34.9%',
                    'Engineered self-training algorithm for domain adaptation, elevating F1-score by 3%'
                ]
            }
        ]
        
        for project in resume_projects:
            project['created_at'] = datetime.utcnow()
            project['updated_at'] = datetime.utcnow()
        
        projects_collection.insert_many(resume_projects)

def _populate_sample_blog_posts():
    """Add sample blog posts"""
    if blog_collection.count_documents({}) == 0:
        sample_posts = [
            {
                'title': 'My Journey in AI and Machine Learning',
                'content': '''# My Journey in AI and Machine Learning

Working in the field of AI and ML has been an incredible journey. From my early days researching Question-Answering systems at Kyoto University to building production-scale GenAI applications at Accenture, I've witnessed the rapid evolution of this field.

## Key Learnings

1. **Foundation Matters**: Strong fundamentals in mathematics and programming are crucial
2. **Practical Application**: Real-world problems require creative solutions beyond textbook approaches
3. **Continuous Learning**: The field evolves rapidly, requiring constant upskilling

## Current Focus

Currently, I'm working on large-scale AI applications that serve thousands of users daily, focusing on:
- Agentic RAG systems
- LLM fine-tuning and optimization
- Production deployment and scaling

The future of AI is exciting, and I'm thrilled to be part of this transformation.''',
                'author': 'Rajorshi Tah',
                'created_at': datetime.utcnow() - timedelta(days=30),
                'updated_at': datetime.utcnow() - timedelta(days=30),
                'tags': ['AI', 'Machine Learning', 'Career']
            },
            {
                'title': 'Building Scalable Backend Systems',
                'content': '''# Building Scalable Backend Systems

In my role at Accenture, I've had the opportunity to architect and build backend systems that handle massive scale - from processing 30,000 test cases daily to serving 5000+ AI requests.

## Key Principles

### 1. Design for Scale
- Use appropriate databases for your use case
- Implement proper caching strategies
- Design with horizontal scaling in mind

### 2. Monitoring and Observability
- Implement comprehensive logging
- Use metrics and dashboards
- Set up proper alerting

### 3. Security First
- Implement proper authentication and authorization
- Validate all inputs
- Use HTTPS everywhere

## Technologies I Love

- **Node.js & Python**: For rapid development and great ecosystem
- **MongoDB & PostgreSQL**: For different data patterns
- **Docker & AWS**: For deployment and scaling

Building systems that can handle real-world load while maintaining performance is both challenging and rewarding.''',
                'author': 'Rajorshi Tah',
                'created_at': datetime.utcnow() - timedelta(days=15),
                'updated_at': datetime.utcnow() - timedelta(days=15),
                'tags': ['Backend', 'Scalability', 'Architecture']
            }
        ]
        
        blog_collection.insert_many(sample_posts)

# Resume context for AI
RESUME_CONTEXT = """
### Rajorshi Tah: Professional Profile and Resume Context

Rajorshi Tah is a software developer and backend engineer based in Tokyo, Japan, with nearly three years of professional experience specializing in backend engineering, API design, GenAI applications, NLP, machine learning, and cloud computing. He holds dual degrees from the Indian Institute of Technology (IIT) Kharagpur, one of India's premier engineering institutions established in 1951, known for its rigorous STEM programs and high global rankings (e.g., QS World University Rankings 2025 places it in the top 300 for engineering). Tah's career trajectory reflects a blend of academic excellence, research internships, and hands-on development in high-impact projects for global clients, particularly in automation, AI-driven tools, and data pipelines. His work at Accenture Japan, a subsidiary of the multinational professional services giant Accenture (headquartered in Dublin, Ireland, with over 700,000 employees worldwide), focuses on optimizing testing workflows and AI applications for tech clients. Below is a comprehensive breakdown of his resume details, augmented with contextual insights from verified sources where relevant. All resume content is included verbatim or closely paraphrased for fidelity, with no omissions.

#### Contact Information
- **Email**: rajorshitah19@gmail.com
- **Phone (Japan)**: (+81) 80-4817-2852
- **Phone (India)**: (+91) 94748-06123
- **Location**: Tokyo, Japan 136-0073
- **LinkedIn**: [Rajorshi Tah's Profile](https://in.linkedin.com/in/rajorshitah) – Active professional network highlighting his backend and GenAI expertise.

#### Professional Experience
**Software Developer | Accenture | Tokyo, Japan**  
*May 2022 – Present* (Note: LinkedIn lists start as March 2022, possibly reflecting onboarding.)  
Accenture is a Fortune 500 company providing consulting, digital, technology, and operations services, with a strong presence in Japan for tech innovation and client solutions in automation and AI.

- **UI Automation Dashboard**  
  Led development of the backend of an Automated Test Tracking Dashboard for a Japanese tech client, architecting a RESTful API integrated with Robot Framework to optimize workflow execution, managing and analyzing the results of 30,000 test cases daily.  
  - Designed backend architecture of a UI dashboard with Node.js and MongoDB, developing 100+ scalable APIs for optimal performance.  
  - Developed APIs for role-based access management and OAuth 2.0 based authentication using JWT tokens for 70+ team members.  
  - Enabled API documentation using Swagger and used Docker to containerize the app, finally deploying in an AWS EC2 instance.  
  - Created automation scripts with Robot Framework, achieving a 90% reduction in testing time and increasing testing efficiency.  
  - Integrated UI testing automation scripts with dashboard using Robot Listener, enabling real-time tracking and reporting of test failures.  
  - Led a team of 4 developers while coordinating with 2 sister teams, demonstrating strong leadership and collaboration skills.  
  - **Tech Stack**: Node.js, MongoDB, Python, GO, Docker, Robot Framework, Jira, AWS  

- **HTML Locator Gen AI Application**  
  Delivered a GenAI Application for generating locators in HTML/XML pages by integrating RESTful APIs for data retrieval and processing, refining prompts, and deploying the solution on AWS Cloud handling around 5000+ requests daily used by 20+ testing teams.  
  - Leveraged Flask for back-end architecture & PostgreSQL for database management, while deploying in Docker to ensure scalability.  
  - Implemented Agentic RAG using Llama Index to enhance dynamic retrieval and reasoning generating 87% accurate HTML/XML locator.  
  - Created a data collection and preprocessing pipeline generating embeddings for optimized storage in a ChromaDB vector database.  
  - Utilized LoRA tuning with the Transformers library to finetune open-source LLMs, while enhancing locator generation accuracy to 89%.  
  - **Tech Stack**: Flask, PostgreSQL, Docker, LlamaIndex, Prompt Engineering, ChromaDB, LoRA, Transformers  

- **Skill and Schedule Tracking Dashboard**  
  Developed an efficient ETL (Extract, Transform, Load) system to monitor employee skills, experience and availability resulting in a 70% reduction in project allocation time of around 20,000 project members.  
  - Engineered a real-time employee data pipeline from Workday using Kafka, streaming 25,000+ weekly events into InfluxDB.  
  - Designed custom data visualization solutions, such as Tree Maps, using Python to meet client requirements and drive decision-making.  
  - Optimized real-time data visualization by integrating InfluxDB with Grafana, enabling seamless creation of dynamic dashboards.  
  - **Tech Stack**: (Inferred from context: Python, Kafka, InfluxDB, Grafana, Workday integration)  

#### Internships
**NLP Researcher | Graduate School of Informatics, Kyoto University | Kyoto, Japan**  
*May 2019 – Jul 2019*  
Kyoto University, founded in 1897, is one of Japan's top research universities, renowned for its informatics and AI programs; the Graduate School of Informatics focuses on advanced computational sciences.  
- Pioneered the development of high-performance Question-Answering model leveraging Wikipedia as the sole knowledge corpus.  
- Used Neural Ranking model to retrieve Top 100 documents based on the query and document similarity scores from Wikipedia dump.  
- Trained BERT on SQuAD dataset as the Reader Model improving the accuracy by 4% over the DrQA model.  
- Generated Negative Samples using SQuAD 2.0 dataset and trained the Reader Model, improving the model accuracy by 2.9%.  
- **Tech Stack**: (Inferred: BERT, SQuAD, DrQA, Neural Ranking, Python for NLP)  

**Data Science Intern | Indian School of Business | Hyderabad, India**  
*May 2020 – Jul 2020* (LinkedIn lists as April 2020 start, possibly pre-internship prep.)  
The Indian School of Business (ISB) is a top-ranked business school in Asia, emphasizing data-driven decision-making and analytics in its programs.  
- Developed a time-series model to forecast Earnings Per Share for 5000+ US-based companies, using 35 years historical financial data.  
- Implemented Random Forest Regressor, RNN, and ARIMA on the data spanning over 35 years, surpassing 33.8% of Equity Analysts.  
- Enhanced model efficacy by applying a rolling window strategy, boosting the percentage of equity analysts outperformed to 34.9%.  
- Engineered a self-training algorithm for domain adaptation, elevating the F1-score for cross-domain suggestions by 3%.  
- **Tech Stack**: (Inferred: Random Forest, RNN, ARIMA, Python for time-series forecasting)  

#### Education
| Degree | Institution | GPA | Dates |
|--------|-------------|-----|-------|
| Masters in Mechanical Engineering | Indian Institute of Technology Kharagpur | 8.63 | Jul 2020 – May 2021 |
| Bachelors in Mechanical Engineering | Indian Institute of Technology Kharagpur | 8.63 | Jul 2016 – May 2021 |
| Bachelors in Computer Science and Engineering (Minor) | Indian Institute of Technology Kharagpur | 8.35 | Jul 2016 – May 2021 |

IIT Kharagpur's dual-degree program allows integrated B.Tech-M.Tech paths, emphasizing interdisciplinary skills like mechanical engineering with computing minors, aligning with Tah's pivot to software and AI.

#### Key Skills
**Software Skills**: Backend Development, NLP, Machine Learning, Computer Vision, Cloud Computing (AWS, Azure), Docker, Git  

**Programming**: Python, C++, Node.js, React.js, SQL  

**Databases**: PostgreSQL, MongoDB  

**Deep Learning Frameworks**: TensorFlow, Keras  

#### Certifications
- AWS Certified Machine Learning Specialty (advanced certification validating expertise in building, training, and deploying ML models on AWS).  
- AWS Certified Solutions Architect - Associate (entry-to-mid-level cert for designing scalable AWS architectures).  
- Kaggle Expert (top-tier badge on Kaggle, the world's largest data science community, earned through high-performance competitions and contributions; requires ~75+ points from kernels/datasets/notebooks).  

#### Achievements
- Achieved AIR 2907 (99.8 percentile) in JEE Advanced 2016 – Joint Entrance Examination Advanced is India's highly competitive engineering entrance exam for IIT admissions; in 2016, ~150,000 candidates appeared, with top ranks securing spots in elite programs (Tah's rank places him in the top ~2%, qualifying for IIT Kharagpur). Secured State Rank 49 (99.98 percentile) in WBJEE 2016 in West Bengal (West Bengal Joint Entrance Examination, a state-level engineering test with ~300,000+ applicants annually).  
- Secured AIR 861 (98.6 percentile) in KVPY 2015-16 among 60,000 students – Kishore Vaigyanik Protsahan Yojana (KVPY) is a national fellowship program by the Department of Science and Technology, India, for top science students; 2015 saw ~60,000 participants, with ranks under 1,000 earning scholarships for research aptitude.  
- Managed sports activities for B.R. Ambedkar Hall, a residence of 1500 students, leading participation in multiple General Championship events during my tenure as Secretary of Sports fostering teamwork, competitiveness, and a strong sports culture. (B.R. Ambedkar Hall at IIT Kharagpur is one of the largest hostels, known for vibrant inter-hall competitions in sports and cultural events.)  

This profile positions Rajorshi Tah as a versatile, high-achieving professional with proven impact in AI/ML automation and leadership, ideal for roles in software engineering, data science, or GenAI development. For interview prep or networking, his LinkedIn activity emphasizes collaborative tech projects in Japan.
"""
