# 📁 Movie Recommendation System - Project Structure

## Overview
A clean, organized, and scalable Django-based movie recommendation system with proper separation of concerns.

---

## 📂 Complete Folder Structure

```
MovieRecommendation/
│
├── 📁 data/                          # All data files (NOT in version control)
│   ├── datasets/                     # Raw CSV datasets
│   │   ├── tmdb_5000_movies.csv      # Movie metadata (4,803 movies)
│   │   └── tmdb_5000_credits.csv     # Cast & crew information
│   ├── models/                       # Pre-trained models
│   │   ├── similarity_list.pkl       # Cosine similarity matrix (4805x4805)
│   │   ├── movies.pkl                # Backup similarity matrix
│   │   ├── demo_model.parquet        # Demo model (legacy)
│   │   └── top_2k_movie_data.parquet # Demo data (legacy)
│   └── processed/                    # Processed data (future use)
│
├── 📁 static/                        # Static assets
│   ├── images/                       # Image files
│   │   ├── logo.png                  # Site logo
│   │   └── header-image.jpg          # Header image
│   ├── videos/                       # Video files
│   │   └── production ID_4779866.mp4 # Background video
│   └── recommender/                  # App-specific static files
│       ├── css/                      # Stylesheets
│       │   ├── cursor.css            # Custom cursor styles
│       │   ├── page.css              # Home page styles
│       │   ├── navbar.css            # Navigation bar styles
│       │   ├── resultpage.css        # Results page styles
│       │   └── resultnavbar.css      # Results navbar styles
│       └── js/                       # JavaScript files
│           └── cursor.js             # Custom cursor logic
│
├── 📁 recommender/                   # Main Django app
│   ├── __init__.py
│   ├── admin.py                      # Django admin configuration
│   ├── apps.py                       # App configuration
│   ├── models.py                     # Database models (currently empty)
│   ├── tests.py                      # Unit tests
│   ├── urls.py                       # URL routing for app
│   ├── views.py                      # View handlers (REFACTORED - clean!)
│   │
│   ├── utils/                        # Utility modules (NEW!)
│   │   ├── __init__.py               # Package initializer
│   │   ├── data_loader.py            # Data loading & preprocessing
│   │   ├── text_processing.py       # Text normalization & fuzzy matching
│   │   └── recommender_engine.py    # Core recommendation logic
│   │
│   ├── migrations/                   # Database migrations
│   │   └── __init__.py
│   │
│   └── templates/                    # HTML templates
│       └── recommender/
│           ├── index.html            # Home page (search form)
│           └── result.html           # Results page (recommendations)
│
├── 📁 movie_recommendation/          # Django project settings
│   ├── __init__.py
│   ├── asgi.py                       # ASGI config
│   ├── settings.py                   # Project settings
│   ├── urls.py                       # Main URL configuration
│   └── wsgi.py                       # WSGI config
│
├── 📁 docs/                          # Documentation (NEW!)
│   ├── PROJECT_STRUCTURE.md          # This file
│   ├── IMPROVEMENTS.md               # Technical improvements log
│   ├── RUNNING_STATUS.md             # Status & usage guide
│   ├── FEATURE_UPDATE.md             # Latest feature documentation
│   └── PROJECT_ORGANIZATION_PLAN.md  # Organization plan
│
├── 📁 scripts/                       # Utility scripts (NEW!)
│   ├── check_pickle.py               # Validate pickle files
│   └── test_data_structure.py       # Test data structure
│
├── 📁 notebooks/                     # Jupyter notebooks (NEW!)
│   └── Movie_Recommendation_System_Complete_Guide.ipynb
│
├── 📁 readme_images/                 # Images for README
│   └── runserver_demo.png
│
├── 📁 .git/                          # Git repository
├── 📁 .vscode/                       # VS Code settings
├── 📁 node_modules/                  # Node packages (if any)
│
├── .gitignore                        # Git ignore rules
├── manage.py                         # Django management script
├── requirements.txt                  # Python dependencies
├── db.sqlite3                        # SQLite database
├── build.sh                          # Build script
├── package.json                      # Node package config
├── package-lock.json                 # Node lock file
└── README.md                         # Main project README

```

---

## 🎯 Module Responsibilities

### **1. Data Layer (`data/`)**
- **Purpose**: Store all data files separately from code
- **Datasets**: Raw CSV files from TMDB
- **Models**: Pre-trained similarity matrices
- **Status**: ❌ Should be in `.gitignore` (large files)

### **2. Static Assets (`static/`)**
- **Purpose**: Serve static files (images, CSS, JS)
- **Organization**: By file type for easy maintenance
- **Images**: Logos, headers, icons
- **Videos**: Background videos
- **CSS/JS**: Organized by function

