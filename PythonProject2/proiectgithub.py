import os
import sys
import subprocess
from git import Repo
import ast
import shutil

def analiza_librarii(project_dir):
    # Analizeaza fisierelor ===> extragerea librariilor
    libraries = set()
    for root, _, files in os.walk(project_dir):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    try:
                        node = ast.parse(f.read(), filename=file_path)
                        for sub_node in ast.walk(node):
                            if isinstance(sub_node, ast.Import):
                                for alias in sub_node.names:
                                    libraries.add(alias.name.split(".")[0])
                            elif isinstance(sub_node, ast.ImportFrom):
                                if sub_node.module:
                                    libraries.add(sub_node.module.split(".")[0])
                    except Exception:
                        pass
    return sorted(libraries)


def generare_fisier(libraries, file_name="requirements.txt"):
    # Genereaza un fisier requirements.txt cu librariile analizate
    with open(file_name, "w") as f:
        for lib in libraries:
            f.write(f"{lib}\n")


def probleme_securitate():
    # Verifica
    subprocess.run(["safety", "check", "--file=requirements.txt", "--full-report"])


def main():
    if len(sys.argv) != 2:
        print("Utilizare: python proiectgithub.py https://github.com/pallets/flask")
        sys.exit(1)

    github_url = sys.argv[1]
    clone_dir = "cloned_repo"

    # Pasul 1: Clonează repository-ul
    repozitor(github_url, clone_dir)

    # Pasul 2: Analizează librăriile
    libraries = analiza_librarii(clone_dir)
    print("Librării găsite:")
    print("\n".join(libraries))

    # Pasul 3: Generează fișierul requirements.txt
    generare_fisier(libraries)

    # Pasul 4: Verifică problemele de securitate
    probleme_securitate()

    # Șterge directorul clonat
    shutil.rmtree(clone_dir)


if __name__ == "__main__":
    main()
