from flask import Flask, render_template, url_for, request, redirect
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

    @property
    def trip_details_by_dict(self):
        return {'trip_name':self.name, 'email':self.email, 'description':self.description, 'completness':self.completness, 'gridCheck':(self.gridCheck)}

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

    @classmethod  
    def read_data_for_trip(cls, filepath, trip_name):
        with open(filepath, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == trip_name:
                    return newTripIdea(row[0], row[1], row[2], row[3], row[4])

    @classmethod
    def read_trip_names(cls, filepath):
        trip_name_list = []
        with open(filepath, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                trip_name_list.append(row[0])
            return trip_name_list



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        trip_name_list = newTripIdea.read_trip_names(join(app.static_folder, 'trip_data.csv'))

        return render_template('index.html', trip_name_list=trip_name_list)
    
    else:
        trip_option = ''
        if 'trip_option' in request.form:
            trip_option = request.form['trip_option']
        
        trip_details = newTripIdea.read_data_for_trip(join(app.static_folder, 'trip_data.csv'), trip_option)

        return render_template('trip_details.html', trip_details=trip_details.trip_details_by_dict)

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
        
        return redirect(url_for('index'))



if __name__ == '__main__':
    app.run()