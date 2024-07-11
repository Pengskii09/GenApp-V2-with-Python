from flask import *
import sqlite3


app = Flask(__name__)

DATABASE = 'database.db'
app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
        sss_number = request.form['sss_number']
        
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Check if the SSS number already exists in the database
            existing = cursor.execute("SELECT 1 FROM APPLICANT_TABLE WHERE sss_number = ?", (sss_number,)).fetchone()
            if existing:
                flash('SSS number already exists in the database.', 'error')
                return redirect(url_for('application_form'))
            
            # APPLICATION TABLE
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

            # EMPLOYMENT TABLE
            employment_type = request.form['employment_type']
            position_applying_for = request.form['position_applying_for']
            years_of_experience = request.form['years_of_experience']
            desired_salary = request.form['desired_salary']
            start_date = request.form['start_date']
            
            # EDUCATION
            school = request.form.getlist('school[]')
            location = request.form.getlist('location[]')
            date_graduated = request.form.getlist('date-graduated[]')
            attainment = request.form.getlist('attainment[]')

            # WORK EXPERIENCE
            company_name = request.form.getlist('company_name[]')
            period_start = request.form.getlist('period_start[]')
            period_end = request.form.getlist('period_end[]')
            position = request.form.getlist('position[]')
            reason_for_leaving = request.form.getlist('reason_for_leaving[]')

            # Handle the contact present employer checkbox and associated fields
            contact_present_employer = 1 if 'contact_present_employer' in request.form else 0
            if contact_present_employer:
                name_of_supervisor = request.form['name_of_supervisor']
                supervisor_contact = request.form['supervisor_contact']
                why_not_contact = None  # No need to contact reason if checkbox is checked
            else:
                name_of_supervisor = None
                supervisor_contact = None
                why_not_contact = request.form['why_not_contact']

            # GENERAL TABLE
            major_skills = request.form['major_skills']
            date_of_application_submission = request.form['date_of_application_submission']
            if 'signature' not in request.files:
                flash('No file part', 'error')
                return redirect(request.url)
            file = request.files['signature']
            if file.filename == '':
                flash('No selected file', 'error')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                # Read the file contents
                file_content = file.read()

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
                            years_of_experience,
                            desired_salary, 
                            start_date) 
                    VALUES (?, ?, ?, ?, ?)
                """, (employment_type, position_applying_for, years_of_experience, desired_salary, start_date))
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
                """, (sss_number, employment_info_key, major_skills, date_of_application_submission, file_content))
                
                conn.commit()
                cursor.close()
                conn.close()
                flash('Application recorded successfully', 'success')
                return redirect(url_for('view_database'))
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            flash(f'A database error occurred: {str(e)}', 'error')
            return redirect(url_for('application_form'))
        except Exception as e:
            if conn:
                conn.rollback()
            flash(f'An unexpected error occurred: {str(e)}', 'error')
            return redirect(url_for('application_form'))
        finally:
            if conn:
                conn.close()
    
    return render_template('applicationForm.html')



#DISPLAYING THE SIGNATURE IMAGE
@app.route('/serve-signature/<path:sss_number>')
def serve_signature(sss_number):

    conn = get_db_connection()
    cursor = conn.cursor()

    query = '''
    SELECT signature FROM GENERAL_TABLE WHERE sss_number = ?
    '''
    result = cursor.execute(query, (sss_number,)).fetchone()

    if result is None:
        return "Image not found", 404

    image_data = result['signature']
    
    cursor.close()
    conn.close()
    
    return Response(image_data, mimetype='image/png')


