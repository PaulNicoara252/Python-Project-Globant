import os
import sys
import subprocess
from git import Repo
from pathlib import Path
import ast
import shutil


def descarca_repositoriu(url_github, director_descarcare="repositoriu_descarcat"):
    # Descarca un repository GitHub intr-un folder.
    print(f"Se descarca repository-ul din {url_github}...")
    if os.path.exists(director_descarcare):
        print(f"Directorul {director_descarcare} exista deja. Se sterge...")
        try:
            shutil.rmtree(director_descarcare)  # Sterge directorul fara functii suplimentare
        except Exception as e:
            raise ValueError(f"Eroare la stergerea directorului existent {director_descarcare}: {e}")
    try:
        repo = Repo.clone_from(url_github, director_descarcare)
        repo.close()  # Asigura eliberarea tuturor handler-elor de fisiere
        print(f"Repository-ul a fost descarcat cu succes in {director_descarcare}")
        return director_descarcare
    except Exception as e:
        raise ValueError(f"Eroare la descarcarea repository-ului: {e}")


def curata_directorul(director):
    # Stergerea unui director specificat.
    try:
        shutil.rmtree(director)  # Sterge directorul fara functii suplimentare
        print(f"Directorul {director} a fost curatat cu succes.")
    except Exception as e:
        print(f"Eroare la curatarea directorului {director}: {e}")


import time


def analizeaza_librariile(director_proiect):
    # Analizeaza directorul proiectului pentru a extrage toate librariile importate din fisierele Python.
    print("\nSe analizeaza librariile importate...")
    start_timp = time.time()  # Porneste cronometrul

    librarii = set()
    for radacina, _, fisiere in os.walk(director_proiect):
        for fisier in fisiere:
            if fisier.endswith(".py"):
                cale_fisier = os.path.join(radacina, fisier)
                with open(cale_fisier, "r", encoding="utf-8") as f:
                    try:
                        nod = ast.parse(f.read(), filename=cale_fisier)
                        for sub_nod in ast.walk(nod):
                            if isinstance(sub_nod, ast.Import):
                                for alias in sub_nod.names:
                                    librarii.add(alias.name.split(".")[0])
                            elif isinstance(sub_nod, ast.ImportFrom):
                                if sub_nod.module:
                                    librarii.add(sub_nod.module.split(".")[0])
                    except Exception as e:
                        print(f"Eroare la analizarea {cale_fisier}: {e}")

    end_timp = time.time()  # Opreste cronometrul
    timp_total = end_timp - start_timp
    print(f"\nTimp necesar pentru analizarea librariilor: {timp_total:.2f} secunde")

    librarii = sorted(librarii)  # Sorteaza librariile pentru consistenta
    print("\nLista librariilor importate:")
    print("\n".join(librarii))
    return librarii


def genereaza_fisier_librarii(librarii, nume_fisier="requirements.txt"):
    # Genereaza un fisier valid cu librariile analizate.
    if not librarii:
        print("Nu s-au gasit librarii de adaugat in requirements.txt.")
        return
    print(f"\nSe genereaza {nume_fisier}...")
    try:
        with open(nume_fisier, "w") as f:
            for librarie in librarii:
                f.write(f"{librarie}\n")
        print(f"{nume_fisier} a fost generat cu succes.")
    except Exception as e:
        raise ValueError(f"Eroare la generarea fisierului {nume_fisier}: {e}")


def verifica_probleme_securitate():
    # Verifica problemele de securitate cunoscute in fisierul generat.
    print("\nSe verifica problemele de securitate cunoscute...")
    try:
        rezultat = subprocess.run(
            ["safety", "check", "--file=requirements.txt", "--full-report"],
            capture_output=True,
            text=True,
        )
        if rezultat.returncode == 0:
            print("\nNu s-au gasit probleme de securitate.")
        else:
            print("\nProbleme de securitate gasite:")
            print(rezultat.stdout)
    except FileNotFoundError:
        print("Eroare: Safety nu este instalat sau nu este disponibil in mediul virtual.")
    except Exception as e:
        print(f"Eroare neasteptata in timpul verificarii de securitate: {e}")


def main():
    # Functia principala pentru rularea analizei de librarii si securitate.
    try:
        if len(sys.argv) != 2:
            raise ValueError("Utilizare: python github_librarii.py <URL GitHub>")
        url_github = sys.argv[1]
        director_descarcare = "repositoriu_descarcat"

        # Pasul 1: Descarca repository-ul
        director_proiect = descarca_repositoriu(url_github, director_descarcare)

        # Pasul 2: Analizeaza librariile
        librarii = analizeaza_librariile(director_proiect)
        if not librarii:
            print("Nu s-au gasit librarii in proiect. Iesire...")
            return

        # Pasul 3: Genereaza fisierul requirements.txt
        genereaza_fisier_librarii(librarii)

        # Pasul 4: Verifica problemele de securitate
        verifica_probleme_securitate()

        # Curatare
        print(f"Se curata repository-ul descarcat: {director_descarcare}")
        curata_directorul(director_descarcare)

    except ValueError as ve:
        print(f"Eroare: {ve}")
    except Exception as e:
        print(f"A aparut o eroare neasteptata: {e}")


if __name__ == "__main__":
    main()
