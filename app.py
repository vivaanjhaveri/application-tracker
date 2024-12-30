import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from database import create_connection

# Initialize the database connection
conn = create_connection()
cursor = conn.cursor()

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

# Streamlit App
def main():
    st.set_page_config(page_title="Job Application Tracker", layout="wide")
    st.title("📊 Job Application Tracking System")

    # Inject custom CSS to hide the blinking cursor
    hide_cursor_style = """
        <style>
        input, textarea {
            caret-color: transparent !important;
        }
        </style>
    """
    st.markdown(hide_cursor_style, unsafe_allow_html=True)

    menu = ["Add Application", "Update Application", "View Applications", "Visualize Progress"]
    choice = st.sidebar.button("Navigation", menu)

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

    elif choice == "View Applications":
        st.subheader("All Job Applications")
        applications_df = get_all_applications()
        if not applications_df.empty:
            st.dataframe(applications_df.drop(columns=['id']))
        else:
            st.info("No applications found. Please add some applications first.")

    elif choice == "Visualize Progress":
        st.subheader("Application Progress Visualization")
        applications_df = get_all_applications()

        if not applications_df.empty:
            # Convert application_date to datetime
            applications_df['application_date'] = pd.to_datetime(applications_df['application_date'])

            # Create columns for layout
            col1, col2 = st.columns(2)

            with col1:
                # Status Count Plot
                st.write("#### Applications by Status")
                status_count = applications_df['status'].value_counts().reset_index()
                status_count.columns = ['Status', 'Count']
                fig1, ax1 = plt.subplots()
                sns.barplot(x='Status', y='Count', data=status_count, ax=ax1, palette='Blues_d')
                ax1.set_xlabel("Status")
                ax1.set_ylabel("Count")
                st.pyplot(fig1)

            with col2:
                # Applications Over Time
                st.write("#### Applications Over Time")
                applications_over_time = applications_df.groupby('application_date').size().reset_index(name='Counts')
                fig2, ax2 = plt.subplots()
                sns.lineplot(x='application_date', y='Counts', data=applications_over_time, marker="o", ax=ax2)
                ax2.set_xlabel("Application Date")
                ax2.set_ylabel("Number of Applications")
                plt.xticks(rotation=45)
                st.pyplot(fig2)

            # Applications by Company
            st.write("#### Applications by Company")
            company_count = applications_df['company_name'].value_counts().reset_index()
            company_count.columns = ['Company Name', 'Count']
            fig3, ax3 = plt.subplots()
            sns.barplot(y='Company Name', x='Count', data=company_count, ax=ax3, palette='viridis')
            ax3.set_xlabel("Count")
            ax3.set_ylabel("Company Name")
            st.pyplot(fig3)

        else:
            st.info("No applications found. Please add some applications first.")

if __name__ == '__main__':
    main()
