from flask import Flask, render_template, request, redirect

from flaskext.mysql import MySQL

app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'law'

sql = MySQL()

sql.init_app(app)


@app.route('/')
def main():
    connection = sql.get_db()
    cursor = connection.cursor()
    
    cursor.execute('SELECT id, name from cases')
    data = cursor.fetchall()
   
    return render_template('index.html', data=data)

@app.route('/case/<id>')
def case(id):
    connection = sql.get_db()
    cursor = connection.cursor()

    cursor.execute('SELECT * from cases WHERE id=%s', (id))
    data = cursor.fetchall()
    fields = [
        'Номер звернення', 'Прізвище, ім\'я та по батькові', 'Спосіб звернення', 
        'Стать', 'Місце проживання', 'Соціальний статус', 'Робота', 'Суть звернення'
    ]
    return render_template('case.html', data=data, fields=fields)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        fields = ['name', 'ask', 'sex', 'address', 'social', 'job', 'about']

        requests = ()
        for field in fields:
            requests += (request.form[field], )
        connection = sql.get_db()
        cursor = connection.cursor()

        query = 'INSERT INTO cases(' + ', '.join(fields) + ') VALUES(' + ', '.join('%s' for i in range(len(fields))) + ')'
    
        cursor.execute(query, requests)
        connection.commit()
        return redirect('/')

    return render_template('add.html')

if __name__ == '__main__':
    app.run()
