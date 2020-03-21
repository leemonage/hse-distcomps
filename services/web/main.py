from app import app, db

if __name__ == '__main__':
    #app.run(debug=True, host='127.0.0.1', port=8091)
    app.run(host='0.0.0.0', port=8091)
