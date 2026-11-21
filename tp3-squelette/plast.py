"""IFT3295 - TP3 - PLAST (a completer).

Completez le corps des fonctions. Ne changez ni leurs noms, ni leurs
signatures, ni les constantes. Respectez les regles de l'enonce.
Vous pouvez ajouter vos propres fonctions. Aucune librairie qui fait le
travail a votre place (Biopython, etc.).
"""

from utils import HSP

MATCH: int = 5
MISMATCH: int = -4
LAMBDA: float = 0.192
K: float = 0.176

def kmers(sequence: str, graine: str) -> dict[str, list[int]]:
    """Retourne un dictionnaire associant chaque mot a ses positions (1.2).

    Exemple : kmers('ACACA', '11') donne {'AC': [0, 2], 'CA': [1, 3]}.
    """
    raise NotImplementedError


def score(requete: str, cible: str, debut_requete: int, debut_cible: int, longueur: int) -> int:
    """Calcule le score d'un HSP. Exemple : score('AC', 'AT', 0, 0, 2) donne 1."""
    raise NotImplementedError


def hsps_initiaux(requete: str, cible: str, graine: str) -> list[HSP]:
    """Recherche les HSPs initiaux (section 1.3).

    Exemple : hsps_initiaux('AC', 'AC', '11') donne [HSP(0, 0, 2, 10)].
    """
    raise NotImplementedError


def etendre(requete: str, cible: str, hsp: HSP, seuil_e: int) -> HSP:
    """Etend un HSP (section 1.4).

    Exemple : etendre('AC', 'AC', HSP(0, 0, 1, 5), 4) donne HSP(0, 0, 2, 10).
    """
    raise NotImplementedError


def chevauchent(a: HSP, b: HSP) -> bool:
    """Vrai si les HSPs alignent au moins une meme paire de positions (1.5).

    Exemple : chevauchent(HSP(0, 0, 2, 10), HSP(1, 1, 2, 10)) donne True.
    """
    raise NotImplementedError


def fusionner(requete: str, cible: str, hsps: list[HSP]) -> list[HSP]:
    """Fusionne les HSPs chevauchants (section 1.5).

    Exemple : fusionner('AAA', 'AAA', [HSP(0, 0, 2, 10), HSP(1, 1, 2, 10)])
    donne [HSP(0, 0, 3, 15)].
    """
    raise NotImplementedError


def meilleur_hsp(requete: str, cible: str, graine: str, seuil_e: int) -> HSP | None:
    """Retourne le meilleur HSP pour une cible, ou None s'il n'y en a pas.

    Exemple : meilleur_hsp('AC', 'AC', '11', 4) donne HSP(0, 0, 2, 10).
    """
    raise NotImplementedError


def statistiques(score_brut: int, m: int, n: int) -> tuple[int, float]:
    """Retourne (bitscore, e-value) du HSP (section 1.6).

    Exemple : statistiques(78, 31397, 41) donne (24, 0.07672768831253052).
    """
    raise NotImplementedError


def rechercher(
    requete: str,
    banque: list[tuple[str, str]],
    graine: str,
    seuil_e: int,
    seuil_ss: float,
) -> list[tuple[int, HSP, int, float]]:
    """Retourne (indice, HSP, bitscore, e-value) par sequence retenue.

    L'indice est celui de la sequence dans la banque. Le seuil est inclus.
    Exemple : rechercher('AC', [('cible', 'AC')], '11', 4, 100) donne
    [(0, HSP(0, 0, 2, 10), 5, 0.125)].
    """
    raise NotImplementedError
