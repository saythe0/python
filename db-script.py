import tkinter as tk
import sqlite3

# для установки tkinter - pip install tk

# Создаем соединение с базой данных SQLite
conn = sqlite3.connect('data.db')

# Создаем курсор для выполнения SQL-запросов
cursor = conn.cursor()

# Создаем таблицу "Пользователи"
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER
    )
''')

# Создаем таблицу "Задачи"
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Tasks (
        id INTEGER PRIMARY KEY,
        task TEXT,
        user_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES Users(id)
    )
''')

# Функция для добавления нового пользователя в базу данных
def add_user(name, age):
    cursor.execute('INSERT INTO Users (name, age) VALUES (?, ?)', (name, age))
    conn.commit()

# Функция для добавления новой задачи в базу данных
def add_task(task, user_id):
    cursor.execute('INSERT INTO Tasks (task, user_id) VALUES (?, ?)', (task, user_id))
    conn.commit()

# Функция для отображения данных о пользователях
def display_users():
    cursor.execute('SELECT * FROM Users')
    users = cursor.fetchall()
    text_users.delete('1.0', tk.END)  # Очистка текстового поля перед выводом новых данных
    for user in users:
        text_users.insert(tk.END, f"ID: {user[0]}, Имя: {user[1]}, Возраст: {user[2]}\n")

# Функция для отображения данных о задачах
def display_tasks():
    cursor.execute('SELECT * FROM Tasks')
    tasks = cursor.fetchall()
    text_tasks.delete('1.0', tk.END)  # Очистка текстового поля перед выводом новых данных
    for task in tasks:
        text_tasks.insert(tk.END, f"ID: {task[0]}, Задача: {task[1]}, ID пользователя: {task[2]}\n")

# Функция для обработки события добавления нового пользователя
def add_user_handler():
    name = entry_name.get()
    age = entry_age.get()
    add_user(name, age)
    display_users()  # После добавления пользователя обновляем данные на экране
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)

# Функция для обработки события добавления новой задачи
def add_task_handler():
    task = entry_task.get()
    user_id = int(entry_user_id.get())
    add_task(task, user_id)
    display_tasks()  # После добавления задачи обновляем данные на экране
    entry_task.delete(0, tk.END)
    entry_user_id.delete(0, tk.END)

# Создаем графический интерфейс с использованием библиотеки tkinter
window = tk.Tk()
window.title("Простое приложение")

label = tk.Label(window, text="Привет, это простое приложение!")
label.pack()

# Поля для ввода данных о пользователе
tk.Label(window, text="Имя:").pack()
entry_name = tk.Entry(window)
entry_name.pack()

tk.Label(window, text="Возраст:").pack()
entry_age = tk.Entry(window)
entry_age.pack()

button_add_user = tk.Button(window, text="Добавить пользователя", command=add_user_handler)
button_add_user.pack()

# Поля для ввода данных о задаче
tk.Label(window, text="Задача:").pack()
entry_task = tk.Entry(window)
entry_task.pack()

tk.Label(window, text="ID пользователя:").pack()
entry_user_id = tk.Entry(window)
entry_user_id.pack()

button_add_task = tk.Button(window, text="Добавить задачу", command=add_task_handler)
button_add_task.pack()

# Текстовые поля для вывода данных
text_users = tk.Text(window, width=50, height=10)
text_users.pack()

text_tasks = tk.Text(window, width=50, height=10)
text_tasks.pack()

# Кнопки для отображения данных о пользователях и задачах
button_display_users = tk.Button(window, text="Отобразить пользователей", command=display_users)
button_display_users.pack()

button_display_tasks = tk.Button(window, text="Отобразить задачи", command=display_tasks)
button_display_tasks.pack()

window.mainloop()

# Закрываем соединение с базой данных при закрытии приложения
conn.close()
