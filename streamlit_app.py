import streamlit as st
import pandas as pd
import psycopg2
import altair as alt
import plotly.express as px

# Database connection details
DB_HOST = "hotel-management-system.c9q8ye2ssfol.us-east-2.rds.amazonaws.com"
DB_NAME = "Hotel_Management"
DB_USER = "postgres"
DB_PASSWORD = "iDNI6m0mtvai6FQRncAg"

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def fetch_table_columns(conn, table_name):
    cur = conn.cursor()
    cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")
    columns = [column[0] for column in cur.fetchall()]
    cur.close()
    # conn.close()
    return columns

def execute_query(conn, query):
    cur = conn.cursor()
    cur.execute(query)
    columns = [desc[0] for desc in cur.description]
    data = cur.fetchall()
    cur.close()
    # conn.close()
    return columns, data

def main():
    # Getting the connection
    connection = get_connection()
    # Set page configuration
    st.set_page_config(
        page_title="Hospitality Management System",
        page_icon=":hotel:",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Add custom CSS styling
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg, #1f1f1f, #2c2c2c);
            animation: gradient-animation 10s ease infinite;
        }
        @keyframes gradient-animation {
            0% {
                background-position: 0% 50%;
            }
            50% {
                background-position: 100% 50%;
            }
            100% {
                background-position: 0% 50%;
            }
        }
        .header {
            font-size: 48px;
            color: #ffffff;
            text-align: center;
            margin-bottom: 2rem;
            padding: 2rem;
            background-color: rgba(0, 0, 0, 0.6);
            border-radius: 1rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            animation: header-animation 1s ease-in-out;
        }
        @keyframes header-animation {
            0% {
                transform: translateY(-50px);
                opacity: 0;
            }
            100% {
                transform: translateY(0);
                opacity: 1;
            }
        }
        .subheader {
            font-size: 36px;
            color: #ffffff;
            margin-bottom: 1rem;
            animation: subheader-animation 1s ease-in-out;
        }
        @keyframes subheader-animation {
            0% {
                transform: translateX(-50px);
                opacity: 0;
            }
            100% {
                transform: translateX(0);
                opacity: 1;
            }
        }
        .tile {
            background-color: rgba(0, 0, 0, 0.6);
            border-radius: 1rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            animation: tile-animation 1s ease-in-out;
        }
        @keyframes tile-animation {
            0% {
                transform: scale(0.8);
                opacity: 0;
            }
            100% {
                transform: scale(1);
                opacity: 1;
            }
        }
        .tile-title {
            font-size: 24px;
            color: #ffffff;
            margin-bottom: 0.5rem;
            text-align: center;
        }
        .tile-description {
            font-size: 18px;
            color: #ffffff;
            line-height: 1.6;
        }
        .problem-statement {
            font-size: 24px;
            color: #ffffff;
            text-align: center;
            margin-bottom: 2rem;
            font-weight: bold;
        }
        .solution {
            font-size: 18px;
            color: #ffffff;
            line-height: 1.6;
            margin-bottom: 1.5rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # App title and description
    st.markdown('<div class="header">Hospitality Management System</div>', unsafe_allow_html=True)
    st.write("Welcome to the Hospitality Management System, your one-stop solution for optimizing hotel operations and maximizing revenue.")

    # Sidebar menu
    menu = ["Home", "Analytics", "About"]
    choice = st.sidebar.selectbox("Select a page", menu)

    if choice == "Home":
        st.markdown('<div class="subheader">Streamline Your Hotel Operations</div>', unsafe_allow_html=True)

        tiles = [
            {
                "title": "Efficiently handle booking management",
                "description": "Centralize all booking-related data in one place, allowing hotel staff to efficiently track reservations, monitor room availability, and manage bookings in real-time."
            },
            {
                "title": "Provide personalized guest experiences",
                "description": "Maintain comprehensive guest profiles, monitor guest preferences, and deliver personalized experiences based on historical data and preferences stored within the database."
            },
            {
                "title": "Optimize room inventory and pricing",
                "description": "Get real-time visibility into room inventory, manage room allocations, adjust pricing dynamically, and optimize room availability to maximize revenue and occupancy rates."
            },
            {
                "title": "Streamline partner and agent relationships",
                "description": "Manage relationships with booking agents and partners more effectively by maintaining detailed records of agreements, commissions, and transactions."
            },
            {
                "title": "Make data-driven decisions",
                "description": "Access robust reporting and analytics capabilities, track key performance metrics, identify trends, and make data-driven decisions to improve operational efficiency and guest satisfaction."
            }
        ]

        for tile in tiles:
            st.markdown(f'<div class="tile"><div class="tile-title">{tile["title"]}</div><div class="tile-description">{tile["description"]}</div></div>', unsafe_allow_html=True)

        st.write("Explore the power of our system and take your hotel management to the next level!")

    elif choice == "Analytics":
        st.markdown('<div class="subheader">Analytics</div>', unsafe_allow_html=True)

        # Sidebar for analytical queries
        analytical_queries = [
            "Top Performing Agents",
        "Total Bookings by Month",
        "High Performing Hotel by number of bookings",
        "Average Lead Time by Customer Market Segment",
        "Average Booking Price for airport hotel and their Agent",
        "Average Booking Durations by Room Type",
        "Total Bookings by Country"
        ]
        selected_query = st.sidebar.selectbox("Select an analytical query", analytical_queries)

        if selected_query == "Top Performing Agents":
            query = """
            SELECT ad.agent_id, COUNT(bd.booking_id) AS total_bookings, SUM(bd.price) AS total_revenue
            FROM AgentDetails ad
            JOIN BookingDetails bd ON ad.agent_id = bd.agent_id
            GROUP BY ad.agent_id
            ORDER BY total_revenue DESC
            LIMIT 10
            """
            columns, result = execute_query(connection, query)
            df = pd.DataFrame(result, columns=columns)

            st.markdown('<div class="title">Top Performing Agents</div>', unsafe_allow_html=True)
            st.write("These are the top 10 agents based on total revenue generated:")
            st.table(df)

        elif selected_query == "Total Bookings by Month":
            query = """
            SELECT 
                arrival_date_month,
                COUNT(booking_id) AS total_bookings
            FROM BookingDetails
            GROUP BY arrival_date_month
            ORDER BY arrival_date_month
            """
            columns, result = execute_query(connection, query)
            df = pd.DataFrame(result, columns=columns)
            
            # Create a mapping of month names to integer values
            month_mapping = {
                'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
                'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
            }
            
            # Convert month names to integer values using the mapping
            df['month_number'] = df['arrival_date_month'].map(month_mapping)
            
            # Sort the DataFrame by month_number
            df = df.sort_values('month_number')
            
            st.markdown('<div class="title">Total Bookings by Month</div>', unsafe_allow_html=True)
            
            # Create an Altair chart
            chart = alt.Chart(df).mark_line(color='#1f77b4').encode(
                x=alt.X('arrival_date_month:N', title='Month', sort=None),
                y=alt.Y('total_bookings', title='Total Bookings'),
                tooltip=['arrival_date_month', 'total_bookings']
            ).properties(
                width=1800,
                height=700,
                title=alt.TitleParams(text='Total Bookings by Month', fontSize=24, anchor='middle')
            ).interactive()
            
            # Center align the chart
            col1, col2, col3 = st.columns([1, 3, 1])
            with col2:
                st.altair_chart(chart, use_container_width=True)

        elif selected_query == "High Performing Hotel by number of bookings":
            query = """
            SELECT 
    h.hotel_id, 
    h.hotel_type, 
    h.city, 
    COUNT(b.booking_id) AS total_bookings
FROM HotelDetails h
JOIN BookingDetails b ON h.hotel_id = b.hotel_id
GROUP BY h.hotel_id, h.hotel_type, h.city
ORDER BY total_bookings DESC limit 10;
            """
            columns, result = execute_query(connection, query)
            df = pd.DataFrame(result, columns=columns)

            st.markdown('<div class="title">High Performing Hotel by number of bookings</div>', unsafe_allow_html=True)
            st.write("This chart shows the revenue generated by each customer classification on a monthly basis:")
            font_size = 16
            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X('hotel_id:N', title='Hotel ID'),
                y=alt.Y('total_bookings', title='Total Bookings', axis=alt.Axis(labelFontSize=font_size)),
                tooltip=['hotel_id', 'total_bookings']
            ).properties(
                width=1400,
                height=600
            )
            chart = chart.properties(
                title=alt.TitleParams(text="Top 10 Performing Hotels by Number of Bookings", anchor='middle'),
                view=alt.ViewConfig(stroke='transparent')
            ).configure_axisY(labelAlign='center')

            st.altair_chart(chart)


        elif selected_query == "Average Lead Time by Customer Market Segment":
            query = """
            SELECT
                cd.customer_classification,
                AVG(bd.lead_time) AS average_lead_time
            FROM
                BookingDetails bd
            JOIN
                CustomerDetails cd ON bd.customer_id = cd.customer_id
            GROUP BY
                cd.customer_classification
            ORDER BY
                average_lead_time DESC
            """
            columns, result = execute_query(connection, query)
            df = pd.DataFrame(result, columns=columns)

            st.markdown('<div class="title">Average Lead Time by Customer Market Segment</div>', unsafe_allow_html=True)
            st.write("This spider chart shows the average lead time for each customer market segment, providing insights into booking behavior:")
            
            # Create a spider chart using plotly
            fig = px.line_polar(df, r='average_lead_time', theta='customer_classification', line_close=True)
            fig.update_layout(width=1200, height=700, margin=dict(l=50, r=50, t=50, b=50))

            # Show the spider chart
            st.plotly_chart(fig)


        elif selected_query == "Average Booking Price for airport hotel and their Agent":
            query = """
            SELECT
                hd.hotel_type,
                bd.agent_id,
                AVG(bd.price) AS average_price
            FROM
                BookingDetails bd
            JOIN
                HotelDetails hd ON bd.hotel_id = hd.hotel_id
            GROUP BY
                hd.hotel_type, bd.agent_id
            ORDER BY
                hd.hotel_type, average_price DESC
            LIMIT 100
            """
            columns, result = execute_query(connection, query)
            df = pd.DataFrame(result, columns=columns)

            st.markdown('<div class="title">Average Booking Price by Hotel Type and Agent</div>', unsafe_allow_html=True)
            st.write("This sunburst chart shows the average booking price for airport hotel combination of hotel type and agent:")
            
            # Create a sunburst chart using plotly
            fig = px.sunburst(df, path=['hotel_type', 'agent_id'], values='average_price')
            
            fig.update_layout(width=1200, height=700, margin=dict(l=50, r=50, t=50, b=50))

            # Show the sunburst chart
            st.plotly_chart(fig)


        elif selected_query == "Average Booking Durations by Room Type":
            query = """
            SELECT
                rd.room_type,
                AVG(bd.stays_in_weekend_nights + bd.stays_in_week_nights) AS average_stay_duration,
                SUM(bd.price) AS total_revenue
            FROM
                BookingDetails bd
            JOIN
                RoomDetails rd ON bd.room_id = rd.room_id
            GROUP BY
                rd.room_type
            ORDER BY
                total_revenue DESC
            LIMIT 100
            """
            columns, result = execute_query(connection, query)
            df = pd.DataFrame(result, columns=columns)

            st.markdown('<div class="title">Average Booking Durations by Room Type</div>', unsafe_allow_html=True)
            st.write("This trend chart shows the average booking duration and total revenue for each room type:")
            
            # Create a period chart using plotly
            fig = px.scatter(df, x='average_stay_duration', y='total_revenue', color='room_type',
                title='Average Booking Durations and Total Revenue by Room Type',
                labels={'average_stay_duration': 'Average Stay Duration', 'total_revenue': 'Total Revenue'})

            fig.update_layout(width=1200, height=700, margin=dict(l=50, r=50, t=50, b=50))

            
            # Show the period chart
            st.write(fig, unsafe_allow_html=True, style="text-align: center;")
            
        elif selected_query == "Total Bookings by Country":
            query = """
            SELECT HotelDetails.country, COUNT(*) AS total_bookings
            FROM BookingDetails
            JOIN HotelDetails ON BookingDetails.hotel_id = HotelDetails.hotel_id
            GROUP BY HotelDetails.country
            ORDER BY COUNT(*) DESC;
            """
            columns, result = execute_query(connection, query)
            df = pd.DataFrame(result, columns=columns)

            st.markdown('<div class="title">Total Bookings by Country</div>', unsafe_allow_html=True)
            st.write("This map shows the total bookings by country. Hover over each country to see the total bookings:")
            
            # Create a choropleth map using plotly
            fig = px.choropleth(df, 
                                locations='country', 
                                locationmode='country names', 
                                color='total_bookings', 
                                hover_name='country', 
                                color_continuous_scale=px.colors.sequential.Plasma,
                                title='Total Bookings by Country')
            
            # Show the map
            st.plotly_chart(fig)


            
    elif choice == "About":
        st.markdown('<div class="subheader">About</div>', unsafe_allow_html=True)
        # Display project content directly in the "About" page
        project_content = """
        <div class="problem-statement">PROBLEM STATEMENT</div>
        In the dynamic landscape of hotel management, optimizing operations and maximizing revenue hinges upon insightful analysis of various facets. Using our dataset, we aim to address some critical challenges by implementing advanced analytics techniques.
        <div class="solution">
        <strong>1. Booking Management:</strong> Hotels generally receive numerous booking requests from different channels, including online travel agencies, and booking agents. Manually managing these bookings or through disparate systems can cause inefficiencies, overbookings, and sometimes errors. The proposed database system will streamline booking management by centralizing all booking-related data in one place, allowing hotel staff to efficiently track reservations, monitor room availability, and manage bookings in real time.
        </div>
        <div class="solution">
        <strong>2. Guest Management:</strong> Hotels need to maintain accurate records of guest information, preferences, and booking history to provide personalized services and enhance guest satisfaction. Without a centralized database system, managing guest data can be challenging and prone to errors. The proposed system will enable hotel staff to maintain comprehensive guest profiles, monitor guest preferences, and deliver personalized experiences based on historical data and preferences stored within the database.
        </div>
        <div class="solution">
        <strong>3. Room Inventory Management:</strong> Effective room inventory management is crucial for hotels to maximize revenue and optimize occupancy rates. Tracking room availability, managing allocations, and adjusting pricing based on demand and seasonality are essential tasks. The proposed database system will provide hotel staff with real-time visibility into room inventory, allowing them to manage room allocations, adjust pricing dynamically, and optimize room availability to maximize revenue and occupancy rates.
        </div>
        <div class="solution">
        <strong>4. Agent and Partner Management:</strong> Many hotels work with booking agents, travel agencies, and distribution partners to attract guests and generate bookings. Managing relationships with these partners, tracking commissions, and ensuring timely payments can be complex without a centralized system. The proposed database system will enable hotels to manage relationships with booking agents and partners more effectively by maintaining detailed records of agreements, commissions, and transactions.
        </div>
        <div class="solution">
        <strong>5. Reporting and Analytics:</strong> Hotels require accurate and timely data for reporting, analysis, and decision-making. Without a centralized database system, compiling and analyzing data from multiple sources can be time-consuming and error-prone. The proposed system will provide hotel management with robust reporting and analytics capabilities, allowing them to track key performance metrics, identify trends, and make data-driven decisions to improve operational efficiency and guest satisfaction.
        </div>
        """
        st.markdown(project_content, unsafe_allow_html=True)

if __name__ == "__main__":
    main()