from flask import Flask, render_template, request
import requests
import smtplib
import os
import dotenv

dotenv.load_dotenv()

USER = os.getenv("REACT_APP_USER_ID")
PASSWORD = os.getenv("REACT_APP_PASSWORD")

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


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == "POST":
        data = request.form
        name, email, phone, message = data["username"], data["email"], data["phone"], data["message"]
        if name != "" and email != "" and phone != "" and message != "":
            mail_to(name, email, phone, message)
            return render_template("contact.html", is_mail="sent")
        else:
            return render_template("contact.html", is_mail="nsent")
    return render_template("contact.html", is_mail="False")


def mail_to(name, email, phone, message):
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=USER, password=PASSWORD)
        connection.sendmail(
            from_addr=USER,
            to_addrs="8bjabhilash@gmail.com",
            msg=f"Subject: Mail from {name} to your blog\n\n"
                f"Message: {message}\nEmail id: {email}\nPhone no: {phone}"
        )


if __name__ == "__main__":
    app.run(debug=True)
