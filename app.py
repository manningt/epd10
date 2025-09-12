from init import create_app

# the following is not used if launching by using: flask run --host=0.0.0.0 --port=5000
if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
