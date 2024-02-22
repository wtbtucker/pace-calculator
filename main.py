from importlib import util

spec = util.spec_from_file_location('app', 'C:\\Users\\order\\repos\\pace-calculator\\applications\\data-collector\\main\\app.py')
app = util.module_from_spec(spec)
spec.loader.exec_module(app)

if __name__ == "__main__":
    app.run()
