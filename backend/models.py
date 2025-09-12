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
Rajorshi Tah is a Software Developer at Accenture in Tokyo, Japan with extensive experience in backend development, AI/ML, and full-stack development. 

Key Experience:
- Currently working as Software Developer at Accenture (May 2022 - Present)
- Led development of UI Automation Dashboard handling 30,000 test cases daily
- Built GenAI Application for HTML locator generation with 89% accuracy
- Developed ETL systems reducing project allocation time by 70%
- Previous research experience at Kyoto University on Question-Answering systems
- Internship at Indian School of Business on financial forecasting models

Education:
- Masters in Mechanical Engineering from IIT Kharagpur (GPA 8.63)
- Bachelors in Mechanical Engineering from IIT Kharagpur (GPA 8.63) 
- Bachelors in Computer Science and Engineering (Minor) from IIT Kharagpur (GPA 8.35)

Technical Skills:
- Programming: Python, C++, Node.js, React.js, SQL
- Databases: PostgreSQL, MongoDB
- Cloud: AWS, Azure, Docker
- AI/ML: TensorFlow, Keras, LlamaIndex, Transformers
- Specialties: Backend Development, NLP, Machine Learning, Computer Vision

Certifications:
- AWS Certified Machine Learning Specialist
- AWS Certified Solution Architect-Associate
- Kaggle Expert

Contact: rajorshitah9@gmail.com, (+81)8048172852, Tokyo, Japan
"""
