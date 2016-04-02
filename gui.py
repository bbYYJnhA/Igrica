﻿import tkinter
import tkinter as tk
from tkinter import ttk
from igra import*
from clovek import*
from racunalnik import*

CRNA = 1
BELA = 2

class Gui():

    def __init__(self, master):
        self.igra = Igra(self)
        
        self.napis1 = tkinter.StringVar(master, value="Dobrodošli v 五子棋")
        tkinter.Label(master, textvariable=self.napis1).grid(row=0, column=0)

        self.napis2 = tkinter.StringVar(master, value="Na potezi je črni")
        tkinter.Label(master, textvariable=self.napis2).grid(row=42, column=0)

        self.plosca = tkinter.Canvas(master, width=648+36+36, height=648+36+36, bg = "lightblue", borderwidth=0)
        self.plosca.grid(row=1, column=0, columnspan=1, rowspan=41)

        self.gumb1 = tkinter.Button(master, text="Nova igra", command=self.nova_igra_gumb)
        self.gumb1.grid(row=1, column=1)

        self.plosca.bind('<Button-1>', self.klik_plosca)
        
        # Glavni meni
        menu = tkinter.Menu(master)
        master.config(menu=menu)

        # Podmeni Igra
        menu_igra = tkinter.Menu(menu)
        menu.add_cascade(label="Igra", menu=menu_igra)
        menu_igra.add_command(label="Nova igra", command=self.nova_igra_gumb)
        menu_igra.add_command(label="Izhod", command=master.destroy)

        for i in range(19):
            self.plosca.create_line(i*36+36, 0+36, i*36+36, 648+36)
            self.plosca.create_line(0+36, i*36+36, 648+36, i*36+36)
        
        self.igralec1 = Clovek(self, Alfabeta(2), CRNI)
        self.igralec2 = Racunalnik(self, Alfabeta(2), BELI)
        self.klik = None
        self.konec = False
        self.igralec1.igraj()

    def sporocilo(self, msg, naslov):
        """
        Funkcija odpre novo okno, z vsebino sporočina in naslovom podanim v funkciji.
        """
        popup = tkinter.Tk()
        #popup.grab_set()
        popup.wm_title(naslov)
        label = ttk.Label(popup, text=msg)
        label.pack(side="top", fill="x", pady=20)
        popup.mainloop()

    def nova_igra(self, igralec1, igralec2, tezavnost_crni=2, tezavnost_beli=2):
        """
        Funkcija prekine že obstoječo igro in nastavi novo glede na parametre,
        ki jih naklika uporabnik v gui.
        """
        if self.igralec1 is not None:
            self.igralec1.prekini()
        if self.igralec2 is not None:
            self.igralec2.prekini()
        #self.igralec1 = igralec1(self, )
        #aplikacija = Gui(root)        
        self.igralec1 = igralec1(self, Alfabeta(tezavnost_crni), CRNI)
        self.igralec2 = igralec2(self, Alfabeta(tezavnost_beli), BELI)
        self.klik = None
        self.konec = False
        self.igra = Igra(self)        
        
        self.plosca.delete("figure")
        self.plosca.delete("crta")
        self.napis2.set("Na potezi je ČRNI")
        self.igralec1.igraj()

    def nova_igra_gumb(self):
        """Ustvari okno za izbiro nastavitev nove igre (če ne obstaja) ter začne novo igro, z izbranimi nastavitvami."""

        def ustvari_igro():
            """Pomožna funkcija, ki ustvari novo igro, nastavi ime igralcev ter zapre okno za izbiro nastavitev."""
            if igralec_1_clovek.get():
                igralec_1 = Clovek
            else:
                igralec_1 = Racunalnik
            if igralec_2_clovek.get():
                igralec_2 = Clovek
            else:
                igralec_2 = Racunalnik
            self.nova_igra(igralec_1, igralec_2, tezavnost_crni.get(), tezavnost_beli.get())
            new_game.destroy()

        # Ustvari novo okno za izbiro nastavitev nove igre.
        new_game = tk.Toplevel()
        new_game.grab_set()                                   # Postavi fokus na okno in ga obdrži
        new_game.title("Nova igra")                           # Naslov okna
        #new_game.resizable(width=False, height=False)         # Velikosti okna ni mogoče spreminjati

        new_game.grid_columnconfigure(0, minsize=120)         # Nastavitev minimalne širine ničtega stolpca
        new_game.grid_columnconfigure(2, minsize=150)         # Nastavitev minimalne širine drugega stolpca
        new_game.grid_rowconfigure(0, minsize=80)             # Nastavitev minimalne višine ničte vrstice
        new_game.grid_rowconfigure(5, minsize=70)             # Nastavitev minimalne višine pete vrstice
        new_game.grid_rowconfigure(9, minsize=80)             # Nastavitev minimalne višine devete vrstice

        tk.Label(new_game, text="Nastavitve nove igre", font=("Helvetica", 20)).grid(row=0, column=0, columnspan=4)

        # Nastavitve težavnosti
        # ---------------------------------------------------------
        #tk.Label(new_game, text="Izberite težavnost:").grid(row=1, column=1, sticky="W")
        tezavnosti = [("Težko", 4) ,("Srednje", 2), ("Lahko", 1)]  # Možne težavnosti
        izbrana_tezavnost = tk.IntVar()                            # Spremenljivka kamor shranimo izbrano težavnost
        izbrana_tezavnost.set(2)                                   # Nastavitev privzete vrednosti

        # Ustvari radijske gumbe za izbrio težavnosti:
        #for vrstica, (besedilo, vrednost) in enumerate(tezavnosti):
        #    tk.Radiobutton(new_game, text=besedilo, variable=izbrana_tezavnost, value=vrednost, width=10,
        #                   anchor="w").grid(row=vrstica + 2, column=1)
        # ---------------------------------------------------------

        # Nastavitve igralcev
        # ---------------------------------------------------------
        tk.Label(new_game, text="ČRNI", font=("Helvetica", 13)).grid(row=2, column=0, sticky="E")
        tk.Label(new_game, text="BELI", font=("Helvetica", 13)).grid(row=2, column=2, sticky="E")
        tk.Label(new_game, text="Vrsta igralca:").grid(row=3, column=0, rowspan=2, sticky="E")
        tk.Label(new_game, text="Vrsta igralca:").grid(row=3, column=2, rowspan=2, sticky="E")

        igralec_1_clovek = tk.BooleanVar()                         # Spremenljivka kamor shranimo vrsto prvega igralca
        igralec_1_clovek.set(True)                                 # Privzeta vrednost vrste prvega igralca
        igralec_2_clovek = tk.BooleanVar()                         # Spremenljivka kamor shranimo vrsto drugega igralca
        igralec_2_clovek.set(True)                                 # Privzeta vrednost vrste drugega igralca
        igralci = [("Človek", True, igralec_1_clovek, 4, 1), ("Računalnik", False, igralec_1_clovek, 5, 1),
                   ("Človek", True, igralec_2_clovek, 4, 3), ("Računalnik", False, igralec_2_clovek, 5, 3)]

        # Ustvari radijske gumbe za izbiro vrste igralcev
        for besedilo, vrednost, spremenljivka, vrstica, stolpec in igralci:
            tk.Radiobutton(new_game, text=besedilo, variable=spremenljivka, value=vrednost, width=10, anchor="w")\
                .grid(row=vrstica, column=stolpec)

        # Gumb za izbiro težavnosti
        
        tezavnost_crni = tk.IntVar()
        tezavnost_crni.set(2)        
        tk.Label(new_game, text="Težavnost:").grid(row=6, column=0, rowspan=2, sticky="E")
        skala_crni = tk.Scale(new_game, from_=1, to=3, variable = tezavnost_crni, orient="horizontal")
        skala_crni.grid(row=6, column=1)
        
        tezavnost_beli = tk.IntVar()
        tezavnost_beli.set(2)          
        tk.Label(new_game, text="Težavnost:").grid(row=6, column=2, rowspan=2, sticky="E")
        skala_crni = tk.Scale(new_game, from_=1, to=3, variable = tezavnost_beli, orient="horizontal")
        skala_crni.grid(row=6, column=3)
        #skala.pack(anchor="center")
        # ---------------------------------------------------------

        # Gumba za začetek nove igre in preklic
        tk.Button(new_game, text="Prekliči", width=20, height=2,
                  command=lambda: new_game.destroy()).grid(row=9, column=0, columnspan=3, sticky="E")
        tk.Button(new_game, text="Začni igro", width=20, height=2,
                  command=lambda: ustvari_igro()).grid(row=9, column=3, columnspan=3, sticky="E")
    


    def klik_plosca(self, event):
        """
        Nariše črne oz. bele krogce na polje.
        """
        x = ((event.x + 18) // 36)
        y = ((event.y + 18) // 36)
        if x > 0 and y > 0 and x < 20 and y < 20:
            if self.igra.na_potezi == CRNI:
                self.igralec1.klik(x, y)
            elif self.igra.na_potezi == BELI:
                self.igralec2.klik(x, y)
            else:
                assert False, "Neveljaven igralec klik"
            
    def narisi1(self, i, j):
        """
        Funkcija riše črne krogce.
        """
        x = i * 36
        y = j * 36
        self.plosca.create_oval(x - 18, y - 18, x + 18, y + 18, fill="black", tags="figure")
        
    def narisi2(self, i, j):
        """
        Funkcija riše bele krogce.
        """
        x = i * 36
        y = j * 36
        self.plosca.create_oval(x - 18, y - 18, x + 18, y + 18, fill="white", tags="figure")     

    def narisi_crto(self, kje):
        """
        Funkcija nariše črto, glede na to kje ji podamo začetno in končno koortinato.
        Uporablja se za povezovanje figur zmagovalne kombinacije.
        """
        (y0, x0) = kje[0]
        (y1, x1) = kje[4]
        self.plosca.create_line((x0+1) * 36, (y0+1) * 36, (x1+1) * 36, (y1+1) * 36, fill="red", width="3", tag="crta") 

    def koncaj_igro(self):
        """
        Funkcija konča igro, in začne novo s privzetimi igralci Clovek vs Racunalnik
        """
        aplikacija = Gui(root)
        self.igra = Igra(self)
        self.igralec1 = Clovek(self, Alfabeta(2) , CRNI)
        self.igralec2 = Racunalnik(self, Alfabeta(2), BELI)

    def preveri_zmago(self, j, i):
        """Preveri, če je konec in vrne trojko (Bool, zmagovalec, zmagovalna petorka)"""
        dolzina = len(self.igra.tabela)

        vrstica = i
        for stolpec in range(dolzina-4):
            if self.igra.tabela[vrstica][stolpec] != 0:
                ena = self.igra.tabela[vrstica][stolpec]
                dva = self.igra.tabela[vrstica][stolpec+1]
                tri = self.igra.tabela[vrstica][stolpec+2]
                stiri = self.igra.tabela[vrstica][stolpec+3]
                pet = self.igra.tabela[vrstica][stolpec+4]
                if ena == dva == tri == stiri == pet:
                    self.konec = True
                    return (True, self.igra.na_potezi, \
                            [(vrstica,stolpec),(vrstica,stolpec+1),(vrstica,stolpec+2),(vrstica,stolpec+3),(vrstica,stolpec+4)])

        stolpec = j
        for vrstica in range(dolzina-4):
            if self.igra.tabela[vrstica][stolpec] != 0:
                    ena = self.igra.tabela[vrstica][stolpec]
                    dva = self.igra.tabela[vrstica+1][stolpec]
                    tri = self.igra.tabela[vrstica+2][stolpec]
                    stiri = self.igra.tabela[vrstica+3][stolpec]
                    pet = self.igra.tabela[vrstica+4][stolpec]
                    if ena == dva == tri == stiri == pet:
                        self.konec = True
                        return (True, self.igra.na_potezi,\
                            [(vrstica,stolpec),(vrstica+1,stolpec),(vrstica+2,stolpec),(vrstica+3,stolpec),(vrstica+4,stolpec)])


        for vrstica in range(4, dolzina):
            for stolpec in range(0, dolzina-4):
                if self.igra.tabela[vrstica][stolpec] != 0:
                    ena = self.igra.tabela[vrstica][stolpec]
                    dva = self.igra.tabela[vrstica-1][stolpec+1]
                    tri = self.igra.tabela[vrstica-2][stolpec+2]
                    stiri = self.igra.tabela[vrstica-3][stolpec+3]
                    pet = self.igra.tabela[vrstica-4][stolpec+4]
                    if ena == dva == tri == stiri == pet:
                        self.konec = True   
                        return (True, self.igra.na_potezi,\
                            [(vrstica,stolpec),(vrstica-1,stolpec+1),(vrstica-2,stolpec+2),(vrstica-3,stolpec+3),(vrstica-4,stolpec+4)])   

        for vrstica in range(0, dolzina-4):
            for stolpec in range(0, dolzina-4):
                if self.igra.tabela[vrstica][stolpec] != 0:
                    ena = self.igra.tabela[vrstica][stolpec] 
                    dva = self.igra.tabela[vrstica+1][stolpec+1]
                    tri = self.igra.tabela[vrstica+2][stolpec+2]
                    stiri = self.igra.tabela[vrstica+3][stolpec+3]
                    pet = self.igra.tabela[vrstica+4][stolpec+4]
                    if ena == dva == tri == stiri == pet:
                        self.konec = True
                        return (True, self.igra.na_potezi,\
                            [(vrstica,stolpec),(vrstica+1,stolpec+1),(vrstica+2,stolpec+2),(vrstica+3,stolpec+3),(vrstica+4,stolpec+4)]) 
        return (False, None, None)
        
    def povleci_potezo(self, x, y):
        """
        Funkcija naredi in nariše potezo.
        """
        i = x - 1
        j = y - 1
        if self.igra.pravilna(i, j):
            trenutni = self.igra.na_potezi
            if self.igra.na_potezi == CRNI:
                self.narisi1(x, y)              
                self.igra.povleci(i, j)
                (kaj, kdo, kje) = self.preveri_zmago(i,j)
                if kaj:
                    self.narisi_crto(kje)
                    self.konec = True
                    self.napis2.set("Zmagal je ČRNI")
                    self.sporocilo("     Zmagal je ČRNI     ", "Igre je konec")
                else:
                    self.napis2.set("Na potezi je beli")
                    self.igralec2.igraj()
            elif self.igra.na_potezi == BELI:
                self.narisi2(x, y)              
                self.igra.povleci(i, j)
                (kaj, kdo, kje) = self.preveri_zmago(i,j)
                if kaj:
                    self.narisi_crto(kje)
                    self.konec = True
                    self.napis2.set("Zmagal je BELI")
                    self.sporocilo("     Zmagal je BELI     ", "Igre je konec")
                else:
                    self.napis2.set("Na potezi je črni")
                    self.igralec1.igraj()
            else:
                assert False, "Neveljaven igralec poskuša povlect potezo."
            

if __name__ == "__main__":
    # Naredimo glavno okno in nastavimo ime
    root = tkinter.Tk()
    root.title("五子棋")
    
    # Naredimo objekt razreda Gui in ga spravimo v spremenljivko,
    # sicer bo Python mislil, da je objekt neuporabljen in ga bo pobrisal
    # iz pomnilnika.
    aplikacija = Gui(root)
    # Kontrolo prepustimo glavnemu oknu. Funkcija mainloop neha
    # delovati, ko okno zapremo.
    root.mainloop()        