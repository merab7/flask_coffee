from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, SelectField
from wtforms.validators import DataRequired 
import csv



app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

class CafeForm(FlaskForm):
    cafe_name = StringField('Cafe name', validators=[DataRequired()])
    cafe_location = StringField('Cafe location on google map(url)', validators=[DataRequired()])
    cafe_open = StringField('Open Time e.g. 8AM', validators=[DataRequired()])
    cafe_close = StringField('Close Time e.g. 10PM', validators=[DataRequired()])
    cafe_qua = SelectField('Coffee Rating', choices=["❌","☕", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"])
    wifi = SelectField('Wifi Strength Rating',choices=["❌","💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"])
    power = SelectField('Power Socket available', choices=["❌","🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"])
    submit = SubmitField('Submit')




# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")



@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = [
            form.cafe_name.data,
            form.cafe_location.data,
            form.cafe_open.data,
            form.cafe_close.data,
            form.cafe_qua.data,
            form.wifi.data,
            form.power.data
        ]

        with open('cafe-data.csv', 'a', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(new_cafe)
        
        return redirect(url_for('cafes'))
    
    return render_template('add.html', form=form)





if __name__ == '__main__':
    app.run(debug=True)
