import dash
from dash import html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd
import folium
import numpy as np
import os
import plotly.graph_objects as go
from geopy.geocoders import Nominatim
import datetime
from collections import Counter

dash.register_page(__name__, path='/')

chemin_fichier = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "data.csv")
chemin_fichier1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "df_final.xlsx")

if os.path.exists(chemin_fichier):
    df = pd.read_csv(chemin_fichier)
else:
    print(f"Erreur : Le fichier {chemin_fichier} n'existe pas.")

arrondissements = df["arrondissement_residence"].unique()
quartiers = df["quartier_residence"].unique()

#Construction de la carte 
def create_cameroon_map(arrondissement=None, quartier=None):
    file_path = "assets/cameroon_map.html"
    map_cameroon = folium.Map(location=[3.848, 11.5021], zoom_start=6)

    grouped_data = pd.read_csv(chemin_fichier)

    # Filtrage selon l'entrée utilisateur
    if arrondissement:
        grouped_data = grouped_data[grouped_data["arrondissement_residence"] == arrondissement]
    if quartier:
        grouped_data = grouped_data[grouped_data["quartier_residence"] == quartier]

    if "coords" not in grouped_data.columns:
        raise KeyError("La colonne 'coords' est introuvable dans le fichier CSV.")

    # Ajout des marqueurs
    for _, row in grouped_data.iterrows():
        try:
            lat, lon = eval(row["coords"])  
            popup_text = f"{row['arrondissement_residence']} - {row['quartier_residence']}<br>Donneurs: {row['count']}"
            folium.Marker([lat, lon], popup=popup_text, icon=folium.Icon(color="red")).add_to(map_cameroon)
        except Exception as e:
            print(f"Erreur avec la ligne {row.to_dict()}: {e}")

    os.makedirs("assets", exist_ok=True)
    map_cameroon.save(file_path)
    return file_path

# Générer la carte
map_path = create_cameroon_map()
with open(map_path, 'r') as f:
    map_html = f.read()


#Diagramme circulaire
if os.path.exists(chemin_fichier1):
    df1 = pd.read_excel(chemin_fichier1)
else:
    print(f"Erreur : Le fichier {chemin_fichier1} n'existe pas.")
    df1 = pd.DataFrame()

if not df1.empty:
    donneurs_malades = df1[df1["a_t_il_deja_donne_sang"] == "Oui"].copy()

    conditions_medicales = [
        "raison_indisponibilite_antibiotherapie",
        "raison_indisponibilite_hemoglobine_bas",
        "raison_indisponibilite_temps_don_inf_3_mois",
        "raison_indisponibilite_ist",
        "raison_de_lindisponibilite_de_la_femme_[allaitement]",
        "raison_de_lindisponibilite_de_la_femme_[a_accoucher_ces_6_derniers_mois]",
        "raison_de_lindisponibilité_de_la_femme_[interruption_de_grossesse__ces_06_derniers_mois]",
        "raison_de_lindisponibilite_de_la_femme_[est_enceinte]",
        "raison_non_eligibilite_total_transfusion",
        "raison_non_eligibilite_Total_hiv",
        "raison_non_eligibilite_total_opere",
        "raison_non_eligibilite_total_drepanocytaire",
        "raison_non_eligibilite_total_diabetique",
        "raison_non_eligibilite_total_hypertendu",
        "raison_non_eligibilite_total_asthmatique",
        "raison_non_eligibilite_total_cardiaque",
        "raison_non_eligibilite_total_tatoue",
        "raison_non_eligibilite_total_scarifie",
        "autres_raisons",
        "si_autres_raisons"
    ]

    # Fonction pour compter le nombre de "Oui" dans une colonne
    def compter_oui(colonne):
        return donneurs_malades[colonne].str.lower().eq("oui").sum()

    # Créer un DataFrame avec les résultats
    resultats = pd.DataFrame({
        "Condition": conditions_medicales,
        "Nombre de dons": [compter_oui(col) for col in conditions_medicales]
    })

    # Renommer les conditions pour l'affichage
    resultats["Condition médicale"] = resultats["Condition"].replace({
        "raison_non_eligibilite_total_opere": "Opéré",
        "raison_de_lindisponibilite_de_la_femme_[est_enceinte]": "Est enceinte",
        "raison_non_eligibilite_total_drepanocytaire": "Drépanocytaire",
        "raison_de_lindisponibilite_de_la_femme_[allaitement]": "Allaitement",
        "raison_de_lindisponibilite_de_la_femme_[a_accoucher_ces_6_derniers_mois]": "Accouché (6 mois)",
        "raison_de_lindisponibilité_de_la_femme_[interruption_de_grossesse__ces_06_derniers_mois]": "Interruption grossesse (6 mois)",
        "raison_non_eligibilite_total_transfusion": "Transfusion",
        "raison_non_eligibilite_Total_hiv": "VIH",
        "raison_non_eligibilite_total_diabetique": "Diabétique",
        "raison_non_eligibilite_total_hypertendu": "Hypertendu",
        "raison_non_eligibilite_total_asthmatique": "Asthmatique",
        "raison_non_eligibilite_total_cardiaque": "Cardiaque",
        "raison_non_eligibilite_total_tatoue": "Tatoué",
        "raison_non_eligibilite_total_scarifie": "Scarifié",
        "raison_indisponibilite_antibiotherapie": "Antibiothérapie",
        "raison_indisponibilite_hemoglobine_bas": "Hémoglobine basse",
        "raison_indisponibilite_temps_don_inf_3_mois": "Don récent (<3 mois)",
        "raison_indisponibilite_ist": "IST",
        "autres_raisons": "Autres raisons",
        "si_autres_raisons": "Si autres raisons"
    })

    # Trier par nombre de "Oui" et sélectionner les 5 premiers
    resultats = resultats.sort_values(by="Nombre de dons", ascending=False).head(5)

    # Créer le diagramme circulaire
    fig_pie = px.pie(
        resultats,
        names="Condition médicale", 
        values="Nombre de dons",
        color_discrete_sequence=["#FFC7C8", "#CF5A5C", "#ED8587", "#EFC94C", "#310809"],
        hole=0.7,
        hover_data=['Nombre de dons'] 
    )

    # Personnalisation
    fig_pie.update_traces(
        textinfo='none',  
        hoverinfo="label+value", 
        marker=dict(line=dict(color="white", width=1)),
    )

    fig_pie.update_layout(
        showlegend=True,  
        margin=dict(l=65, r=0, t=0, b=10),
        hoverlabel=dict(
            bgcolor="#DFA3A3",
            font_size=12,  
            bordercolor="black",
        ),
        width=400,
        height=180,
    )

