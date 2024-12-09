from flask import Flask,request,render_template,redirect,url_for
import numpy as np
import pandas as pd
import pickle


with open('cropPrediction.pkl','rb') as file:
    model=pickle.load(file)



with open('crop_recommendation.pkl','rb') as file:
     model1=pickle.load(file)  




with open('modified_df.pkl', 'rb') as f1:
    loaded_df = pickle.load(f1)


def rain_check(df, state):
    filtered_df = df[df['SUBDIVISION'] == state]
    max_row = filtered_df[filtered_df['ANNUAL'] == filtered_df['ANNUAL'].max()]
    # print(max_row)
    result_dict = max_row.to_dict(orient='records')[0]
    print (result_dict)

with open('rain_check.pkl', 'rb') as f:
    try:
        loaded_function = pickle.load(f)
        loaded_function(loaded_df,2)  # Call the loaded function
    except EOFError:
        print("The pickle file is empty or corrupted.")

app=Flask(__name__)






@app.route('/',methods=['GET'])
def start():
    # model2.rain_check(1)
    return render_template('index.html')

@app.route('/form',methods=['GET','POST'])
def form():
     return render_template("form.html")

# @app.route('/prediction/<int:result>')
# @app.route('/prediction')
# def result(result):
#      return "the yield is "+ str(result)

@app.route('/yield',methods=['GET','POST'])
def submit():
       if request.method=="GET":
          return render_template('form.html')
         
       else:
           
            try:
               #   crops=request.form["crops"]
                crop=int(request.form["crops"])
           
                # Seasons=request.form["seasons"]
                season=int(request.form["seasons"])

                # States=request.form["states"]
                state=int(request.form["states"])
           
                #  Area=request.form["area"]
                area=float(request.form["area"])

                # Production=request.form["production"]
                production=int(request.form["production"])

                # Annual_Rainfall=request.form["annual_rainfall"]
                annual_rainfall=float(request.form["annual_rainfall"])

                # Fertilizer=request.form["fertilizer"]
                fertilizer=float(request.form["fertilizer"])

                # Pesticide=request.form["pesticide"]
                pesticide=float(request.form["pesticide"])

            except ValueError as e:
               print("Invalid input:", e)
               return "Error: Please provide valid inputs."

            print(crop,season,state,area,production,annual_rainfall,fertilizer,pesticide)

            data=(crop,season,state,area,production,annual_rainfall,fertilizer,pesticide)
            data_as_array=np.asarray(data)
            data_as_array_reshape=data_as_array.reshape(1,-1)
 
            try: 
              y1=model.predict(data_as_array_reshape)
              print("Predicted Yield",y1[0])
            
            except Exception as e:
                print("Error during prediction:", e)
                return "Error: Could not predict yield."


            # to pass value in another html file
            return render_template('predict.html',result=y1[0])

           # by this we pass value with url 
           # return redirect(url_for("result",result=y1))

           # return render_template('predict.html')




label_mapping={
    'Rice':1, 'Maize':2, 'Chickpea':3, 'Kidneybeans':4, 'Pigeonpeas':5, 'Mothbeans':6,
 'Mungbean':7, 'Blackgram':8, 'Lentil':9, 'Pomegranate':10, 'Banana':11, 'Mango':12, 'Grapes':12,
 'Watermelon':13, 'Muskmelon':14, 'Apple':15, 'Orange':16, 'Papaya':17, 'Coconut':18, 'Cotton':19,
 'Jute':21, 'Coffee':22
}

            
@app.route('/recommendation',methods=['GET','POST'])
def recommend():
          return render_template('recommendation_form.html')

@app.route('/crop',methods=["GET","POST"])
def think():
     if request.method=="GET":
          return render_template('recommendation_form.html')
     else:
          try:
              nitrogen=int(request.form["nitrogen"])
              phosphorous=int(request.form["phosphorous"])
              potassium=int(request.form["potassium"])
              temperature=float(request.form["temperature"])
              humidity=float(request.form["humidity"])
              ph=float(request.form["ph"])
              rainfall=float(request.form["rainfall"])
          
          except ValueError as e:
               print("Invalid input:", e)
               return "Error: Please provide valid inputs."
          
          print(nitrogen,phosphorous,potassium,temperature,humidity,ph,rainfall)

          data1=(nitrogen,phosphorous,potassium,temperature,humidity,ph,rainfall)
          data1_as_array=np.asarray(data1)
          data1_as_array_reshape=data1_as_array.reshape(1,-1)

          try: 
              y2=model1.predict(data1_as_array_reshape)
              value_to_find = int(y2[0])

              keys = [key for key, value in label_mapping.items() if value == value_to_find]
              
              print("Predicted Yield",keys[0])
            
          except Exception as e:
                print("Error during prediction:", e)
                return "Error: Could not predict yield."
          
          return render_template('recommended.html',crop=keys[0])
          


@app.route('/rain',methods=['GET','POST'])
def rain():
        #   if request.method=='GET':
        #     return render_template('rain_form.html')
          
        return render_template('rain_form.html')


@app.route('/rain_prediction',methods=['GET','POST'])
def prediction():
          if request.method=="GET":
            return render_template('rain_form.html')
          
          else:
               return render_template('rain_prediction.html')
     
        




if __name__=="__main__":
      app.run(debug=True)



