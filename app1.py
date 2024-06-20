from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

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
        # #EMPLOYMENT TABLE
        employment_type = request.form['employment_type']
        position_applying_for = request.form['position_applying_for']
        desired_salary = request.form['desired_salary']
        start_date = request.form['start_date']
        
        #EDUCATION
        school = request.form.getlist('school[]')
        location = request.form.getlist('location[]')
        date_graduated = request.form.getlist('date-graduated[]')
        attainment = request.form.getlist('attainment[]')

        # #WORK EXPERIENCE
        # company_name = request.form.getlist('company_name[]')
        # period_start = request.form.getlist('period_start[]')
        # period_end = request.form.getlist('period_end')
        # position = request.form.getlist('position')
        # reason_for_leaving = request.form.getlist('reason_for_leaving')
        # contact_present_employer = request.form['contact_present_employer']
        # why_not_contact = request.form['why_not_contact']
        # name_of_supervisor = request.form['name_of_supervisor']
        # supervisor_contact = request.form['supervisor_contact']

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

        # for i in range(len(company_name)):
        #     cursor.execute("""
        #         INSERT INTO WORK_EXPERIENCE_TABLE(
        #                 sss_number, 
        #                 company_name, 
        #                 period_start, 
        #                 period_end, 
        #                 position, 
        #                 reason_for_leaving, 
        #                 contact_present_employer, 
        #                 why_not_contact, 
        #                 name_of_supervisor, 
        #                 supervisor_contact) 
        #         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        #     """, (sss_number, company_name[i], period_start[i], period_end[i], position[i], reason_for_leaving[i], contact_present_employer[i], why_not_contact[i], name_of_supervisor[i], supervisor_contact[i]))

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

@app.route('/view-database')
def view_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    applicants_query = '''
    SELECT * FROM APPLICANT_TABLE
    INNER JOIN GENERAL_TABLE ON APPLICANT_TABLE.sss_number = GENERAL_TABLE.sss_number
    INNER JOIN EMPLOYMENT_TABLE ON GENERAL_TABLE.employment_info_key = EMPLOYMENT_TABLE.employment_info_key;
    '''
    applicants = cursor.execute(applicants_query).fetchall()

    
    education_query = '''
    SELECT * FROM EDUCATION_TABLE WHERE sss_number = ?;
    '''
    
    for applicant in applicants:
    # Convert the sqlite3.Row object into a dictionary
        applicant_dict = dict(applicant)
        sss_number = applicant_dict['sss_number']
        education_records = cursor.execute(education_query, (sss_number,)).fetchall()
        
        education_records_dicts = [dict(record) for record in education_records]
        
        applicant_dict['education'] = education_records_dicts

        applicants[applicants.index(applicant)] = applicant_dict

    conn.close()
    
    return render_template('viewDatabase.html', applicants=applicants)


@app.route('/<string:sss_number>/update', methods=('GET', 'POST'))
def update(sss_number):
    conn = get_db_connection()
    applicant = conn.execute('SELECT * FROM APPLICANT_TABLE WHERE sss_number = ?', (sss_number,)).fetchone()

    if request.method == 'POST':
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
        criminal_conviction_status = request.form['criminal_conviction_status']
        reason_for_conviction = request.form['reason_for_conviction']

        conn.execute("""
            UPDATE APPLICANT_TABLE SET
                given_name = ?, last_name = ?, middle_initial = ?, suffix = ?,
                birth_date = ?, address = ?, city = ?, state = ?, zip_code = ?,
                phone_1 = ?, phone_2 = ?, email = ?, criminal_conviction_status = ?, reason_for_conviction = ?
            WHERE sss_number = ?
        """, (
            given_name, last_name, middle_initial, suffix, birth_date, address, city, state,
            zip_code, phone_1, phone_2, email, criminal_conviction_status, reason_for_conviction,
            sss_number
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('update.html', applicant=applicant)

@app.route('/<string:sss_number>/delete', methods=('POST',))
def delete(sss_number):
    conn = get_db_connection()
    conn.execute('DELETE FROM APPLICANT_TABLE WHERE sss_number = ?', (sss_number,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