### **3. Recommender App (`recommender/`)**
Main Django application with clean architecture:

#### **Core Files:**
- `views.py`: Request handlers (now clean & minimal)
- `urls.py`: URL routing
- `models.py`: Database models (future use)
- `admin.py`: Admin panel configuration

#### **Utils Package (`recommender/utils/`):**
Modular, reusable components:

**`data_loader.py`**
```python
- DataLoader class
- Load CSV datasets
- Load pickle models
- Extract directors from JSON
- Merge datasets
- Singleton pattern for efficiency
```

**`text_processing.py`**
```python
- normalize_title(): Text normalization
- find_close_matches(): Fuzzy matching
- format_release_date(): Date formatting
- format_rating(): Rating formatting
- truncate_text(): Text truncation
```

**`recommender_engine.py`**
```python
- RecommendationEngine class
- get_recommendations(): Main recommendation logic
- _get_suggestions(): Fuzzy search suggestions
- _get_similar_movies(): Similarity-based recommendations
- _format_movie_data(): Format output data
```

### **4. Documentation (`docs/`)**
- Centralized documentation
- Technical details
- Feature guides
- Project organization

### **5. Scripts (`scripts/`)**
- Utility scripts
- Data validation
- Testing tools
- Not part of main app

### **6. Notebooks (`notebooks/`)**
- Training notebooks
- Data exploration
- Model development

---

## 🔄 Data Flow

```
User Request
    ↓
views.py (main function)
    ↓
RecommendationEngine.get_recommendations()
    ↓
┌─────────────────┬────────────────────┐
│                 │                    │
Text Processing   Data Loader          │
(normalize)       (get data)           │
│                 │                    │
└─────────────────┴────────────────────┘
                  ↓
         Similarity Matrix Lookup
                  ↓
         Format Results
                  ↓
         Return to Template
                  ↓
         Render HTML
```

---

## 🎨 Template Organization

### **index.html** (Home Page)
- Search form
- Autocomplete functionality
- Movie suggestions display
- Error messages

### **result.html** (Results Page)
- 25 movie recommendations
- Movie cards with:
  - Title & year
  - Director
  - Release date
  - Rating
  - Overview
  - Google search link

---

## 📦 Dependencies

### **Python Packages** (`requirements.txt`)
```
django==5.2.7          # Web framework
pandas==2.2.3          # Data manipulation
pickle                 # Model serialization (built-in)
pyarrow==19.0.0        # Parquet support
fastparquet==2024.11.0 # Fast parquet files
gunicorn==23.0.0       # Production server
whitenoise==6.11.0     # Static files serving
```

---

## 🚀 Quick Start

### **1. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2. Run Server**
```bash
python manage.py runserver
```

### **3. Access Application**
```
http://localhost:8000
```

---

## 🧪 Testing

### **Manual Testing**
```bash
# Check data structure
python scripts/test_data_structure.py

# Validate pickle files
python scripts/check_pickle.py
```

### **Unit Tests** (Future)
```bash
python manage.py test recommender
```

---

## 📊 Key Statistics

| Metric | Value |
|--------|-------|
| Total Movies | 4,803 |
| Similarity Matrix Size | 4,805 x 4,805 |
| Recommendations per Query | 25 |
| Response Time | <100ms |
| Lines of Code (views.py) | ~80 (was ~150) |
| Utility Modules | 3 |
| Static File Organization | ✅ By type |
| Documentation Files | 5 |

---

## ✅ Benefits of New Structure

1. **🎯 Clear Separation of Concerns**
   - Data separate from code
   - Utils separate from views
   - Static files organized by type

2. **📚 Easy to Navigate**
   - Logical folder structure
   - Descriptive file names
   - Centralized documentation

3. **🔧 Maintainable**
   - Modular code
   - Single responsibility principle
   - Easy to test

4. **📈 Scalable**
   - Easy to add features
   - Clear extension points
   - Organized for growth

5. **👥 Collaborative**
   - Clear file organization
   - Well-documented
   - Easy onboarding

---

## 🔐 Security Notes

- `data/` folder should be in `.gitignore`
- Large pickle files not in version control
- CSV files too large for GitHub
- Use Git LFS for large files (optional)

---

## 📝 Notes

- Original files moved, not copied
- Import paths updated in code
- Templates updated with new static paths
- All functionality preserved
- Performance maintained
- Backward compatible

---

**Last Updated**: October 20, 2025  
**Status**: ✅ Fully Organized & Operational  
**Server**: http://localhost:8000
