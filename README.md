# Multi-Domain Intelligence Platform

A Streamlit-based web application that unifies **Cybersecurity**, **Data Science**, and **IT Operations** insights into a single platform, powered by Google's Gemini AI.

## Features

### Core Functionality
- **User Authentication** — Secure login/registration with bcrypt password hashing
- **Role-based Access** — Protected dashboards requiring authentication
- **Session Management** — Persistent login state across pages

### Cybersecurity Dashboard
- Real-time metrics (total incidents, open incidents, critical/high severity count)
- Full CRUD operations for security incidents
- Interactive visualizations (incidents by category, severity, and status)
- AI Assistant for security recommendations

### Data Science Dashboard
- Key metrics (total datasets, total rows, average rows per dataset)
- Full CRUD operations for dataset metadata
- Visualizations (column/row distribution, datasets by uploader)
- AI Assistant for data governance recommendations

### IT Operations Dashboard
- Performance metrics (total tickets, open tickets, avg resolution time)
- Full CRUD operations for support tickets
- Visual analytics (status/priority distribution, resolution by assignee)
- Performance analysis (fastest/slowest assignees)
- AI Assistant for operational improvements

### AI Integration
- Context-aware AI assistant embedded in each dashboard
- Domain-specific recommendations powered by Google Gemini
- Automatic data context injection for relevant insights

## Installation

1. Clone or download this repository

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Set up your Gemini API key for AI features:
   ```bash
   export GEMINI_API_KEY="your-api-key-here"
   ```
   Or add to `.streamlit/secrets.toml`:
   ```toml
   gemini_api_key = "your-api-key-here"
   ```

## Usage

1. Initialize the database with sample data:
   ```bash
   python -m scripts.init_db
   ```

2. Run the Streamlit application:
   ```bash
   streamlit run Home.py
   ```

3. Open your browser to the URL shown (typically http://localhost:8501)

4. Login with the default admin credentials:
   - Username: `admin`
   - Password: `adminpass`

## Project Structure

```
CST1510CW2/
├── Home.py                     # Main entry point
├── pages/                      # Streamlit pages
│   ├── 1_Login.py              # Authentication page
│   ├── 2_Cybersecurity.py      # Security incidents dashboard
│   ├── 3_Data_Science.py       # Dataset governance dashboard
│   └── 4_IT_Operations.py      # IT tickets dashboard
├── services/                   # Business logic layer
│   ├── ai_assistant.py         # Gemini AI integration
│   ├── auth_manager.py         # Authentication service
│   ├── database_manager.py     # Database access layer
│   ├── dataset_service.py      # Dataset CRUD operations
│   ├── it_service.py           # IT ticket CRUD operations
│   └── security_service.py     # Incident CRUD operations
├── models/                     # Data model classes
│   ├── user.py                 # User entity
│   ├── security_incident.py    # Incident entity
│   ├── dataset.py              # Dataset metadata entity
│   └── it_ticket.py            # IT ticket entity
├── components/                 # Shared UI components
│   └── auth.py                 # Authentication helpers
├── database/                   # SQLite database
│   ├── db.py                   # Connection management
│   └── platform.db             # Database file
├── data/                       # Sample CSV data
│   ├── cyber_incidents.csv
│   ├── datasets_metadata.csv
│   └── it_tickets.csv
├── scripts/                    # Utility scripts
│   └── init_db.py              # Database initialization
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Architecture

### Data Flow
1. **Pages** (`pages/`) — Streamlit UI components
2. **Services** (`services/`) — Business logic and data access
3. **Database** (`database/`) — SQLite storage with Row factory
4. **Models** (`models/`) — Entity classes (optional, for type hints)

### Authentication Flow
1. User submits credentials on Login page
2. AuthManager verifies password using bcrypt
3. User data stored in `st.session_state.current_user`
4. Protected pages check authentication via `require_auth()`

### AI Integration
1. User enters question in AI Assistant section
2. Current data context is automatically injected
3. Prompt sent to Gemini API via AIAssistant service
4. Response displayed in the dashboard

## Key Capabilities

### Data Management
- **Create** — Add new records through intuitive forms
- **Read** — View data in interactive tables
- **Update** — Edit existing records with pre-populated forms
- **Delete** — Remove records with confirmation

### Analytics & Visualization
- Real-time metrics dashboards
- Interactive Plotly charts (pie charts, bar charts)
- Performance analysis and trend identification

### Security
- Passwords hashed with bcrypt (automatic salt generation)
- Protected routes require authentication
- Session-based access control

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | ≥1.28.0 | Web application framework |
| pandas | ≥2.0.0 | Data manipulation |
| plotly | ≥5.15.0 | Interactive visualizations |
| bcrypt | ≥4.0.0 | Password hashing |
| google-genai | ≥0.1.0 | Gemini AI SDK (optional) |

## Notes

- The AI Assistant requires a valid Gemini API key to function
- Without an API key, the app displays guidance on enabling AI features
- Database is SQLite-based, stored in `database/platform.db`
- Sample data can be loaded from CSV files in `data/` directory
- Default model: `gemini-2.5-flash` with 2048 max output tokens