# Construction du diagramme en bâtons
donneurs_malades = df1[df1["a_t_il_deja_donne_sang"] == "Oui"].copy()

# Liste des champs représentant une condition médicale
conditions_rename = {
    "raison_non_eligibilite_total_opere": "Opéré",
    "raison_de_lindisponibilite_de_la_femme_[est_enceinte]": "Est enceinte",
    "raison_non_eligibilite_total_drepanocytaire": "Drépanocytaire",
    "raison_de_lindisponibilite_de_la_femme_[allaitement]": "Allaitement",
    "raison_de_lindisponibilite_de_la_femme_[a_accoucher_ces_6_derniers_mois]": "Accouché (6 mois)",
    "raison_de_lindisponibilité_de_la_femme_[interruption_de_grossesse__ces_06_derniers_mois]": "Interruption grossesse (6 mois)",
    "raison_non_eligibilite_total_transfusion": "Transfusion",
    "raison_non_eligibilite_Total_hiv": "VIH",
    "raison_non_eligibilite_total_diabetique": "Diabétique",
    "raison_non_eligibilite_total_hypertendu": "Hypertendu",
    "raison_non_eligibilite_total_asthmatique": "Asthmatique",
    "raison_non_eligibilite_total_cardiaque": "Cardiaque",
    "raison_non_eligibilite_total_tatoue": "Tatoué",
    "raison_non_eligibilite_total_scarifie": "Scarifié",
    "raison_indisponibilite_antibiotherapie": "Antibiothérapie",
    "raison_indisponibilite_hemoglobine_bas": "Hémoglobine basse",
    "raison_indisponibilite_temps_don_inf_3_mois": "Don récent (<3 mois)",
    "raison_indisponibilite_ist": "IST"
}

# Fonction pour extraire les dates uniques et compter les "Oui" et "Non"
def extraire_dates_uniques_et_compter(colonne):
    dates_oui = donneurs_malades[donneurs_malades[colonne].str.lower() == "oui"]["si_oui_date_dernier_don"].fillna("24-03-2020").unique().tolist()
    dates_non = donneurs_malades[donneurs_malades[colonne].str.lower() == "non"]["si_oui_date_dernier_don"].fillna("24-03-2020").unique().tolist()
    return {"oui": dates_oui, "non": dates_non}

# Créer un dictionnaire pour stocker les résultats
resultats_dates_uniques = {}

# Analyser chaque condition individuellement
for condition in conditions_medicales:
    resultats_dates_uniques[condition] = extraire_dates_uniques_et_compter(condition)

# Calculer le nombre total de participations pour chaque condition
participations = {condition: len(valeurs["oui"]) + len(valeurs["non"]) for condition, valeurs in resultats_dates_uniques.items()}

