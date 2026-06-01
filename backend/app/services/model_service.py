import os
import joblib
import numpy as np
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")
LABEL_ENCODER_PATH = os.path.join(MODEL_DIR, "label_encoder.pkl")
FEATURE_COLUMNS_PATH = os.path.join(MODEL_DIR, "feature_columns.pkl")
MLB_DICT_PATH = os.path.join(MODEL_DIR, "mlb_dict.pkl")

model = joblib.load(MODEL_PATH)
label_encoder = joblib.load(LABEL_ENCODER_PATH)
feature_columns = joblib.load(FEATURE_COLUMNS_PATH)
mlb_dict = joblib.load(MLB_DICT_PATH)

MERGED_TO_ORIGINAL = {
    "Digital Technology": [
        "Digital Technology"
    ],
    "Education": [
        "Education"
    ],
    "Financial Services": [
        "Financial Services"
    ],
    "Agriculture & Natural Resources": [
        "Agriculture",
        "Energy & Natural Resources"
    ],
    "Engineering & Manufacturing": [
        "Advanced Manufacturing",
        "Construction"
    ],
    "Healthcare & Public Services": [
        "Healthcare & Human Services",
        "Public Service & Safety"
    ],
    "Business & Management": [
        "Marketing & Sales",
        "Management & Entrepreneurship",
        "Supply Chain & Transportation"
    ],
    "Creative & Hospitality": [
        "Arts, Entertainment & Design",
        "Hospitality, Events & Tourism"
    ],
}


