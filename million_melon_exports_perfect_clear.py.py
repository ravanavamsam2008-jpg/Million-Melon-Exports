from datetime import datetime
import os
from flask import Flask, flash, redirect, render_template_string, request, url_for
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
app.secret_key = "cyber_falcon_watermelon_secret_key"
OWNER_PIN = "1234"

# Ungaloda direct Neon Pooled Database URL
DATABASE_URL = os.environ.get(
    "DATABASE_URL", 
    "postgresql://neondb_owner:npg_SZaBURp3Ft0z@ep-fancy-cell-bbqyof0l-pooler.c-15.us-east-1.aws.neon.tech/neondb?sslmode=require"
)


def get_db_connection():
    return psycopg2.connect(DATABASE_URL)


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            user_from TEXT NOT NULL,
            tons REAL NOT NULL,
            load_to TEXT NOT NULL,
            phone TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pricing (
            id INT PRIMARY KEY,
            cut1 TEXT NOT NULL,
            cut2 TEXT NOT NULL,
            cut3 TEXT NOT NULL
        );
    """)
    cursor.execute("SELECT COUNT(*) FROM pricing;")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO pricing (id, cut1, cut2, cut3) VALUES (1, '15k to 20k', '8.5k to 15k', '6k to 8.5k');"
        )
    conn.commit()
    cursor.close()
    conn.close()


def get_prices():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT cut1, cut2, cut3 FROM pricing WHERE id = 1;")
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return {"cut1": row[0], "cut2": row[1], "cut3": row[2]}
    except Exception:
        pass
    return {
        "cut1": "15k to 20k",
        "cut2": "8.5k to 15k",
        "cut3": "6k to 8.5k",
    }


# ----------------- SINGLE FILE EMBEDDED FRONTEND -----------------
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ta">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HI WELCOME TO ELLAPPAN'S MART</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }

        body {
            min-height: 100vh;
            background: #0d0b18 url('/static/ellu1.png') no-repeat center top fixed;
            background-size: cover;
            color: #ffffff;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 14px 10px 40px;
            overflow-x: hidden;
        }

        .brand-bar {
            width: 100%;
            max-width: 620px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 14px;
            background: rgba(18, 14, 33, 0.92);
            border-radius: 16px;
            border: 1px solid rgba(0, 242, 254, 0.35);
            margin-bottom: 16px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
        }

        .brand-logo-wrap {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .falcon-logo {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            border: 2px solid #00f2fe;
            object-fit: cover;
        }

        .lorry-logo {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            border: 2px solid #ff4b2b;
            object-fit: cover;
            background: #ffffff;
        }

        .brand-title {
            font-size: 1rem;
            font-weight: 800;
            letter-spacing: 0.5px;
            color: #00f2fe;
            text-transform: uppercase;
        }

        .main-heading {
            text-align: center;
            font-size: 1.4rem;
            font-weight: 900;
            letter-spacing: 1px;
            margin: 6px 0 16px;
            text-transform: uppercase;
            color: #ffffff;
            text-shadow: 0 2px 10px rgba(0, 242, 254, 0.8);
        }

        .alert-box {
            width: 100%;
            max-width: 620px;
            background: rgba(0, 242, 254, 0.2);
            border-left: 4px solid #00f2fe;
            padding: 10px 14px;
            border-radius: 8px;
            margin-bottom: 14px;
            font-weight: 600;
        }

        .owner-card {
            width: 100%;
            max-width: 620px;
            background: rgba(18, 14, 33, 0.92);
            border: 1px solid rgba(0, 255, 135, 0.4);
            border-radius: 18px;
            padding: 16px;
            margin-bottom: 18px;
            display: flex;
            align-items: center;
            gap: 16px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
        }

        .owner-img {
            width: 95px;
            height: 115px;
            border-radius: 14px;
            object-fit: cover;
            border: 2px solid #00ff87;
            box-shadow: 0 0 10px rgba(0, 255, 135, 0.4);
            flex-shrink: 0;
        }

        .owner-details {
            flex-grow: 1;
        }

        .owner-name {
            font-size: 1.15rem;
            font-weight: 800;
            color: #00ff87;
            margin-bottom: 4px;
        }

        .owner-role {
            font-size: 0.8rem;
            color: #b0c4de;
            margin-bottom: 8px;
            text-transform: uppercase;
            font-weight: 600;
        }

        .contact-links {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }

        .contact-btn {
            display: inline-flex;
            align-items: center;
            padding: 6px 10px;
            border-radius: 8px;
            font-size: 0.78rem;
            font-weight: 700;
            text-decoration: none;
            color: #ffffff;
        }

        .btn-call { background: #2575fc; }
        .btn-wa { background: #25D366; }
        .btn-insta { background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888); }

        .rate-card {
            width: 100%;
            max-width: 620px;
            background: rgba(18, 14, 33, 0.92);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 18px;
            padding: 14px;
            margin-bottom: 18px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
        }

        .rate-card h3 {
            font-size: 0.95rem;
            margin-bottom: 10px;
            color: #00ff87;
            text-align: center;
            text-transform: uppercase;
        }

        .rates-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
        }

        .rate-item {
            background: rgba(255, 255, 255, 0.05);
            padding: 10px 4px;
            border-radius: 10px;
            text-align: center;
            border: 1px solid rgba(0, 242, 254, 0.2);
        }

        .rate-cut-name {
            font-size: 0.75rem;
            color: #b0c4de;
            margin-bottom: 4px;
            font-weight: 600;
        }

        .rate-price {
            font-size: 0.95rem;
            font-weight: 800;
            color: #ffb703;
        }

        .glass-box {
            width: 100%;
            max-width: 620px;
            background: rgba(18, 14, 33, 0.92);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 18px;
            padding: 20px 16px;
            margin-bottom: 18px;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
        }

        .glass-box h2 {
            font-size: 1.15rem;
            margin-bottom: 14px;
            text-align: center;
            color: #00f2fe;
            text-transform: uppercase;
        }

        .form-group {
            margin-bottom: 12px;
        }

        .form-group label {
            display: block;
            margin-bottom: 4px;
            font-size: 0.82rem;
            font-weight: 600;
            color: #d8e2dc;
        }

        .form-control {
            width: 100%;
            padding: 11px 12px;
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            background: rgba(255, 255, 255, 0.07);
            color: #ffffff;
            font-size: 0.9rem;
            outline: none;
        }

        .form-control:focus {
            border-color: #00f2fe;
            background: rgba(255, 255, 255, 0.12);
        }

        .btn {
            display: inline-block;
            width: 100%;
            padding: 12px;
            border-radius: 10px;
            border: none;
            cursor: pointer;
            font-size: 0.92rem;
            font-weight: 700;
            text-transform: uppercase;
            text-align: center;
            text-decoration: none;
        }

        .btn-order {
            background: #00b09b;
            color: #ffffff;
        }

        .btn-owner {
            background: #ff416c;
            color: #ffffff;
            margin-top: 8px;
        }

        .table-responsive {
            width: 100%;
            overflow-x: auto;
            margin-top: 12px;
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.15);
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.82rem;
            text-align: left;
        }

        th, td {
            padding: 10px 8px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            white-space: nowrap;
        }

        th {
            background: rgba(0, 242, 254, 0.2);
            color: #00ff87;
        }

        tr:nth-child(even) {
            background: rgba(255, 255, 255, 0.03);
        }
    </style>
</head>
<body>

    <header class="brand-bar">
        <div class="brand-logo-wrap">
            <img src="/static/ellu3.png" alt="Cyber Falcon" class="falcon-logo" loading="lazy">
            <div>
                <div class="brand-title">ELLAPPAN MART</div>
                <small style="color: #00f2fe; font-size: 0.7rem;">WATERMELON EXPORTS</small>
            </div>
        </div>
        <img src="/static/ellu2.png" alt="Million Melon Exports" class="lorry-logo" loading="lazy">
    </header>

    <h1 class="main-heading">HI WELCOME TO ELLAPPAN'S MART</h1>

    {% with messages = get_flashed_messages() %}
      {% if messages %}
        {% for message in messages %}
          <div class="alert-box">⚡ {{ message }}</div>
        {% endfor %}
      {% endif %}
    {% endwith %}

    <section class="owner-card">
        <img src="/static/ellu4.png" alt="Ellappan Bsc.AI" class="owner-img">
        <div class="owner-details">
            <div class="owner-name">Ellappan Bsc.AI</div>
            <div class="owner-role">Founder & Harvesting Incharge</div>
            <div class="contact-links">
                <a href="tel:+919342423765" class="contact-btn btn-call">📞 Call</a>
                <a href="https://wa.me/919342423765" target="_blank" class="contact-btn btn-wa">💬 WhatsApp</a>
                <a href="https://instagram.com/million_melon_exports" target="_blank" class="contact-btn btn-insta">📸 Insta</a>
            </div>
        </div>
    </section>

    <section class="rate-card">
        <h3>🍉 LIVE WATERMELON RATES (PER TON) 🍉</h3>
        <div class="rates-grid">
            <div class="rate-item">
                <div class="rate-cut-name">1ST CUTTING</div>
                <div class="rate-price">₹ {{ rates.cut1 }}</div>
            </div>
            <div class="rate-item">
                <div class="rate-cut-name">2ND CUTTING</div>
                <div class="rate-price">₹ {{ rates.cut2 }}</div>
            </div>
            <div class="rate-item">
                <div class="rate-cut-name">3RD CUTTING</div>
                <div class="rate-price">₹ {{ rates.cut3 }}</div>
            </div>
        </div>
    </section>

    <div class="glass-box">
        <h2>📦 BOOK WATERMELON LOAD</h2>
        <form action="/book_order" method="POST">
            <div class="form-group">
                <label>Customer Name</label>
                <input type="text" name="name" class="form-control" placeholder="Enter customer name" required>
            </div>
            <div class="form-group">
                <label>User From (Oor / Harvesting Location)</label>
                <input type="text" name="user_from" class="form-control" placeholder="E.g., Tindivanam, Gingee" required>
            </div>
            <div class="form-group">
                <label>Number's of Tons</label>
                <input type="number" step="0.1" name="tons" class="form-control" placeholder="E.g., 10, 15.5" required>
            </div>
            <div class="form-group">
                <label>Load To (Destination / Market)</label>
                <input type="text" name="load_to" class="form-control" placeholder="E.g., Koyambedu Market" required>
            </div>
            <div class="form-group">
                <label>User Phone Number</label>
                <input type="tel" name="phone" class="form-control" placeholder="E.g., 9876543210" required>
            </div>
            <button type="submit" class="btn btn-order">SUBMIT LOAD ORDER 🚀</button>
        </form>
    </div>

    {% if not owner_logged_in %}
    <div class="glass-box">
        <h2>🔐 OWNER DASHBOARD ACCESS</h2>
        <form action="/owner_login" method="POST">
            <div class="form-group">
                <label>Enter Owner Password / PIN</label>
                <input type="password" name="pin" class="form-control" placeholder="Enter PIN" required>
            </div>
            <button type="submit" class="btn btn-owner">LOGIN AS OWNER</button>
        </form>
    </div>
    {% else %}

    <div class="glass-box" style="border-color: #00ff87;">
        <h2>🛠️ UPDATE CUTTING PRICES</h2>
        <form action="/update_prices" method="POST">
            <div class="form-group">
                <label>1st Cutting Price (Per Ton)</label>
                <input type="text" name="cut1" class="form-control" value="{{ rates.cut1 }}" required>
            </div>
            <div class="form-group">
                <label>2nd Cutting Price (Per Ton)</label>
                <input type="text" name="cut2" class="form-control" value="{{ rates.cut2 }}" required>
            </div>
            <div class="form-group">
                <label>3rd Cutting Price (Per Ton)</label>
                <input type="text" name="cut3" class="form-control" value="{{ rates.cut3 }}" required>
            </div>
            <button type="submit" class="btn btn-order" style="background: #00f2fe; color: #000000;">SAVE NEW PRICES ✅</button>
        </form>
    </div>

    <div class="glass-box" style="max-width: 900px; border-color: #00f2fe;">
        <h2>📋 ALL WATERMELON ORDERS (SORTED BY DATE)</h2>
        {% if orders %}
        <div class="table-responsive">
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Date & Time</th>
                        <th>Name</th>
                        <th>From</th>
                        <th>Tons</th>
                        <th>Destination</th>
                        <th>Phone</th>
                    </tr>
                </thead>
                <tbody>
                    {% for order in orders %}
                    <tr>
                        <td>#{{ order[0] }}</td>
                        <td style="color: #00ff87;">{{ order[6] }}</td>
                        <td>{{ order[1] }}</td>
                        <td>{{ order[2] }}</td>
                        <td><strong>{{ order[3] }} T</strong></td>
                        <td>{{ order[4] }}</td>
                        <td><a href="tel:{{ order[5] }}" style="color: #00f2fe; text-decoration: none;">📞 {{ order[5] }}</a></td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        {% else %}
        <p style="text-align: center; color: #b0c4de; padding: 15px;">No orders recorded yet.</p>
        {% endif %}
        <br>
        <a href="/" class="btn btn-owner" style="background: #333333;">LOGOUT OWNER VIEW</a>
    </div>
    {% endif %}

</body>
</html>
"""


