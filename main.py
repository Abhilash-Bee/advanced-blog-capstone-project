from flask import Flask, render_template
import requests

app = Flask(__name__)

blog_url = "https://api.npoint.io/8033d54aaf7b369914dd"
response = requests.get(url=blog_url)
all_posts = response.json()


@app.route('/')
def home():
    return render_template("index.html", all_posts=all_posts)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/post/<int:num>')
def post(num):
    requested_post = ""
    for post in all_posts:
        if post["id"] == num:
            requested_post = post
    return render_template("post.html", requested_post=requested_post)


@app.route('/contact')
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