# Sélectionner les 3 conditions avec le plus de participations
top_conditions = sorted(participations, key=participations.get, reverse=True)[:3]



#Definintion de la page 
layout = html.Div([
    html.Div([
        
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id="arrondissement-dropdown",
                    options=[{"label": arr, "value": arr} for arr in arrondissements],
                    value="Tous",
                    placeholder="Arrondissement",
                    clearable=False,
                    
                ),
                dcc.Dropdown(
                    id="quartier-dropdown",
                    options=[{"label": q, "value": q} for q in quartiers],
                    placeholder="Quartier",
                ),
            ], className="drop-div", style={
                    "display": "flex",
                    "justify-content": "space-between",
                    "width": "100%",
                    "margin-bottom": "0.3rem"}),
            html.Iframe(
                id="map-container",
                srcDoc=open("assets/cameroon_map.html", 'r').read(),  # Carte initiale pré-générée
                width="100%",
                height="350px"
            ),
        ], className="map-block"),

        html.Div([

            html.Div([
                html.Div([
                    html.P("Portions de dons suivant les conditions de santé", className="diagram-p"),
                    html.Span("From 1 Jan to 29 Dec 2019", className="diagram-span"),
                    dcc.Graph(figure=fig_pie)
                ], className="left-section"),
                    
            ], className="diagram-block"),


            html.Div([
                html.P("Participations", className="diagram-P"),
                html.Span(id="total-participations", className="diagram-Sp"),
                dcc.Graph(id="bar-chart"),
                html.P("Donneurs", className="diagram-dp"),
                
                html.Div([
                    html.Div([
                        html.P(id="oui-count"),
                    ], className="Box-number"),
                    
                    html.Div([
                        html.P(id="non-count"),
                    ], className="Box-number"),
                    
                    html.Div([    
                        html.P(id="selected-condition"),     
                    ], className="dropdown-menu")
                ], className='Box-stat'),

                html.Div([
                    html.P("Eligibles"),
                    html.P("Non-eligibles")
                ], className="Box-text"),

                html.Div([
                    dcc.Checklist(
                        id="condition-checklist",
                        className="checkbox-line",
                        options=[
                            {
                                'label': conditions_rename.get(condition, condition), 
                                'value': condition
                            } for condition in top_conditions
                        ],
                        value=[top_conditions[0]],  
                        inline=True
                    ),
                ], className="")
            ], className="diagram-block2")

        ], className="diagram-container")

    ], className="grid main-content")

], className="content-container")

@callback(
    Output("map-container", "srcDoc"),
    [Input("arrondissement-dropdown", "value"),
     Input("quartier-dropdown", "value")]
)
def update_map(selected_arrondissement, selected_quartier):
    file_path = create_cameroon_map(selected_arrondissement, selected_quartier)

    with open(file_path, 'r') as f:
        return f.read()
    

@callback(
    Output("bar-chart", "figure"),
    Output("total-participations", "children"),
    Output("oui-count", "children"),
    Output("non-count", "children"),
    Output("selected-condition", "children"),
    Input("condition-checklist", "value")
)
def update_chart(selected_conditions):
    top_conditions = sorted(participations, key=participations.get, reverse=True)[:3]
    
    # Filtrer les conditions de la checklist pour n'inclure que les top 3
    selected_conditions = [c for c in selected_conditions if c in top_conditions]
    
    if not selected_conditions:
        selected_conditions = [top_conditions[0]]  # Par défaut, la première condition
    
    selected_condition = selected_conditions[0]
    
    # Compter le nombre total de "Oui" et "Non"
    total_oui = donneurs_malades[donneurs_malades[selected_condition].str.lower() == "oui"].shape[0]
    total_non = donneurs_malades[donneurs_malades[selected_condition].str.lower() == "non"].shape[0]
    
    # Créer le graphique à barres
    fig = go.Figure(data=[
        go.Bar(x=['Oui', 'Non'], y=[total_oui, total_non], 
               marker_color=['#CF5A5C', 'lightgrey'])
    ])
    
    fig.update_layout(
        title='',
        height=150, 
        width=600, 
        showlegend=False, 
        margin=dict(l=0, r=0, t=15, b=0)
    )

    return fig, participations[selected_condition], total_oui, total_non, conditions_rename.get(selected_condition, selected_condition)

top_conditions_renamed = [conditions_rename.get(condition, condition) for condition in top_conditions]


dcc.Checklist(
    id="condition-checklist",
    options=[{"label": condition, "value": list(conditions_rename.keys())[list(conditions_rename.values()).index(condition)]} for condition in top_conditions_renamed],
    value=[list(conditions_rename.keys())[list(conditions_rename.values()).index(top_conditions_renamed[0])]]
)