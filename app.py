from flask import Flask, render_template, url_for, request

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

        #print(new_trip_idea.name, new_trip_idea.email, new_trip_idea.description, new_trip_idea.completness, new_trip_idea.gridCheck)
    
        return render_template('trip_details.html')



if __name__ == '__main__':
    app.run()