from flask import Flask, render_template, url_for, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    
    if request.method == 'GET':
        return render_template('index.html')
    
    else:
        return render_template('trip_details.html')

@app.route('/new_trip_form')
def new_trip_form():
    
    return render_template('new_trip_form.html')

if __name__ == '__main__':
    app.run()