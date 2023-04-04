# Importation des packages nécessaires
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import requests as rq
from bs4 import BeautifulSoup as bs
from scipy.spatial.distance import cosine
#%matplotlib inline

## I- Collecte de Données

# 1- Scrapping des des hotels de yaoundé
#Ces hotels seront ceux pour lesquels nous proposerons à l'usager 

# Lien cible
Lien ='https://www.expedia.fr/Tous-Les-Hotels-De-Yaounde.d3886.Voyage-Guide-Ville-Tout-Hotels'
# Télechargement du contenu
Reponse= rq.get(Lien)
# Analyse de la page
Soup = bs(Reponse.content, 'html.parser')




clas="uitk-layout-grid uitk-layout-grid-has-auto-columns uitk-layout-grid-has-columns-by-small uitk-layout-grid-has-columns-by-large uitk-layout-grid-has-columns uitk-layout-grid-has-space uitk-layout-grid-display-grid uitk-spacing no-bullet uitk-spacing-padding-inline-four uitk-spacing-padding-block-two"

retour = Soup.find('ul', class_=clas).find_all('a') # Resultat de la soupe filtrée


# Liste de tous les Hotels de Yaoundé
liste_hotel = []
for ret in retour:
    liste_hotel.append(ret.get_text())
liste_hotel


### 2- Importation du jeu de données sur lesReservations des clients

df = pd.read_csv('HotelReservations.csv')
df.head() # Vérification de l' importattion



# II - Evaluation des Données

print('Dimension :{0}\n{1}'.format(df.shape, df.info()))


numerical = [var for var in df.columns if df[var].dtype != 'O']
numerical


set(df['avg_price_per_room'])


set(df['lead_time'])



set(df['arrival_date'])


set(df['arrival_month'])


# Recherche des données dupliquées
df.duplicated().sum()


df.nunique()


df.isnull().sum()


### Problèmes du jeu de données 'Hotel_Reviews'

#- Problèmes de Qualité**
# required_car_parking_space, lead_time', 'arrival_year', 'arrival_month', 'arrival_date' sont formatés en int


## II- Nettoyage de Données

df_copy = df.copy()


cols = ['required_car_parking_space', 'lead_time', 'arrival_year', 'arrival_month', 'arrival_date']
for col in cols:
    df_copy[col]=df_copy[col].astype('str')


months_letter={'1':'January', '2':'Febuary', '3':'March', '4':'April', '5':'May', '6':'June',
                '7':'July', '8':'August', '9':'September', '10':'October', '11':'November', '12':'December'}
df_copy['arrival_month'].replace(months_letter, inplace=True)


df_copy.info()


###  III - Analyse

## 1- Analyse Univariée

# Variables qualitatives


def diagramme_bar(var):
    '''
    diagramme_bar est une fonction qui prend une colonne en paramètre et 
    affiche le diagramme bar des effectifs de modalités
    '''
    x = df_copy[var].value_counts(sort=True).index
    y = df_copy[var].value_counts(sort=True)
    plt.xticks(rotation=90)
    return plt.bar(x, y);


#### Question1: Quel est le niveau de commodité du repas fréquemment commandé?

## Visualisation1:

var = 'type_of_meal_plan'
diagramme_bar(var)


#### Observation1: Le repas du niveau de commodité 1 est fréquement commandé
## Question2: Quelle est année pour laquelle il y'a eu plus de reservation?

# Visualisation2: 

df_copy['arrival_year'].value_counts().plot(kind='pie')


#### Observation2: L'année 2018 est celle aucours de laquelle le client a plus fait des reservations

### Question3: A Quelle période en termes de mois, le client arrive-t-il à l'hotel?
## Visualisation2: Quel est le repas fréquemment commandé?


var ='arrival_month'
diagramme_bar(var)


#### Observation3: On constacte de Juin en Octobre, représente le moment pour lequel le client arrive à l'hotel

df_copy.info()


#### Question4: Quel est le niveau de commodité par rapport au standing souvent préféré?

#### Visualisation4:

var = 'room_type_reserved'
diagramme_bar(var)


#### Observation4: Le client a généralement préféré le standing du type1 ou le type 4 mais rarement les types 6, 2 et 5 et presque jamais les types 7 et 3
#### Question5: Quel service le client a-t-il souvent sollicité?
### Visualisation5

var ='market_segment_type'
diagramme_bar(var)

#### Observation5: Le client sollicite le plus le service en ligne
### Analyse des variables quatitatives

