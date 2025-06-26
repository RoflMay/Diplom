import os
from flask import Flask, render_template, request, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from wtforms import BooleanField
from wtforms.widgets import CheckboxInput
from markupsafe import Markup
from flask_babel import Babel

app = Flask(__name__)

# Настройки для SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

# Локализация на русский язык
app.config['BABEL_DEFAULT_LOCALE'] = 'ru'
babel = Babel(app)

# Инициализация базы данных
db = SQLAlchemy(app)

# Модель для проектов
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Project {self.title}>"

# Модель для консультаций
class Consultation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Consultation {self.name}, {self.phone}>"

# Модель для услуг
class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    page_name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<Service {self.title}>"

# Формы для админ панели
class ProjectForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    image_url = StringField('URL изображения', validators=[DataRequired()])
    category = SelectField('Категория', choices=[('residential', 'Жилые'), ('commercial', 'Коммерческие')], validators=[DataRequired()])

class PrettyCheckbox(CheckboxInput):
    def __call__(self, field, **kwargs):
        html = f'''
        <div style="display: flex; align-items: center; gap: 8px;">
            <input type="checkbox" name="{field.name}" {'checked' if field.data else ''} id="{field.id}" style="width: 18px; height: 18px;">
            <label for="{field.id}" style="margin: 0;">{field.label.text if hasattr(field, 'label') else ''}</label>
        </div>
        '''
        return Markup(html)

class ServiceForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    description = TextAreaField(
        'Описание',
        validators=[DataRequired()],
        render_kw={"rows": 10, "style": "resize: vertical; min-height: 200px;"}
    )
    icon = StringField('Иконка (URL)', validators=[DataRequired()])
    page_name = StringField('Название страницы (например: works)', validators=[DataRequired()])
    is_active = BooleanField('Активна', widget=PrettyCheckbox())

# Кастомный индекс для админки
class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return redirect('/superpanel/project/')

# Кастомные представления моделей
class ProjectModelView(ModelView):
    form = ProjectForm
    form_columns = ['title', 'description', 'image_url', 'category']
    column_labels = {
        'title': 'Название',
        'description': 'Описание',
        'image_url': 'Изображение',
        'category': 'Категория'
    }
    def _category_formatter(view, context, model, name):
        return 'Жилые' if model.category == 'residential' else 'Коммерческие'
    column_formatters = {
        'category': _category_formatter
    }

class ServiceModelView(ModelView):
    form = ServiceForm
    form_columns = ['title', 'description', 'icon', 'page_name', 'is_active']
    column_labels = {
        'title': 'Название',
        'description': 'Описание',
        'icon': 'Иконка',
        'page_name': 'Название страницы',
        'is_active': 'Активна'
    }

    def on_model_change(self, form, model, is_created):
        super().on_model_change(form, model, is_created)
        if is_created:
            templates_dir = os.path.join(app.root_path, 'templates', 'services')
            os.makedirs(templates_dir, exist_ok=True)

            file_path = os.path.join(templates_dir, f'{model.page_name}.html')

            if not os.path.exists(file_path):
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>{{{{ service.title }}}}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="{{{{ url_for('static', filename='css/style.css') }}}}">
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-dark custom-navbar">
  <div class="container">
    <a class="navbar-brand" href="{{{{ url_for('index') }}}}">Строительная организация “Чериковская ПМК-280”</a>
    <div>
      <ul class="navbar-nav me-auto mb-2 mb-lg-0 d-flex flex-row gap-3">
        <a class="nav-link" href="{{{{ url_for('index') }}}}">Главная</a>
        <a class="nav-link" href="{{{{ url_for('about') }}}}">О компании</a>
        <a class="nav-link" href="{{{{ url_for('services') }}}}">Услуги</a>
        <a class="nav-link" href="{{{{ url_for('projects') }}}}">Проекты</a>
        <a class="nav-link" href="{{{{ url_for('contact') }}}}">Контакты</a>
        <li class="nav-item">
        <img id="toggleAccessibility"
        src="{{{{ url_for('static', filename='icons/eye.png') }}}}"
        alt="Версия для слабовидящих"
        title="Версия для слабовидящих"
        style="cursor:pointer; width: 33px; margin-top: 4px;">
        </li>
      </ul>
    </div>
  </div>
</nav>

<div class="container mt-5">
  <h1 class="mb-4 text-center">{{{{ service.title }}}}</h1>
  <p class="lead" style="white-space: pre-line; text-align: justify;">{{{{ service.description }}}}</p>
  <div class="text-center mt-4">
    <a href="{{{{ url_for('services') }}}}" class="btn btn-secondary">← Назад к услугам</a>
  </div>
</div>

</body>
</html>""")


    def on_model_delete(self, model):
        file_path = os.path.join(app.root_path, 'templates', 'services', f'{model.page_name}.html')
        if os.path.exists(file_path):
            os.remove(file_path)
        super().on_model_delete(model)

class ConsultationModelView(ModelView):
    column_labels = {
        'name': 'Имя',
        'phone': 'Телефон'
    }

# Настройка админ панели
admin = Admin(app, name='Админ панель', index_view=MyAdminIndexView(), template_mode='bootstrap3', url='/superpanel')
admin.add_view(ProjectModelView(Project, db.session, name='Проекты'))
admin.add_view(ConsultationModelView(Consultation, db.session, name='Консультации'))
admin.add_view(ServiceModelView(Service, db.session, name='Услуги'))

# Роуты
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    if username == "admin" and password == "1234":
        return redirect("/superpanel")
    return redirect(request.referrer or "/")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    services = Service.query.all()
    return render_template('services.html', services=services)

@app.route('/services/<page_name>')
def service_page(page_name):
    service = Service.query.filter_by(page_name=page_name, is_active=True).first()
    if not service:
        abort(404)
    template_file = f'services/{page_name}.html'
    return render_template(template_file, service=service)

@app.route('/projects', methods=['GET'])
def projects():
    category = request.args.get('category', '')
    if category:
        projects = Project.query.filter_by(category=category).all()
    else:
        projects = Project.query.all()
    return render_template('projects.html', projects=projects)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit_consultation', methods=['POST'])
def submit_consultation():
    name = request.form['name']
    phone = request.form['phone']
    consultation = Consultation(name=name, phone=phone)
    db.session.add(consultation)
    db.session.commit()
    return redirect(url_for('index', success=1))

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
