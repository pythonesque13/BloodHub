from fastapi import FastAPI
import joblib
import pandas as pd
from pydantic import BaseModel, Field

app = FastAPI()

# Charger le pipeline
pipeline = joblib.load("api/model.pkl")

# Créer un modèle Pydantic pour les données d'entrée
class DonSangInput(BaseModel):
    genre: str = Field(..., alias="Genre_", description="Genre du donneur")
    age: int = Field(..., alias="Age", description="Age du donneur")
    deja_donne: str = Field(..., alias="A-t-il_(elle)_déjà_donné_le_sang_", description="Historique de don")
    taux_hemoglobine: float = Field(..., alias="Taux_d’hémoglobine_", description="Taux d'hémoglobine")
    sous_antibiotherapie: str = Field(..., alias="Raison_indisponibilité__[Est_sous_anti-biothérapie__]")
    hemoglobine_bas: str = Field(..., alias="Raison_indisponibilité__[Taux_d’hémoglobine_bas_]")
    dernier_don_recent: str = Field(..., alias="Raison_indisponibilité__[date_de_dernier_Don_<_3_mois_]")
    ist_recente: str = Field(..., alias="Raison_indisponibilité__[IST_récente_(Exclu_VIH,_Hbs,_Hcv)]")
    ddr_mauvais: str = Field(..., alias="Raison_de_l’indisponibilité_de_la_femme_[La_DDR_est_mauvais_si_<14_jour_avant_le_don]")
    allaitement: str = Field(..., alias="Raison_de_l’indisponibilité_de_la_femme_[Allaitement_]")
    accouchement_recent: str = Field(..., alias="Raison_de_l’indisponibilité_de_la_femme_[A_accoucher_ces_6_derniers_mois__]")
    interruption_grossesse: str = Field(..., alias="Raison_de_l’indisponibilité_de_la_femme_[Interruption_de_grossesse__ces_06_derniers_mois]")
    enceinte: str = Field(..., alias="Raison_de_l’indisponibilité_de_la_femme_[est_enceinte_]")
    antecedent_transfusion: str = Field(..., alias="Raison_de_non-eligibilité_totale__[Antécédent_de_transfusion]")
    porteur_virus: str = Field(..., alias="Raison_de_non-eligibilité_totale__[Porteur(HIV,hbs,hcv)]")
    opere: str = Field(..., alias="Raison_de_non-eligibilité_totale__[Opéré]")
    drepanocytaire: str = Field(..., alias="Raison_de_non-eligibilité_totale__[Drepanocytaire]")
    diabetique: str = Field(..., alias="Raison_de_non-eligibilité_totale__[Diabétique]")
    hypertendu: str = Field(..., alias="Raison_de_non-eligibilité_totale__[Hypertendus]")
    asthmatique: str = Field(..., alias="Raison_de_non-eligibilité_totale__[Asthmatiques]")
    cardiaque: str = Field(..., alias="Raison_de_non-eligibilité_totale__[Cardiaque]")
    tatoue: str = Field(..., alias="Raison_de_non-eligibilité_totale__[Tatoué]")
    scarifie: str = Field(..., alias="Raison_de_non-eligibilité_totale__[Scarifié]")

    class Config:
        from_attributes = True
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "genre": "Homme",
                "age": 25,
                "deja_donne": "Non",
                "taux_hemoglobine": 14.5,
                "sous_antibiotherapie": "Non",
                "hemoglobine_bas": "Non",
                "dernier_don_recent": "Non",
                "ist_recente": "Non",
                "ddr_mauvais": "Non",
                "allaitement": "Non",
                "accouchement_recent": "Non",
                "interruption_grossesse": "Non",
                "enceinte": "Non",
                "antecedent_transfusion": "Non",
                "porteur_virus": "Non",
                "opere": "Non",
                "drepanocytaire": "Non",
                "diabetique": "Non",
                "hypertendu": "Non",
                "asthmatique": "Non",
                "cardiaque": "Non",
                "tatoue": "Non",
                "scarifie": "Non"
            }
        }

