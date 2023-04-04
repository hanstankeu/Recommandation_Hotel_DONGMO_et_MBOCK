from flask import Flask, request, render_template, jsonify
import pickle
import pandas as pd


# recomm = pickle.load(open('model/Pickle_Hotel_Model.pkl','rb'))
# similary = pickle.load(open('model/Pickle_Hotel_Similary.pkl','rb'))

# def fetch_poster (hotel_voisin_id):
#     url= "https://www.expedia.fr/Tous-Les-Hotels-De-Yaounde.d3886.Voyage-Guide-Ville-Tout-Hotels".format(hotel_voisin_id)
#     data = request.get (url)
#     data = data.json()
#     poster_path = data['poster_path']
#     full_path = "https://www.expedia.fr/Yaounde-Hotel-Hilton-Yaounde.h185147.Description-Hotel"+poster_path
#     return full_path


# def recommand(hotel_voisin):
#     index = recomm[recomm['title']==hotel_voisin].index[0]
#     distances = sorted(list(enumerate(similary[index])),reverse=True, key =lambda x: x[1])
#     recommended_hotel_name = []
#     recommended_hotel_poster = []
#     for i in distances [1:6]:
#         hotel_voisin_id = hotel_voisin.iloc[i[0]].hotel_voisin_id
#         recommended_hotel_poster.append(fetch_poster(hotel_voisin))



app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")



@app.route("/recommandation")
def recommandation():
    return render_template('recommandation.html')


#@app.route('/hotel', methods = ['GET','POST'])
@app.route("/hotel")
def hotel():
    hotel1 = pd.read_csv('model/data_end.csv')

    data1 = hotel1[0]
    df = pd.DataFrame(list(data1.item()))

    return render_template('hotel.html', hotel1 = hotel1,  df=df)


    
if __name__== "__main__":
    app.debug = True
    app.run()

#  """    hotel_voisin_list = recomm['title'].values
#     if request.method == "POST":
#         try:
#             if request.form:
#                 hotel_voisin_name = request.form['recomm']
#                 #print(recomm_name)
#                 recommended_hotel_name,recommended_hotel_poster  = recommand(hotel_voisin_name)
#                 return render_template("recommandation.html", recomm_name=recommended_hotel_name, poster = recommended_hotel_poster,hotel_voisin_list=hotel_voisin_list)
#         except Exception as e:
#             error = {'error':e}
#             return render_template("recommandation.html",hotel_voisin_list=hotel_voisin_list)
#     else:
#         return render_template("recommandation.html", hotel_voisin_list=hotel_voisin_list)
#  """


    