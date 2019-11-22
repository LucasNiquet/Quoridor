import networkx as nx


def construire_graphe(joueurs, murs_horizontaux, murs_verticaux):
    """
    Crée le graphe des déplacements admissibles pour les joueurs.

    :param joueurs: une liste des positions (x,y) des joueurs.
    :param murs_horizontaux: une liste des positions (x,y) des murs horizontaux.
    :param murs_verticaux: une liste des positions (x,y) des murs verticaux.
    :returns: le graphe bidirectionnel (en networkX) des déplacements admissibles.
    """
    graphe = nx.DiGraph()

    # pour chaque colonne du damier
    for x in range(1, 10):
        # pour chaque ligne du damier
        for y in range(1, 10):
            # ajouter les arcs de tous les déplacements possibles pour cette tuile
            if x > 1:
                graphe.add_edge((x, y), (x-1, y))
            if x < 9:
                graphe.add_edge((x, y), (x+1, y))
            if y > 1:
                graphe.add_edge((x, y), (x, y-1))
            if y < 9:
                graphe.add_edge((x, y), (x, y+1))

    # retirer tous les arcs qui croisent les murs horizontaux
    for x, y in murs_horizontaux:
        graphe.remove_edge((x, y-1), (x, y))
        graphe.remove_edge((x, y), (x, y-1))
        graphe.remove_edge((x+1, y-1), (x+1, y))
        graphe.remove_edge((x+1, y), (x+1, y-1))

    # retirer tous les arcs qui croisent les murs verticaux
    for x, y in murs_verticaux:
        graphe.remove_edge((x-1, y), (x, y))
        graphe.remove_edge((x, y), (x-1, y))
        graphe.remove_edge((x-1, y+1), (x, y+1))
        graphe.remove_edge((x, y+1), (x-1, y+1))

    # retirer tous les arcs qui pointent vers les positions des joueurs
    # et ajouter les sauts en ligne droite ou en diagonale, selon le cas
    for joueur in map(tuple, joueurs):

        for prédécesseur in list(graphe.predecessors(joueur)):
            graphe.remove_edge(prédécesseur, joueur)

            # si admissible, ajouter un lien sauteur
            successeur = (2*joueur[0]-prédécesseur[0], 2*joueur[1]-prédécesseur[1])

            if successeur in graphe.successors(joueur) and successeur not in joueurs:
                # ajouter un saut en ligne droite
                graphe.add_edge(prédécesseur, successeur)

            else:
                # ajouter les liens en diagonal
                for successeur in list(graphe.successors(joueur)):
                    if prédécesseur != successeur and successeur not in joueurs:
                        graphe.add_edge(prédécesseur, successeur)

    # ajouter les noeuds objectifs des deux joueurs
    for x in range(1, 10):
        graphe.add_edge((x, 9), 'B1')
        graphe.add_edge((x, 1), 'B2')

    return graphe
    
def __init__(self, joueurs, murs=None):
    if joueurs is None:
        raise QuoridorError("joueurs n'est pas un itérable.")

    if len(joueurs) > 2:
        raise QuoridorError("l'itérable de joueurs en contient plus de deux.")

    if joueurs[0]['pos'][0] < 1 or joueurs[0]['pos'][0] > 9 or joueurs[0]['pos'][1] < 1 or joueurs[0]['pos'][1] > 9 or joueurs[1]['pos'][0] < 1 or joueurs[1]['pos'][0] > 9 or joueurs[1]['pos'][1] < 1 or joueurs[1]['pos'][1] > 9:
        raise QuoridorError("la position d'un joueur est invalide.")

    if joueurs[0]['murs'] > 10 or joueurs[0]['murs'] < 0 or joueurs[1]['murs'] > 10 or joueurs[1]['murs'] < 0:
        raise QuoridorError(
            "le nombre de murs qu'un joueur peut placer est >10, ou négatif.")

    if murs is not None and murs is not dict:
        raise QuoridorError("murs n'est pas un dictionnaire lorsque présent.")

    if len(murs['horizontaux']) + len(murs['verticaux']) + joueurs[0]['murs'] + joueurs[1]['murs'] != 20:
        raise QuoridorError(
            "le total des murs placés et plaçables n'est pas égal à 20.")

    if murs is not None:
        for i in murs['horizonraux']:
            if i[0] < 1 or i[0] > 9 or i[1] < 1 or i[1] > 9:
                raise QuoridorError("la position d'un mur est invalide.")
        for i in murs['verticaux']:
            if i[0] < 1 or i[0] > 9 or i[1] < 1 or i[1] > 9:
                raise QuoridorError("la position d'un mur est invalide.")

    self.joueurs = joueurs
    self.murs = murs