# =========================================================
# EXPANDED CAMBODIA-ORIENTED MICRO MAJOR DICTIONARY
# =========================================================
ORIGINAL_TO_MICRO = {
    "Digital Technology": [
        "Computer Science",
        "Software Engineering",
        "Information Technology",
        "Information Systems",
        "Management Information Systems",
        "Data Science",
        "Data Analytics",
        "Business Analytics",
        "Data Engineering",
        "Artificial Intelligence",
        "AI Engineering",
        "Machine Learning",
        "Computer Engineering",
        "Computer Networks",
        "Network Engineering",
        "Cyber Security",
        "Cybersecurity",
        "Information Security",
        "Digital Forensics",
        "Cloud Computing",
        "Internet of Things",
        "IoT Engineering",
        "Web Development",
        "Web Engineering",
        "Mobile Application Development",
        "Mobile App Development",
        "Application Development",
        "System Development",
        "Database Systems",
        "Database Administration",
        "Software Development",
        "Software Testing",
        "UI UX Design",
        "Human Computer Interaction",
        "Robotics Programming",
        "Embedded Systems",
        "Computer Vision",
        "Natural Language Processing",
        "E Commerce Technology",
        "Digital Economy",
        "Financial Technology",
        "FinTech",
        "Blockchain Technology",
        "Smart City Technology",
        "ICT",
        "Information and Communication Technology",
        "Information and Communication Engineering",
        "Digital Business Technology",
        "Automation Systems",
        "IT Management",
        "IT Audit",
        "ERP Systems",
        "Digital Transformation",
        "Game Development",
        "AR VR Development",
        "Bioinformatics",
        "Health Informatics",
        "DevOps",
        "System Administration",
        "Network Administration"
    ],

    "Education": [
        "Education",
        "English Education",
        "Mathematics Education",
        "Math Education",
        "Science Education",
        "Biology Education",
        "Chemistry Education",
        "Physics Education",
        "Khmer Literature Education",
        "History Education",
        "Geography Education",
        "Moral and Civic Education",
        "Primary Education",
        "Secondary Education",
        "Early Childhood Education",
        "Preschool Education",
        "Special Education",
        "Inclusive Education",
        "Educational Leadership",
        "School Leadership",
        "Educational Management",
        "Education Management",
        "Curriculum and Instruction",
        "Teaching Methodology",
        "Pedagogy",
        "TESOL",
        "TEFL",
        "Applied Linguistics Education",
        "Language Teaching",
        "STEM Education",
        "Educational Technology",
        "Digital Pedagogy",
        "Instructional Design",
        "Assessment and Evaluation",
        "Educational Measurement",
        "Guidance and Counseling",
        "School Counseling",
        "Educational Psychology",
        "Teacher Education",
        "Teacher Training",
        "Higher Education Administration",
        "Adult Education",
        "Non Formal Education",
        "Technical and Vocational Education",
        "TVET Education",
        "Physical Education Teaching",
        "Art Education",
        "Music Education",
        "Education Policy",
        "Comparative Education",
        "Education Research",
        "Learning Sciences",
        "Learning Analytics"
    ],

    "Financial Services": [
        "Accounting",
        "Finance",
        "Banking",
        "Economics",
        "International Economics",
        "Development Economics",
        "Financial Technology",
        "FinTech",
        "Corporate Finance",
        "Investment",
        "Investment Analysis",
        "Commercial Banking",
        "Bank Management",
        "Banking and Finance",
        "Risk Management",
        "Credit Risk",
        "Insurance",
        "Actuarial Science",
        "Auditing",
        "Taxation",
        "Tax Accounting",
        "Managerial Accounting",
        "Financial Accounting",
        "Public Finance",
        "Financial Management",
        "Microfinance",
        "Digital Finance",
        "Financial Markets",
        "Financial Services",
        "Treasury Management",
        "Financial Reporting",
        "Forensic Accounting",
        "Accounting Information Systems",
        "Quantitative Finance",
        "Business Finance",
        "Corporate Banking",
        "Retail Banking",
        "Wealth Management",
        "Asset Management",
        "Portfolio Management",
        "Compliance",
        "AML Compliance",
        "Economic Policy",
        "International Finance",
        "Investment Banking",
        "Credit Management",
        "Loan Management",
        "Financial Analysis",
        "Economic Development",
        "Banking Operations",
        "Financial Planning",
        "Financial Engineering"
    ],

    "Agriculture": [
        "Agriculture",
        "Agronomy",
        "Crop Science",
        "Animal Science",
        "Livestock Science",
        "Veterinary Science",
        "Agricultural Economics",
        "Agribusiness",
        "Agricultural Business",
        "Agricultural Engineering",
        "Agricultural Technology",
        "Food Science",
        "Food Technology",
        "Food Processing",
        "Plant Science",
        "Horticulture",
        "Soil Science",
        "Soil and Water Management",
        "Irrigation Agriculture",
        "Fisheries",
        "Aquaculture",
        "Forestry Agriculture",
        "Agro Industry",
        "Post Harvest Technology",
        "Seed Science",
        "Plant Protection",
        "Pest Management",
        "Weed Science",
        "Organic Agriculture",
        "Sustainable Agriculture",
        "Climate Smart Agriculture",
        "Agroecology",
        "Farm Management",
        "Rural Development",
        "Agricultural Extension",
        "Agricultural Marketing",
        "Agricultural Finance",
        "Precision Agriculture",
        "Farm Mechanization",
        "Agri Entrepreneurship",
        "Dairy Science",
        "Poultry Science",
        "Animal Nutrition",
        "Crop Production",
        "Agroforestry",
        "Food Security",
        "Agricultural Supply Chain",
        "Rice Science",
        "Tropical Agriculture",
        "Water Management in Agriculture"
    ],

    "Energy & Natural Resources": [
        "Environmental Science",
        "Environmental Management",
        "Environmental Engineering",
        "Renewable Energy",
        "Energy Engineering",
        "Electrical and Energy Engineering",
        "Sustainable Energy",
        "Climate Change Studies",
        "Climate Science",
        "Natural Resource Management",
        "Water Resource Management",
        "Hydrology",
        "Hydrology and Water Resources",
        "Water Environmental Engineering",
        "Water Resources and Rural Infrastructure",
        "Geology",
        "Geoscience",
        "Geo Resources",
        "Geo Resources and Petroleum",
        "Petroleum Engineering",
        "Mining Engineering",
        "Geotechnical Engineering",
        "Geography and Environment",
        "Forestry",
        "Conservation Biology",
        "Ecology",
        "Biodiversity Conservation",
        "Land Management",
        "Land and Water Resources",
        "Environmental Policy",
        "Environmental Sustainability",
        "Disaster Risk Management",
        "Natural Disaster Management",
        "Rural Infrastructure",
        "Waste Management",
        "Solid Waste Management",
        "Water Supply Engineering",
        "Sanitation Engineering",
        "Energy Policy",
        "Green Technology",
        "Resource Economics",
        "Environmental Health",
        "Marine Resources",
        "Fisheries Resource Management",
        "Protected Area Management",
        "Environmental Monitoring",
        "Sustainable Development",
        "Carbon Management",
        "Hydro Power Engineering",
        "Solar Energy Systems"
    ],

    "Advanced Manufacturing": [
        "Mechanical Engineering",
        "Industrial Engineering",
        "Manufacturing Engineering",
        "Mechatronics",
        "Mechatronics Engineering",
        "Electrical Engineering",
        "Electronics Engineering",
        "Industrial and Mechanical Engineering",
        "Automation Engineering",
        "Robotics Engineering",
        "Robotics and Automation Engineering",
        "Smart Automation Systems",
        "Electronics and Smart Automation System",
        "Materials Science",
        "Materials Science and Engineering",
        "Chemical Engineering",
        "Food Engineering",
        "Food Science and Engineering",
        "Production Engineering",
        "Industrial Production",
        "Quality Engineering",
        "Process Engineering",
        "Instrumentation Engineering",
        "Control Engineering",
        "Embedded Electronics",
        "Electromechanical Engineering",
        "Automotive Engineering",
        "Aerospace Engineering",
        "Industrial Technology",
        "Sustainable Manufacturing",
        "Factory Automation",
        "Machine Design",
        "Thermal Engineering",
        "Power Engineering",
        "Industrial Maintenance",
        "Product Development",
        "Industrial Design Engineering",
        "Operations Engineering",
        "Supply Chain Engineering",
        "Packaging Engineering",
        "Biomedical Engineering",
        "Nanotechnology Engineering",
        "Materials Processing",
        "Welding Engineering",
        "Industrial Robotics",
        "Electronic Systems Engineering",
        "Microelectronics",
        "Semiconductor Technology",
        "Textile Engineering",
        "Garment Technology"
    ],

    "Construction": [
        "Civil Engineering",
        "Construction Management",
        "Construction Management and Infrastructure Engineering",
        "Architecture",
        "Architectural Engineering",
        "Architecture Technology",
        "Structural Engineering",
        "Surveying",
        "Quantity Surveying",
        "Urban Planning",
        "Town Planning",
        "Infrastructure Engineering",
        "Building Engineering",
        "Building Technology",
        "Geotechnical Engineering",
        "Transportation Engineering",
        "Bridge Engineering",
        "Highway Engineering",
        "Road Engineering",
        "Water Supply and Sanitation Engineering",
        "Municipal Engineering",
        "Construction Technology",
        "Project Construction Management",
        "Land Surveying",
        "Geomatic Engineering",
        "Real Estate Development",
        "Interior Architecture",
        "Landscape Architecture",
        "Housing Development",
        "Rural Infrastructure Engineering",
        "Hydraulic Structures",
        "Construction Economics",
        "Construction Supervision",
        "Building Services Engineering",
        "Environmental Civil Engineering",
        "Public Works Engineering",
        "Smart Infrastructure",
        "Urban Infrastructure Planning",
        "Concrete Technology",
        "Foundation Engineering",
        "Site Engineering",
        "Building Information Modeling",
        "BIM Engineering",
        "Property Development",
        "Urban Design",
        "Regional Planning",
        "Industrial Construction",
        "Water Infrastructure",
        "Drainage Engineering",
        "Coastal Engineering"
    ],

    "Healthcare & Human Services": [
        "Medicine",
        "General Medicine",
        "Nursing",
        "Midwifery",
        "Pharmacy",
        "Public Health",
        "Medical Laboratory Science",
        "Medical Biology",
        "Dentistry",
        "Dental Surgery",
        "Dental Hygiene",
        "Physiotherapy",
        "Physical Therapy",
        "Occupational Therapy",
        "Radiology",
        "Medical Imaging",
        "Biomedical Science",
        "Biomedicine",
        "Nutrition and Dietetics",
        "Nutrition",
        "Epidemiology",
        "Health Education",
        "Health Services Management",
        "Healthcare Management",
        "Hospital Management",
        "Clinical Psychology",
        "Psychology",
        "Counseling Psychology",
        "Social Work",
        "Community Development",
        "Community Health",
        "Maternal and Child Health",
        "Environmental Health",
        "Health Information Management",
        "Health Informatics",
        "Laboratory Technology",
        "Medical Technology",
        "Emergency Care",
        "Paramedical Science",
        "Rehabilitation Science",
        "Speech Therapy",
        "Mental Health",
        "Behavioral Science",
        "Population Studies",
        "Gerontology",
        "Occupational Health",
        "Pharmaceutical Science",
        "Clinical Pharmacy",
        "Disease Prevention",
        "Health Promotion"
    ],

    "Public Service & Safety": [
        "Law",
        "Public Administration",
        "Political Science",
        "International Relations",
        "Public Policy",
        "Governance",
        "Public Management",
        "Criminal Justice",
        "Criminology",
        "Security Studies",
        "Peace and Conflict Studies",
        "Human Rights",
        "Diplomacy",
        "Public Affairs",
        "Development Studies",
        "International Development",
        "Community Development",
        "Local Governance",
        "Public Sector Management",
        "Judicial Studies",
        "Legal Studies",
        "Constitutional Law",
        "Business Law",
        "Private Law",
        "Public Law",
        "Administrative Law",
        "International Law",
        "Civil Law",
        "Criminal Law",
        "Police Administration",
        "Border Management",
        "Disaster Management",
        "Emergency Management",
        "Social Policy",
        "Public Leadership",
        "Decentralization Studies",
        "Legislative Studies",
        "Mediation and Conflict Resolution",
        "Regional Studies",
        "ASEAN Studies",
        "Strategic Studies",
        "National Security",
        "Public Safety",
        "Policy Analysis",
        "Development Policy",
        "NGO Management",
        "Public Service Management",
        "Refugee and Migration Studies",
        "Anti Corruption Studies",
        "Civic Education"
    ],

    "Marketing & Sales": [
        "Marketing",
        "Digital Marketing",
        "Sales Management",
        "Brand Management",
        "Market Research",
        "Advertising",
        "Public Relations",
        "Consumer Behavior",
        "Retail Management",
        "E Commerce",
        "E Commerce Management",
        "International Marketing",
        "Strategic Marketing",
        "Marketing Communication",
        "Integrated Marketing Communication",
        "Social Media Marketing",
        "Content Marketing",
        "Product Marketing",
        "Trade Marketing",
        "Customer Relationship Management",
        "CRM",
        "Business Development",
        "Merchandising",
        "Sales and Marketing",
        "Service Marketing",
        "Luxury Brand Management",
        "Tourism Marketing",
        "Hospitality Marketing",
        "Digital Business",
        "Marketing Analytics",
        "Corporate Communication",
        "Media Marketing",
        "Event Marketing",
        "Promotion Management",
        "Channel Management",
        "Distribution Marketing",
        "Consumer Insights",
        "Online Sales",
        "Export Marketing",
        "International Trade Marketing",
        "Relationship Marketing",
        "B2B Marketing",
        "B2C Marketing",
        "Visual Merchandising",
        "Pricing Strategy",
        "Brand Communication",
        "Customer Experience Management",
        "Sales Operations",
        "Marketing Strategy",
        "Commercial Management"
    ],

    "Management & Entrepreneurship": [
        "Business Administration",
        "Management",
        "Entrepreneurship",
        "Human Resource Management",
        "Project Management",
        "International Business",
        "Strategic Management",
        "Operations Management",
        "Organizational Management",
        "Leadership",
        "Innovation Management",
        "Business Management",
        "General Management",
        "Small Business Management",
        "Family Business Management",
        "Management of Technology",
        "Office Management",
        "Public Management",
        "Hospital Management",
        "Education Management",
        "Event Management",
        "Hotel Management",
        "Tourism Management",
        "Supply Management",
        "Business Development",
        "Enterprise Management",
        "Corporate Management",
        "Administrative Management",
        "Human Capital Management",
        "Talent Management",
        "Training and Development",
        "Change Management",
        "Knowledge Management",
        "Management Science",
        "Decision Science",
        "Service Management",
        "Innovation and Entrepreneurship",
        "Start Up Management",
        "SME Management",
        "Business Strategy",
        "Quality Management",
        "Operations Strategy",
        "Commercial Management",
        "Retail Management",
        "Franchise Management",
        "Procurement Management",
        "Management Information Systems",
        "Business Economics",
        "Executive Management",
        "Professional Management"
    ],

    "Supply Chain & Transportation": [
        "Supply Chain Management",
        "Logistics",
        "Logistics and Supply Chain Management",
        "Procurement",
        "Transportation Management",
        "Operations Management",
        "Inventory Management",
        "Warehouse Management",
        "Distribution Management",
        "Purchasing Management",
        "Shipping and Logistics",
        "Maritime Studies",
        "Port Management",
        "Freight Management",
        "Customs and Logistics",
        "International Trade Logistics",
        "Global Supply Chain",
        "Import Export Management",
        "Trade and Logistics",
        "Aviation Management",
        "Air Transport Management",
        "Passenger Transport Management",
        "Rail and Transport Studies",
        "Urban Transport Planning",
        "Fleet Management",
        "Cold Chain Management",
        "Procurement and Supply",
        "Operations and Logistics",
        "Transport Economics",
        "Last Mile Delivery Management",
        "Demand Planning",
        "Supply Planning",
        "Sourcing Management",
        "Strategic Procurement",
        "Production Planning",
        "Materials Management",
        "Order Fulfillment",
        "Warehouse Operations",
        "Transport and Logistics Engineering",
        "Distribution and Retail Logistics",
        "Shipping Management",
        "Cargo Management",
        "Supply Chain Analytics",
        "Supply Chain Digitalization",
        "Manufacturing Supply Chain",
        "Retail Supply Chain",
        "Humanitarian Logistics",
        "Trade Facilitation",
        "Cross Border Transport",
        "Operations Research"
    ],

    "Arts, Entertainment & Design": [
        "Graphic Design",
        "Media and Communication",
        "Media Studies",
        "Communication",
        "Journalism",
        "Animation",
        "Fashion Design",
        "Film Production",
        "Film and Television",
        "Visual Arts",
        "Fine Arts",
        "Interior Design",
        "Industrial Design",
        "Multimedia Design",
        "Digital Media",
        "Digital Design",
        "Photography",
        "Music",
        "Music Production",
        "Performing Arts",
        "Theatre Arts",
        "Dance",
        "Creative Arts",
        "Advertising Design",
        "Illustration",
        "Painting",
        "Sculpture",
        "Cinema Studies",
        "Broadcasting",
        "Public Communication",
        "Mass Communication",
        "Creative Media",
        "Video Production",
        "Sound Engineering",
        "Audio Production",
        "Fashion Marketing",
        "Art History",
        "Khmer Arts",
        "Cultural Studies",
        "Heritage Studies",
        "Museum Studies",
        "Creative Writing",
        "Script Writing",
        "Communication Design",
        "Visual Communication",
        "Digital Content Creation",
        "Motion Graphics",
        "3D Design",
        "Entertainment Management",
        "Event Production"
    ],

    "Hospitality, Events & Tourism": [
        "Hospitality Management",
        "Tourism Management",
        "Event Management",
        "Hotel Management",
        "Travel and Leisure Management",
        "Restaurant Management",
        "Food and Beverage Management",
        "Culinary Arts",
        "Tourism and Hospitality",
        "Resort Management",
        "Front Office Management",
        "Housekeeping Management",
        "Airline Hospitality",
        "Travel Agency Management",
        "Tour Guiding",
        "Tour Operation Management",
        "Destination Management",
        "Ecotourism",
        "Sustainable Tourism",
        "Heritage Tourism",
        "Cultural Tourism",
        "MICE Management",
        "Meetings and Events Management",
        "Convention Management",
        "Leisure Management",
        "Cruise and Hospitality",
        "Hospitality Entrepreneurship",
        "Service Excellence Management",
        "Tourism Marketing",
        "Visitor Management",
        "Hotel and Tourism Management",
        "Hospitality Operations",
        "Resort and Spa Management",
        "Accommodation Management",
        "Restaurant Entrepreneurship",
        "Travel Business Management",
        "Event Production Management",
        "Wedding and Event Planning",
        "Festival Management",
        "Casino Hospitality Management",
        "Recreation Management",
        "Food Service Management",
        "Guest Relations Management",
        "Tourism Development",
        "Community Based Tourism",
        "Hospitality and Customer Service",
        "Aviation Hospitality",
        "Airport Service Management",
        "Tourism Economics",
        "International Tourism"
    ],
}