# ----------------- ROUTING LOGIC -----------------
@app.route("/")
def home():
    rates = get_prices()
    return render_template_string(
        HTML_TEMPLATE, rates=rates, owner_logged_in=False
    )


@app.route("/book_order", methods=["POST"])
def book_order():
    name = request.form.get("name")
    user_from = request.form.get("user_from")
    tons = request.form.get("tons")
    load_to = request.form.get("load_to")
    phone = request.form.get("phone")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO orders (name, user_from, tons, load_to, phone) 
        VALUES (%s, %s, %s, %s, %s);
    """,
        (name, user_from, tons, load_to, phone),
    )
    conn.commit()
    cursor.close()
    conn.close()

    flash(
        "Watermelon load order booked successfully! Ellappan anna will review it."
    )
    return redirect(url_for("home"))


@app.route("/owner_login", methods=["POST"])
def owner_login():
    pin = request.form.get("pin")
    rates = get_prices()

    if pin != OWNER_PIN:
        flash("Wrong password! Access denied.")
        return redirect(url_for("home"))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, user_from, tons, load_to, phone, to_char(created_at, 'YYYY-MM-DD HH24:MI:SS') 
        FROM orders 
        ORDER BY created_at DESC;
    """)
    orders = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template_string(
        HTML_TEMPLATE, rates=rates, owner_logged_in=True, orders=orders
    )


@app.route("/update_prices", methods=["POST"])
def update_prices():
    cut1 = request.form.get("cut1")
    cut2 = request.form.get("cut2")
    cut3 = request.form.get("cut3")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE pricing 
        SET cut1 = %s, cut2 = %s, cut3 = %s 
        WHERE id = 1;
    """,
        (cut1, cut2, cut3),
    )
    conn.commit()
    cursor.close()
    conn.close()

    flash("Cutting prices updated successfully!")
    return redirect(url_for("home"))


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
