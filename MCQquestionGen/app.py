from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import warnings

import models
import random
warnings.filterwarnings('ignore')
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/process")
async def process(request: Request):
    data_json = await request.json()
    input_text = data_json['input_text']
    max_answers = int(data_json['max_answers'])
    input_text = ' '.join(input_text.split())
    generate_distractor = bool(int(data_json['generate_distractor']))

    questions_t5, _answers_t5 = models.generate_from_T5(input_text, n=max_answers)
    answers_t5 = []
    for (q,a) in zip(questions_t5,_answers_t5):
        dis = models.generate_distractor(q,a, 3)
        dis=dis.splitlines()
        dis.append((a,True))
        random.shuffle(dis)
        answers_t5.append(dis)

    '''questions_t2, _answers_t2 = models.generate_from_t2t(input_text, n=max_answers)
    answers_t2 = []
    for a in _answers_t2:
        if not generate_distractor:
            ans = [(a, True)]
        else:
            dis = models.generate_distractor(a, 4)
            ans = [(a, True)] + dis
        random.shuffle(ans)
        answers_t2.append(ans)'''

    return {
        "q_t5": questions_t5, "a_t5": answers_t5,
        #"q_t2": questions_t2, "a_t2": answers_t2
    }
