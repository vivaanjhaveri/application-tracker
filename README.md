### Job Application Tracking System
# By Vivaan Jhaveri

## Description
A web application designed to help co-op students and job seekers in STEM fields efficiently manage and track their job applications in Vancouver, Canada. This system provides an intuitive interface for adding and updating job applications, visualizing application progress through interactive charts, and analyzing application data for insights.

## Features
Add New Applications: Input details such as company name, position, application date, status, and notes.
Update Existing Applications: Modify the status and notes of applications as you progress through the hiring process.
View Applications: Display all your applications in a structured and readable format.
Visualize Progress: Interactive charts to track your application statuses, applications over time, and applications by company.
User-Friendly Interface: Clean and intuitive GUI built with Streamlit for easy navigation and use.

## Technologies Used
Python: Backend development and application logic.
Streamlit: Creation of the interactive web interface.
SQLite: Lightweight database for storing application data.
Pandas: Data manipulation and analysis.
Matplotlib & Seaborn: Data visualization for generating interactive charts.

## Navigate the Application

Add Application: Use this section to add new job applications by filling out the form with the company name, position, application date, status, and any notes.
Update Application: Update the status and notes of existing applications. Select an application from the dropdown menu, review current details, and submit updates.
View Applications: View all your job applications in a table format for easy reference.
Visualize Progress: Access interactive visualizations to analyze your application statuses, track applications over time, and see applications by company.

## Project Structure
app.py: Main application script containing the Streamlit app.
database.py: Handles database connections and operations.
applications.db: SQLite database file where application data is stored.
requirements.txt: List of required Python packages for the project.
README.md: This README file.

## Development Process
Planning and Requirements Gathering
Identified the need for an efficient system to track job applications.
Outlined core functionalities: data entry, status updates, data visualization, and analysis.

## Database Setup
Created a SQLite database to store application data securely.
Defined a schema including fields for company name, position, application date, status, and notes.
Building the Streamlit Application
Designed a user-friendly interface with a sidebar for navigation.
Implemented forms for adding and updating applications.
Developed functions to interact with the database.

## Enhancements and Bug Fixes
Improved the GUI layout for better user experience.
Replaced the application ID selection with a dropdown menu showing company name, position, and status.
Injected custom CSS to remove the blinking cursor from input fields.
Added validation checks and informative messages for better feedback.

## Visualizations
Applications by Status: Bar chart displaying the count of applications in each status category.
Applications Over Time: Line chart showing the number of applications submitted over time.
Applications by Company: Bar chart illustrating the number of applications per company.

## Challenges and Solutions
User-Friendly Selection: Users initially found it difficult to select applications by ID. Solved by displaying applications in a dropdown menu with meaningful details.
Blinking Cursor Distraction: Removed the blinking cursor using custom CSS to enhance focus.
Form Submission Issues: Implemented st.form and st.form_submit_button for proper form handling within Streamlit.
Empty Data Handling: Added checks to prevent errors when the database is empty and provided prompts to guide the user.

## Future Improvements
Additional Filters: Implement filters in the "View Applications" section to sort or search applications.
Notifications: Add functionality to set reminders for follow-ups on applications.
Data Export: Allow users to export their data to CSV or Excel for external analysis.
User Authentication: Implement authentication for multi-user support while ensuring data privacy.
Deployment: Deploy the application to a cloud platform for remote access.

Contact
For questions, suggestions, or feedback, please contact vivaan.jhaveri@gmail.com