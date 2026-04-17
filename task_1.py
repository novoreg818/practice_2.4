import tkinter as tk
from tkinter import messagebox, ttk
import requests
from io import BytesIO
from PIL import Image, ImageTk
import threading


def poluchit_pogodu():
    zapros = vvod_goroda.get().strip()

    if not zapros:
        messagebox.showwarning("Внимание", "Пожалуйста, введите название города.")
        return

    vibor_mer = combo_mer.get()
    if vibor_mer == "Цельсии (metric)":
        sistema_mer = "metric"
        znak = "°C"
    elif vibor_mer == "Фаренгейты (imperial)":
        sistema_mer = "imperial"
        znak = "°F"
    else:
        sistema_mer = "standard"
        znak = "K"

    vibor_yazyka = combo_yazyk.get()
    if vibor_yazyka == "Русский":
        yazyk = "ru"
    else:
        yazyk = "en"

    knopka_poisk.config(state=tk.DISABLED)
    metka_temperatura.config(text="Загрузка данных...")

    threading.Thread(target=potok_pogody, args=(zapros, sistema_mer, znak, yazyk), daemon=True).start()


def potok_pogody(zapros, sistema_mer, znak, yazyk):
    api_klyuch = "8e700964cf44f16e2a038514902ae5ad"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={zapros}&appid={api_klyuch}&units={sistema_mer}&lang={yazyk}"

    try:
        otvet = requests.get(url, timeout=5)

        if otvet.status_code == 200:
            dannie = otvet.json()
            temperatura = dannie["main"]["temp"]
            opisanie = dannie["weather"][0]["description"].capitalize()
            kod_ikonki = dannie["weather"][0]["icon"]

            okno.after(0, lambda: metka_temperatura.config(text=f"Температура: {temperatura} {znak}\n{opisanie}"))

            url_ikonki = f"http://openweathermap.org/img/wn/{kod_ikonki}@2x.png"
            otvet_ikonka = requests.get(url_ikonki, timeout=5)

            kartinka = Image.open(BytesIO(otvet_ikonka.content))
            kartinka_tk = ImageTk.PhotoImage(kartinka)

            def ustanovit_ikonku(izobrazhenie):
                metka_ikonka.config(image=izobrazhenie)
                metka_ikonka.image = izobrazhenie

            okno.after(0, ustanovit_ikonku, kartinka_tk)

        elif otvet.status_code == 404:
            okno.after(0, lambda: messagebox.showerror("Ошибка", "Город не найден. Проверьте правильность написания."))
            okno.after(0, Sbrosit_tekst)
        elif otvet.status_code == 401:
            okno.after(0, lambda: messagebox.showerror("Ошибка", "Неверный API ключ."))
            okno.after(0, Sbrosit_tekst)
        else:
            okno.after(0, lambda: messagebox.showerror("Ошибка", f"Проблема на сервере. Код: {otvet.status_code}"))
            okno.after(0, Sbrosit_tekst)

    except requests.exceptions.RequestException:
        okno.after(0, lambda: messagebox.showerror("Ошибка", "Отсутствует подключение к интернету!"))
        okno.after(0, Sbrosit_tekst)
    except Exception:
        okno.after(0, lambda: messagebox.showerror("Ошибка", "Произошла непредвиденная ошибка."))
        okno.after(0, Sbrosit_tekst)
    finally:
        okno.after(0, lambda: knopka_poisk.config(state=tk.NORMAL))


def Sbrosit_tekst():
    metka_temperatura.config(text="Температура: --")


okno = tk.Tk()
okno.title("Погода OpenWeather PRO")
okno.geometry("450x450")
okno.resizable(False, False)

tk.Label(okno, text="Введите город (можно в формате Город,Код страны):", font=("Arial", 11)).pack(pady=(15, 5))

vvod_goroda = tk.Entry(okno, font=("Arial", 12), width=25)
vvod_goroda.pack(pady=5)
vvod_goroda.insert(0, "Москва,RU")

freym_nastroyki = tk.Frame(okno)
freym_nastroyki.pack(pady=10)

tk.Label(freym_nastroyki, text="Единицы:").grid(row=0, column=0, padx=5)
combo_mer = ttk.Combobox(freym_nastroyki, values=["Цельсии (metric)", "Фаренгейты (imperial)", "Кельвины (standard)"],
                         state="readonly", width=20)
combo_mer.current(0)
combo_mer.grid(row=0, column=1, padx=5)

tk.Label(freym_nastroyki, text="Язык:").grid(row=1, column=0, padx=5, pady=5)
combo_yazyk = ttk.Combobox(freym_nastroyki, values=["Русский", "English"], state="readonly", width=20)
combo_yazyk.current(0)
combo_yazyk.grid(row=1, column=1, padx=5, pady=5)

knopka_poisk = tk.Button(okno, text="Узнать погоду", font=("Arial", 12), command=poluchit_pogodu)
knopka_poisk.pack(pady=15)

metka_temperatura = tk.Label(okno, text="Температура: --", font=("Arial", 14))
metka_temperatura.pack(pady=10)

metka_ikonka = tk.Label(okno)
metka_ikonka.pack(pady=5)

okno.mainloop()