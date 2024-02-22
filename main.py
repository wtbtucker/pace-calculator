from importlib import import_module

app = import_module('applications.data-collector.main.app')

if __name__ == "__main__":
    app.run()