print(set(df_copy['no_of_children']))
print(set(df_copy['no_of_adults']))


df_copy.describe()


##############################################################################

figure = plt.figure(figsize =(10, 8))
plt.boxplot(df_copy[['no_of_adults', 'no_of_children', 'no_of_weekend_nights', 'no_of_week_nights','repeated_guest','no_of_previous_cancellations', 'no_of_previous_bookings_not_canceled','avg_price_per_room','no_of_special_requests']])
plt.show()

#######


numericals = ['no_of_adults', 'no_of_weekend_nights', 'no_of_week_nights','repeated_guest','no_of_previous_cancellations', 'no_of_previous_bookings_not_canceled','avg_price_per_room','no_of_special_requests']


for var in numericals:
    IQR = df_copy[var].quantile(0.75) - df_copy[var].quantile(0.25)
    Lower = df_copy[var].quantile(0.25) - (1.5*IQR)
    upper = df_copy[var].quantile(0.75) + (1.5*IQR)
    vec=df_copy[var].values
    for i in range(len(vec)):
        if(vec[i]>upper):
            vec[i]=upper
        if (vec[i]<Lower):
            vec[i]=Lower

##########################################################################""
figure = plt.figure(figsize =(10, 8))
plt.boxplot(df_copy[['no_of_adults', 'no_of_children', 'no_of_weekend_nights', 'no_of_week_nights','repeated_guest','no_of_previous_cancellations', 'no_of_previous_bookings_not_canceled','avg_price_per_room','no_of_special_requests']])
plt.show()


### Traitement des données sur l'hotel

type(liste_hotel)

###########################################

dat={'hotel_name':liste_hotel}
hotel =pd.DataFrame(data= dat, columns=['hotel_name'])

##########################################

hotel.head()

######################################
### Création du Trame final
#######################################

df_final = df_copy.set_index(df_copy.index).join(hotel.set_index(hotel.index))


############################################################

df_final.to_csv("data_end.csv") # Sauvegarde


###################################################
# Contruction du système de recommation des hotels


### Préparation des données

df_cleaning = df_final.copy()

################################################################

df_cleaning.drop(columns=['Booking_ID','repeated_guest', 'no_of_previous_cancellations', 'no_of_previous_bookings_not_canceled'], inplace=True)

#####################################################################

df_cleaning=df_cleaning[df_cleaning['hotel_name'].isna() == False]


####################################################################
df_cleaning.tail(4)


##################################################################

df_dumirised = pd.get_dummies(df_cleaning, columns=['required_car_parking_space','type_of_meal_plan','lead_time','room_type_reserved', 'arrival_month', 'arrival_year','arrival_date',
                                                   'market_segment_type', 'booking_status', 'hotel_name'])
                            
####################################################################

set(df_dumirised.columns)

#################################################################"

### Création du Trame des hotls similaires

hotel_similiaire = pd.DataFrame(index= df_dumirised.columns, columns=df_dumirised.columns)


#####################################################################"

hotel_similiaire.columns

########################################################################

df_dumirised.iloc[:,1].shape

####################################################################

hotel_similiaire.columns.shape

###################################################################

# remplire les similitudes
for i in range(0, len(hotel_similiaire.columns)):
    # on boucle à travers les colonnes pour chaque colonne
    for j in range(0, len(hotel_similiaire.columns)):
        hotel_similiaire.iloc[i,j]= 1-cosine(df_dumirised.iloc[:,i],df_dumirised.iloc[:,j])


##########################################################################"

# Creer des hotels en remplacement pour fermer les voisins d'un hotels
hotel_voisin =pd.DataFrame(index=hotel_similiaire.iloc[96:,].index, columns=[i for i in range(1,50)])


############################################################################

# Configuration de l'affichage 
pd.set_option('display.max_rows', None)


#############################################################################

# On remplit les noms des hotels voisins
for i in range(0, 50):
    hotel_voisin.iloc[i, :49]=hotel_similiaire.iloc[96:,i].sort_values(ascending=False)[:49].index


################################################################################

hotel_voisin

###########################################################################

import pickle
Pkl_Filename = "Pickle_Hotel_Model.pkl"  
# Ouverture d'un fichier en mode écriture binaire
with open(Pkl_Filename, 'wb') as file:  
    # Enregistrement du dictionnaire dans le fichier
    pickle.dump(hotel_voisin, file)


df_final.to_csv("hotel_voisin.csv")