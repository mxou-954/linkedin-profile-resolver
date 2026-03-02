# LinkedIn Scraper — Recherche automatique de profils LinkedIn

Script Python qui enrichit un fichier Excel en trouvant automatiquement le premier lien LinkedIn correspondant à chaque requête via Google Search.

Conçu pour retrouver rapidement les pages LinkedIn d'entreprises ou de contacts à partir d'une liste de prospects.

---

## Comment ça marche

Pour chaque ligne du fichier Excel :

1. Lit la requête dans la colonne configurée ("Recherche")
2. Lance une recherche Google (via `googlesearch-python`)
3. Parcourt les résultats et retourne le premier lien `linkedin.com`
4. Écrit le résultat dans la colonne "Lien_Linkedin"
5. Sauvegarde après chaque ligne (reprise automatique en cas d'interruption)

Le script détecte automatiquement les lignes déjà traitées et les passe.

---

## Structure

```
linkedin-scraper/
├── main.py              ← Point d'entrée + boucle principale
├── config.py            ← Constantes (fichiers, colonnes, délais)
├── scraper.py           ← Recherche Google + détection LinkedIn
├── excel_handler.py     ← Lecture / écriture Excel + reprise
├── requirements.txt
└── README.md
```

---

## Installation

### Prérequis

- Python >= 3.10

### Dépendances

```bash
pip install -r requirements.txt
```

---

## Utilisation

```bash
python main.py
```

Pas d'arguments en ligne de commande : tout se configure dans `config.py`.

### Progression en temps réel

```
350 lignes à traiter.

[1/350] Requête : 'Dupont SAS directeur linkedin' ... 
  → Lien LinkedIn trouvé : https://www.linkedin.com/in/jean-dupont
[2/350] Déjà renseigné → 'https://www.linkedin.com/company/martin-co'
[3/350] Requête vide, on passe.
```

---

## Configuration

Tout se modifie dans `config.py` :

| Variable | Default | Description |
|----------|---------|-------------|
| `INPUT_XLSX` | `sss.xlsx` | Fichier Excel d'entrée |
| `OUTPUT_XLSX` | `output.xlsx` | Fichier Excel de sortie |
| `SHEET_NAME` | `ColisConsult` | Nom de l'onglet à lire |
| `COLUMN_QUERY` | `Recherche` | Colonne contenant la requête Google |
| `COLUMN_LINKEDIN` | `Lien_Linkedin` | Colonne de sortie pour le lien trouvé |
| `MAX_RESULTS_GOOGLE` | `10` | Nombre de résultats Google inspectés |
| `DELAY_BETWEEN_QUERIES` | `1.0` | Pause entre requêtes (secondes, anti-blocage) |

---

## Format Excel

### Entrée

| Recherche | ... |
|-----------|-----|
| Dupont SAS directeur linkedin | ... |
| Martin & Co linkedin | ... |

### Sortie

| Recherche | Lien_Linkedin | ... |
|-----------|---------------|-----|
| Dupont SAS directeur linkedin | https://www.linkedin.com/in/jean-dupont | ... |
| Martin & Co linkedin | https://www.linkedin.com/company/martin-co | ... |

---

## Reprise après interruption

- **Ctrl+C** : le script intercepte le signal et sauvegarde immédiatement le fichier de sortie avant de quitter.
- **Relance** : si `output.xlsx` existe déjà, le script reprend là où il en était en sautant les lignes déjà renseignées.
- **Crash** : le fichier est sauvegardé après chaque ligne, la perte maximale est d'une seule requête.

---

## Notes

- Augmentez `DELAY_BETWEEN_QUERIES` si Google bloque les requêtes (erreurs 429).
- La librairie `googlesearch-python` fait du scraping Google : elle peut être bloquée en cas d'usage intensif. Prévoyez des pauses raisonnables.