# VIEW DATABASE PAGE
@app.route('/view-database')
def view_database():
    # Get query parameters for sorting, searching, and filtering
    sort_order = request.args.get('sort_order', 'date_desc')
    categories = request.args.getlist('category[]')
    search_last_name = request.args.get('searchLastName', '')

    # Base query for fetching applicants
    query = '''
    SELECT APPLICANT_TABLE.*, GENERAL_TABLE.*, EMPLOYMENT_TABLE.*
    FROM APPLICANT_TABLE
    INNER JOIN GENERAL_TABLE ON APPLICANT_TABLE.sss_number = GENERAL_TABLE.sss_number
    INNER JOIN EMPLOYMENT_TABLE ON GENERAL_TABLE.employment_info_key = EMPLOYMENT_TABLE.employment_info_key
    '''
    query_params = []
    conditions = []

    # Search functionality
    if search_last_name:
        conditions.append('last_name LIKE ?')
        query_params.append('%' + search_last_name + '%')

    # Position filtering
    position_categories = [
        'Front-End Developer', 'Back-End Developer', 'UI/UX Designer', 
        'Full-Stack Developer', 'Project Manager', 'Quality Assurance', 
        'DevOps Engineer', 'Data Scientist', 'Mobile App Developer'
    ]
    
    selected_positions = [cat for cat in categories if cat in position_categories]
    
    if selected_positions:
        position_conditions = []
        for position in selected_positions:
            position_conditions.append("position_applying_for LIKE ?")
            query_params.append(f"%{position}%")
        conditions.append('(' + ' OR '.join(position_conditions) + ')')

    # Criminal conviction status filtering
    criminal_conditions = []
    if '1' in categories:
        criminal_conditions.append("criminal_conviction_status = 1")
    if '0' in categories:
        criminal_conditions.append("criminal_conviction_status = 0")

    if criminal_conditions:
        conditions.append('(' + ' OR '.join(criminal_conditions) + ')')

    # Combine all conditions
    if conditions:
        query += ' WHERE ' + ' AND '.join(conditions)

    # Sorting
    if sort_order == 'last_name_asc':
        query += ' ORDER BY last_name ASC'
    elif sort_order == 'last_name_desc':
        query += ' ORDER BY last_name DESC'
    elif sort_order == 'date_asc':
        query += ' ORDER BY GENERAL_TABLE.date_of_application_submission ASC'  
    elif sort_order == 'date_desc':
        query += ' ORDER BY GENERAL_TABLE.date_of_application_submission DESC'
    elif sort_order == 'experience_asc':
        query += ' ORDER BY EMPLOYMENT_TABLE.years_of_experience ASC'
    elif sort_order == 'experience_desc':
        query += ' ORDER BY EMPLOYMENT_TABLE.years_of_experience DESC'

    conn = get_db_connection()
    cursor = conn.cursor()

    # Execute query and fetch results
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

        if applicant_dict['signature']:
            applicant_dict['signature_url'] = f"/serve-signature/{sss_number}"
        else:
            applicant_dict['signature_url'] = None
        # Update the applicant dictionary in the list
        applicants[i] = applicant_dict
    
    # Calculate aggregate desired_salary data if categories include Developer or Designer
    desired_salary_aggregate_query = '''
    SELECT 
        MAX(desired_salary) AS max_desired_salary, 
        MIN(desired_salary) AS min_desired_salary, 
        AVG(desired_salary) AS avg_desired_salary, 
        SUM(desired_salary) AS total_desired_salary
    FROM EMPLOYMENT_TABLE
    WHERE position_applying_for LIKE ?
    '''
    aggregate_params = ['%Developer%']
    desired_salary_aggregates = cursor.execute(desired_salary_aggregate_query, aggregate_params).fetchone()

    
    # Format the salary aggregates to two decimal places
    max_desired_salary = f"{desired_salary_aggregates[0]:,.2f}"
    min_desired_salary = f"{desired_salary_aggregates[1]:,.2f}"
    avg_desired_salary = f"{desired_salary_aggregates[2]:,.2f}"
    total_desired_salary = f"{desired_salary_aggregates[3]:,.2f}"

    conn.close()
    return render_template(
        'viewDatabase.html', 
        applicants=applicants, 
        sort_order=sort_order, 
        categories=categories,
        max_desired_salary=max_desired_salary,
        min_desired_salary=min_desired_salary,
        avg_desired_salary=avg_desired_salary,
        total_desired_salary=total_desired_salary
    )



