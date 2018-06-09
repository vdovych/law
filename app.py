from flask import Flask, render_template, request, redirect, send_from_directory
from flaskext.mysql import MySQL
from flask_dropzone import Dropzone
from datetime import datetime
import locale
import os

app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'law'

sql = MySQL()

sql.init_app(app)

dropzone = Dropzone(app)

app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
app.config['DROPZONE_MAX_FILE_SIZE'] = 100
app.config['DROPZONE_DEFAULT_MESSAGE'] = "Щоб додати документи, натисніть або перетягніть файли"

locale.setlocale(locale.LC_ALL, 'uk_UA.utf8')

def sql_connection():    
    connection = sql.get_db()
    cursor = connection.cursor()
    return connection, cursor

def form():
    fields = [
        'name', 'name1', 'date', 'ask', 'birth', 'sex', 
        'address', 'phone', 'email', 'social', 'job', 
        'media', 'queue', 'law', 'about', 'help', 'student', 
        'open', 'close', 'stage', 'present', 'result', 'appeal', 
        'client', 'info', 'comment'
    ]

    requests = ()

    for field in fields:
        requests += (request.form[field], )

    return requests, fields

def change_date(date):
    return datetime.strptime(str(date), '%Y-%m-%d').strftime('%d %B %Y')

@app.route('/')
def main():
    connection, cursor = sql_connection()

    cursor.execute('SELECT id, name from cases')
    data = cursor.fetchall()
   
    return render_template('index.html', data=data)

@app.route('/case/<id>')
def case(id):
    connection, cursor = sql_connection()

    cursor.execute('SELECT * from cases WHERE id=%s', (id))
    data = list(cursor.fetchall()[0])
    fields =  [
        'Номер звернення', 'ПІП клієнта', 'ПІП особи яка звертається', 'Дата звернення', 'Спосіб звернення', 
        'Дата народження', 'Стать', 'Телефон', 'Електронна адреса', 'Місце проживання', 'Соціальний статус', 
        'Робота', 'Звідки дізналися', 'Черговість звернення', 'Галузь права', 'Суть звернення', 'Допомога', 
        'Консультанти', 'Дата відкриття справи', 'Дата закриття справи', 'Стадія розгляду справи', 'Cудове представництво', 
        'Результат', 'Спосіб оскарження', 'Характеристика клієнта', 'Додаткова інформація', 'Комментарі'
    ]

    data[fields.index('Дата народження')] = change_date(data[fields.index('Дата народження')])
    data[fields.index('Дата звернення')] = change_date(data[fields.index('Дата звернення')])

    files = [file for file in os.listdir('uploads') if file.split('_', 1)[0] == str(id)]
  
    return render_template('case.html', data=data, fields=fields, files=files)

@app.route('/download/<path>', methods=['GET'])
def download(path):
    return send_from_directory('uploads', path, as_attachment=True, attachment_filename=path.split('_', 1)[-1])

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    connection, cursor = sql_connection()

    if request.method == 'POST':
        if 'form' in request.form:
            requests, fields = form()
            requests += (id, )
            query = 'UPDATE cases SET ' + '=%s, '.join(fields) + '=%s ' + 'WHERE id=%s'
            cursor.execute(query, requests)
            connection.commit()
        else:
            for key, file in request.files.items():
                if key.startswith('file'):
                    file.save(os.path.join('uploads', str(id) + '_' + file.filename))

        return redirect('/case/' + id)
    
    cursor.execute('SELECT * from cases WHERE id=%s', (id))
    data = cursor.fetchall()[0]
   
    return render_template('edit.html', data=data, i=1)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        connection, cursor = sql_connection()
        cursor.execute('SELECT max(id) from cases')

        id = cursor.fetchall()[0][0]
        if id is not None:
            id += 1
        else:
            id = 1

        if 'form' in request.form:
            requests, fields = form()
           
            query = 'INSERT INTO cases(' + ', '.join(fields) + ') VALUES(' + ', '.join('%s' for i in range(len(fields))) + ')'
    
            cursor.execute(query, requests)
            connection.commit()
        else:
            for key, file in request.files.items():
                if key.startswith('file'):
                    file.save(os.path.join('uploads', str(id) + '_' + file.filename))

        return redirect('/')

    return render_template('add.html', now=datetime.now().strftime('%Y-%m-%d'))

@app.route('/remove-file/<path>')
def remove_file(path):
    id = path.split('_', 1)[0]
    os.remove(os.path.join('uploads', path))
    return redirect('/case/' + id)

@app.route('/remove/<id>')
def remove(id):
    connection, cursor = sql_connection()
    cursor.execute('DELETE from cases WHERE id=%s', (id))
    connection.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run()
