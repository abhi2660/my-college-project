from flask import Flask,request,render_template,redirect,url_for
import numpy as np
import pickle


with open('cropPrediction.pkl','rb') as file:
    model=pickle.load(file)

app=Flask(__name__)






@app.route('/',methods=['GET'])
def start():
    return render_template('index.html')

@app.route('/form',methods=['GET','POST'])
def form():
     return render_template("form.html")

# @app.route('/prediction/<int:result>')
@app.route('/prediction')
def result(result):
     return "the yield is "+ str(result)

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
            
         
        
       




if __name__=="__main__":
      app.run(debug=True)


