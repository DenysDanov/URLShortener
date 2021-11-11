from flask import Flask,redirect,request
from flask.templating import render_template
from db import DB
import random
import string
app = Flask(__name__,
            static_url_path='', 
            static_folder='./static',
            template_folder='./templates')


def getLinkList():
    conn = DB()
    conn.create_connection()
    return conn.select("*","link")

def insertLinkInDB(shortlink,link):
    data = {
        "shortlink" : shortlink,
        "link" : link
    }
    conn = DB()
    conn.create_connection()
    conn.insert(data,"link")

@app.route("/")
@app.route("/<link>")
def index(link=""):
    if link and '.' not in link: 
        print(link)
        return redirect("".join([l if s == link else "" for s,l in getLinkList()]))
    else: return render_template(
        "index.html",
        title = "Main"
    )

@app.route("/generate/", methods = ['POST'])
def generate():
    if not request.form.get("lnk"): return render_template(
                                                            "index.html",
                                                            title = "Main",
                                                            link = "Error"
                                                        )

    links = [short_link for short_link,link in getLinkList()]
    while True:
        link = ''.join([random.choice(string.ascii_letters) for n in range(8)])
        if link not in links: break
    
    insertLinkInDB(link,request.form.get("lnk"))

    return render_template(
                                "index.html",
                                title = "Main",
                                link=link
                            )

if __name__ == "__main__":
    app.run(debug=True)