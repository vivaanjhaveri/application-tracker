# Job Application Tracking System
### By Vivaan Jhaveri

A web application built with **Python** and **Streamlit** to manage and analyze job applications efficiently. This project leverages a **SQLite** database for persistent data storage, **Pandas** for data manipulation, and **Matplotlib**, **Seaborn**, and **Plotly** for rich visualizations. The user interface includes **color-coded tables** and **summary statistics**, providing a comprehensive overview of the job search process.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Key Components](#key-components)
  - [Database Schema](#database-schema)
  - [View Applications (Color-Coded Table)](#view-applications-color-coded-table)
  - [Visualize Progress (Summary Statistics & Interactive Charts)](#visualize-progress-summary-statistics--interactive-charts)
- [Future Improvements](#future-improvements)
- [Contact](#contact)

---

## Features

1. **Add & Update Applications**  
   - Forms for adding new job applications (company name, position, date, status, notes).
   - Update forms to modify the status and notes of existing applications.

2. **Color-Coded Table with Black Text**  
   - Easily distinguish between **Rejected**, **Offered**, **Interviewed**, and **Applied** statuses.
   - Each row is highlighted according to the application status for instant recognition.

3. **Summary Statistics**  
   - Displays key metrics like **total applications**, **rejections**, **interviews**, **offers**, and **most common company/position**.
   - Provides a high-level overview of the job search progress at a glance.

4. **Interactive Charts**  
   - **Pie charts** to visualize the distribution of applications by status and by company.
   - A **line chart** showing how many applications were submitted over time.
   - All visualizations have matching backgrounds to seamlessly blend with the Streamlit interface.

5. **Persistent Data Storage**  
   - A **SQLite** database stores all job application records.
   - Data remains available across sessions, ensuring no information is lost on application restarts.

6. **Custom UI Enhancements**  
   - Injected **custom CSS** to remove the blinking cursor in text fields.
   - Made several layout improvements, ensuring an **intuitive** user interface.

---

## Tech Stack

- **Python** (3.7+)
- **Streamlit** for the web application interface
- **SQLite** for database storage
- **Pandas** for data manipulation
- **Matplotlib**, **Seaborn**, **Plotly** for data visualization

---

## Installation

1. **Clone this repository**:
   ```bash
   git clone https://github.com/yourusername/job-application-tracker.git
   cd job-application-tracker
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

   Make sure your `requirements.txt` includes:
   ```
   streamlit
   pandas
   matplotlib
   seaborn
   plotly
   ```
   and any other dependencies (e.g., `sqlite3` is typically included with Python).

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```
   The application will open in your default web browser at [http://localhost:8501/](http://localhost:8501/).

---

## Usage

1. **Navigation**  
   - **Add Application**: Fill in the form with company name, position, date, status (Applied, Interviewed, Offered, Rejected), and notes.  
   - **Update Application**: Choose an existing application and modify its status or notes.
   - **View Applications**: Browse all applications in a **color-coded table**, where each row is styled based on status.  
   - **Visualize Progress**: Check summary statistics (e.g., total applications, rejections, interviews, offers) and interactive charts for a deeper look into your job search patterns.

2. **Data Persistence**  
   - All entries are saved to a **SQLite** database (`applications.db` by default).  
   - When the application restarts, previous records remain intact.

3. **User Interface Enhancements**  
   - **Custom CSS** hides the blinking cursor in text input fields.  
   - **Black text** in the table ensures readability, with background highlighting indicating each application’s status.

---

## Key Components

### Database Schema

The `applications` table includes:
- **id**: Primary key (integer, autoincrement)
- **company_name**: Name of the company
- **position**: Title of the job role
- **application_date**: Date the application was submitted
- **status**: Current status (Applied, Interviewed, Offered, Rejected)
- **notes**: Additional details

### View Applications (Color-Coded Table)

- Displays a **styled Pandas DataFrame** where each row is highlighted based on its status:
  - Applied (light blue), Interviewed (light yellow), Offered (light green), Rejected (light red).
- Text is **black** to ensure maximum readability.
- Allows quick scanning to identify the status of every application at a glance.

### Visualize Progress (Summary Statistics & Interactive Charts)

- **Summary Stats**:
  - **Total Applications**, **Rejected**, **Interviewed**, **Offered**, **Applied**, **Most Common Company**, **Most Common Position**.
  - Presented using `st.metric` and additional text.
- **Pie Charts**:
  - **Applications by Status**.
  - **Applications by Company**.
- **Line Chart**:
  - Trends over time for total applications submitted each day.

All charts are generated with **Plotly** and set to **transparent backgrounds**, blending seamlessly with Streamlit’s default theme.

---

## Future Improvements

- **Filtering & Sorting**: Add advanced filters (e.g., filter by date range or status) to quickly find specific applications.
- **Notifications & Reminders**: Integrate email or system notifications for upcoming interviews or follow-up reminders.
- **Success Rate Analysis**: Calculate more metrics, such as interview-to-offer conversion rates or time-to-hire.
- **Deployment**: Host the application on a cloud platform (e.g., Streamlit Cloud, Heroku) for remote access.
  
---

## Contact

For questions, suggestions, or feedback, please reach out to [vivaan.jhaveri@gmail.com](mailto:vivaan.jhaveri@gmail.com).

**Happy Tracking!**
