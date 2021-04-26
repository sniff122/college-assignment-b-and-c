from quart import Quart, render_template, send_file, request, redirect
import json

app = Quart(__name__)
app.Title = "Motor Rent"
app.port = 5000
app.host = "127.0.0.1"
with open("cars.json", "r") as f:
    app.cars = json.load(f)


def save_contact_form(formdata):
    with open("contact_form.json", "r") as f:
        contactform = json.load(f)
    contactform.append(formdata)
    with open("contact_form.json", "w") as f:
        json.dump(contactform, f)


@app.route('/')
async def index_page():
    return await render_template("index.html")


@app.route('/about')
async def about_page():
    return await render_template("about.html")


@app.route('/cars')
async def cars_page():
    return await render_template("cars.html", cars=app.cars)


@app.route('/faq')
async def faq_page():
    return await render_template("faq.html")


@app.route('/contact', defaults={'formsubmit': "False"})
@app.route('/contact/<formsubmit>')
async def contact_page(formsubmit):
    if formsubmit != "True":
        formsubmit = False
    else:
        formsubmit = True
    return await render_template("contact.html", formsubmit=bool(formsubmit))


@app.route("/form_submit", methods=["POST"])
async def fom_submit():
    form = await request.form
    name = form.get("fname")
    email = form.get("email")
    message = form.get("message")
    formdata = {"name": name, "email": email, "message": message}
    save_contact_form(formdata)
    return redirect("/contact/True")


@app.route("/static/bootstrap/js/bootstrap.js", methods=["GET"])
async def bootstrapJS():
    try:
        return await send_file("static/bootstrap/js/bootstrap.js")
    except FileNotFoundError:
        return {"Error": 404, "Info": "File Not Found"}


@app.route("/favicon.ico", methods=["GET"])
async def favicon():
    try:
        return await send_file("static/images/favicon.ico")
    except FileNotFoundError:
        return {"Error": 404, "Info": "File Not Found"}


@app.route("/static/bootstrap/css/bootstrap.min.css", methods=["GET"])
async def bootstrapCSS():
    try:
        return await send_file("static/bootstrap/css/bootstrap.min.css")
    except FileNotFoundError:
        return {"Error": 404, "Info": "File Not Found"}


@app.route("/static/images/logo.png", methods=["GET"])
async def carimage():
    try:
        return await send_file("static/images/logo.png")
    except FileNotFoundError:
        return {"Error": 404, "Info": "File Not Found"}


@app.route("/static/images/car.png", methods=["GET"])
async def imagelogo():
    try:
        return await send_file("static/images/car.png")
    except FileNotFoundError:
        return {"Error": 404, "Info": "File Not Found"}


@app.route("/static/images/cars/<carimg>", methods=["GET"])
async def get_the_car(carimg):
    try:
        return await send_file(f"static/images/cars/{carimg}")
    except:
        return {"Error": 404, "Info": "File Not Found"}


if __name__ == '__main__':
    app.run(debug=False, use_reloader=False, port=app.port, host=app.host)
