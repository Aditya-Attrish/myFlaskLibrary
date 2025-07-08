from myFlask import MyFlask, render_tamplate
from logining import login_required
app = MyFlask()

@app.route('/')
@login_required
def home():
    return render_tamplate("test.html")

@app.route('/about')
def about():
    return "<h1>About Page</h1>"

if __name__ == '__main__':
	app.run()