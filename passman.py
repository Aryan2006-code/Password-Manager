from flask import Flask, render_template, request, redirect, url_for, flash
from password_manager_app import PasswordManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management
pm = PasswordManager()

# Store paths globally to manage keys and files
key_path = None
password_file_path = None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/key', methods=['GET', 'POST'])
def key():
    global key_path

    if request.method == 'POST':
        action = request.form.get('action')
        path = request.form.get('key_path')

        try:
            if action == 'create':
                pm.create_key(path)
                key_path = path
                flash('Key created successfully!', 'success')
            elif action == 'load':
                pm.load_key(path)
                key_path = path
                flash('Key loaded successfully!', 'success')
            else:
                flash('Invalid action!', 'danger')
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')

        return redirect(url_for('file'))

    return render_template('key.html')

@app.route('/file', methods=['GET', 'POST'])
def file():
    global password_file_path

    if request.method == 'POST':
        action = request.form.get('action')
        path = request.form.get('file_path')

        try:
            if action == 'create':
                pm.create_password_file(path)
                password_file_path = path
                flash('Password file created successfully!', 'success')
            elif action == 'load':
                pm.load_password_file(path)
                password_file_path = path
                flash('Password file loaded successfully!', 'success')
            else:
                flash('Invalid action!', 'danger')
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')

        return redirect(url_for('manage_passwords'))

    return render_template('file.html')

@app.route('/manage_passwords', methods=['GET', 'POST'])
def manage_passwords():
    if request.method == 'POST':
        action = request.form.get('action')

        try:
            if action == 'add':
                site = request.form.get('site')
                password = request.form.get('password')
                pm.add_password(site, password)
                flash('Password added successfully!', 'success')
            elif action == 'get':
                site = request.form.get('site')
                password = pm.get_password(site)
                flash('Password retrieved successfully!', 'success')
                return render_template('manage_passwords.html', retrieved_password=password)
            else:
                flash('Invalid action!', 'danger')
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')

    return render_template('manage_passwords.html')

if __name__ == '__main__':
    app.run(debug=True)