def __str__(self):
    tab = []
    for i in range(9):
        tab += [[' . ', ' '] * 8 + [' . ']]
        if i != 8:
            tab += [['   ', ' '] * 8 + ['   ']]

    # place les joueurs sur le damier
    tab[(9 - self.joueurs[0]["pos"][1]) *
        2][(self.joueurs[0]["pos"][0]-1) * 2] = ' 1 '
    tab[(9-self.joueurs[1]["pos"][1]) *
        2][(self.joueurs[1]["pos"][0]-1) * 2] = ' 2 '

    # place les murs sur le damier
    for i in self.murs["verticaux"]:
        tab[(9 - i[1]) * 2][(i[0] - 1) * 2 - 1] = '|'
        tab[(9 - i[1]) * 2 - 1][(i[0] - 1) * 2 - 1] = '|'
        tab[(9 - i[1] - 1) * 2][(i[0] - 1) * 2 - 1] = '|'

    for i in self.murs["horizontaux"]:
        tab[(9 - i[1]) * 2 + 1][(i[0] - 1) * 2] = '---'
        tab[(9 - i[1]) * 2 + 1][(i[0] - 1) * 2 + 1] = '-'
        tab[(9 - i[1]) * 2 + 1][(i[0]) * 2] = '---'

    # transforme le damier en chaine de caractère
    damier = f'Légende: 1={self.joueurs[0]["nom"]}, 2={self.joueurs[1]["nom"]}\n'
    damier += '   ' + '-' * 35 + '\n'
    debut2 = '  |'
    ligneF = '--|' + '-' * 35 + '\n  | 1   2   3   4   5   6   7   8   9'

    for i in range(9):
        debut1 = f'{9 - i} |'
        ligne1 = debut1 + ''.join(tab[2 * i]) + '|\n'
        if i != 8:
            ligne2 = debut2 + ''.join(tab[2 * i + 1]) + '|\n'
        else:
            ligne2 = ''
        damier += ligne1 + ligne2

    damier += ligneF
    return damier


def déplacer_jeton(self, joueur, position):
    if joueur > 2 or joueur < 1:
        raise QuoridorError("le numéro du joueur est autre que 1 ou 2.")

    if position[0] > 9 or position[0] < 1 or position[1] > 9 or position[1] < 1:
        raise QuoridorError("la position est invalide (en dehors du damier).")

    graphe = construire_graphe([joueur['pos'] for joueur in self.joueurs],
    self.murs['horizontaux'], self.murs['verticaux'])

    #vérifie position valide
    if position in graphe.successors(self.joueurs[joueur-1]['pos']):
        self.joueurs[joueur-1]['pos'] = position
        
    else:
        raise QuoridorError("la position est invalide pour l'état actuel du jeu.")

def jouer_coup(self, joueur):
    if joueur > 2 or joueur < 1:
        raise QuoridorError("le numéro du joueur est autre que 1 ou 2.")

    if partie_terminée(self) is not False:
        raise QuoridorError("la partie est déjà terminée.")

    graphe = construire_graphe([joueur['pos'] for joueur in self.joueurs],
    self.murs['horizontaux'], self.murs['verticaux'])
    coups= nx.shortest_path(graphe, self.joueurs[joueur - 1]['pos'], 'B' + str(joueur))
    coupsAdver= nx.shortest_path(graphe, self.joueurs[2 - joueur]['pos'], 'B' + str(3 - joueur))

    if len(coups) <= len(coupsAdver):
        déplacer_jeton(self, joueur, coups[1])
    else:

        #si horizontal
        if coupsAdver[0][0]-coupsAdver[1][0] == 0:
            #je pense pas que c'est fonctionnel
            placer_mur(self, joueur, coupsAdver[1], 'horizontaux')
        
        #si vertical
        elif coupsAdver[0][1]-coupsAdver[1][1] == 0:
            #je pense pas que c'est fonctionnel
            placer_mur(self, joueur, coupsAdver[1], 'verticaux')


def état_partie(self):
    """
    Produire l'état actuel de la partie.

    :returns: une copie de l'état actuel du jeu sous la forme d'un dictionnaire:
    {
        'joueurs': [
            {'nom': nom1, 'murs': n1, 'pos': (x1, y1)},
            {'nom': nom2, 'murs': n2, 'pos': (x2, y2)},
        ],
        'murs': {
            'horizontaux': [...],
            'verticaux': [...],
        }
    }

    où la clé 'nom' d'un joueur est associée à son nom, la clé 'murs' est associée 
    au nombre de murs qu'il peut encore placer sur ce damier, et la clé 'pos' est 
    associée à sa position sur le damier. Une position est représentée par un tuple 
    de deux coordonnées x et y, où 1<=x<=9 et 1<=y<=9.

    Les murs actuellement placés sur le damier sont énumérés dans deux listes de
    positions (x, y). Les murs ont toujours une longueur de 2 cases et leur position
    est relative à leur coin inférieur gauche. Par convention, un mur horizontal se
    situe entre les lignes y-1 et y, et bloque les colonnes x et x+1. De même, un
    mur vertical se situe entre les colonnes x-1 et x, et bloque les lignes x et x+1.
    """


def partie_terminée(self):
    """
    Déterminer si la partie est terminée.

    :returns: le nom du gagnant si la partie est terminée; False autrement.
    """
    terminée = False
    # Reste à savoir si le joueur[0] commence toujours en bas et l'inverse pour la condition ==9 et ==0
    # Implémenté comme cela fait en sorte que le joueur 1 gagne s'il atteint la ligne 9 puisqu'il part à 1
    # et vice-versa pour le joueur 2
    if état_partie(self)['joueurs'][0]['pos'][1] == 9:
        terminée = f'Le gagnant est: {état_partie(self)["joueurs"][0]["nom"]}'
    elif état_partie(self)['joueurs'][1]['pos'][1] == 1:
        terminée = f'Le gagnant est: {état_partie(self)["joueurs"][1]["nom"]}'
    return terminée


def placer_mur(self, joueur: int, position: tuple, orientation: str):
    """
    Pour le joueur spécifié, placer un mur à la position spécifiée.

    :param joueur: le numéro du joueur (1 ou 2).
    :param position: le tuple (x, y) de la position du mur.
    :param orientation: l'orientation du mur ('horizontal' ou 'vertical').
    :raises QuoridorError: le numéro du joueur est autre que 1 ou 2.
    :raises QuoridorError: un mur occupe déjà cette position.
    :raises QuoridorError: la position est invalide pour cette orientation.
    :raises QuoridorError: le joueur a déjà placé tous ses murs.
    """

class QuoridorError(Exception):
    pass
