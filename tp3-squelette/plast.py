"""IFT3295 - TP3 - PLAST (a completer).

Completez le corps des fonctions. Ne changez ni leurs noms, ni leurs
signatures, ni les constantes. Respectez les regles de l'enonce.
Vous pouvez ajouter vos propres fonctions. Aucune librairie qui fait le
travail a votre place (Biopython, etc.).
"""

from utils import HSP
import math
MATCH: int = 5
MISMATCH: int = -4
LAMBDA: float = 0.192
K: float = 0.176

def mot_graine(sequence: str, debut: int, graine: str) -> str:
    mot = ""
    for j in range(len(graine)):
        if graine[j] == "1":
            mot += sequence[debut + j]
    return mot

def kmers(sequence: str, graine: str) -> dict[str, list[int]]:
    """Retourne un dictionnaire associant chaque mot a ses positions (1.2).

    Exemple : kmers('ACACA', '11') donne {'AC': [0, 2], 'CA': [1, 3]}.
    """
    k = len(graine)
    positions = {}
    for debut in range(len(sequence) - k + 1):
        mot = mot_graine(sequence, debut, graine)
        if mot not in positions:
            positions[mot] = []
            positions[mot].append(debut)
    return positions


def score(requete: str, cible: str, debut_requete: int, debut_cible: int, longueur: int) -> int:
    """Calcule le score d'un HSP. Exemple : score('AC', 'AT', 0, 0, 2) donne 1."""
    total = 0
    for i in range(longueur):
        if requete[debut_requete + i] == cible[debut_cible + i]:
            total += MATCH
        else:
            total += MISMATCH
    return total


def hsps_initiaux(requete: str, cible: str, graine: str) -> list[HSP]:
    """Recherche les HSPs initiaux (section 1.3).

    Exemple : hsps_initiaux('AC', 'AC', '11') donne [HSP(0, 0, 2, 10)].
    """
    k = len(graine)
    mots_requete = kmers(requete, graine)
    mots_cible = kmers(cible, graine)

    hsps: list[HSP] = []
    for mot, positions_requete in mots_requete.items():
        positions_cible = mots_cible.get(mot)
        if positions_cible is None:
            continue
        for debut_requete in positions_requete:
            for debut_cible in positions_cible:
                score_initial = score(requete, cible, debut_requete, debut_cible, k)
                hsps.append(HSP(debut_requete, debut_cible, k, score_initial))

    hsps.sort(key=lambda hsp: (hsp.debut_requete, hsp.debut_cible))
    return hsps


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
    bitscore = round((LAMBDA * score_brut - math.log(K)) / math.log(2))
    evalue = m * n * 2 ** (-bitscore)
    return bitscore, evalue


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
