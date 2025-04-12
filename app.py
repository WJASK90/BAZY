import customtkinter as ctk

def add_author():
    print("Dodanie autora kliknięte!")

if __name__ == '__main__':
    ctk.set_appearance_mode('dark') #ciemny wyglad
    app = ctk.CTk()
    app.title = 'Biblioteka' #nazwa
    app.geometry('1024x700') #rozdzielczosc

    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(1, weight=1)

    menu_bar = ctk.CTkFrame(app, corner_radius=20)
    menu_bar.grid_columnconfigure(0, weight=1)
    menu_bar.grid(row=0, column=0, sticky='ew', padx=10, pady=10)

    app_title = ctk.CTkLabel(menu_bar, text='Biblioteka', font=ctk.CTkFont(size=15, weight='bold')) #pogrubiony tekst i rozmiar
    app_title.grid(row=0, column=0, padx=10, pady=10)

    add_author_button = ctk.CTkButton(menu_bar, text='Dodaj autora', command=add_author) #command czyli ze zadzieje sie funkcja po kliknieciu na przycisku
    add_author_button.grid(row=0, column=1, padx=10, pady=10)

    app.mainloop()