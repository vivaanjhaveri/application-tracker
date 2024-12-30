import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from database import create_connection

# Initialize the database connection
conn = create_connection()
cursor = conn.cursor()

#########################
# Database Functions
#########################

# Function to add a new application
def add_application(company_name, position, application_date, status, notes):
    cursor.execute('''
    INSERT INTO applications (company_name, position, application_date, status, notes)
    VALUES (?, ?, ?, ?, ?)
    ''', (company_name, position, application_date, status, notes))
    conn.commit()

# Function to update an existing application
def update_application(app_id, status, notes):
    cursor.execute('''
    UPDATE applications
    SET status = ?, notes = ?
    WHERE id = ?
    ''', (status, notes, app_id))
    conn.commit()

# Function to fetch all applications
def get_all_applications():
    cursor.execute('SELECT * FROM applications')
    data = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    return pd.DataFrame(data, columns=columns)

#########################
# Enhanced View Section
#########################

def view_applications_expanded(applications_df):
    """
    Display applications using Streamlit expanders for a more intuitive view.
    Each application is wrapped in an expander showing key details.
    """
    st.subheader("All Job Applications (Enhanced View)")
    # Sort by application_date (descending) to see recent applications first
    applications_df = applications_df.sort_values(by="application_date", ascending=False)

    for _, row in applications_df.iterrows():
        with st.expander(f"{row['company_name']} - {row['position']} ({row['status']})", expanded=False):
            st.write(f"**Application Date:** {row['application_date']}")
            st.write(f"**Notes:** {row['notes'] if row['notes'] else 'N/A'}")

#########################
# Interactive Visualization Section
#########################

def visualize_progress_interactive(applications_df):
    """
    Show interactive charts (pie, line) using Plotly, matching Streamlit's background.
    """

    # Ensure 'application_date' is a datetime
    applications_df['application_date'] = pd.to_datetime(applications_df['application_date'])

    st.subheader("Interactive Application Progress Visualization")

    # --- Pie Chart: Applications by Status ---
    st.write("### Applications by Status (Pie Chart)")
    status_count = applications_df['status'].value_counts().reset_index()
    status_count.columns = ['Status', 'Count']

    fig_status = px.pie(
        status_count,
        names='Status',
        values='Count',
        title="Distribution of Applications by Status",
        template='plotly_white'  # Use a clean template
    )
    # Match chart background with the page background
    fig_status.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_status, use_container_width=True)

    st.write("---")

    # --- Line Chart: Applications Over Time ---
    st.write("### Applications Over Time (Line Chart)")
    apps_over_time = applications_df.groupby('application_date').size().reset_index(name='Counts')
    fig_line = px.line(
        apps_over_time,
        x='application_date',
        y='Counts',
        markers=True,
        title="Number of Applications Submitted Over Time",
        template='plotly_white'
    )
    fig_line.update_layout(
        xaxis_title="Application Date",
        yaxis_title="Number of Applications",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_line, use_container_width=True)

    st.write("---")

    # --- Pie Chart: Applications by Company ---
    st.write("### Applications by Company (Pie Chart)")
    company_count = applications_df['company_name'].value_counts().reset_index()
    company_count.columns = ['Company Name', 'Count']

    fig_company = px.pie(
        company_count,
        names='Company Name',
        values='Count',
        title="Distribution of Applications by Company",
        template='plotly_white'
    )
    fig_company.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_company, use_container_width=True)

#########################
# Main Streamlit App
#########################

def main():
    st.set_page_config(page_title="Job Application Tracker", layout="wide")
    st.title("📊 Job Application Tracking System")

    # Inject custom CSS to hide the blinking cursor (optional)
    hide_cursor_style = """
        <style>
        input, textarea {
            caret-color: transparent !important;
        }
        </style>
    """
    st.markdown(hide_cursor_style, unsafe_allow_html=True)

    # Navigation Menu
    menu = ["Add Application", "Update Application", "View Applications", "Visualize Progress"]
    choice = st.sidebar.selectbox("Navigation", menu)

    # 1. Add Application
    if choice == "Add Application":
        st.subheader("Add New Job Application")

        with st.form(key='add_application_form'):
            company_name = st.text_input("Company Name")
            position = st.text_input("Position")
            application_date = st.date_input("Application Date")
            status = st.selectbox("Status", ["Applied", "Interviewed", "Offered", "Rejected"])
            notes = st.text_area("Notes")

            submit_button = st.form_submit_button(label='Add Application')

        if submit_button:
            if company_name and position:
                add_application(company_name, position, application_date.strftime('%Y-%m-%d'), status, notes)
                st.success(f"Application for **{position}** at **{company_name}** added successfully!")
            else:
                st.error("Please enter both Company Name and Position.")

    # 2. Update Application
    elif choice == "Update Application":
        st.subheader("Update Existing Application")
        applications_df = get_all_applications()

        if not applications_df.empty:
            # Create a user-friendly dropdown menu
            applications_df['display'] = applications_df.apply(
                lambda row: f"{row['company_name']} - {row['position']} [{row['status']}]",
                axis=1
            )
            application_list = applications_df['display'].tolist()
            selected_application = st.selectbox("Select Application", application_list)

            # Get the selected application details
            selected_index = application_list.index(selected_application)
            selected_app = applications_df.iloc[selected_index]
            app_id = selected_app['id']

            st.write("### Current Details")
            st.write(f"**Company Name:** {selected_app['company_name']}")
            st.write(f"**Position:** {selected_app['position']}")
            st.write(f"**Application Date:** {selected_app['application_date']}")
            st.write(f"**Current Status:** {selected_app['status']}")
            st.write(f"**Current Notes:** {selected_app['notes']}")

            st.write("---")
            st.write("### Update Details")

            with st.form(key='update_application_form'):
                new_status = st.selectbox(
                    "New Status",
                    ["Applied", "Interviewed", "Offered", "Rejected"],
                    index=["Applied", "Interviewed", "Offered", "Rejected"].index(selected_app['status'])
                )
                new_notes = st.text_area("New Notes", value=selected_app['notes'])
                update_button = st.form_submit_button(label='Update Application')

            if update_button:
                update_application(app_id, new_status, new_notes)
                st.success("Application updated successfully!")

        else:
            st.info("No applications found. Please add some applications first.")

    # 3. View Applications (Enhanced)
    elif choice == "View Applications":
        applications_df = get_all_applications()
        if not applications_df.empty:
            # Drop the 'id' column before display
            df_no_id = applications_df.drop(columns=['id'])
            view_applications_expanded(df_no_id)
        else:
            st.info("No applications found. Please add some applications first.")

    # 4. Visualize Progress (Interactive Charts)
    elif choice == "Visualize Progress":
        applications_df = get_all_applications()

        if not applications_df.empty:
            visualize_progress_interactive(applications_df)
        else:
            st.info("No applications found. Please add some applications first.")

if __name__ == '__main__':
    main()