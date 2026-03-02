import os
import pandas as pd
from config import (
    INPUT_XLSX,
    OUTPUT_XLSX,
    SHEET_NAME,
    COLUMN_LINKEDIN,
)

def load_dataframe() -> pd.DataFrame:
    if not os.path.isfile(INPUT_XLSX):
        raise FileNotFoundError(f"Fichier d'entree '{INPUT_XLSX}' introuvable.")

    try:
        df_input = pd.read_excel(INPUT_XLSX, sheet_name=SHEET_NAME)
    except Exception as e:
        raise RuntimeError(
            f"Erreur lors de la lecture de '{INPUT_XLSX}' (feuille '{SHEET_NAME}') : {e}"
        )

    if os.path.isfile(OUTPUT_XLSX):
        try:
            df_output = pd.read_excel(OUTPUT_XLSX)
            print(f"  -> Reprise depuis '{OUTPUT_XLSX}', {len(df_output)} lignes deja traitees.")

            if set(df_input.columns) <= set(df_output.columns):
                return df_output.copy()
        except Exception as e:
            print(f"Erreur lecture '{OUTPUT_XLSX}' : {e}")
            print("On repart de zero sur le fichier d'entree.")

    df = df_input.copy()
    if COLUMN_LINKEDIN not in df.columns:
        df[COLUMN_LINKEDIN] = ""

    return df

def save_dataframe(df: pd.DataFrame) -> None:
    """Sauvegarde le DataFrame en .xlsx."""
    try:
        df.to_excel(OUTPUT_XLSX, index=False)
    except Exception as e:
        print(f"  -> Echec de l'enregistrement : {e}")