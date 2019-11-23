import networkx as nx
import unittest


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
            successeur = (2*joueur[0]-prédécesseur[0],
                          2*joueur[1]-prédécesseur[1])

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


class Quoridor:

    def __init__(self, joueurs, murs=None):
        if joueurs is None:
            raise QuoridorError("joueurs n'est pas un itérable.")

        if len(joueurs) > 2:
            raise QuoridorError(
                "l'itérable de joueurs en contient plus de deux.")

        if joueurs[0]['pos'][0] < 1 or joueurs[0]['pos'][0] > 9 or joueurs[0]['pos'][1] < 1 or joueurs[0]['pos'][1] > 9 or joueurs[1]['pos'][0] < 1 or joueurs[1]['pos'][0] > 9 or joueurs[1]['pos'][1] < 1 or joueurs[1]['pos'][1] > 9:
            raise QuoridorError("la position d'un joueur est invalide.")

        if joueurs[0]['murs'] > 10 or joueurs[0]['murs'] < 0 or joueurs[1]['murs'] > 10 or joueurs[1]['murs'] < 0:
            raise QuoridorError(
                "le nombre de murs qu'un joueur peut placer est >10, ou négatif.")

        if murs is not None and murs is not dict:
            raise QuoridorError(
                "murs n'est pas un dictionnaire lorsque présent.")

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
            raise QuoridorError(
                "la position est invalide (en dehors du damier).")

        graphe = construire_graphe([joueur['pos'] for joueur in self.joueurs],
                                   self.murs['horizontaux'], self.murs['verticaux'])

        # vérifie position valide
        if position in graphe.successors(self.joueurs[joueur-1]['pos']):
            self.joueurs[joueur-1]['pos'] = position

        else:
            raise QuoridorError(
                "la position est invalide pour l'état actuel du jeu.")

    def jouer_coup(self, joueur):
        if joueur > 2 or joueur < 1:
            raise QuoridorError("le numéro du joueur est autre que 1 ou 2.")

        if self.partie_terminée() is not False:
            raise QuoridorError("la partie est déjà terminée.")

        graphe = construire_graphe([joueur['pos'] for joueur in self.joueurs],
                                   self.murs['horizontaux'], self.murs['verticaux'])
        coups = nx.shortest_path(
            graphe, self.joueurs[joueur - 1]['pos'], 'B' + str(joueur))
        coupsAdver = nx.shortest_path(
            graphe, self.joueurs[2 - joueur]['pos'], 'B' + str(3 - joueur))

        if len(coups) <= len(coupsAdver) or self.joueurs[joueur-1]['murs'] < 1:
            self.déplacer_jeton(joueur, coups[1])
            #si horizontal
            if coupsAdver[0][0]-coupsAdver[1][0] == 0:
                for i in graphe.successors(coupsAdver[0]):
                    if i not in self.murs["horizontaux"] or [i[0]-1,i[1]] not in self.murs["horizontaux"]:
                        placer_mur(joueur, tuple(i), 'horizontaux')
                        break
        
            #si vertical
            else: 
                for i in graphe.successors(coupsAdver[0]):
                    if i not in self.murs["verticaux"] or [i[0],i[1]-1] not in self.murs["verticaux"]:
                        placer_mur(joueur, tuple(i), 'verticaux')
                        break

    def état_partie(self):
        # murs a tirer de la methode placer_mur
        état = {'joueurs': [
            {'nom': self.joueurs[0], 'murs': self.joueurs[0].murs,
                'pos': self.joueurs[0]['pos']},
            {'nom': self.joueurs[1], 'murs': self.joueurs[1].murs,
                'pos': self.joueurs[1]['pos']},
        ],
            'murs': {
                'horizontaux': self.murs['horizontaux'],
            'vertcaux': self.murs['verticaux'],
        }
        }
        return état

    def partie_terminée(self):
        """
        Déterminer si la partie est terminée.
        :returns: le nom du gagnant si la partie est terminée; False autrement.
        """
        terminée = False
        # Reste à savoir si le joueur[0] commence toujours en bas et l'inverse pour la condition ==9 et ==0
        # Implémenté comme cela fait en sorte que le joueur 1 gagne s'il atteint la ligne 9 puisqu'il part à 1
        # et vice-versa pour le joueur 2
        if self.état_partie()['joueurs'][0]['pos'][1] == 9:
            terminée = f'La partie est terminée, le joueur {self.état_partie()["joueurs"][0]["nom"]} a remporté!'
        elif self.état_partie()['joueurs'][1]['pos'][1] == 1:
            terminée = f'La partie est terminée, le joueur {self.état_partie()["joueurs"][1]["nom"]} a remporté!'
        return terminée

    def placer_mur(self, joueur: int, position: tuple, orientation: str):
        if joueur != 1 and joueur != 2:
            raise QuoridorError('le numéro du joueur est autre que 1 ou 2.')

        if orientation == 'horizontal':
            for mur in self.murs['horizontaux']:
                if position == mur or (position[0] == (mur[0]+1) and position[1] == mur[1]):
                    raise QuoridorError('un mur occupe déjà cette position.')
                if mur[0] > 8 or mur[0] < 1 or mur[1] < 2 or mur[1] > 9:
                    raise QuoridorError(
                        'la position est invalide pour cette orientation.')
            # on ajoute le tuple position au murs horizontaux

            self.murs['horizontaux'].append(position)
        if orientation == 'vertical':
            for mur in self.murs['verticaux']:
                if position == mur or (position[1] == (mur[1]+1) and position[0] == mur[0]):
                    raise QuoridorError('un mur occupe déjà cette position.')
                if mur[0] > 9 or mur[0] < 2 or mur[1] < 1 or mur[1] > 8:
                    raise QuoridorError(
                        'la position est invalide pour cette orientation.')
            # on ajoute le tuple position au murs verticaux
            self.murs['verticaux'].append(position)

        if self.joueurs[joueur-1]['murs'] > 9:
            raise QuoridorError('le joueur a déjà placé tous ses murs.')


class QuoridorError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)