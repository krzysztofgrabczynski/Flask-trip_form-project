from flask import Flask, render_template, url_for, request
import csv
from os.path import exists, join

app = Flask(__name__)


class newTripIdea:
    def __init__(self, name, email, description, completness, gridCheck):
        self.name = name
        self.email = email
        self.description = description
        self.completness = completness
        self.gridCheck = gridCheck
    def __repr__(self):
        return f'Trip name: {self.name}'

    def write_data(self, file_path):
        headers_list = ['Trip name', 'Email', 'Description', 'Completness', 'Grid Check']
        form_data = [self.name, self.email, self.description, self.completness, str(self.gridCheck)]

        if not exists(file_path):
            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=headers_list)
                writer.writeheader()
        with open(file_path, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(form_data)
        
    def read_data(self, filepath, trip_name):
        with open(filepath, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == trip_name:
                    return newTripIdea(row[0], row[1], row[2], row[3], row[4])

        


@app.route('/', methods=['GET', 'POST'])
def index():
    
    if request.method == 'GET':
        return render_template('index.html')
    
    else:
        return render_template('trip_details.html')

@app.route('/new_trip_form', methods=['GET', 'POST'])
def new_trip_form():
    
    if request.method == 'GET':
        return render_template('new_trip_form.html')
    else:
        trip_name = 'blank_line'
        if 'trip_name' in request.form:
            trip_name = request.form['trip_name']
        email = 'blank_line'
        if 'email' in request.form:
            email = request.form['email']  
        description = 'blank_line'
        if 'description' in request.form:
            description = request.form['description']
        completness = 'option2'
        if 'completness' in request.form:
            completness = request.form['completness']
        gridCheck = False
        if 'gridCheck1' in request.form:
            gridCheck = True

        new_trip_idea = newTripIdea(trip_name, email, description, completness, gridCheck)
        new_trip_idea.write_data(join(app.static_folder, 'trip_data.csv'))
        
        return render_template('trip_details.html')



if __name__ == '__main__':
    app.run()