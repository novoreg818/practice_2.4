import tkinter as tk
from tkinter import messagebox
import requests
from io import BytesIO
from PIL import Image, ImageTk
import threading


def poluchit_kartinku(url_api, klyuch_json):
    knopka_kot.config(state=tk.DISABLED)
    knopka_sobaka.config(state=tk.DISABLED)
    metka_kartinka.config(text="Загрузка картинки...", image="")

    threading.Thread(target=potok_zagruzki, args=(url_api, klyuch_json), daemon=True).start()


def potok_zagruzki(url_api, klyuch_json):
    try:
        otvet_api = requests.get(url_api, timeout=10)

        if otvet_api.status_code == 200:
            dannie = otvet_api.json()

            if isinstance(dannie, list):
                url_kartinki = dannie[0][klyuch_json]
            else:
                url_kartinki = dannie[klyuch_json]

            otvet_kartinka = requests.get(url_kartinki, timeout=10)
            kartinka_bayty = Image.open(BytesIO(otvet_kartinka.content))

            kartinka_bayty.thumbnail((450, 450))
            kartinka_tk = ImageTk.PhotoImage(kartinka_bayty)

            okno.after(0, ustanovit_kartinku, kartinka_tk)
        else:
            okno.after(0, lambda: messagebox.showerror("Ошибка", f"Ошибка сервера: {otvet_api.status_code}"))
            okno.after(0, sbros_sostoyaniya)

    except requests.exceptions.RequestException:
        okno.after(0, lambda: messagebox.showerror("Ошибка", "Ошибка соединения с интернетом."))
        okno.after(0, sbros_sostoyaniya)
    except Exception:
        okno.after(0, lambda: messagebox.showerror("Ошибка", "Произошла непредвиденная ошибка."))
        okno.after(0, sbros_sostoyaniya)


def ustanovit_kartinku(kartinka):
    metka_kartinka.config(image=kartinka, text="")
    metka_kartinka.image = kartinka
    knopka_kot.config(state=tk.NORMAL)
    knopka_sobaka.config(state=tk.NORMAL)


def sbros_sostoyaniya():
    metka_kartinka.config(text="Не удалось загрузить картинку. Попробуйте еще раз.")
    knopka_kot.config(state=tk.NORMAL)
    knopka_sobaka.config(state=tk.NORMAL)


def zapros_kota():
    poluchit_kartinku("https://api.thecatapi.com/v1/images/search", "url")


def zapros_sobaki():
    poluchit_kartinku("https://dog.ceo/api/breeds/image/random", "message")


okno = tk.Tk()
okno.title("Коты и Собаки")
okno.geometry("500x550")
okno.resizable(False, False)

freym_knopok = tk.Frame(okno)
freym_knopok.pack(pady=20)

knopka_kot = tk.Button(freym_knopok, text="Получить кота", font=("Arial", 12), command=zapros_kota, width=15)
knopka_kot.grid(row=0, column=0, padx=10)

knopka_sobaka = tk.Button(freym_knopok, text="Получить собаку", font=("Arial", 12), command=zapros_sobaki, width=15)
knopka_sobaka.grid(row=0, column=1, padx=10)

metka_kartinka = tk.Label(okno, text="Нажмите на кнопку, чтобы увидеть питомца!", font=("Arial", 12))
metka_kartinka.pack(expand=True, pady=10)

okno.mainloop()