# =========================================================
# RULE-BASED SCORING CONFIG
# =========================================================
MICRO_PROFILE_RULES = {
    "Digital Technology": {
        "Computer Science": {
            "favorite_subjects": {"Computer Science / ICT": 4, "Mathematics": 2},
            "good_at_subjects": {"Computer Science / ICT": 4, "Mathematics": 2},
            "interests": {"Technology / AI": 4, "Research / Science": 1},
            "hobbies": {"Coding / Programming": 4, "Gaming": 1},
        },
        "Software Engineering": {
            "favorite_subjects": {"Computer Science / ICT": 4},
            "good_at_subjects": {"Computer Science / ICT": 4, "Mathematics": 1},
            "interests": {"Technology / AI": 3},
            "hobbies": {"Coding / Programming": 5},
        },
        "Information Technology": {
            "favorite_subjects": {"Computer Science / ICT": 3},
            "good_at_subjects": {"Computer Science / ICT": 3},
            "interests": {"Technology / AI": 3},
            "hobbies": {"Gaming": 1, "Coding / Programming": 2},
        },
        "Cyber Security": {
            "favorite_subjects": {"Computer Science / ICT": 2},
            "good_at_subjects": {"Computer Science / ICT": 4, "Mathematics": 1},
            "interests": {"Technology / AI": 4},
            "hobbies": {"Coding / Programming": 3},
        },
        "Cybersecurity": {
            "favorite_subjects": {"Computer Science / ICT": 2},
            "good_at_subjects": {"Computer Science / ICT": 4, "Mathematics": 1},
            "interests": {"Technology / AI": 4},
            "hobbies": {"Coding / Programming": 3},
        },
        "Data Science": {
            "favorite_subjects": {"Mathematics": 4, "Computer Science / ICT": 2},
            "good_at_subjects": {"Mathematics": 4, "Computer Science / ICT": 2},
            "interests": {"Technology / AI": 4, "Research / Science": 2},
            "hobbies": {"Coding / Programming": 2},
        },
        "Artificial Intelligence": {
            "favorite_subjects": {"Mathematics": 3, "Computer Science / ICT": 3},
            "good_at_subjects": {"Mathematics": 3, "Computer Science / ICT": 3},
            "interests": {"Technology / AI": 5, "Research / Science": 2},
            "hobbies": {"Coding / Programming": 3, "Gaming": 1},
        },
        "Machine Learning": {
            "favorite_subjects": {"Mathematics": 4, "Computer Science / ICT": 2},
            "good_at_subjects": {"Mathematics": 4, "Computer Science / ICT": 2},
            "interests": {"Technology / AI": 5, "Research / Science": 2},
            "hobbies": {"Coding / Programming": 3},
        },
        "Information Systems": {
            "favorite_subjects": {"Computer Science / ICT": 2, "Business": 2},
            "good_at_subjects": {"Computer Science / ICT": 2, "Business": 2},
            "interests": {"Technology / AI": 2, "Business / Entrepreneurship": 2},
            "hobbies": {},
        },
        "Management Information Systems": {
            "favorite_subjects": {"Computer Science / ICT": 2, "Business": 3},
            "good_at_subjects": {"Computer Science / ICT": 2, "Business": 3},
            "interests": {"Technology / AI": 2, "Business / Entrepreneurship": 3},
            "hobbies": {},
        },
        "__default__": {
            "favorite_subjects": {"Computer Science / ICT": 3, "Mathematics": 1},
            "good_at_subjects": {"Computer Science / ICT": 3, "Mathematics": 1},
            "interests": {"Technology / AI": 3, "Research / Science": 1},
            "hobbies": {"Coding / Programming": 2, "Gaming": 1},
        },
    },

    "Education": {
        "English Education": {
            "favorite_subjects": {"English": 5},
            "good_at_subjects": {"English": 5},
            "interests": {"Education / Teaching": 4},
            "hobbies": {"Tutoring friends": 3},
        },
        "Mathematics Education": {
            "favorite_subjects": {"Mathematics": 5},
            "good_at_subjects": {"Mathematics": 5},
            "interests": {"Education / Teaching": 4},
            "hobbies": {"Tutoring friends": 3},
        },
        "Science Education": {
            "favorite_subjects": {"Biology": 2, "Chemistry": 2, "Physics": 2},
            "good_at_subjects": {"Biology": 2, "Chemistry": 2, "Physics": 2},
            "interests": {"Education / Teaching": 4, "Research / Science": 1},
            "hobbies": {"Tutoring friends": 2},
        },
        "Educational Leadership": {
            "favorite_subjects": {},
            "good_at_subjects": {},
            "interests": {"Education / Teaching": 4},
            "hobbies": {"Tutoring friends": 2},
        },
        "Curriculum and Instruction": {
            "favorite_subjects": {},
            "good_at_subjects": {},
            "interests": {"Education / Teaching": 4},
            "hobbies": {"Tutoring friends": 3},
        },
        "__default__": {
            "favorite_subjects": {"English": 2, "Mathematics": 2},
            "good_at_subjects": {"English": 2, "Mathematics": 2},
            "interests": {"Education / Teaching": 4},
            "hobbies": {"Tutoring friends": 3},
        },
    },

    "Financial Services": {
        "Accounting": {
            "favorite_subjects": {"Accounting": 5, "Economics": 1, "Business": 1},
            "good_at_subjects": {"Accounting": 5, "Economics": 1, "Business": 1},
            "interests": {"Finance / Investment": 2},
            "hobbies": {},
        },
        "Finance": {
            "favorite_subjects": {"Economics": 2, "Accounting": 1, "Business": 1},
            "good_at_subjects": {"Economics": 2, "Accounting": 1, "Business": 1},
            "interests": {"Finance / Investment": 5},
            "hobbies": {"Stock / Crypto trading": 3},
        },
        "Banking": {
            "favorite_subjects": {"Economics": 2, "Business": 2},
            "good_at_subjects": {"Economics": 2, "Business": 2},
            "interests": {"Finance / Investment": 4},
            "hobbies": {},
        },
        "Economics": {
            "favorite_subjects": {"Economics": 5, "Mathematics": 1},
            "good_at_subjects": {"Economics": 5, "Mathematics": 1},
            "interests": {"Finance / Investment": 3, "Research / Science": 1},
            "hobbies": {},
        },
        "Financial Technology": {
            "favorite_subjects": {"Accounting": 1, "Economics": 2, "Computer Science / ICT": 2},
            "good_at_subjects": {"Accounting": 1, "Economics": 2, "Computer Science / ICT": 2},
            "interests": {"Finance / Investment": 4, "Technology / AI": 3},
            "hobbies": {"Stock / Crypto trading": 1, "Coding / Programming": 1},
        },
        "FinTech": {
            "favorite_subjects": {"Accounting": 1, "Economics": 2, "Computer Science / ICT": 2},
            "good_at_subjects": {"Accounting": 1, "Economics": 2, "Computer Science / ICT": 2},
            "interests": {"Finance / Investment": 4, "Technology / AI": 3},
            "hobbies": {"Stock / Crypto trading": 1, "Coding / Programming": 1},
        },
        "__default__": {
            "favorite_subjects": {"Accounting": 3, "Economics": 2, "Business": 1},
            "good_at_subjects": {"Accounting": 3, "Economics": 2, "Business": 1},
            "interests": {"Finance / Investment": 4},
            "hobbies": {"Stock / Crypto trading": 2},
        },
    },

    "Agriculture": {
        "Agronomy": {
            "favorite_subjects": {"Biology": 3},
            "good_at_subjects": {"Biology": 3},
            "interests": {"Agriculture": 5},
            "hobbies": {},
        },
        "Animal Science": {
            "favorite_subjects": {"Biology": 3},
            "good_at_subjects": {"Biology": 3},
            "interests": {"Agriculture": 4},
            "hobbies": {},
        },
        "Agricultural Economics": {
            "favorite_subjects": {"Biology": 1, "Business": 2, "Economics": 2},
            "good_at_subjects": {"Business": 2, "Economics": 2},
            "interests": {"Agriculture": 4, "Business / Entrepreneurship": 1},
            "hobbies": {},
        },
        "Crop Science": {
            "favorite_subjects": {"Biology": 3},
            "good_at_subjects": {"Biology": 3},
            "interests": {"Agriculture": 5},
            "hobbies": {},
        },
        "Food Science": {
            "favorite_subjects": {"Biology": 2, "Chemistry": 3},
            "good_at_subjects": {"Biology": 2, "Chemistry": 3},
            "interests": {"Agriculture": 2, "Research / Science": 2},
            "hobbies": {},
        },
        "__default__": {
            "favorite_subjects": {"Biology": 2, "Chemistry": 1},
            "good_at_subjects": {"Biology": 2, "Chemistry": 1},
            "interests": {"Agriculture": 4, "Research / Science": 1},
            "hobbies": {},
        },
    },

    "Energy & Natural Resources": {
        "Environmental Science": {
            "favorite_subjects": {"Biology": 2, "Chemistry": 1},
            "good_at_subjects": {"Biology": 2, "Chemistry": 1},
            "interests": {"Environment / Sustainability": 5, "Research / Science": 2},
            "hobbies": {},
        },
        "Renewable Energy": {
            "favorite_subjects": {"Physics": 3, "Mathematics": 2},
            "good_at_subjects": {"Physics": 3, "Mathematics": 2},
            "interests": {"Environment / Sustainability": 4, "Technology / AI": 1},
            "hobbies": {"DIY / Building projects": 1},
        },
        "Geology": {
            "favorite_subjects": {"Physics": 2, "Biology": 1},
            "good_at_subjects": {"Physics": 2},
            "interests": {"Research / Science": 3, "Environment / Sustainability": 1},
            "hobbies": {},
        },
        "Hydrology": {
            "favorite_subjects": {"Physics": 2, "Mathematics": 2},
            "good_at_subjects": {"Physics": 2, "Mathematics": 2},
            "interests": {"Environment / Sustainability": 4, "Research / Science": 1},
            "hobbies": {},
        },
        "__default__": {
            "favorite_subjects": {"Biology": 1, "Physics": 1},
            "good_at_subjects": {"Biology": 1, "Physics": 1, "Mathematics": 1},
            "interests": {"Environment / Sustainability": 4, "Research / Science": 2},
            "hobbies": {},
        },
    },

    "Advanced Manufacturing": {
        "Mechanical Engineering": {
            "favorite_subjects": {"Physics": 3, "Mathematics": 2},
            "good_at_subjects": {"Physics": 3, "Mathematics": 2},
            "interests": {"Engineering / Building things": 5},
            "hobbies": {"DIY / Building projects": 3},
        },
        "Electrical Engineering": {
            "favorite_subjects": {"Physics": 3, "Mathematics": 2},
            "good_at_subjects": {"Physics": 3, "Mathematics": 2},
            "interests": {"Engineering / Building things": 4, "Technology / AI": 1},
            "hobbies": {"DIY / Building projects": 2},
        },
        "Industrial Engineering": {
            "favorite_subjects": {"Mathematics": 3, "Business": 1},
            "good_at_subjects": {"Mathematics": 3, "Business": 1},
            "interests": {"Engineering / Building things": 3, "Business / Entrepreneurship": 1},
            "hobbies": {"DIY / Building projects": 1},
        },
        "Manufacturing Engineering": {
            "favorite_subjects": {"Physics": 2, "Mathematics": 2},
            "good_at_subjects": {"Physics": 2, "Mathematics": 2},
            "interests": {"Engineering / Building things": 5},
            "hobbies": {"DIY / Building projects": 2},
        },
        "Mechatronics": {
            "favorite_subjects": {"Physics": 2, "Mathematics": 2, "Computer Science / ICT": 1},
            "good_at_subjects": {"Physics": 2, "Mathematics": 2, "Computer Science / ICT": 1},
            "interests": {"Engineering / Building things": 4, "Technology / AI": 2},
            "hobbies": {"DIY / Building projects": 2, "Coding / Programming": 1},
        },
        "Mechatronics Engineering": {
            "favorite_subjects": {"Physics": 2, "Mathematics": 2, "Computer Science / ICT": 1},
            "good_at_subjects": {"Physics": 2, "Mathematics": 2, "Computer Science / ICT": 1},
            "interests": {"Engineering / Building things": 4, "Technology / AI": 2},
            "hobbies": {"DIY / Building projects": 2, "Coding / Programming": 1},
        },
        "__default__": {
            "favorite_subjects": {"Physics": 2, "Mathematics": 2},
            "good_at_subjects": {"Physics": 2, "Mathematics": 2},
            "interests": {"Engineering / Building things": 4},
            "hobbies": {"DIY / Building projects": 2},
        },
    },

    "Construction": {
        "Civil Engineering": {
            "favorite_subjects": {"Physics": 2, "Mathematics": 3},
            "good_at_subjects": {"Physics": 2, "Mathematics": 3},
            "interests": {"Engineering / Building things": 5},
            "hobbies": {"DIY / Building projects": 2},
        },
        "Construction Management": {
            "favorite_subjects": {"Business": 1, "Mathematics": 2},
            "good_at_subjects": {"Business": 1, "Mathematics": 2},
            "interests": {"Engineering / Building things": 4, "Business / Entrepreneurship": 1},
            "hobbies": {"DIY / Building projects": 2},
        },
        "Architecture Technology": {
            "favorite_subjects": {"Art / Design": 2, "Mathematics": 1},
            "good_at_subjects": {"Art / Design": 2, "Mathematics": 1},
            "interests": {"Engineering / Building things": 3, "Creative Arts": 1},
            "hobbies": {"Drawing / Design": 4},
        },
        "Architecture": {
            "favorite_subjects": {"Art / Design": 2, "Mathematics": 1},
            "good_at_subjects": {"Art / Design": 2, "Mathematics": 1},
            "interests": {"Engineering / Building things": 3, "Creative Arts": 2},
            "hobbies": {"Drawing / Design": 4},
        },
        "Structural Engineering": {
            "favorite_subjects": {"Physics": 2, "Mathematics": 4},
            "good_at_subjects": {"Physics": 2, "Mathematics": 4},
            "interests": {"Engineering / Building things": 4},
            "hobbies": {},
        },
        "__default__": {
            "favorite_subjects": {"Physics": 1, "Mathematics": 2, "Art / Design": 1},
            "good_at_subjects": {"Physics": 1, "Mathematics": 2, "Art / Design": 1},
            "interests": {"Engineering / Building things": 4},
            "hobbies": {"Drawing / Design": 1, "DIY / Building projects": 1},
        },
    },

    "Healthcare & Human Services": {
        "Medicine": {
            "favorite_subjects": {"Biology": 4, "Chemistry": 3},
            "good_at_subjects": {"Biology": 4, "Chemistry": 3},
            "interests": {"Healthcare / Medicine": 5, "Research / Science": 1},
            "hobbies": {"Volunteering": 1},
        },
        "General Medicine": {
            "favorite_subjects": {"Biology": 4, "Chemistry": 3},
            "good_at_subjects": {"Biology": 4, "Chemistry": 3},
            "interests": {"Healthcare / Medicine": 5, "Research / Science": 1},
            "hobbies": {"Volunteering": 1},
        },
        "Nursing": {
            "favorite_subjects": {"Biology": 4},
            "good_at_subjects": {"Biology": 4},
            "interests": {"Healthcare / Medicine": 5},
            "hobbies": {"Volunteering": 2},
        },
        "Pharmacy": {
            "favorite_subjects": {"Biology": 2, "Chemistry": 4},
            "good_at_subjects": {"Biology": 2, "Chemistry": 4},
            "interests": {"Healthcare / Medicine": 4},
            "hobbies": {},
        },
        "Medical Laboratory Science": {
            "favorite_subjects": {"Biology": 3, "Chemistry": 3},
            "good_at_subjects": {"Biology": 3, "Chemistry": 3},
            "interests": {"Healthcare / Medicine": 3, "Research / Science": 2},
            "hobbies": {},
        },
        "Public Health": {
            "favorite_subjects": {"Biology": 2},
            "good_at_subjects": {"Biology": 2},
            "interests": {"Healthcare / Medicine": 4, "Social Work": 2},
            "hobbies": {"Volunteering": 2},
        },
        "Social Work": {
            "favorite_subjects": {},
            "good_at_subjects": {},
            "interests": {"Social Work": 5},
            "hobbies": {"Volunteering": 3},
        },
        "Psychology": {
            "favorite_subjects": {"Biology": 1, "English": 1},
            "good_at_subjects": {"English": 1},
            "interests": {"Psychology / Human behavior": 5, "Social Work": 1},
            "hobbies": {},
        },
        "__default__": {
            "favorite_subjects": {"Biology": 2, "Chemistry": 2},
            "good_at_subjects": {"Biology": 2, "Chemistry": 2},
            "interests": {"Healthcare / Medicine": 4, "Social Work": 1},
            "hobbies": {"Volunteering": 1},
        },
    },

    "Public Service & Safety": {
        "Law": {
            "favorite_subjects": {"English": 1},
            "good_at_subjects": {"English": 1},
            "interests": {"Law / Politics": 5},
            "hobbies": {"Debate / Public speaking": 4},
        },
        "International Relations": {
            "favorite_subjects": {"English": 1},
            "good_at_subjects": {"English": 1},
            "interests": {"Law / Politics": 4, "Media / Communication": 1},
            "hobbies": {"Debate / Public speaking": 2},
        },
        "Public Administration": {
            "favorite_subjects": {"Business": 1},
            "good_at_subjects": {"Business": 1},
            "interests": {"Law / Politics": 4, "Social Work": 1},
            "hobbies": {"Volunteering": 1},
        },
        "Criminal Justice": {
            "favorite_subjects": {},
            "good_at_subjects": {},
            "interests": {"Law / Politics": 5},
            "hobbies": {},
        },
        "Community Development": {
            "favorite_subjects": {},
            "good_at_subjects": {},
            "interests": {"Social Work": 3, "Law / Politics": 1},
            "hobbies": {"Volunteering": 2},
        },
        "__default__": {
            "favorite_subjects": {},
            "good_at_subjects": {},
            "interests": {"Law / Politics": 4, "Social Work": 1},
            "hobbies": {"Debate / Public speaking": 2, "Volunteering": 1},
        },
    },

    "Marketing & Sales": {
        "Marketing": {
            "favorite_subjects": {"Business": 2},
            "good_at_subjects": {"Business": 2},
            "interests": {"Media / Communication": 3, "Business / Entrepreneurship": 2},
            "hobbies": {"Social Media Content Creation": 2},
        },
        "Digital Marketing": {
            "favorite_subjects": {"Business": 1, "Art / Design": 1},
            "good_at_subjects": {"Business": 1, "Art / Design": 1},
            "interests": {"Media / Communication": 4},
            "hobbies": {"Social Media Content Creation": 5, "Photography / Videography": 1},
        },
        "Brand Management": {
            "favorite_subjects": {"Business": 1, "Art / Design": 1},
            "good_at_subjects": {"Business": 1, "Art / Design": 1},
            "interests": {"Media / Communication": 3, "Creative Arts": 2},
            "hobbies": {"Social Media Content Creation": 2},
        },
        "Market Research": {
            "favorite_subjects": {"Business": 2, "Mathematics": 1},
            "good_at_subjects": {"Business": 2, "Mathematics": 1},
            "interests": {"Media / Communication": 2, "Research / Science": 1},
            "hobbies": {},
        },
        "__default__": {
            "favorite_subjects": {"Business": 2, "Art / Design": 1},
            "good_at_subjects": {"Business": 2, "Art / Design": 1},
            "interests": {"Media / Communication": 3, "Business / Entrepreneurship": 1},
            "hobbies": {"Social Media Content Creation": 3, "Photography / Videography": 1},
        },
    },

    "Management & Entrepreneurship": {
        "Business Administration": {
            "favorite_subjects": {"Business": 4},
            "good_at_subjects": {"Business": 4},
            "interests": {"Business / Entrepreneurship": 4},
            "hobbies": {"Online Business": 2},
        },
        "Management": {
            "favorite_subjects": {"Business": 4},
            "good_at_subjects": {"Business": 4},
            "interests": {"Business / Entrepreneurship": 3},
            "hobbies": {"Online Business": 1},
        },
        "Entrepreneurship": {
            "favorite_subjects": {"Business": 3},
            "good_at_subjects": {"Business": 3},
            "interests": {"Business / Entrepreneurship": 5},
            "hobbies": {"Online Business": 5},
        },
        "Human Resource Management": {
            "favorite_subjects": {"Business": 2, "English": 1},
            "good_at_subjects": {"Business": 2, "English": 1},
            "interests": {"Psychology / Human behavior": 4, "Business / Entrepreneurship": 1},
            "hobbies": {},
        },
        "Project Management": {
            "favorite_subjects": {"Business": 2, "Mathematics": 1},
            "good_at_subjects": {"Business": 2, "Mathematics": 1},
            "interests": {"Business / Entrepreneurship": 3, "Engineering / Building things": 1},
            "hobbies": {},
        },
        "__default__": {
            "favorite_subjects": {"Business": 3},
            "good_at_subjects": {"Business": 3},
            "interests": {"Business / Entrepreneurship": 4, "Psychology / Human behavior": 1},
            "hobbies": {"Online Business": 2},
        },
    },

    "Supply Chain & Transportation": {
        "Supply Chain Management": {
            "favorite_subjects": {"Business": 2, "Mathematics": 2},
            "good_at_subjects": {"Business": 2, "Mathematics": 2},
            "interests": {"Business / Entrepreneurship": 2},
            "hobbies": {},
        },
        "Logistics": {
            "favorite_subjects": {"Business": 1, "Mathematics": 2},
            "good_at_subjects": {"Business": 1, "Mathematics": 2},
            "interests": {"Business / Entrepreneurship": 1},
            "hobbies": {},
        },
        "Procurement": {
            "favorite_subjects": {"Business": 2},
            "good_at_subjects": {"Business": 2},
            "interests": {"Business / Entrepreneurship": 2},
            "hobbies": {},
        },
        "Transportation Management": {
            "favorite_subjects": {"Business": 1, "Mathematics": 1},
            "good_at_subjects": {"Business": 1, "Mathematics": 1},
            "interests": {},
            "hobbies": {},
        },
        "Operations Management": {
            "favorite_subjects": {"Business": 2, "Mathematics": 2},
            "good_at_subjects": {"Business": 2, "Mathematics": 2},
            "interests": {"Business / Entrepreneurship": 1},
            "hobbies": {},
        },
        "__default__": {
            "favorite_subjects": {"Business": 1, "Mathematics": 2},
            "good_at_subjects": {"Business": 1, "Mathematics": 2},
            "interests": {"Business / Entrepreneurship": 1},
            "hobbies": {},
        },
    },

    "Arts, Entertainment & Design": {
        "Graphic Design": {
            "favorite_subjects": {"Art / Design": 5},
            "good_at_subjects": {"Art / Design": 5},
            "interests": {"Creative Arts": 4},
            "hobbies": {"Drawing / Design": 5},
        },
        "Media and Communication": {
            "favorite_subjects": {"English": 1},
            "good_at_subjects": {"English": 1},
            "interests": {"Media / Communication": 5},
            "hobbies": {"Photography / Videography": 2},
        },
        "Animation": {
            "favorite_subjects": {"Art / Design": 3},
            "good_at_subjects": {"Art / Design": 3},
            "interests": {"Creative Arts": 3},
            "hobbies": {"Drawing / Design": 3, "Gaming": 1},
        },
        "Fashion Design": {
            "favorite_subjects": {"Art / Design": 3},
            "good_at_subjects": {"Art / Design": 3},
            "interests": {"Creative Arts": 4},
            "hobbies": {"Drawing / Design": 3},
        },
        "Film Production": {
            "favorite_subjects": {},
            "good_at_subjects": {},
            "interests": {"Media / Communication": 3, "Creative Arts": 1},
            "hobbies": {"Photography / Videography": 5},
        },
        "__default__": {
            "favorite_subjects": {"Art / Design": 3, "English": 1},
            "good_at_subjects": {"Art / Design": 3, "English": 1},
            "interests": {"Creative Arts": 3, "Media / Communication": 2},
            "hobbies": {"Drawing / Design": 3, "Photography / Videography": 1},
        },
    },

    "Hospitality, Events & Tourism": {
        "Hospitality Management": {
            "favorite_subjects": {"English": 1, "Business": 1},
            "good_at_subjects": {"English": 1, "Business": 1},
            "interests": {"Tourism / Hospitality": 5},
            "hobbies": {},
        },
        "Tourism Management": {
            "favorite_subjects": {"English": 1, "Business": 1},
            "good_at_subjects": {"English": 1, "Business": 1},
            "interests": {"Tourism / Hospitality": 5},
            "hobbies": {},
        },
        "Event Management": {
            "favorite_subjects": {"Business": 1},
            "good_at_subjects": {"Business": 1},
            "interests": {"Tourism / Hospitality": 2, "Media / Communication": 2},
            "hobbies": {"Photography / Videography": 1},
        },
        "Hotel Management": {
            "favorite_subjects": {"English": 1, "Business": 1},
            "good_at_subjects": {"English": 1, "Business": 1},
            "interests": {"Tourism / Hospitality": 4},
            "hobbies": {},
        },
        "Travel and Leisure Management": {
            "favorite_subjects": {"English": 1},
            "good_at_subjects": {"English": 1},
            "interests": {"Tourism / Hospitality": 4},
            "hobbies": {},
        },
        "__default__": {
            "favorite_subjects": {"English": 1, "Business": 1},
            "good_at_subjects": {"English": 1, "Business": 1},
            "interests": {"Tourism / Hospitality": 4, "Media / Communication": 1},
            "hobbies": {"Photography / Videography": 1},
        },
    },
}


