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
        raise QuoridorError("la position est invalide pour l'état actuel du jeu.")

class QuoridorError(Exception):
    pass
