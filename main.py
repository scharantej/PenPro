
# Import the necessary modules.
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

# Create a Flask application.
app = Flask(__name__)

# Connect to the database.
conn = sqlite3.connect('pension_agency.db')
c = conn.cursor()

# Define the main route.
@app.route('/')
def index():
  # Render the index.html template.
  return render_template('index.html')

# Define the route to handle the submission of the pension form.
@app.route('/pension-form', methods=['POST'])
def pension_form():
  # Get the data from the form.
  name = request.form['name']
  ssn = request.form['ssn']
  dob = request.form['dob']

  # Insert the data into the database.
  c.execute('INSERT INTO pension (name, ssn, dob) VALUES (?, ?, ?)', (name, ssn, dob))
  conn.commit()

  # Redirect the user to the pension results page.
  return redirect(url_for('pension_results'))

# Define the route to display the pension results.
@app.route('/pension-results')
def pension_results():
  # Get the user's data from the database.
  c.execute('SELECT * FROM pension WHERE ssn = ?', (request.form['ssn'],))
  data = c.fetchone()

  # Calculate the user's estimated pension benefits.
  pension = 1000 * data[2]

  # Render the pension results page.
  return render_template('pension_results.html', pension=pension)

# Define the route to display the about page.
@app.route('/about')
def about():
  # Render the about.html template.
  return render_template('about.html')

# Define the route to display the contact page.
@app.route('/contact')
def contact():
  # Render the contact.html template.
  return render_template('contact.html')

# Run the application.
if __name__ == '__main__':
  app.run(debug=True)