# =========================================================
# WORKPLACE + WORKSTYLE RULE PATCH
# =========================================================
# IMPORTANT:
# These values must match the frontend/user-input options exactly.
MACRO_WORKPLACE_WORKSTYLE_RULES = {
    "Digital Technology": {
        "work_style": {
            "working with machines / technology": 5,
            "working with numbers/data": 3,
            "business/management roles": 1,
        },
        "future_workplace": {
            "private company": 4,
            "start up": 4,
            "government": 1,
        },
    },

    "Education": {
        "work_style": {
            "working with people": 5,
            "working in creative / art fields": 1,
        },
        "future_workplace": {
            "government": 4,
            "non-governmental organization (NGO)": 4,
            "private company": 1,
        },
    },

    "Financial Services": {
        "work_style": {
            "working with numbers/data": 5,
            "business/management roles": 3,
            "working with people": 1,
        },
        "future_workplace": {
            "private company": 5,
            "government": 2,
            "start up": 1,
        },
    },

    "Agriculture": {
        "work_style": {
            "working outdoors": 5,
            "working with machines / technology": 2,
            "working with numbers/data": 1,
        },
        "future_workplace": {
            "non-governmental organization (NGO)": 4,
            "government": 3,
            "private company": 2,
            "start up": 1,
        },
    },

    "Energy & Natural Resources": {
        "work_style": {
            "working outdoors": 5,
            "working with numbers/data": 2,
            "working with machines / technology": 2,
        },
        "future_workplace": {
            "government": 4,
            "non-governmental organization (NGO)": 4,
            "private company": 2,
            "start up": 1,
        },
    },

    "Advanced Manufacturing": {
        "work_style": {
            "working with machines / technology": 5,
            "working with numbers/data": 2,
            "working outdoors": 1,
        },
        "future_workplace": {
            "private company": 5,
            "start up": 2,
            "government": 1,
        },
    },

    "Construction": {
        "work_style": {
            "working outdoors": 4,
            "working with machines / technology": 3,
            "business/management roles": 2,
        },
        "future_workplace": {
            "private company": 4,
            "government": 3,
            "start up": 1,
        },
    },

    "Healthcare & Human Services": {
        "work_style": {
            "working with people": 5,
            "working with numbers/data": 1,
        },
        "future_workplace": {
            "government": 4,
            "non-governmental organization (NGO)": 4,
            "private company": 2,
        },
    },

    "Public Service & Safety": {
        "work_style": {
            "working with people": 4,
            "business/management roles": 2,
            "working with numbers/data": 1,
        },
        "future_workplace": {
            "government": 5,
            "non-governmental organization (NGO)": 4,
            "private company": 1,
        },
    },

    "Marketing & Sales": {
        "work_style": {
            "working in creative / art fields": 4,
            "working with people": 4,
            "business/management roles": 3,
            "working with numbers/data": 1,
        },
        "future_workplace": {
            "private company": 5,
            "start up": 3,
            "non-governmental organization (NGO)": 1,
        },
    },

    "Management & Entrepreneurship": {
        "work_style": {
            "business/management roles": 5,
            "working with people": 3,
            "working with numbers/data": 2,
        },
        "future_workplace": {
            "start up": 5,
            "private company": 4,
            "government": 1,
        },
    },

    "Supply Chain & Transportation": {
        "work_style": {
            "business/management roles": 4,
            "working with numbers/data": 3,
            "working with machines / technology": 2,
        },
        "future_workplace": {
            "private company": 5,
            "government": 2,
            "start up": 1,
        },
    },

    "Arts, Entertainment & Design": {
        "work_style": {
            "working in creative / art fields": 5,
            "working with people": 2,
            "working with machines / technology": 1,
        },
        "future_workplace": {
            "private company": 3,
            "start up": 3,
            "non-governmental organization (NGO)": 2,
        },
    },

    "Hospitality, Events & Tourism": {
        "work_style": {
            "working with people": 5,
            "business/management roles": 2,
            "working in creative / art fields": 1,
        },
        "future_workplace": {
            "private company": 5,
            "start up": 2,
            "non-governmental organization (NGO)": 1,
        },
    },
}

