import datetime
import random

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

# Show app title and description.
st.set_page_config(page_title="Support tickets", page_icon="🎫")
st.title("🎫 KGI  Support tickets")
st.write(
    """
    This app shows how you can build an internal tool in Streamlit. Here, we are 
    implementing a support ticket workflow. The user can create a ticket, edit 
    existing tickets, and view some statistics.
    """
)

# Create a random Pandas dataframe with existing tickets.
if "df" not in st.session_state:

    # Set seed for reproducibility.
    np.random.seed(42)

    # Make up some fake issue descriptions.
    issue_descriptions = [
        "Network connectivity issues in the office",
        "Software application crashing on startup",
        "Printer not responding to print commands",
        "Email server downtime",
        "Data backup failure",
        "Login authentication problems",
        "Website performance degradation",
        "Security vulnerability identified",
        "Hardware malfunction in the server room",
        "Employee unable to access shared files",
        "Database connection failure",
        "Mobile application not syncing data",
        "VoIP phone system issues",
        "VPN connection problems for remote employees",
        "System updates causing compatibility issues",
        "File server running out of storage space",
        "Intrusion detection system alerts",
        "Inventory management system errors",
        "Customer data not loading in CRM",
        "Collaboration tool not sending notifications",
    ]

    # Generate the dataframe with 100 rows/tickets.
    data = {
        "ID": [f"TICKET-{i}" for i in range(1100, 1000, -1)],
        "Issue": np.random.choice(issue_descriptions, size=100),
        "Status": np.random.choice(["Open", "In Progress", "Closed"], size=100),
        "Priority": np.random.choice(["High", "Medium", "Low"], size=100),
        "Date Submitted": [
            datetime.date(2023, 6, 1) + datetime.timedelta(days=random.randint(0, 182))
            for _ in range(100)
        ],
    }
    df = pd.DataFrame(data)

    # Save the dataframe in session state (a dictionary-like object that persists across
    # page runs). This ensures our data is persisted when the app updates.
    st.session_state.df = df


# Show a section to add a new ticket.
st.header("Add a ticket")

# We're adding tickets via an `st.form` and some input widgets. If widgets are used
# in a form, the app will only rerun once the submit button is pressed.
with st.form("add_ticket_form"):
    issue = st.text_area("Describe the issue")
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])
    submitted = st.form_submit_button("Submit")

if submitted:
    # Make a dataframe for the new ticket and append it to the dataframe in session
    # state.
    recent_ticket_number = int(max(st.session_state.df.ID).split("-")[1])
    today = datetime.datetime.now().strftime("%m-%d-%Y")
    df_new = pd.DataFrame(
        [
            {
                "ID": f"TICKET-{recent_ticket_number+1}",
                "Issue": issue,
                "Status": "Open",
                "Priority": priority,
                "Date Submitted": today,
            }
        ]
    )

    # Show a little success message.
    st.write("Ticket submitted! Here are the ticket details:")
    st.dataframe(df_new, use_container_width=True, hide_index=True)
    st.session_state.df = pd.concat([df_new, st.session_state.df], axis=0)

# Show section to view and edit existing tickets in a table.
st.header("KGI Tickets - Existing tickets")
st.write(f"Number of tickets: `{len(st.session_state.df)}`")

st.info(
    "You can edit the tickets by double clicking on a cell. Note how the plots below "
    "update automatically! You can also sort the table by clicking on the column headers.",
    icon="✍️",
)

# Show the tickets dataframe with `st.data_editor`. This lets the user edit the table
# cells. The edited data is returned as a new dataframe.
edited_df = st.data_editor(
    st.session_state.df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Status": st.column_config.SelectboxColumn(
            "Status",
            help="Ticket status",
            options=["Open", "In Progress", "Closed"],
            required=True,
        ),
        "Priority": st.column_config.SelectboxColumn(
            "Priority",
            help="Priority",
            options=["High", "Medium", "Low"],
            required=True,
        ),
    },
    # Disable editing the ID and Date Submitted columns.
    disabled=["ID", "Date Submitted"],
)

