from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/api/greet/<name>', methods=['GET'])
def greet(name):
    return jsonify(message=f"Hello, {name}!")


if __name__ == '__main__':
    app.run(debug=True)



# Test cases
# check 200 response for valid input like name, number, special characters
# check 404 response for invalid input like empty string, None, Null