def apply_workplace_workstyle_rules():
    """
    Add work_style and future_workplace rules to every micro-major rule,
    including __default__, without manually editing every micro-major.
    """
    for original_class, micro_rules in MICRO_PROFILE_RULES.items():
        extra = MACRO_WORKPLACE_WORKSTYLE_RULES.get(original_class, {})
        work_style_rules = extra.get("work_style", {})
        workplace_rules = extra.get("future_workplace", {})

        for _, rule in micro_rules.items():
            rule.setdefault("work_style", work_style_rules)
            rule.setdefault("future_workplace", workplace_rules)


apply_workplace_workstyle_rules()

def normalize_user_value(field, value):
    value = str(value).strip()

    alias_map = {
        "work_style": {
            "Working with numbers": "Working with data",
            "Working with numbers/data": "Working with data",
            "working with numbers": "Working with data",
            "working with numbers/data": "Working with data",
            "Working with data": "Working with data",
            "working with data": "Working with data",

            "Working with people": "Working with people",
            "working with people": "Working with people",

            "Working with machines / technology": "Working with machines/technology",
            "Working with machines/technology": "Working with machines/technology",
            "working with machines / technology": "Working with machines/technology",
            "working with machines/technology": "Working with machines/technology",

            "Working in creative / art fields": "Working in creative/art fields",
            "Working in creative/art fields": "Working in creative/art fields",
            "working in creative / art fields": "Working in creative/art fields",
            "working in creative/art fields": "Working in creative/art fields",

            "Working outdoors": "Working outdoors",
            "working outdoors": "Working outdoors",

            "Business/management roles": "Business/management roles",
            "business/management roles": "Business/management roles",
        },

        "future_workplace": {
            "Private Company": "private company",
            "private company": "private company",

            "Government": "government",
            "government": "government",

            "Start my own business": "start up",
            "Start up": "start up",
            "Startup": "start up",
            "start up": "start up",

            "Non-governmental organization (NGO)": "non-governmental organization (NGO)",
            "NGO": "non-governmental organization (NGO)",
            "non-governmental organization (NGO)": "non-governmental organization (NGO)",
        },
    }

    return alias_map.get(field, {}).get(value, value)

