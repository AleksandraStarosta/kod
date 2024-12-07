import tkinter as tk
from tkinter import messagebox
import sqlite3

# Функция для подключения к базе данных и создания таблицы
def connect_db():
    conn = sqlite3.connect('patients.db')  # Создаём базу данных или подключаемся к существующей
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS patients (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        surname TEXT,
                        dob TEXT,
                        gender TEXT,
                        address TEXT,
                        phone TEXT)''')  # Создаём таблицу, если она не существует
    conn.commit()
    return conn

# Функция для сохранения данных в базе данных
def save_to_db(name, surname, dob, gender, address, phone):
    conn = connect_db()  # Подключаемся к базе данных
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO patients (name, surname, dob, gender, address, phone)
                      VALUES (?, ?, ?, ?, ?, ?)''', (name, surname, dob, gender, address, phone))
    conn.commit()
    conn.close()

# Функция для обработки отправки формы
def submit_form():
    # Считываем введённые данные
    name = entry_name.get()
    surname = entry_surname.get()
    dob = entry_dob.get()
    gender = gender_var.get()
    address = entry_address.get()
    phone = entry_phone.get()

    # Проверка на пустые поля
    if not all([name, surname, dob, gender, address, phone]):
        messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
        return

    # Сохраняем данные в базу данных
    save_to_db(name, surname, dob, gender, address, phone)

    # Выводим данные (можно заменить на сохранение в базу данных)
    print(f"Имя: {name}")
    print(f"Фамилия: {surname}")
    print(f"Дата рождения: {dob}")
    print(f"Пол: {gender}")
    print(f"Адрес: {address}")
    print(f"Телефон: {phone}")
    
    messagebox.showinfo("Успех", "Регистрация прошла успешно!")

# Функция для получения списка всех пациентов из базы данных
def get_all_patients():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, surname, dob, gender, address, phone FROM patients")
    patients = cursor.fetchall()
    conn.close()
    return patients

# Функция для отображения всех пациентов
def show_patients():
    patients = get_all_patients()
    
    # Создание нового окна для вывода списка пациентов
    window = tk.Toplevel(root)
    window.title("Список всех пациентов")
    window.geometry("600x400")
    
    # Заголовки таблицы
    headers = ["ID", "Имя", "Фамилия", "Дата Рождения", "Пол", "Адрес", "Телефон"]
    for col, header in enumerate(headers):
        tk.Label(window, text=header, font=("Arial", 12, "bold")).grid(row=0, column=col, padx=10, pady=10)

    # Заполнение таблицы данными из базы
    for row, patient in enumerate(patients, start=1):
        for col, data in enumerate(patient):
            tk.Label(window, text=data, font=("Arial", 12)).grid(row=row, column=col, padx=10, pady=5)

# Создание главного окна
root = tk.Tk()
root.title("Регистрация пациента")

# Устанавливаем размер окна
root.geometry("400x500")
root.config(bg="lightyellow")  # Цвет фона для окна

# Создание основного фрейма для блока формы
frame = tk.Frame(root, padx=20, pady=20, bg="lightyellow")
frame.pack(padx=10, pady=10)

# Заголовок формы
title_label = tk.Label(frame, text="Регистрация пациента", font=("Arial", 16, "bold"), bg="lightyellow")
title_label.grid(row=0, column=0, columnspan=2, pady=10)

# Имя
tk.Label(frame, text="Имя:", bg="lightyellow").grid(row=1, column=0, sticky="w", padx=10, pady=5)
entry_name = tk.Entry(frame)
entry_name.grid(row=1, column=1, padx=10, pady=5)

# Фамилия
tk.Label(frame, text="Фамилия:", bg="lightyellow").grid(row=2, column=0, sticky="w", padx=10, pady=5)
entry_surname = tk.Entry(frame)
entry_surname.grid(row=2, column=1, padx=10, pady=5)

# Дата рождения
tk.Label(frame, text="Дата рождения (ДД/ММ/ГГГГ):", bg="lightyellow").grid(row=3, column=0, sticky="w", padx=10, pady=5)
entry_dob = tk.Entry(frame)
entry_dob.grid(row=3, column=1, padx=10, pady=5)

# Пол
tk.Label(frame, text="Пол:", bg="lightyellow").grid(row=4, column=0, sticky="w", padx=10, pady=5)
gender_var = tk.StringVar()

gender_male = tk.Radiobutton(frame, text="Мужской", variable=gender_var, value="Мужской", bg="lightyellow")
gender_male.grid(row=4, column=1, padx=10, pady=5, sticky="w")

gender_female = tk.Radiobutton(frame, text="Женский", variable=gender_var, value="Женский", bg="lightyellow")
gender_female.grid(row=4, column=1, padx=10, pady=5, sticky="e")

# Адрес
tk.Label(frame, text="Адрес:", bg="lightyellow").grid(row=5, column=0, sticky="w", padx=10, pady=5)
entry_address = tk.Entry(frame)
entry_address.grid(row=5, column=1, padx=10, pady=5)

# Телефон
tk.Label(frame, text="Телефон:", bg="lightyellow").grid(row=6, column=0, sticky="w", padx=10, pady=5)
entry_phone = tk.Entry(frame)
entry_phone.grid(row=6, column=1, padx=10, pady=5)

# Кнопка для отправки формы
submit_button = tk.Button(frame, text="Зарегистрировать", command=submit_form, width=20, height=2, bg="lightgreen")
submit_button.grid(row=7, column=0, columnspan=2, pady=20)

# Кнопка для отображения всех пациентов
show_button = tk.Button(frame, text="Показать всех пациентов", command=show_patients, width=20, height=2, bg="lightblue")
show_button.grid(row=8, column=0, columnspan=2, pady=10)

# Запуск приложения
root.mainloop()


