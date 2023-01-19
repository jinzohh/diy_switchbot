from flask import Flask

app = Flask(__name__)

@app.route('/door')
def get_data():
    with open('door.txt', 'r') as f: # Reading value from text file "door.txt"
        status_raw = f.readlines()
        status = str(status_raw)[2:3]
    return '<h5>{}</h5>'.format(status)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090, debug=True)