def preprocess_input(user_input):
    row = {}

    multi_label_fields = [
        "favorite_subjects_sorted",
        "good_at_subjects_sorted",
        "interests_sorted",
        "hobbies_sorted",
        "work_style",
        "future_workplace"
    ]

    for field in multi_label_fields:
        values = user_input.get(field, [])

        if values is None:
            values = []
        elif isinstance(values, str):
            values = [values]
        elif not isinstance(values, list):
            values = [str(values)]

        values = [
            normalize_user_value(field, v)
            for v in values
            if str(v).strip() != ""
        ]

        if field not in mlb_dict:
            raise KeyError(f"Missing encoder for field: {field}")

        mlb = mlb_dict[field]
        transformed = mlb.transform([values])

        for cls, val in zip(mlb.classes_, transformed[0]):
            row[f"{field}__{cls}"] = int(val)

    df = pd.DataFrame([row])

    for col in feature_columns:
        if col not in df.columns:
            df[col] = 0

    df = df[feature_columns]
    return df


def clean_feature_name(feature_name):
    if "__" not in feature_name:
        return feature_name

    field, value = feature_name.split("__", 1)

    field_map = {
        "favorite_subjects_sorted": "Favorite Subject",
        "good_at_subjects_sorted": "Good At Subject",
        "interests_sorted": "Interest",
        "hobbies_sorted": "Hobby",
        "work_style": "Preferred Work Style",
        "future_workplace": "Preferred Workplace",
    }

    pretty_field = field_map.get(field, field)
    return f"{pretty_field}: {value}"


