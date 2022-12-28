from flask import Flask, render_template


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/blogs")
def blogs():
    return render_template("blog.html")


@app.route("/forum")
def forum():
    return render_template("forum.html")


@app.route("/search")
def search():
    return render_template("hledat.html")

@app.route("/news")
def news():
    return render_template("zpravy.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")





















if __name__ == "__main__":
    app.run(debug=True)
