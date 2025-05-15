from infrastructure.app.app import App

application = App()
application.configure()
app = application.get_server()