def get_user_feature_importance(X, class_index, top_n=5):
    coef = model.coef_[class_index]
    contributions = X.iloc[0].values * coef

    feature_contrib = pd.DataFrame({
        "feature": X.columns,
        "contribution": contributions
    })

    feature_contrib = feature_contrib[feature_contrib["contribution"] > 0].copy()

    total_positive = feature_contrib["contribution"].sum()
    if total_positive > 0:
        feature_contrib["importance_pct"] = (
            feature_contrib["contribution"] / total_positive
        ) * 100
    else:
        feature_contrib["importance_pct"] = 0

    feature_contrib = feature_contrib.sort_values(
        "importance_pct", ascending=False
    ).head(top_n)

    result = []
    for _, row in feature_contrib.iterrows():
        result.append({
            "feature": clean_feature_name(row["feature"]),
            "importance": round(float(row["importance_pct"]), 2)
        })

    return result


def _format_list(items):
    items = [str(x).strip() for x in items if str(x).strip()]
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    return f"{', '.join(items[:-1])}, and {items[-1]}"


def generate_explanation(user_input, macro_major):
    favorite_subjects = user_input.get("favorite_subjects_sorted", [])
    good_at_subjects = user_input.get("good_at_subjects_sorted", [])
    interests = user_input.get("interests_sorted", [])
    hobbies = user_input.get("hobbies_sorted", [])
    work_style = user_input.get("work_style", [])
    future_workplace = user_input.get("future_workplace", [])

    matched_subjects = []
    matched_strengths = []
    matched_interests = []
    matched_hobbies = []
    matched_work_style = []
    matched_workplace = []
    career_phrase = ""

    if macro_major == "Agriculture & Natural Resources":
        matched_subjects = [x for x in favorite_subjects if x in ["Biology", "Chemistry"]]
        matched_strengths = [x for x in good_at_subjects if x in ["Biology", "Chemistry"]]
        matched_interests = [x for x in interests if x in ["Agriculture", "Environment / Sustainability", "Research / Science"]]
        matched_hobbies = [x for x in hobbies if x in ["Reading", "Volunteering"]]
        career_phrase = "careers in agriculture, environmental systems, and natural resource management"

    elif macro_major == "Digital Technology":
        matched_subjects = [x for x in favorite_subjects if x in ["Computer Science / ICT", "Mathematics", "Physics"]]
        matched_strengths = [x for x in good_at_subjects if x in ["Computer Science / ICT", "Mathematics", "Physics"]]
        matched_interests = [x for x in interests if x in ["Technology / AI", "Research / Science"]]
        matched_hobbies = [x for x in hobbies if x in ["Coding / Programming", "Gaming"]]
        career_phrase = "careers in software, data, and digital technology"

    elif macro_major == "Healthcare & Public Services":
        matched_subjects = [x for x in favorite_subjects if x in ["Biology", "Chemistry"]]
        matched_strengths = [x for x in good_at_subjects if x in ["Biology", "Chemistry"]]
        matched_interests = [x for x in interests if x in ["Healthcare / Medicine", "Social Work", "Law / Politics"]]
        matched_hobbies = [x for x in hobbies if x in ["Volunteering", "Debate / Public speaking"]]
        career_phrase = "careers in healthcare, community service, and public-facing professions"

    elif macro_major == "Financial Services":
        matched_subjects = [x for x in favorite_subjects if x in ["Accounting", "Economics", "Mathematics", "Business"]]
        matched_strengths = [x for x in good_at_subjects if x in ["Accounting", "Economics", "Mathematics", "Business"]]
        matched_interests = [x for x in interests if x in ["Finance / Investment", "Business / Entrepreneurship"]]
        matched_hobbies = [x for x in hobbies if x in ["Stock / Crypto trading", "Online Business"]]
        career_phrase = "careers in accounting, finance, banking, and financial analysis"

    elif macro_major == "Engineering & Manufacturing":
        matched_subjects = [x for x in favorite_subjects if x in ["Mathematics", "Physics", "Chemistry"]]
        matched_strengths = [x for x in good_at_subjects if x in ["Mathematics", "Physics", "Chemistry"]]
        matched_interests = [x for x in interests if x in ["Engineering / Building things", "Technology / AI"]]
        matched_hobbies = [x for x in hobbies if x in ["DIY / Building projects", "Coding / Programming"]]
        career_phrase = "careers in engineering, manufacturing, and technical problem-solving"

    elif macro_major == "Education":
        matched_subjects = [x for x in favorite_subjects if x in ["English", "Mathematics", "Biology", "History"]]
        matched_strengths = [x for x in good_at_subjects if x in ["English", "Mathematics", "Biology", "History"]]
        matched_interests = [x for x in interests if x in ["Education / Teaching", "Psychology / Human behavior"]]
        matched_hobbies = [x for x in hobbies if x in ["Tutoring friends", "Reading", "Writing"]]
        career_phrase = "careers in teaching, training, and educational development"

    elif macro_major == "Business & Management":
        matched_subjects = [x for x in favorite_subjects if x in ["Business", "Accounting", "Economics"]]
        matched_strengths = [x for x in good_at_subjects if x in ["Business", "Accounting", "Economics"]]
        matched_interests = [x for x in interests if x in ["Business / Entrepreneurship", "Media / Communication", "Finance / Investment"]]
        matched_hobbies = [x for x in hobbies if x in ["Online Business", "Social Media Content Creation"]]
        career_phrase = "careers in business operations, entrepreneurship, management, and marketing"

    elif macro_major == "Creative & Hospitality":
        matched_subjects = [x for x in favorite_subjects if x in ["Art / Design", "English"]]
        matched_strengths = [x for x in good_at_subjects if x in ["Art / Design", "English"]]
        matched_interests = [x for x in interests if x in ["Creative Arts", "Tourism / Hospitality", "Media / Communication"]]
        matched_hobbies = [x for x in hobbies if x in ["Drawing / Design", "Photography / Videography", "Social Media Content Creation"]]
        career_phrase = "careers in design, media, hospitality, events, and tourism"

    for original_class in MERGED_TO_ORIGINAL.get(macro_major, [macro_major]):
        default_rule = _get_macro_default_rule(original_class)

        matched_work_style.extend([
            x for x in work_style
            if x in default_rule.get("work_style", {})
        ])

        matched_workplace.extend([
            x for x in future_workplace
            if x in default_rule.get("future_workplace", {})
        ])

    matched_work_style = list(dict.fromkeys(matched_work_style))
    matched_workplace = list(dict.fromkeys(matched_workplace))

    parts = []

    if matched_interests:
        parts.append(f"you selected {_format_list(matched_interests)} as your interest areas")
    if matched_subjects:
        parts.append(f"you like {_format_list(matched_subjects)} as favorite subjects")
    if matched_strengths:
        parts.append(f"you identified {_format_list(matched_strengths)} as subjects you are strong in")
    if matched_hobbies:
        parts.append(f"your hobbies such as {_format_list(matched_hobbies)} also support this direction")
    if matched_work_style:
        parts.append(f"your preferred work style, such as {_format_list(matched_work_style)}, fits this field")
    if matched_workplace:
        parts.append(f"your preferred workplace, such as {_format_list(matched_workplace)}, matches this pathway")

    if parts:
        return (
            f"This major was recommended because {', '.join(parts)}, "
            f"which are highly aligned with {career_phrase}."
        )

    return (
        "This major was recommended because your selected subjects, interests, "
        "hobbies, preferred work style, and preferred workplace show a meaningful "
        "overall alignment with this career pathway."
    )


