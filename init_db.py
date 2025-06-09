from app import app, db

# Создание всех таблиц в базе данных
with app.app_context():
    db.create_all()

print("База данных и таблицы успешно созданы!")