# DISPLAY OF VALUE FOR UPDATE
@app.route('/update-page/<string:sss_number>', methods=['GET'])
def update_page(sss_number):
    try:
        conn = get_db_connection()
        # Retrieve applicant data based on SSS number
        applicant_data = conn.execute('SELECT * FROM APPLICANT_TABLE WHERE sss_number = ?', (sss_number,)).fetchone()
        employment_data = conn.execute('SELECT * FROM EMPLOYMENT_TABLE WHERE employment_info_key IN (SELECT employment_info_key FROM GENERAL_TABLE WHERE sss_number = ?)', (sss_number,)).fetchone()
        education_data = conn.execute('SELECT * FROM EDUCATION_TABLE WHERE sss_number = ?', (sss_number,)).fetchall()
        work_experience_data = conn.execute('SELECT * FROM WORK_EXPERIENCE_TABLE WHERE sss_number = ?', (sss_number,)).fetchall()
        general_data = conn.execute('SELECT * FROM GENERAL_TABLE WHERE sss_number = ?', (sss_number,)).fetchone()
        conn.close()
    except Exception as e:
        print(f"Error: {str(e)}")
        applicant_data = None
    
    return render_template('update_form.html', 
                           applicant_data=applicant_data, 
                           employment_data=employment_data ,
                           general_data=general_data,
                           education_data=education_data,
                           work_experience_data=work_experience_data)

