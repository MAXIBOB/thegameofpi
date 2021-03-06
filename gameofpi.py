from flask import Flask, render_template, redirect, url_for
try:
    from sense_hat import SenseHat
    sense=SenseHat()
except ImportError:
    pass

def color(c,d):
    global sense
    sense.set_pixel(c,d,255,0,0)

def clear(c,d):
    global sense
    sense.set_pixel(c,d,0,0,0)

def blank():
    for x in range(8):
        for y in range(8):
            clear(x, y)

app = Flask(__name__)
app.debug=True

x=4
y=4

@app.route("/")
def index():
    return "Hello World!"

@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
    if name:
        sense.show_message(name)
    return render_template('hello.html', name=name)

@app.route('/map')
def mapping():
    my_map=[]
    global sense
    position=sense.get_pixels()
    for y in range(8):
        my_map.append([])
        for x in range(8):
            a=position[y*8+x]
            my_map[y].append(a)
                
    return render_template('map.html', map=my_map)

@app.route("/down")
def down():
    global x,y
    clear(x,y)
    y = y+1
    if y>7:
        y=0
    color(x,y)
    return redirect(url_for("mapping"))

@app.route("/up")
def up():
    global x,y
    clear(x,y)
    y = y-1
    if y<0:
        y=7
    color(x,y)
    return redirect(url_for("mapping"))

@app.route("/left")
def left():
    global x,y
    clear(x,y)
    x=x-1
    if x<0:
        x=7
    color(x,y)
    return redirect(url_for("mapping"))

@app.route("/right")
def right():
    global x,y
    clear(x,y)
    x=x+1
    if x>7:
        x=0
    color(x,y)
    return redirect(url_for("mapping"))

if __name__ == "__main__":
    blank()
    app.run()
