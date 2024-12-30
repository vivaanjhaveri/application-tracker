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

def add_application(company_name, position, application_date, status, notes):
    cursor.execute('''
    INSERT INTO applications (company_name, position, application_date, status, notes)
    VALUES (?, ?, ?, ?, ?)
    ''', (company_name, position, application_date, status, notes))
    conn.commit()

def update_application(app_id, status, notes):
    cursor.execute('''
    UPDATE applications
    SET status = ?, notes = ?
    WHERE id = ?
    ''', (status, notes, app_id))
    conn.commit()

def get_all_applications():
    cursor.execute('SELECT * FROM applications')
    data = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    return pd.DataFrame(data, columns=columns)

#########################
# View Applications (Stylized Table)
#########################

def view_applications_table(applications_df):
    """
    Display applications in a color-coded Pandas table with black text.
    """
    st.subheader("All Job Applications")

    # Drop the 'id' column if it exists
    if 'id' in applications_df.columns:
        applications_df = applications_df.drop(columns=['id'])

    # Convert application_date to datetime and sort descending if applicable
    if 'application_date' in applications_df.columns:
        applications_df['application_date'] = pd.to_datetime(applications_df['application_date'], errors='coerce')
        applications_df = applications_df.sort_values(by="application_date", ascending=False)

    # Define background colors for each status
    def highlight_status(row):
        status = str(row['status'])
        if status == 'Rejected':
            return ['background-color: #f8d7da; color: black'] * len(row)
        elif status == 'Offered':
            return ['background-color: #d4edda; color: black'] * len(row)
        elif status == 'Interviewed':
            return ['background-color: #fff3cd; color: black'] * len(row)
        elif status == 'Applied':
            return ['background-color: #dbeafe; color: black'] * len(row)
        else:
            # Default: Keep black text, no special bg color
            return ['color: black'] * len(row)

    styled_df = applications_df.style.apply(highlight_status, axis=1)
    # Force text color to black overall (in case columns not covered by highlight_status)
    styled_df = styled_df.set_properties(**{'color': 'black'})

    st.write(styled_df)

#########################
# Visualize Progress
#########################

def visualize_progress_interactive(applications_df):
    """
    Show interactive charts (pie/line) using Plotly, plus summary statistics.
    """
    st.subheader("Application Progress Visualization")

    # Ensure 'application_date' is datetime
    applications_df['application_date'] = pd.to_datetime(applications_df['application_date'])

    # 1. Display Summary Statistics
    st.write("### Key Statistics")

    total_applications = len(applications_df)

    # Count how many times each status appears
    status_counts = applications_df['status'].value_counts()
    rejected_count = status_counts.get('Rejected', 0)
    interviewed_count = status_counts.get('Interviewed', 0)
    offered_count = status_counts.get('Offered', 0)
    applied_count = status_counts.get('Applied', 0)

    # Example additional stats:
    # - Count by position or company
    top_company = applications_df['company_name'].value_counts().idxmax() if not applications_df.empty else "N/A"
    top_position = applications_df['position'].value_counts().idxmax() if not applications_df.empty else "N/A"

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("Total Applications", total_applications)
    col2.metric("Rejected", rejected_count)
    col3.metric("Interviewed", interviewed_count)
    col4.metric("Offered", offered_count)
    col5.metric("Applied", applied_count)
    col6.metric("Most Common Company", top_company)

    st.write(f"Most Common Position: **{top_position}**")

    st.write("---")

    # 2. Pie Chart: Applications by Status
    st.write("### Applications by Status (Pie Chart)")
    status_count_df = status_counts.reset_index()
    status_count_df.columns = ['Status', 'Count']

    fig_status = px.pie(
        status_count_df,
        names='Status',
        values='Count',
        title="Distribution of Applications by Status",
        template='plotly_white'
    )
    fig_status.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_status, use_container_width=True)

    st.write("---")

    # 3. Line Chart: Applications Over Time
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

    # 4. Pie Chart: Applications by Company
    st.write("### Applications by Company (Pie Chart)")
    company_counts = applications_df['company_name'].value_counts().reset_index()
    company_counts.columns = ['Company Name', 'Count']

    fig_company = px.pie(
        company_counts,
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

    # Optional: Hide blinking cursor
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

    elif choice == "Update Application":
        st.subheader("Update Existing Application")
        applications_df = get_all_applications()

        if not applications_df.empty:
            # User-friendly dropdown
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

    elif choice == "View Applications":
        applications_df = get_all_applications()
        if not applications_df.empty:
            view_applications_table(applications_df)
        else:
            st.info("No applications found. Please add some applications first.")

    elif choice == "Visualize Progress":
        applications_df = get_all_applications()
        if not applications_df.empty:
            visualize_progress_interactive(applications_df)
        else:
            st.info("No applications found. Please add some applications first.")

if __name__ == '__main__':
    main()