# UPDATE RECORD
@app.route('/view-database/<string:sss_number>/update', methods=['GET', 'POST'])
def update(sss_number):
    if request.method not in ['POST', 'GET']:
        flash('Invalid request method.', 'error')
        return redirect(url_for('view_database'))

    if request.method == 'GET':
        # Assuming you want to redirect to the update form on GET
        return redirect(url_for('update_page', sss_number=sss_number))

    # Validate sss_number in form data
    if 'sss_number' not in request.form:
        flash('SSS number is missing in the form data.', 'error')
        return redirect(url_for('view_database'))

    new_sss_number = request.form['sss_number']
    
    conn = None
    try:
        conn = get_db_connection()
        conn.execute("BEGIN TRANSACTION")
        cursor = conn.cursor()

        # Check if the new SSS number already exists (if it's being changed)
        if sss_number != new_sss_number:
            existing = cursor.execute("SELECT 1 FROM APPLICANT_TABLE WHERE sss_number = ?", (new_sss_number,)).fetchone()
            if existing:
                raise ValueError("The new SSS number already exists in the database.")

        # Update APPLICANT_TABLE
        cursor.execute('''UPDATE APPLICANT_TABLE SET 
            sss_number = ?, given_name = ?, middle_initial = ?, last_name = ?, suffix = ?, 
            birth_date = ?, address = ?, city = ?, state = ?, zip_code = ?, 
            phone_1 = ?, phone_2 = ?, email = ?, criminal_conviction_status = ?, 
            reason_for_conviction = ? WHERE sss_number = ?''',
            (new_sss_number, request.form['given_name'], request.form['middle_initial'], 
             request.form['last_name'], request.form['suffix'], 
             request.form['birth_date'], request.form['address'], 
             request.form['city'], request.form['state'], 
             request.form['zip_code'], request.form['phone_1'], 
             request.form['phone_2'], request.form['email'], 
             'criminal_conviction_status' in request.form,
             request.form.get('reason_for_conviction', ''), sss_number))

        # Update GENERAL_TABLE
        cursor.execute('''UPDATE GENERAL_TABLE SET 
            sss_number = ?, major_skills = ? WHERE sss_number = ?''',
            (new_sss_number, request.form['major_skills'], sss_number))

        # Update EMPLOYMENT_TABLE (via GENERAL_TABLE)
        cursor.execute('''UPDATE EMPLOYMENT_TABLE SET 
            employment_type = ?, position_applying_for = ?, years_of_experience = ?,
            desired_salary = ?, start_date = ? WHERE employment_info_key = 
            (SELECT employment_info_key FROM GENERAL_TABLE WHERE sss_number = ?)''',
            (request.form['employment_type'], request.form['position_applying_for'], 
             request.form['years_of_experience'], request.form['desired_salary'], 
             request.form['start_date'], new_sss_number))

        # Update EDUCATION_TABLE
        cursor.execute('DELETE FROM EDUCATION_TABLE WHERE sss_number = ?', (sss_number,))
        for school, location, date_graduated, attainment in zip(
            request.form.getlist('school[]'),
            request.form.getlist('location[]'),
            request.form.getlist('date-graduated[]'),
            request.form.getlist('attainment[]')):
            cursor.execute('''INSERT INTO EDUCATION_TABLE 
                (sss_number, school, location, date_graduated, attainment) 
                VALUES (?, ?, ?, ?, ?)''',
                (new_sss_number, school, location, date_graduated, attainment))

        # Update WORK_EXPERIENCE_TABLE
        cursor.execute('DELETE FROM WORK_EXPERIENCE_TABLE WHERE sss_number = ?', (sss_number,))
        for company_name, period_start, period_end, position, reason_for_leaving in zip(
            request.form.getlist('company_name[]'),
            request.form.getlist('period_start[]'),
            request.form.getlist('period_end[]'),
            request.form.getlist('position[]'),
            request.form.getlist('reason_for_leaving[]')):
            cursor.execute('''INSERT INTO WORK_EXPERIENCE_TABLE 
                (sss_number, company_name, period_start, period_end, position, 
                reason_for_leaving, contact_present_employer, name_of_supervisor, supervisor_contact, why_not_contact) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (new_sss_number, company_name, period_start, period_end, position, 
                 reason_for_leaving, 'contact_present_employer' in request.form, 
                 request.form.get('name_of_supervisor', ''), request.form.get('supervisor_contact', ''),  
                 request.form.get('why_not_contact', '')))

        # Handle file upload for signature
        file = request.files.get('signature')
        if file and file.filename != '' and allowed_file(file.filename):
            file_content = file.read()
            cursor.execute('''UPDATE GENERAL_TABLE SET 
                signature = ? WHERE sss_number = ?''',
                (file_content, new_sss_number))

        conn.commit()
        flash('Application updated successfully', 'success')
        return redirect(url_for('view_database'))

    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        flash(f'A database error occurred: {str(e)}', 'error')
        return redirect(url_for('view_database'))
    except ValueError as e:
        if conn:
            conn.rollback()
        flash(str(e), 'error')
        return redirect(url_for('view_database'))
    except Exception as e:
        if conn:
            conn.rollback()
        flash(f'An unexpected error occurred: {str(e)}', 'error')


        


# DELETE Function
@app.route('/view-database/<string:sss_number>/delete', methods=['POST'])
def delete(sss_number):
    print("Delete route accessed")
    print(f"SSS Number to delete: {sss_number}")
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM EMPLOYMENT_TABLE WHERE employment_info_key IN (SELECT employment_info_key FROM GENERAL_TABLE WHERE sss_number = ?)', (sss_number,))
        conn.execute('DELETE FROM APPLICANT_TABLE WHERE sss_number = ?', (sss_number,))
        conn.execute('DELETE FROM EDUCATION_TABLE WHERE sss_number = ?', (sss_number,))
        conn.execute('DELETE FROM WORK_EXPERIENCE_TABLE WHERE sss_number = ?', (sss_number,))
        conn.execute('DELETE FROM GENERAL_TABLE WHERE sss_number = ?', (sss_number,))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error: {str(e)}")
    return redirect(url_for('view_database'))


if __name__ == '__main__':
    app.run(debug=True)
