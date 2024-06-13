from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///applications.db'
db=SQLAlchemy(app)

class Applicant(db.Model):
    __tablename__ = 'applicant_table'

    sss_number = db.Column(db.Integer, primary_key=True)
    given_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    middle_initial = db.Column(db.String(5), nullable=True)
    suffix = db.Column(db.String(20), nullable=True)
    # birth_date = db.Column(db.DateTime)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    phone_1 = db.Column(db.String(15), nullable=False)
    phone_2 = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    criminal_conviction_status = db.Column(db.Boolean, default=False)
    reason_for_conviction = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return '<Applicant %r>' % self.sss_number


    # Define relationship
#     general_info = relationship("General_Table", back_populates="applicant_info")


# class Employment_Table(db.Model):
#     __tablename__ = 'employment_table'

#     employment_info_key = db.Column(db.Integer, primary_key=True)
#     employment_type = db.Column(db.String(50), nullable=False)

#     # Define relationship
#     general_info = relationship("General_Table", back_populates="general_info")

# class General_Table(db.Model):
#     __tablename__ = 'general_table'

#     sss_number = db.Column(db.Integer, ForeignKey('applicant_table.sss_number'), primary_key=True)
#     employment_info_key = db.Column(db.Integer, ForeignKey('employment_table.employment_info_key'), primary_key=True)
#     date_applied = db.Column(db.DateTime, default=datetime.utcnow)

#     # Define Relationships
#     applicant_info = relationship("Applicant_Table", backref="general_table")
#     employment_info = relationship("Employment_Table", backref="general_table")

# Routes html pages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/view-database')
def view_database():
    applications = Applicant.query.all()
    return render_template('viewDatabase.html', applications=applications)

@app.route('/application-form', methods=['POST', 'GET'])
def application_form():
    if request.method == 'POST':
        sss_number = request.form['sss_number']
        given_name = request.form['given_name']
        last_name = request.form['last_name']
        middle_initial = request.form.get('middle_initial', None)
        suffix = request.form.get('suffix', None)
        # birth_date = request.form.get('birth_date', None)
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip_code']
        phone_1 = request.form['phone_1']
        phone_2 = request.form['phone_2']
        email = request.form['email']
        criminal_conviction_status = 'criminal_conviction_status' in request.form
        reason_for_conviction = request.form.get('reason_for_conviction', None)

        new_applicant = Applicant(sss_number=sss_number, given_name=given_name, last_name=last_name,
                                middle_initial=middle_initial, suffix=suffix,
                                address=address, city=city, state=state, zip_code=zip_code,
                                phone_1=phone_1, phone_2=phone_2, email=email,
                                criminal_conviction_status=criminal_conviction_status,
                                reason_for_conviction=reason_for_conviction)

        try:
            db.session.add(new_applicant)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue submitting your application.'

    else:
        applications = Applicant.query.all()
        return render_template('applicationForm.html', applications=applications)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(port=8000, debug=True)

# Command to enter python virtual environment: 'source env/bin/activate'