# Définir les labels possibles
ELIGIBILITY_LABELS = {
    0: "Eligible",
    1: "Définitivement non-eligible",
    2: "Temporairement Non-eligible"
}

@app.post("/predict")
def predict(donnees: DonSangInput):
    # Créer un DataFrame avec toutes les features dans le bon ordre
    features = pd.DataFrame([[
        donnees.genre,
        donnees.age,
        donnees.deja_donne,
        donnees.taux_hemoglobine,
        donnees.sous_antibiotherapie,
        donnees.hemoglobine_bas,
        donnees.dernier_don_recent,
        donnees.ist_recente,
        donnees.ddr_mauvais,
        donnees.allaitement,
        donnees.accouchement_recent,
        donnees.interruption_grossesse,
        donnees.enceinte,
        donnees.antecedent_transfusion,
        donnees.porteur_virus,
        donnees.opere,
        donnees.drepanocytaire,
        donnees.diabetique,
        donnees.hypertendu,
        donnees.asthmatique,
        donnees.cardiaque,
        donnees.tatoue,
        donnees.scarifie
    ]], columns=[
        "Genre_",
        "Age",
        "A-t-il_(elle)_déjà_donné_le_sang_",
        "Taux_d’hémoglobine_",
        "Raison_indisponibilité__[Est_sous_anti-biothérapie__]",
        "Raison_indisponibilité__[Taux_d’hémoglobine_bas_]",
        "Raison_indisponibilité__[date_de_dernier_Don_<_3_mois_]",
        "Raison_indisponibilité__[IST_récente_(Exclu_VIH,_Hbs,_Hcv)]",
        "Raison_de_l’indisponibilité_de_la_femme_[La_DDR_est_mauvais_si_<14_jour_avant_le_don]",
        "Raison_de_l’indisponibilité_de_la_femme_[Allaitement_]",
        "Raison_de_l’indisponibilité_de_la_femme_[A_accoucher_ces_6_derniers_mois__]",
        "Raison_de_l’indisponibilité_de_la_femme_[Interruption_de_grossesse__ces_06_derniers_mois]",
        "Raison_de_l’indisponibilité_de_la_femme_[est_enceinte_]",
        "Raison_de_non-eligibilité_totale__[Antécédent_de_transfusion]",
        "Raison_de_non-eligibilité_totale__[Porteur(HIV,hbs,hcv)]",
        "Raison_de_non-eligibilité_totale__[Opéré]",
        "Raison_de_non-eligibilité_totale__[Drepanocytaire]",
        "Raison_de_non-eligibilité_totale__[Diabétique]",
        "Raison_de_non-eligibilité_totale__[Hypertendus]",
        "Raison_de_non-eligibilité_totale__[Asthmatiques]",
        "Raison_de_non-eligibilité_totale__[Cardiaque]",
        "Raison_de_non-eligibilité_totale__[Tatoué]",
        "Raison_de_non-eligibilité_totale__[Scarifié]"
    ])

    # Faire la prédiction
    prediction = pipeline.predict(features)[0]
    probabilities = pipeline.predict_proba(features)[0]
    result = {
        "status": ELIGIBILITY_LABELS[prediction],
        "probabilities": {
            "Eligible": float(probabilities[0]),
            "Définitivement non-eligible": float(probabilities[1]),
            "Temporairement Non-eligible": float(probabilities[2])
        }
    }

    # Ajouter des recommandations selon le statut
    if result["status"] == "Eligible":
        result["message"] = "Vous êtes éligible au don de sang."
    elif result["status"] == "Temporairement Non-eligible":
        result["message"] = "Vous n'êtes pas éligible temporairement au don de sang. Veuillez réessayer plus tard."
    else:
        result["message"] = "Vous n'êtes pas éligible au don de sang de façon définitive."

    return result