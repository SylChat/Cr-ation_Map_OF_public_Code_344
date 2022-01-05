########################################
#Lecture du csv des OF                 #
########################################
#Assignation du chemin des fichiers
import urllib
urlFichCsvOF = "https://www.monactiviteformation.emploi.gouv.fr/mon-activite-formation/public/listePubliqueOF?format=csv"
urllib.request.urlretrieve(urlFichCsvOF,'/content/drive/MyDrive/OF.csv')
sCSV = "/content/drive/MyDrive/OF.csv"
dCSV = "/content/drive/MyDrive/OF_Filtres.csv"

#df = dataframe issu du fichier source (sCSV)
df = pd.read_csv(sCSV, sep=";", dtype="str")

#dfTrier = dataframe qui recevra les données triées
CodeSST = "344"
dfTemp = df.loc[((df[' informationsDeclarees.specialitesDeFormation.codeSpecialite1'] == CodeSST)|
                 (df[' informationsDeclarees.specialitesDeFormation.codeSpecialite2'] == CodeSST)| 
                 (df[' informationsDeclarees.specialitesDeFormation.codeSpecialite3'] == CodeSST))]
dfFiltree=dfTemp[pd.notnull(dfTemp[' adressePhysiqueOrganismeFormation.ville'])]

#Sélection des colonnes
selected_column = dfFiltree.iloc[:,[2,3,5,6,7]]
dfTrier = selected_column.copy()
#boucle sur chaque pour geocoder les adresses
for i, row in dfTrier.iterrows():
  adresse = str(row[' adressePhysiqueOrganismeFormation.voie']) + ", " + str(row[' adressePhysiqueOrganismeFormation.codePostal']) + ", " + str(row[' adressePhysiqueOrganismeFormation.ville'])
  dfTrier.loc[i,['GPSX','GPSY']] = LatLong(adresse)

#exportation au format CSV
dfTrier.to_csv(dCSV)

########################################
#Geocodage via API adresse.data.gouv.fr#
########################################
import requests
import pandas as pd
import urllib.parse
#Fonction pour obtenir coordonnées GPS
def LatLong(Ad: str):
  if Ad != "":
    try:
      url = 'https://api-adresse.data.gouv.fr/search/?q=' + urllib.parse.quote(Ad)
      response = requests.get(url).json()
      #print(response)
      X = (response['features'][0]['geometry']['coordinates'][1])
      Y = (response['features'][0]['geometry']['coordinates'][0])
      #print (response)
      return [X,Y]
    except:
      Ad=input('Corriger l adresse pour pouvoir la géocoder ' + Ad)
      url = 'https://api-adresse.data.gouv.fr/search/?q=' + urllib.parse.quote(Ad)
      response = requests.get(url).json()
      #print(response)
      X = (response['features'][0]['geometry']['coordinates'][1])
      Y = (response['features'][0]['geometry']['coordinates'][0])
      #print (response)
      return [X,Y]
  else:
    print('Erreur')
    return "Adresse non geocodable"
#fin de la fonction
#####################

####################
#Création de la map#
####################
#importation des librairies
import folium
import pandas as pd
#Définition du chemin du CSV
CSV="/content/drive/MyDrive/OF_Filtres.csv"
#Création du dataframe
df_source=pd.read_csv(CSV,sep=",")

#Création de la maps vide centrée sur la france
m = folium.Map(location=[45,5], zoom_start=6)

#Ajout des points à la map
for index, row in df_source.iterrows():
  #print(row[' denomination'], row['GPSX'],row['GPSY'])
  folium.Marker(location=[row['GPSX'],row['GPSY']],popup=row[' denomination']+ row[' adressePhysiqueOrganismeFormation.voie']).add_to(m)

#show map
m.save('/content/drive/MyDrive/Maps.html')
m
