from flaskr import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(app.config.get('HOST'), app.config.get('PORT'))
