from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
from database import init_db, add_student, get_all_students, get_ranked_students

app = Flask(__name__)
app.secret_key = "ibm_exam_system_secret"

init_db()


def process_dataframe(df):
    """Total, Percentage, Result calculate karta hai"""
    if df.empty:
        return df
    
    df['total'] = df['maths'] + df['physics'] + df['chemistry']
    df['percentage'] = (df['total'] / 300) * 100
    df['result'] = df.apply(
        lambda row: 'Pass' if (row['maths'] >= 40 and row['physics'] >= 40 and row['chemistry'] >= 40) else 'Fail',
        axis=1
    )
    return df


# ==================== HOME PAGE ====================
@app.route('/')
def index():
    """Home page - 3 options ke saath"""
    return render_template('index.html')


# ==================== ADD PAGE ====================
@app.route('/add', methods=['GET'])
def add_page():
    """Add form dikhane ke liye (GET)"""
    return render_template('add.html')


@app.route('/add', methods=['POST'])
def add():
    """Form submit hone pe data save karne ke liye (POST)"""
    roll = request.form.get('roll', '').strip()
    name = request.form.get('name', '').strip()

    if not roll or not name:
        flash("Roll number and Name cannot be empty.", "error")
        return redirect(url_for('add_page'))

    try:
        maths = int(request.form.get('maths'))
        physics = int(request.form.get('physics'))
        chemistry = int(request.form.get('chemistry'))
    except (ValueError, TypeError):
        flash("Marks must be valid integers.", "error")
        return redirect(url_for('add_page'))

    if not (0 <= maths <= 100 and 0 <= physics <= 100 and 0 <= chemistry <= 100):
        flash("(b) Marks must be between 0 and 100.", "error")
        return redirect(url_for('add_page'))

    success, message = add_student(roll, name, maths, physics, chemistry)

    if not success:
        flash(message, "error")
        return redirect(url_for('add_page'))

    total = maths + physics + chemistry
    percentage = total / 3.0
    result = "Pass" if (maths >= 40 and physics >= 40 and chemistry >= 40) else "Fail"

    flash(
        f"Record added: {roll} | {name} <br>"
        f"Total: {total} | Percentage: {percentage:.2f}% | Result: {result}",
        "success"
    )
    return redirect(url_for('add_page'))


# ==================== VIEW PAGE ====================
@app.route('/view')
def view():
    """Saare records dikhane ke liye"""
    df = get_all_students()
    df = process_dataframe(df)
    records = df.to_dict('records') if not df.empty else []
    return render_template('view.html', records=records)


# ==================== RANK PAGE ====================
@app.route('/rank')
def rank():
    """Rank list dikhane ke liye"""
    df = get_ranked_students()
    df = process_dataframe(df)
    records = df.to_dict('records') if not df.empty else []
    return render_template('rank.html', records=records)


if __name__ == '__main__':
    app.run(debug=True)