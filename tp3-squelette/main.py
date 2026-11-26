"""IFT3295 - TP3 - Programme principal (a completer).

    python3 main.py -i <sequence ou fichier FASTA> -db tRNAs.fasta \
        [-E 4] [-ss 1e-3] [-seed 11111111111]

Completez le corps des fonctions sans changer leurs noms ni leurs
signatures. L'affichage est celui de l'exemple de l'enonce.
"""

import argparse
import os
from plast import rechercher
from utils import lire_fasta

def afficher(requete: str, banque: list[tuple[str, str]], args: argparse.Namespace) -> None:
    """Affiche les resultats ; les positions de fin sont incluses (1.7).

    Exemple : un HSP de debut 0 et de longueur 2 affiche les positions 0 et 1.
    """
    resultats = rechercher(requete, banque, args.seed, args.E, args.ss)
    resultats = sorted(resultats, key=lambda r: (r[3], -r[2]))

    for indice, hsp, bitscore, evalue in resultats:
        nom, cible = banque[indice]
        fin_requete = hsp.debut_requete + hsp.longueur - 1
        fin_cible = hsp.debut_cible + hsp.longueur - 1
        segment_requete = requete[hsp.debut_requete:fin_requete + 1]
        segment_cible = cible[hsp.debut_cible:fin_cible + 1]

        print(f">{nom}")
        print(f"# Best HSP score:{hsp.score:.2f}, bitscore:{bitscore:.2f}, evalue: {evalue:.2e}")
        print(f"{hsp.debut_requete} {segment_requete} {fin_requete}")
        print(f"{hsp.debut_cible} {segment_cible} {fin_cible}")
        print()

    print("----------------------------------------")
    print(f"Total : {len(resultats)}")


def main() -> None:
    """Execute le programme."""
    
    parseur = argparse.ArgumentParser(prog="plast")
    parseur.add_argument("-i", required=True)
    parseur.add_argument("-db", required=True)
    parseur.add_argument("-E", type=int, default=4)
    parseur.add_argument("-ss", type=float, default=1e-3)
    parseur.add_argument("-seed", default="11111111111")
    args = parseur.parse_args()

    banque = lire_fasta(args.db)

    if os.path.isfile(args.i):
        for nom, sequence in lire_fasta(args.i):
            afficher(sequence, banque, args)
            print()     # saute une ligne entre les 2 séquences
    else:
        afficher(args.i.strip().upper(), banque, args)


if __name__ == "__main__":
    main()
