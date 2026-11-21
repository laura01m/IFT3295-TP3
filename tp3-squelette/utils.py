"""IFT3295 - TP3 - Utilitaires fournis (ne pas modifier)."""

from typing import NamedTuple


class HSP(NamedTuple):
    """Debuts a 0 dans les deux sequences, longueur et score du HSP.

    Exemple : HSP(1, 3, 2, 10) aligne deux caracteres a partir des
    positions 1 de la requete et 3 de la cible, pour un score de 10.
    """

    debut_requete: int
    debut_cible: int
    longueur: int
    score: int


def lire_fasta(chemin: str) -> list[tuple[str, str]]:
    """Retourne les couples (identifiant, sequence) du fichier FASTA.

    Exemple : le fichier contenant '>seq1' puis 'ACGT' donne [('seq1', 'ACGT')].
    """
    enregistrements: list[tuple[str, str]] = []
    with open(chemin) as fichier:
        for ligne in fichier:
            ligne = ligne.strip()
            if ligne.startswith(">"):
                enregistrements.append((ligne[1:], ""))
            elif ligne and enregistrements:
                nom, sequence = enregistrements[-1]
                enregistrements[-1] = (nom, sequence + ligne.upper())
    return enregistrements
