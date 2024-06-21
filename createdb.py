import sqlite3

connection = sqlite3.connect('database.db')

with connection:
    # Drop tables if they exist
    connection.execute("DROP TABLE IF EXISTS APPLICANT_TABLE")
    connection.execute("DROP TABLE IF EXISTS EMPLOYMENT_TABLE")
    connection.execute("DROP TABLE IF EXISTS EDUCATION_TABLE")
    connection.execute("DROP TABLE IF EXISTS WORK_EXPERIENCE_TABLE")
    connection.execute("DROP TABLE IF EXISTS GENERAL_TABLE")

    # Create APPLICANT_TABLE ////// CRIMINAL_CONVICTION_STATUS = true/false NOT NULL
    connection.execute("""
        CREATE TABLE APPLICANT_TABLE (
            sss_number TEXT PRIMARY KEY,
            given_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            middle_initial TEXT,
            suffix TEXT,
            birth_date DATE NOT NULL,
            address TEXT NOT NULL,
            city TEXT NOT NULL,
            state TEXT NOT NULL,
            zip_code TEXT NOT NULL,
            phone_1 TEXT NOT NULL,
            phone_2 TEXT,
            email TEXT NOT NULL,
            criminal_conviction_status BOOOLEAN NOT NULL,
            reason_for_conviction TEXT
        );
    """)

    # Create EMPLOYMENT_TABLE    
    connection.execute("""
        CREATE TABLE EMPLOYMENT_TABLE (
            employment_info_key INTEGER PRIMARY KEY AUTOINCREMENT,
            employment_type TEXT NOT NULL,
            position_applying_for TEXT NOT NULL,
            desired_salary REAL NOT NULL,
            start_date DATE NOT NULL
        );
    """)

    # Create EDUCATION_TABLE
    connection.execute("""
        CREATE TABLE EDUCATION_TABLE (
            education_key INTEGER PRIMARY KEY AUTOINCREMENT,
            sss_number TEXT NOT NULL,
            school TEXT NOT NULL,
            location TEXT NOT NULL,
            date_graduated DATE NOT NULL,
            attainment TEXT NOT NULL,
            FOREIGN KEY (sss_number) REFERENCES APPLICANT_TABLE (sss_number)
        );
    """)

    # Create WORK_EXPERIENCE_TABLE
    connection.execute("""
        CREATE TABLE WORK_EXPERIENCE_TABLE (
            work_experience_key INTEGER PRIMARY KEY AUTOINCREMENT,
            sss_number TEXT NOT NULL,
            company_name TEXT NOT NULL,
            period_start DATE NOT NULL,
            period_end DATE NOT NULL,
            position TEXT NOT NULL,
            reason_for_leaving TEXT NOT NULL,
            contact_present_employer BOOLEAN NOT NULL,
            why_not_contact TEXT,
            name_of_supervisor TEXT,
            supervisor_contact TEXT,
            FOREIGN KEY (sss_number) REFERENCES APPLICANT_TABLE (sss_number)
        );
    """)

    # Create GENERAL_TABLE //// SIGNATURE(BLOB)
    connection.execute("""
        CREATE TABLE GENERAL_TABLE (
            sss_number TEXT NOT NULL,
            employment_info_key INTEGER NOT NULL,
            major_skills TEXT NOT NULL,
            date_of_application_submission DATE NOT NULL,
            signature BLOB NOT NULL, 
            PRIMARY KEY (sss_number, employment_info_key),
            FOREIGN KEY (sss_number) REFERENCES APPLICANT_TABLE (sss_number),
            FOREIGN KEY (employment_info_key) REFERENCES EMPLOYMENT_TABLE (employment_info_key)
        );
    """)

print("Database initialized!")
