from flask import Flask, jsonify, request
# from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLAlchemy_DATABASE_URl'] = 'sqlite:///reports.db'
# api = Api(app)

db = SQLAlchemy(app)


# Создаем таблицу в базе данных
class Reportings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    servis = db.Column(db.String(100))
    report = db.Column(db.String(5000))

    def __init__(self, name, servis, report):
        self.name = name
        self.servis = servis
        self.report = report


with app.app_context():
    db.create_all()


# Метод для добавления репорта
@app.route('/add_report', methods=['POST'])
def add_report():
    name = request.form['name']
    servis = request.form['servis']
    report = request.form['report']
    rep = Reportings(name, servis, report)
    db.session.add(rep)
    db.session.commit()
    return jsonify({'message': 'Report added successfully'})


# Метод для получения отчетов по № id
@app.route('/viewing_report_fitler_id/<int:id>')
def viewing_report_fitler_id(id):
    report = Reportings.query.get(id)
    if report:
        return jsonify({
            'id': report.id,
            'name': report.name,
            'servis': report.servis,
            'report': report.report
        })
    else:
        return {'error': 'There is no such ID in the list of reports'}


# Метод для получения всех репортов
@app.route('/viewing_report', methods=['GET'])
def viewing_report():
    reports = Reportings.query.all()
    response = []
    for report in reports:
        response.append({
            'id': report.id,
            'name': report.name,
            'servis': report.servis,
            'report': report.report
        })
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
