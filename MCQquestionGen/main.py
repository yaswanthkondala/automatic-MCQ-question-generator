from flask import Flask,render_template,request
import models
import random
app=Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/t5', methods=['GET','POST'])
def t5():
    if request.method == 'POST':
        try:
            context=request.form['input-text']
            maxquestions=int(request.form['max_answers'])
            #generateDis=int(request.form['generate_distractor'])
            questions_t5, _answers_t5 = models.generate_from_T5(context, n=maxquestions)
            answers_t5=[]
            for (q,a) in zip(questions_t5,_answers_t5):
                dis = models.generate_distractor(q,a, 4)
                dis.append((a,True))
                random.shuffle(dis)
                answers_t5.append(dis)
            return render_template('index.html',name="t5",data=[questions_t5,answers_t5])
        except Exception as e:
               return render_template('index.html',name="error",data=e)
    else:
        return "error"

if __name__ == '__main__':
    app.run(debug=True)
        