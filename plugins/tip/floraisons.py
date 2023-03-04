import discord

NOMS_MOIS = [
    'Janvier',
    'Février',
    'Mars',
    'Avril',
    'Mai',
    'Juin',
    'Juillet',
    'Août',
    'Septembre',
    'Octobre',
    'Novembre',
    'Décembre',
]

COULEURS = {
    'BLANC': (255, 255, 255),
    'OCRE_JAUNE': (252, 255, 202),
    'JAUNE_BRUN': (254, 202, 154),
    'ROUGE_BRUN': (251, 153, 200),
    'VERT_BOUTEILLE': (154, 252, 51),
    'GRIS_CLAIR': (190, 191, 195),
    'VERT_ORANGE': (237, 244, 76),
    'JAUNE_OR': (255, 253, 6),
    'ORANGE': (253, 204, 3),
    'BEIGE_ROSE': (254, 201, 207),
    'ROUGE_FONCE': (128, 0, 0),
    'VERT_CLAIR': (202, 254, 205),
    'JAUNE_VERT': (152, 200, 2),
    'BRUN_VERT': (203, 205, 0),
    'VERDATRE': (117, 155, 46),
    'GRIS_JAUNE': (253, 254, 150),
    'VERT_PALE': (202, 255, 203),
    'ROSE': (226, 185, 183),
    'BLEU_ROUGE': (200, 154, 253),
    'JAUNE': (253, 254, 2),
    'ORANGE_BRUN': (243, 191, 29),
    'NOIR': (0, 0, 0),
}

class Fleur:
    def __init__(self, nom: str, floraison: tuple[int], couleur: str):
        self.nom = nom
        self.floraison = floraison
        self.couleur = couleur
    
    def en_floraison(self, mois: int) -> bool:
        """Retournes `True` si la fleur est en floraison au mois indiqué"""
        if self.floraison[0] < self.floraison[1]:
            return self.floraison[0] <= mois and mois <= self.floraison[1]
        elif self.floraison[0] == self.floraison[1]:
            return self.floraison[0] == mois
        else:
            return self.floraison[0] <= mois + 12 and mois <= self.floraison[1]
        
    def to_str(self, emojis: dict[str, discord.Emoji]) -> str:
        if self.floraison == (1, 12):
            floraison_str = "Toute l'année"
        elif self.floraison[0] == self.floraison[1]:
            floraison_str = NOMS_MOIS[self.floraison[0]-1]
        else:
            floraison_str = f"{NOMS_MOIS[self.floraison[0]-1]} - {NOMS_MOIS[self.floraison[1]-1]}"

        return f"{emojis.get(self.couleur, '🎨')} {self.nom} ({floraison_str})"


FLEURS = [
    Fleur('Fausse roquette', [1, 12], 'JAUNE_VERT'),
    Fleur('Colza', [3, 5], 'JAUNE'),
    Fleur('Véronique de Perse', [2, 3], 'BLANC'),
    Fleur('Noisetier', [1, 3], 'OCRE_JAUNE'),
    Fleur('Aulne', [2, 3], 'JAUNE_BRUN'),
    Fleur('Perce-Neige', [2, 3], 'ROUGE_BRUN'),
    Fleur('Buis', [3, 3], 'VERT_BOUTEILLE'),
    Fleur('Narcisse', [3, 4], 'GRIS_CLAIR'),
    Fleur('Cerisier', [4, 4], 'VERT_ORANGE'),
    Fleur('Saule', [3, 4], 'GRIS_CLAIR'),
    Fleur('Prairie', [3, 4], 'JAUNE_OR'),
    Fleur('Crocus', [3, 4], 'ORANGE'),
    Fleur('Pissenlit', [3, 11], 'ORANGE'),
    Fleur('Romarin', [3, 4], 'BEIGE_ROSE'),
    Fleur('Peuplier', [3, 4], 'ROUGE_FONCE'),
    Fleur('Tulipe', [3, 5], 'GRIS_CLAIR'),
    Fleur('Groseiller', [4, 5], 'VERT_CLAIR'),
    Fleur('Erable', [4, 5], 'JAUNE_VERT'),
    Fleur('Poirier', [4, 5], 'ORANGE'),
    Fleur('Aubépine', [4, 5], 'BRUN_VERT'),
    Fleur('Robinier', [5, 5], 'VERDATRE'),
    Fleur('Pommier', [5, 5], 'GRIS_CLAIR'),
    Fleur('Chêne', [5, 5], 'JAUNE_VERT'),
    Fleur('Genêt', [5, 5], 'ORANGE'),
    Fleur('Fraisier', [5, 5], 'JAUNE_BRUN'),
    Fleur('Bouleau', [5, 5], 'ROUGE_BRUN'),
    Fleur('Giroflée', [5, 6], 'GRIS_JAUNE'),
    Fleur('Framboisier', [5, 6], 'VERT_PALE'),
    Fleur('Marronnier', [5, 6], 'ROUGE_FONCE'),
    Fleur('Coucou blanc', [5, 9], 'JAUNE_BRUN'),
    Fleur('Lavande', [6, 9], 'GRIS_JAUNE'),
    Fleur('Sapin', [6, 9], 'BLANC'),
    Fleur('Boule de neige', [6, 9], 'GRIS_CLAIR'),
    Fleur('Knautié des champs', [6, 7], 'ROSE'),
    Fleur('Bleué', [6, 7], 'GRIS_JAUNE'),
    Fleur('Coquelicot', [6, 7], 'NOIR'),
    Fleur('Tilleul', [6, 7], 'JAUNE_VERT'),
    Fleur('Châtaigner', [6, 7], 'GRIS_JAUNE'),
    Fleur('Réséda', [6, 10], 'ROUGE_FONCE'),
    Fleur('Trèfle blanc', [6, 10], 'BRUN_VERT'),
    Fleur('Pavot', [6, 8], 'BLEU_ROUGE'),
    Fleur('Vigne Vierge', [7, 8], 'JAUNE'),
    Fleur('Asperge', [7, 7], 'JAUNE_OR'),
    Fleur('Ronce', [6, 8], 'VERT_PALE'),
    Fleur('Bruyère', [8, 9], 'GRIS_JAUNE'),
    Fleur('Verge d\'or', [8, 9], 'JAUNE_OR'),
    Fleur('Lière', [9, 11], 'ORANGE_BRUN'),
    Fleur('Chalef Piquant', [9, 12], 'GRIS_JAUNE'),
    Fleur('Hellébore', [12, 3], 'GRIS_JAUNE'),
    Fleur('Tournesol', [7, 10], 'ORANGE'),
]