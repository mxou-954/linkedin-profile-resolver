import sys
import signal
import time
from config import COLUMN_QUERY, COLUMN_LINKEDIN, OUTPUT_XLSX, DELAY_BETWEEN_QUERIES
from excel_handler import load_dataframe, save_dataframe
from scraper import find_first_linkedin

_df_global = None

def _on_interrupt(signum=None, frame=None):
    if _df_global is not None:
        save_dataframe(_df_global)
        print(f"\nScript interrompu : contenu sauvegarde dans '{OUTPUT_XLSX}'.")
    else:
        print("\nScript interrompu avant le chargement des donnees.")
    sys.exit(0)

signal.signal(signal.SIGINT, _on_interrupt)

def main() -> None:
    global _df_global

    df = load_dataframe()
    _df_global = df

    if COLUMN_QUERY not in df.columns:
        raise KeyError(
            f"Colonne '{COLUMN_QUERY}' introuvable. Colonnes disponibles : {df.columns.tolist()}"
        )

    total = len(df)
    print(f"{total} lignes a traiter.\n")

    try:
        for idx, row in df.iterrows():
            valeur_actuelle = row[COLUMN_LINKEDIN]
            if isinstance(valeur_actuelle, str) and valeur_actuelle.strip():
                print(f"[{idx+1}/{total}] Deja renseigne -> '{valeur_actuelle.strip()}'")
                continue

            query = str(row[COLUMN_QUERY]).strip()
            if not query:
                print(f"[{idx+1}/{total}] Requete vide, on passe.")
                continue

            print(f"[{idx+1}/{total}] Requete : '{query}'")
            linkedin_url = find_first_linkedin(query)

            if linkedin_url:
                print(f"  -> Lien LinkedIn trouve : {linkedin_url}")
            else:
                print("  -> Aucun lien LinkedIn trouve.")

            df.at[idx, COLUMN_LINKEDIN] = linkedin_url

            save_dataframe(df)
            time.sleep(DELAY_BETWEEN_QUERIES)

    except KeyboardInterrupt:
        _on_interrupt()

    print(f"\nTraitement termine. Fichier de sortie : {OUTPUT_XLSX}")

if __name__ == "__main__":
    main()