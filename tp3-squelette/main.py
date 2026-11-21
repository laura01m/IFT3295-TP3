"""IFT3295 - TP3 - Programme principal (a completer).

    python3 main.py -i <sequence ou fichier FASTA> -db tRNAs.fasta \
        [-E 4] [-ss 1e-3] [-seed 11111111111]

Completez le corps des fonctions sans changer leurs noms ni leurs
signatures. L'affichage est celui de l'exemple de l'enonce.
"""

import argparse

from plast import rechercher
from utils import lire_fasta


def afficher(requete: str, banque: list[tuple[str, str]], args: argparse.Namespace) -> None:
    """Affiche les resultats ; les positions de fin sont incluses (1.7).

    Exemple : un HSP de debut 0 et de longueur 2 affiche les positions 0 et 1.
    """
    resultats = rechercher(requete, banque, args.seed, args.E, args.ss)
    # A completer : afficher les resultats.
    raise NotImplementedError


def main() -> None:
    """Execute le programme."""
    parseur = argparse.ArgumentParser(prog="plast")
    parseur.add_argument("-i", required=True, help="sequence ADN ou fichier FASTA de requetes")
    # A completer : ajouter les autres arguments et executer la recherche.
    raise NotImplementedError


if __name__ == "__main__":
    main()