# =========================================================
# SCORING HELPERS
# =========================================================
def _get_sorted_list(user_input, key):
    value = user_input.get(key, [])
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    return list(value)


def _score_from_rule(
    rule,
    favorite_subjects,
    good_at_subjects,
    interests,
    hobbies,
    work_style,
    future_workplace,
):
    score = 0

    for item, weight in rule.get("favorite_subjects", {}).items():
        if item in favorite_subjects:
            score += weight

    for item, weight in rule.get("good_at_subjects", {}).items():
        if item in good_at_subjects:
            score += weight

    for item, weight in rule.get("interests", {}).items():
        if item in interests:
            score += weight

    for item, weight in rule.get("hobbies", {}).items():
        if item in hobbies:
            score += weight

    for item, weight in rule.get("work_style", {}).items():
        if item in work_style:
            score += weight

    for item, weight in rule.get("future_workplace", {}).items():
        if item in future_workplace:
            score += weight

    return score


def _get_macro_default_rule(original_class):
    return MICRO_PROFILE_RULES.get(original_class, {}).get("__default__", {})


def _get_micro_rule(original_class, micro):
    macro_rules = MICRO_PROFILE_RULES.get(original_class, {})
    return macro_rules.get(micro, macro_rules.get("__default__", {}))


# =========================================================
# RANK ORIGINAL CLASSES
# =========================================================
def rank_original_classes(user_input, merged_class):
    candidates = MERGED_TO_ORIGINAL.get(merged_class, [])
    scores = []

    favorite_subjects = _get_sorted_list(user_input, "favorite_subjects_sorted")
    good_at_subjects = _get_sorted_list(user_input, "good_at_subjects_sorted")
    interests = _get_sorted_list(user_input, "interests_sorted")
    hobbies = _get_sorted_list(user_input, "hobbies_sorted")
    work_style = _get_sorted_list(user_input, "work_style")
    future_workplace = _get_sorted_list(user_input, "future_workplace")

    for original in candidates:
        rule = _get_macro_default_rule(original)
        score = _score_from_rule(
            rule,
            favorite_subjects,
            good_at_subjects,
            interests,
            hobbies,
            work_style,
            future_workplace,
        )

        scores.append({
            "original_class": original,
            "fit_score": score
        })

    return sorted(scores, key=lambda x: x["fit_score"], reverse=True)


# =========================================================
# RANK MICRO MAJORS
# =========================================================
def rank_micro_majors_by_original(user_input, original_class, top_n=3):
    candidates = ORIGINAL_TO_MICRO.get(original_class, [])
    scores = []

    favorite_subjects = _get_sorted_list(user_input, "favorite_subjects_sorted")
    good_at_subjects = _get_sorted_list(user_input, "good_at_subjects_sorted")
    interests = _get_sorted_list(user_input, "interests_sorted")
    hobbies = _get_sorted_list(user_input, "hobbies_sorted")
    work_style = _get_sorted_list(user_input, "work_style")
    future_workplace = _get_sorted_list(user_input, "future_workplace")

    for micro in candidates:
        rule = _get_micro_rule(original_class, micro)
        score = _score_from_rule(
            rule,
            favorite_subjects,
            good_at_subjects,
            interests,
            hobbies,
            work_style,
            future_workplace,
        )
        scores.append((micro, score))

    scores = sorted(scores, key=lambda x: (-x[1], x[0]))
    return [micro for micro, _ in scores[:top_n]]


# =========================================================
# BUILD SUGGESTIONS
# =========================================================
def build_original_class_suggestions(user_input, merged_class, top_originals=5, top_micro=3):
    ranked_originals = rank_original_classes(user_input, merged_class)[:top_originals]

    result = []
    for item in ranked_originals:
        original_class = item["original_class"]
        result.append({
            "original_class": original_class,
            "fit_score": item["fit_score"],
            "top_micro_majors": rank_micro_majors_by_original(
                user_input,
                original_class,
                top_n=top_micro
            )
        })

    return result


# =========================================================
# MAIN PREDICTION
# =========================================================
def predict_top3_recommendations(user_input):
    X = preprocess_input(user_input)

    print("=== MODEL INPUT (ACTIVE FEATURES) ===")
    active_features = X.iloc[0][X.iloc[0] == 1]
    print(active_features)

    probs = model.predict_proba(X)[0]

    print("=== MODEL OUTPUT PROBABILITIES ===")
    for class_name, prob in zip(label_encoder.classes_, probs):
        print(f"{class_name}: {prob:.6f}")

    top3_idx = np.argsort(probs)[::-1][:3]

    recommendations = []
    for idx in top3_idx:
        macro_major = label_encoder.inverse_transform([idx])[0]
        confidence = round(float(probs[idx]) * 100, 2)

        recommendations.append({
            "macro_major": macro_major,
            "confidence": confidence,
            "score": confidence,
            "why_recommended": generate_explanation(user_input, macro_major),
            "feature_importance": get_user_feature_importance(X, idx, top_n=5),
            "original_class_suggestions": build_original_class_suggestions(
                user_input,
                macro_major,
                top_originals=5,
                top_micro=3
            )
        })

    print("=== FINAL TOP 3 RECOMMENDATIONS ===")
    for i, rec in enumerate(recommendations, start=1):
        print(
            f"Top {i}: {rec['macro_major']} | "
            f"Confidence: {rec['confidence']:.2f}%"
        )

    return recommendations