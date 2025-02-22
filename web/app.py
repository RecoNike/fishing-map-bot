import psycopg2
from flask import Flask, jsonify, render_template
from config import DB_URL

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("map.html")

@app.route("/api/markers")
def get_markers():
    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT latitude, longitude, fish_type, bait FROM fishing_spots")
    markers = cursor.fetchall()
    conn.close()

    markers_list = [{"lat": lat, "lng": lng, "fish": fish, "bait": bait} for lat, lng, fish, bait in markers]
    return jsonify(markers_list)

if __name__ == "__main__":
    app.run(debug=True)
