from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# LANDING PAGE
@app.route('/')
def index():
    return render_template('index.html')

# APPLICATION FORM PAGE
@app.route('/application-form', methods=('GET', 'POST'))
def application_form():
    
    if request.method == 'POST':
        #APPLICATION TABLE
        sss_number = request.form['sss_number']
        given_name = request.form['given_name']
        last_name = request.form['last_name']
        middle_initial = request.form['middle_initial']
        suffix = request.form['suffix']
        birth_date = request.form['birth_date']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip_code']
        phone_1 = request.form['phone_1']
        phone_2 = request.form['phone_2']
        email = request.form['email']
        criminal_conviction_status = 'criminal_conviction_status' in request.form
        if criminal_conviction_status:
            reason_for_conviction = request.form['reason_for_conviction']
        else:
            reason_for_conviction = None

        #EMPLOYMENT TABLE
        employment_type = request.form['employment_type']
        position_applying_for = request.form['position_applying_for']
        desired_salary = request.form['desired_salary']
        start_date = request.form['start_date']
        
        #EDUCATION
        school = request.form.getlist('school[]')
        location = request.form.getlist('location[]')
        date_graduated = request.form.getlist('date-graduated[]')
        attainment = request.form.getlist('attainment[]')

        #WORK EXPERIENCE
        company_name = request.form.getlist('company_name[]')
        period_start = request.form.getlist('period_start[]')
        period_end = request.form.getlist('period_end[]')
        position = request.form.getlist('position[]')
        reason_for_leaving = request.form.getlist('reason_for_leaving[]')

        # Handle the contact present employer checkbox and associated fields
        contact_present_employer = 'contact_present_employer' in request.form
        if contact_present_employer:
            name_of_supervisor = request.form['name_of_supervisor']
            supervisor_contact = request.form['supervisor_contact']
            why_not_contact = None  # No need to contact reason if checkbox is checked
        else:
            name_of_supervisor = None
            supervisor_contact = None
            why_not_contact = request.form['why_not_contact']

        #GENERAL TABLE
        major_skills = request.form['major_skills']
        date_of_application_submission = request.form['date_of_application_submission']
        signature = request.form['signature']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO APPLICANT_TABLE(
                     sss_number, 
                     given_name, 
                     last_name, 
                     middle_initial,
                     suffix, 
                     birth_date, 
                     address, 
                     city, state, 
                     zip_code, 
                     phone_1, 
                     phone_2, 
                     email, 
                     criminal_conviction_status, 
                     reason_for_conviction) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (sss_number, given_name, last_name, middle_initial, suffix, birth_date, address, city, state, zip_code, phone_1, phone_2, email, criminal_conviction_status, reason_for_conviction))

        cursor.execute("""
            INSERT INTO EMPLOYMENT_TABLE(
                     employment_type, 
                     position_applying_for, 
                     desired_salary, 
                     start_date) 
            VALUES (?, ?, ?, ?)
        """, (employment_type, position_applying_for, desired_salary, start_date))
        employment_info_key = cursor.lastrowid

        for i in range(len(school)):
            cursor.execute("""
                INSERT INTO EDUCATION_TABLE(
                         sss_number, 
                         school, 
                         location, 
                         date_graduated, 
                         attainment)
                VALUES (?,?,?,?,?)
                         """, (sss_number, school[i], location[i], date_graduated[i], attainment[i]))

        for i in range(len(company_name)):
          cursor.execute("""
                INSERT INTO WORK_EXPERIENCE_TABLE(
                    sss_number, company_name, period_start, period_end, position, reason_for_leaving,
                    contact_present_employer, why_not_contact, name_of_supervisor, supervisor_contact
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                sss_number, company_name[i], period_start[i], period_end[i], position[i], reason_for_leaving[i],
                contact_present_employer, why_not_contact, name_of_supervisor, supervisor_contact
            ))


        cursor.execute("""
            INSERT INTO GENERAL_TABLE(
                     sss_number,
                     employment_info_key,
                     major_skills,
                     date_of_application_submission,
                     signature)
            VALUES (?, ?, ?, ?, ?)
        """, (sss_number, employment_info_key, major_skills, date_of_application_submission, signature))
        
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template('applicationForm.html')

# VIEW DATABASE PAGE
@app.route('/view-database')
def view_database():
    # Get query parameters for sorting, searching, and filtering
    sort_by = request.args.getlist('sort_by[]') or ['last_name']
    sort_order = request.args.getlist('sort_order[]')
    categories = request.args.getlist('category[]')
    search_last_name = request.args.get('searchLastName', '')

    # Base query for fetching applicants
    query = '''
    SELECT * FROM APPLICANT_TABLE
    INNER JOIN GENERAL_TABLE ON APPLICANT_TABLE.sss_number = GENERAL_TABLE.sss_number
    INNER JOIN EMPLOYMENT_TABLE ON GENERAL_TABLE.employment_info_key = EMPLOYMENT_TABLE.employment_info_key
    '''
    query_params = []

    # Add search functionality
    if search_last_name:
        query += ' WHERE last_name LIKE ?'
        query_params.append('%' + search_last_name + '%')

    # Add category filtering functionality
    if categories:
        if 'WHERE' in query:
            query += ' AND'
        else:
            query += ' WHERE'
        category_conditions = []
        for category in categories:
            if category in ['Developer', 'Designer']:
                category_conditions.append(f"position_applying_for = ?")
                query_params.append(category)
            elif category == '1':
                category_conditions.append("criminal_conviction_status = 1")
            elif category == '0':
                category_conditions.append("criminal_conviction_status = 0")
        query += ' (' + ' OR '.join(category_conditions) + ')'

    # Add sorting functionality
    if sort_order:
        query += ' ORDER BY ' + ', '.join([f'{by} {order}' for by, order in zip(sort_by, sort_order)])

    conn = get_db_connection()
    cursor = conn.cursor()

    # Execute the query with or without the search parameter
    applicants = cursor.execute(query, query_params).fetchall()

    # Queries for fetching additional details
    education_query = '''
    SELECT * FROM EDUCATION_TABLE WHERE sss_number = ?;
    '''
    work_experience_query = '''
    SELECT * FROM WORK_EXPERIENCE_TABLE WHERE sss_number = ?;
    '''

    # Fetch education and work experience for each applicant
    for i, applicant in enumerate(applicants):
        applicant_dict = dict(applicant)
        sss_number = applicant_dict['sss_number']

        # Fetch education records
        education_records = cursor.execute(education_query, (sss_number,)).fetchall()
        education_records_dicts = [dict(record) for record in education_records]
        applicant_dict['education'] = education_records_dicts

        # Fetch work experience records
        work_experience_records = cursor.execute(work_experience_query, (sss_number,)).fetchall()
        work_experience_records_dicts = [dict(record) for record in work_experience_records]
        applicant_dict['work_experience'] = work_experience_records_dicts

        # Update the applicant dictionary in the list
        applicants[i] = applicant_dict

    conn.close()

    return render_template('viewDatabase.html', applicants=applicants, sort_by=sort_by, sort_order=sort_order, categories=categories)


# UPDATE
# @app.route('/update_form.html')
# def update():
#     return render_template('update_form.html')


# DELETE

if __name__ == '__main__':
    app.run(debug=True)
