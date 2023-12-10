import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import random

def extract_data_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    def lip():
        ma_liste=[]
        for i in table:
            prix = i.find("span", class_="priceTag hardShadow float-right floatL")
            titre=i.find("div", class_="inBlock w100")
            if prix and titre:  # Vérifier si les éléments prix et titre sont trouvés
                prix_text = prix.text.strip()  # Obtenir le texte de l'élément prix
                titre_text = titre.text.strip()  # Obtenir le texte de l'élément titre

                diction = {"prix": prix_text, "titre": titre_text}
                ma_liste.append(diction)
        return ma_liste
    
    table = soup.find_all("li")
    recuperation = lip()

    # Nettoyer les prix
    for element in recuperation:
        if 'prix' in element:
            prix_brut = element['prix']
            prix_nettoye = prix_brut.replace('\xa0', ' ')
            element['prix'] = prix_nettoye  # Remplacer la valeur brute par la valeur nettoyée

    # Créer un DataFrame pandas à partir de la liste de dictionnaires
    df = pd.DataFrame(recuperation)

    return df

# Interface Streamlit
def main():
    st.title("Extraction de données d'annonces immobilières")
    st.subheader("AUTEUR : DJÉGUI-WAGUÉ")
    
    # Demander à l'utilisateur d'entrer l'URL
    url = st.text_input("Entrez l'URL de la page d'annonces immobilières")

    if st.button("Extraire les données"):
        if url:
            # Extraire les données à partir de l'URL
            data = extract_data_from_url(url)

            # Afficher le DataFrame
            # Afficher les statistiques et les données
            st.write(f"Nombre de produits : {len(data)}")
            st.write(data)
            data[['Nb_Chambres', 'Surface']] = data["titre"].str.split(', ', expand=True)
            data= data.drop("titre",axis=1)
            data["Nb_Chambres"]=data["Nb_Chambres"].str.replace("chambres", "").str.replace("chambre","").astype(int)
            data['prix'] = data['prix'].str.replace(' DH', '').replace("Prix à consulter","rien")
            data['prix'] = data['prix'].str.replace(' ', '', regex=False)
            data['prix'] = pd.to_numeric(data['prix'], errors='coerce')
            #data["prix"]= data['prix'].astype(int)
            data["Surface"]= data["Surface"].str.replace("m²","")
            # Convertir la colonne "surface" en type numérique (float)
            data['Surface'] = pd.to_numeric(data['Surface'], errors='coerce')
            
            data = data.dropna().astype(int)
            
            # Supprimer les lignes avec des valeurs nulles dans n'importe quelle colonne
            
            typess= data["Surface"].dtype
            
            st.write(typess)
            st.write(data)
            st.write("Statistiques sur les prix :")

                        # Calcul de la matrice de corrélation (supposons que vous ayez déjà une DataFrame 'data')
            matrice_correlation = data.corr()


            palett = ['viridis', 'coolwarm', 'YlGnBu', 'BuPu']  # Liste de palettes disponibles
            random_palett = random.choice(palett)
            # Affichage des statistiques descriptives avec des couleurs utilisant Seaborn
            plt.figure(figsize=(10, 6))
            sns.heatmap(matrice_correlation, annot=True, cmap=random_palett, fmt=".2f")
            plt.title('Matrice de corrélation')
            plt.xticks(rotation=45)
            plt.yticks(rotation=0)

            # Affichage du graphique dans Streamlit
            st.pyplot(plt)

            st.write("")
            st.write("")
            st.write("")
            # Calcul des statistiques descriptives
            stats = data.describe()

            # Affichage de la heatmap des statistiques descriptives avec Seaborn
            # Génération aléatoire d'une palette de couleurs
            palettes = ['viridis', 'coolwarm', 'YlGnBu', 'BuPu']  # Liste de palettes disponibles
            random_palette = random.choice(palettes)
            plt.figure(figsize=(8, 6))
            sns.heatmap(stats, annot=True, cmap=random_palette, fmt=".2f", cbar=False)
            plt.title('Statistiques Descriptives (Tableau)')
            # Affichage du graphique dans Streamlit
            st.pyplot(plt)

             
            interpretation = """
            - count (nombre) : nombre d'observations non nulles pour chaque colonne.
            - mean (moyenne) : moyenne arithmétique des valeurs dans chaque colonne.
            - std (écart type) : mesure de la dispersion des valeurs par rapport à la moyenne.
            - min (minimum) : valeur la plus basse dans chaque colonne.
            - 25% (premier quartile) : 25% des données en dessous, 75% au-dessus.
            - 50% (médiane) : point où 50% des données sont en dessous, 50% au-dessus.
            - 75% (troisième quartile) : 75% des données en dessous, 25% au-dessus.
            - max (maximum) : valeur la plus élevée dans chaque colonne.
            """

           # Affichage de l'interprétation des statistiques descriptives
            st.title("Interpretation des statistques :")
            st.write(interpretation)               
        else:
            st.warning("Veuillez entrer une URL valide")

if __name__ == "__main__":
    main()


