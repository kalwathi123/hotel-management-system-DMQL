# Hotel Management System Database Project

## Overview
This project aims to develop a database system to streamline and optimize hotel management operations. The system addresses key challenges such as centralizing booking management, maintaining guest profiles, optimizing room inventory, managing partner relationships, and enabling data-driven decision making through reporting and analytics.

Live website: https://hotel-management-system-dmql-vmb5gaj9ulnbhmnetrh9yh.streamlit.app/

## Dataset
The project utilizes the "Hotel Booking Demand" dataset from Kaggle. The dataset was preprocessed using Python and Excel to handle null values and add custom price and city columns.

## Database Design
The database schema was designed and normalized to Boyce-Codd Normal Form (BCNF) to eliminate redundancy and anomalies. The key tables in the schema include:
- HotelDetails
- CustomerDetails
- RoomDetails
- ReservationDetails
- BookingDetails
- AgentDetails

Indexing was implemented on foreign key columns to optimize query performance for complex analytics queries involving joins and aggregations.

## Cloud Implementation
The database is hosted on an Amazon Web Services (AWS) RDS PostgreSQL instance. The website interface is hosted on Streamlit Community Cloud.

## Website Features
The project website showcases the hotel management system and includes the following pages:
- Home: Introduces the system's capabilities
- About: Details the project's goals and challenges addressed
- Analytics: Presents insights such as top performing agents and average lead time by customer market segment

## Repository Structure
- `sql/`: Contains SQL scripts for creating the database schema and queries
- `preprocessing/`: Includes Python and Excel files used for data preprocessing
- `website/`: Holds the Streamlit website code and assets
- `images/`: Contains relevant images and screenshots

## Setup and Usage
1. Clone the repository
2. Set up an AWS RDS PostgreSQL instance and configure the connection details
3. Execute the SQL scripts in the `sql/` directory to create the database schema
4. Preprocess the dataset using the scripts in the `preprocessing/` directory
5. Load the preprocessed data into the database
6. Configure the Streamlit app in the `website/` directory to connect to your RDS instance
7. Run the Streamlit app to launch the website

## Contributors
- Venkata Sai Sunil Bhattar Paruchuri
- Pavan Kalyan Reddy Bodugu
- Mohammed Abdul Rahman Kalwathi Jahir Hussain

Feel free to explore the repository and website to learn more about our hotel management database system!
