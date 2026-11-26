"""IFT3295 - TP3 - PLAST (a completer).

Completez le corps des fonctions. Ne changez ni leurs noms, ni leurs
signatures, ni les constantes. Respectez les regles de l'enonce.
Vous pouvez ajouter vos propres fonctions. Aucune librairie qui fait le
travail a votre place (Biopython, etc.).
"""

import math

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
    HSP_etendu = HSP(hsp.debut_requete, hsp.debut_cible, hsp.longueur, hsp.score)
    score_max = HSP_etendu.score

    while True:
        score_act = 0 # Pour vérifier si, au fil des itérations, le score descend en dessous de seuil_e
        score_gauche = -5
        score_droite = -5
        #Extension gauche
        if HSP_etendu.debut_requete > 0 and HSP_etendu.debut_cible > 0:
            score_gauche = score(requete, cible, HSP_etendu.debut_requete - 1, HSP_etendu.debut_cible -1, 1)
        
        #Extension droite
        if HSP_etendu.debut_requete + HSP_etendu.longueur < len(requete) and HSP_etendu.debut_cible + HSP_etendu.longueur < len(cible):
            score_droite = score(requete, cible, HSP_etendu.debut_requete + HSP_etendu.longueur, HSP_etendu.debut_cible + HSP_etendu.longueur, 1)

        if score_gauche == -5 and score_droite == -5:
            break

        if score_gauche >= score_droite:
            act = HSP(HSP_etendu.debut_requete - 1, 
                      HSP_etendu.debut_cible - 1, 
                      HSP_etendu.longueur + 1, 
                      HSP_etendu.score + score_gauche)
        else:
            act = HSP(HSP_etendu.debut_requete, 
                      HSP_etendu.debut_cible, 
                      HSP_etendu.longueur + 1, 
                      HSP_etendu.score + score_droite)

        score_max = max(score_max, act.score)

        if score_max - act.score >= seuil_e:
            break

        HSP_etendu = act

    return HSP_etendu

def chevauchent(a: HSP, b: HSP) -> bool:
    """Vrai si les HSPs alignent au moins une meme paire de positions (1.5).

    Exemple : chevauchent(HSP(0, 0, 2, 10), HSP(1, 1, 2, 10)) donne True.
    """
    intervalle_a = [(a.debut_requete + i, a.debut_cible + i) for i in range(a.longueur)]
    intervalle_b = [(b.debut_requete + i, b.debut_cible + i) for i in range(b.longueur)]

    return bool(set(intervalle_a) & set(intervalle_b))

def fusionner(requete: str, cible: str, hsps: list[HSP]) -> list[HSP]:
    """Fusionne les HSPs chevauchants (section 1.5).

    Exemple : fusionner('AAA', 'AAA', [HSP(0, 0, 2, 10), HSP(1, 1, 2, 10)])
    donne [HSP(0, 0, 3, 15)].
    """
    #hsps_etendus = [etendre(requete, cible, hsps[i],4) for i in range(len(hsps))]

    chevauchements = {i : [] for i in range(len(hsps))} # Paires d'indices d'HSPs étendus chevauchants 
    for i in range(len(hsps)):
        for j in range(i + 1, len(hsps)):
            if chevauchent(hsps[i], hsps[j]):
                chevauchements[i].append(j)
                chevauchements[j].append(i)
    hsps_fusion = [] # Liste d'HSPs fusionnés
    visites = []
    for i in range(len(hsps)):
        if i not in visites:
            voisins = []
            a_fusionner = [i]
            while a_fusionner:
                courant = a_fusionner.pop()
                if courant not in visites:
                    visites.append(courant)
                    voisins.append(courant)
                    a_fusionner.extend(chevauchements[courant])

            if len(voisins) == 1:
                hsps_fusion.append(hsps[i])
            else:
                debut_requete_fusion = min(hsps[j].debut_requete for j in voisins)
                debut_cible_fusion = min(hsps[j].debut_cible for j in voisins)
                longueur_fusion = max(hsps[j].debut_requete + hsps[j].longueur for j in voisins) - debut_requete_fusion
                score_fusion = score(requete, cible, debut_requete_fusion, debut_cible_fusion, longueur_fusion)
                hsps_fusion.append(HSP(debut_requete_fusion, debut_cible_fusion, longueur_fusion, score_fusion))

    return hsps_fusion
    
def meilleur_hsp(requete: str, cible: str, graine: str, seuil_e: int) -> HSP | None:
    """Retourne le meilleur HSP pour une cible, ou None s'il n'y en a pas.

    Exemple : meilleur_hsp('AC', 'AC', '11', 4) donne HSP(0, 0, 2, 10).
    """
    if len(graine) > len(requete) or len(graine) > len(cible):
        return None

    hsp_init = hsps_initiaux(requete, cible, graine)
    if hsp_init == []:
        return None

    hsp_etendus = [etendre(requete, cible, hsp, seuil_e) for hsp in hsp_init]
    hsp_fusionnes = fusionner(requete, cible, hsp_etendus)

    bitscore = [round((LAMBDA * hsp.score - math.log(K)) / math.log(2)) for hsp in hsp_fusionnes]
    
    index_max_B = bitscore.index(max(bitscore))

    return hsp_fusionnes[index_max_B]

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
    n = len(requete)
    m = sum(len(cibles) for _,cibles in banque)

    seq_pertinentes = []
    for i in range(len(banque)):
        cible = banque[i][1]
        hsp = meilleur_hsp(requete, cible, graine, seuil_e)
        if hsp is not None:
            bitscore, e_value = statistiques(hsp.score, m, n)
            if e_value <= seuil_ss:
                seq_pertinentes.append((i, hsp, bitscore, e_value))

    return seq_pertinentes