# Show some metrics and charts about the ticket.
st.header("Statistics")

# Show metrics side by side using `st.columns` and `st.metric`.
col1, col2, col3 = st.columns(3)
num_open_tickets = len(st.session_state.df[st.session_state.df.Status == "Open"])
col1.metric(label="Number of open tickets", value=num_open_tickets, delta=10)
col2.metric(label="First response time (hours)", value=5.2, delta=-1.5)
col3.metric(label="Average resolution time (hours)", value=16, delta=2)

# Show two Altair charts using `st.altair_chart`.
st.write("")
st.write("##### Ticket status per month")
status_plot = (
    alt.Chart(edited_df)
    .mark_bar()
    .encode(
        x="month(Date Submitted):O",
        y="count():Q",
        xOffset="Status:N",
        color="Status:N",
    )
    .configure_legend(
        orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
    )
)
st.altair_chart(status_plot, use_container_width=True, theme="streamlit")

st.write("##### Current ticket priorities")
priority_plot = (
    alt.Chart(edited_df)
    .mark_arc()
    .encode(theta="count():Q", color="Priority:N")
    .properties(height=300)
    .configure_legend(
        orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
    )
)
st.altair_chart(priority_plot, use_container_width=True, theme="streamlit")


import datetime
import random

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

# Set up the page title and description.
st.set_page_config(page_title="Support Tickets Dashboard", page_icon="🎫", layout="wide")
st.title("🎫 KGI Support Tickets Dashboard")
st.write(
    """
    This app demonstrates a comprehensive support ticket workflow management tool. 
    You can create, edit, and visualize tickets, as well as analyze performance metrics 
    with detailed insights.
    """
)

# Create a random Pandas dataframe with existing tickets if not already present in session.
if "df" not in st.session_state:

    # Set seed for reproducibility.
    np.random.seed(42)

    # Define some example issue descriptions.
    issue_descriptions = [
        "Network connectivity issues", "Application crashing", "Printer malfunction", 
        "Email server downtime", "Backup failure", "Login problems", "Website slowdown",
        "Security vulnerability", "Hardware malfunction", "Access issue with shared files",
        "Database connection issue", "App data not syncing", "VoIP phone issues", 
        "VPN problems for remote workers", "System update issues", "File server storage low",
        "Intrusion detection alerts", "Inventory system errors", "Customer data missing", 
        "Collaboration tool issue"
    ]

    # Generate a dataframe with 100 rows/tickets.
    data = {
        "ID": [f"TICKET-{i}" for i in range(1100, 1000, -1)],
        "Issue": np.random.choice(issue_descriptions, size=100),
        "Status": np.random.choice(["Open", "In Progress", "Closed"], size=100),
        "Priority": np.random.choice(["High", "Medium", "Low"], size=100),
        "Date Submitted": [
            datetime.date(2023, 6, 1) + datetime.timedelta(days=random.randint(0, 182))
            for _ in range(100)
        ],
        "Assigned To": np.random.choice(["John Doe", "Jane Smith", "Alex Brown", "Chris White"], size=100),
        "Response Time (hours)": np.random.randint(1, 12, size=100),
        "Resolution Time (hours)": np.random.randint(10, 72, size=100)
    }
    df = pd.DataFrame(data)

    # Save the dataframe in session state for persistence.
    st.session_state.df = df


# Section for adding new tickets.
st.header("📝 Add a new ticket")

with st.form("add_ticket_form"):
    issue = st.text_area("Describe the issue")
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])
    assigned_to = st.selectbox("Assign to", ["John Doe", "Jane Smith", "Alex Brown", "Chris White"])
    response_time = st.slider("Estimated first response time (hours)", 1, 12, 3)
    resolution_time = st.slider("Estimated resolution time (hours)", 12, 72, 24)
    submitted = st.form_submit_button("Submit")

