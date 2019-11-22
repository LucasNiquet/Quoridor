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
    x = position[0]
    y = position[1]
    xJ = self.joueurs[joueur - 1]['pos'][0]
    yJ = self.joueurs[joueur - 1]['pos'][1]

    if joueur > 2 or joueur < 1:
        raise QuoridorError("le numéro du joueur est autre que 1 ou 2.")

    if x > 9 or x < 1 or y > 9 or y < 1:
        raise QuoridorError("la position est invalide (en dehors du damier).")

    # si le joueur se déplace à gauche
    if xJ - x == 1 and yJ == y and self.joueurs[joueur-1]['pos'] not in self.murs['verticaux'] and [xJ, yJ-1] not in self.murs['verticaux']:
        self.joueurs[joueur-1]['pos'] = position

    # si le joueur se déplace à droite
    elif xJ - x == -1 and yJ == y and [xJ+1, yJ] not in self.murs['verticaux'] and [xJ+1, yJ-1] not in self.murs['verticaux']:
        self.joueurs[joueur-1]['pos'] = position

    # si le joueur se déplace vers le bas
    elif xJ == x and yJ - y == 1 and self.joueurs[joueur-1]['pos'] not in self.murs['horizontaux'] and [xJ - 1, yJ] not in self.murs['horizontaux']:
        self.joueurs[joueur-1]['pos'] = position

    # si le joueur se déplace vers le haut
    elif xJ == x and yJ - y == -1 and [xJ, yJ + 1] not in self.murs['horizontaux'] and [xJ - 1, yJ + 1] not in self.murs['horizontaux']:
        self.joueurs[joueur-1]['pos'] = position

    # si le joueur saute par dessus le pion adverse et qu'il n'y a pas de mur
    elif [x, y] == self.joueurs[2 - joueur]['pos']:
        self.joueurs[joueur-1]['pos'] = position

    # si le joueur saute par dessus le pion adverse et qu'il y a un mur
    elif [x, y] == self.joueurs[2 - joueur]['pos']:
        self.joueurs[joueur-1]['pos'] = position

    else:
        raise QuoridorError(
            "la position est invalide pour l'état actuel du jeu.")


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
