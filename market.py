from flask import Flask,render_template,redirect,url_for
app=Flask(__name__)
@app.route("/")
def welcome():
   return render_template('home.html')
@app.route("/success/<int:score>")
def success(score):
   return "the person is pass and the mark is"+str(score)

@app.route("/fail/<int:score>")
def fail(score):
   return "the person is fail and the mark is"+str(score)

@app.route("/results/<int:mark>")
def results(mark):
   result=""
   if mark>50:
      result="success"
   else:
      result="fail"
   return redirect(url_for(result,score=mark ))
if(__name__== '__main__'):
   app.run(debug=True)