if submitted:
    # Create a dataframe for the new ticket.
    recent_ticket_number = int(max(st.session_state.df.ID).split("-")[1])
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    df_new = pd.DataFrame(
        [
            {
                "ID": f"TICKET-{recent_ticket_number+1}",
                "Issue": issue,
                "Status": "Open",
                "Priority": priority,
                "Date Submitted": today,
                "Assigned To": assigned_to,
                "Response Time (hours)": response_time,
                "Resolution Time (hours)": resolution_time,
            }
        ]
    )

    # Update the session state dataframe.
    st.write("🎉 Ticket submitted successfully!")
    st.dataframe(df_new, use_container_width=True, hide_index=True)
    st.session_state.df = pd.concat([df_new, st.session_state.df], axis=0)


# Section to view and edit tickets.
st.header("🛠 Manage existing tickets")
st.write(f"Total tickets: `{len(st.session_state.df)}`")

# Add search and filter functionality.
with st.expander("🔍 Filter and Search Tickets"):
    status_filter = st.multiselect("Filter by status", options=["Open", "In Progress", "Closed"], default=["Open", "In Progress", "Closed"])
    priority_filter = st.multiselect("Filter by priority", options=["High", "Medium", "Low"], default=["High", "Medium", "Low"])
    assigned_filter = st.multiselect("Filter by assigned team member", options=["John Doe", "Jane Smith", "Alex Brown", "Chris White"], default=["John Doe", "Jane Smith", "Alex Brown", "Chris White"])
    search_query = st.text_input("Search by issue description")

# Apply filters.
filtered_df = st.session_state.df[
    (st.session_state.df["Status"].isin(status_filter)) &
    (st.session_state.df["Priority"].isin(priority_filter)) &
    (st.session_state.df["Assigned To"].isin(assigned_filter)) &
    (st.session_state.df["Issue"].str.contains(search_query, case=False))
]

# Display the tickets dataframe with `st.data_editor`.
edited_df = st.data_editor(
    filtered_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Status": st.column_config.SelectboxColumn(
            "Status",
            help="Ticket status",
            options=["Open", "In Progress", "Closed"],
            required=True,
        ),
        "Priority": st.column_config.SelectboxColumn(
            "Priority",
            help="Priority",
            options=["High", "Medium", "Low"],
            required=True,
        ),
    },
    disabled=["ID", "Date Submitted"],
)

# Display statistics and metrics.
st.header("📊 Performance Metrics")

# Show ticket-related metrics side by side.
col1, col2, col3 = st.columns(3)
num_open_tickets = len(st.session_state.df[st.session_state.df.Status == "Open"])
col1.metric(label="Open Tickets", value=num_open_tickets)
avg_response_time = st.session_state.df["Response Time (hours)"].mean()
col2.metric(label="Avg Response Time (hours)", value=f"{avg_response_time:.1f}")
avg_resolution_time = st.session_state.df["Resolution Time (hours)"].mean()
col3.metric(label="Avg Resolution Time (hours)", value=f"{avg_resolution_time:.1f}")

# Advanced visualizations.
st.write("#### Ticket Status Distribution")
status_plot = alt.Chart(st.session_state.df).mark_bar().encode(
    x="Status:N", y="count():Q", color="Status:N"
).properties(title="Number of Tickets by Status").configure_title(fontSize=18)
st.altair_chart(status_plot, use_container_width=True)

st.write("#### Tickets by Assigned Team Member")
assigned_plot = alt.Chart(st.session_state.df).mark_bar().encode(
    x="Assigned To:N", y="count():Q", color="Assigned To:N"
).properties(title="Number of Tickets per Team Member").configure_title(fontSize=18)
st.altair_chart(assigned_plot, use_container_width=True)

st.write("#### Ticket Resolution Time Distribution")
resolution_plot = alt.Chart(st.session_state.df).mark_boxplot().encode(
    x="Resolution Time (hours):Q"
).properties(title="Resolution Time Distribution").configure_title(fontSize=18)
st.altair_chart(resolution_plot, use_container_width=True)

# Option to download the ticket data.
st.header("📂 Export Data")
st.download_button(
    label="Download tickets data as CSV",
    data=st.session_state.df.to_csv(index=False).encode("utf-8"),
    file_name="support_tickets.csv",
    mime="text/csv",
)
