from pipelines import pipeline
from transformers.pipelines.text2text_generation import Text2TextGenerationPipeline
import nltk
from nltk.stem.porter import *
import spacy
from sense2vec import Sense2VecComponent
import os
from langchain import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
os.environ["OPENAI_API_KEY"]="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"

# spacy_nlp = spacy.blank("en")
# s2v = Sense2VecComponent(spacy_nlp.vocab).from_disk("./s2v_old")
# @spacy_nlp.component("my_components")
# def my_components(s2v):
#     return s2v
# spacy_nlp.add_pipe("my_components")
t5_generator = pipeline("question-generation")
#t2t_generator = Text2TextGenerationPipeline(output_type="question")


def generate_from_T5(context, n=5):
    res = t5_generator(context)
    ans = []
    que = []
    for i, r in enumerate(res):
        if i < n:
            ans.append(r['answer'])
            que.append(r['question'])
    return que, ans


'''def generate_from_t2t(context, n=5):
    res = t2t_generator.predict([context] * n)
    ans = []
    que = []
    for r in res:
        if r[0] not in que:
            que.append(r[0])
            ans.append(r[1])
    return que, ans'''


# q1, a1 = generate_from_T5(text5)
# q2, a2 = generate_from_t2t(text5)


# %%
# def generate_distractor(question,ans,n=5):
#     doc = spacy_nlp(sentence)
#     ans = [doc]
#     for ent in doc:
#         try:
#             assert ent._.in_s2v
#             most_similar = ent._.s2v_most_similar(10)
#             for m in most_similar:
#                 text = m[0][0].lower()
#                 if text not in ans:
#                     ans.append((text, False))
#             return ans[-n:]
#         except:
#             return ([('none', False)] * n)
def generate_distractor(question,ans,n=5):
    demo_template='''give me the {n} distractors by using question is : {question} and answer is:{answer}'''
    prompt=PromptTemplate(input_variables=['n','question','answer'],
              template=demo_template)
    llm=OpenAI(temperature=0.7)
    chain1=LLMChain(llm=llm,prompt=prompt)
    try:
        response=chain1.run(n=n,question=question,answer=ans)
        response=response.strip()
        response=response.splitlines()
        return response[-n:]
    except:
        return ([('none', False)] * n)
        
