import pke
import requests
import json
import re
import random
import pprint
import itertools
import string
from summarizer import Summarizer
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from flashtext import KeywordProcessor
from pywsd.similarity import max_similarity
from pywsd.lesk import adapted_lesk
from pywsd.lesk import simple_lesk
from pywsd.lesk import cosine_lesk
def question(text,summarizedText):
    def read(full_text):
        model = Summarizer()
        result = model(full_text, min_length=60, max_length = 500 , ratio = 0.4)
        summarized_text = ''.join(result)
        return summarized_text
    def get_nouns_multipartite(text):
        out=[]

        extractor = pke.unsupervised.MultipartiteRank(

        )

        #    not contain punctuation marks or stopwords as candidates.
        pos = {'PROPN'}
        #pos = {'VERB', 'ADJ', 'NOUN'}
        stoplist = list(string.punctuation)
        stoplist += ['-lrb-', '-rrb-', '-lcb-', '-rcb-', '-lsb-', '-rsb-']
        stoplist += stopwords.words('english')
        extractor.load_document(input=text,stoplist=stoplist)
        extractor.candidate_selection(pos=pos)
        # 4. build the Multipartite graph and rank candidates using random walk,
        #    alpha controls the weight adjustment mechanism, see TopicRank for
        #    threshold/method parameters.
        extractor.candidate_weighting(alpha=1.1,
                                    threshold=0.75,
                                    method='average')
        keyphrases = extractor.get_n_best(n=20)

        for key in keyphrases:
            out.append(key[0])

        return out
    def filter(keywords,summarized_text):
        keys=[]
        for keyword in keywords:
            if keyword.lower() in summarized_text.lower():
                keys.append(keyword)
        return keys
    def tokenize_sentences(text):
        sentences = [sent_tokenize(text)]
        sentences = [y for x in sentences for y in x]
        # Remove any short sentences less than 20 letters.
        sentences = [sentence.strip() for sentence in sentences if len(sentence) > 20]
        return sentences

    def get_sentences_for_keyword(keywords,sentences):
        keyword_processor = KeywordProcessor()
        keyword_sentences = {}
        for word in keywords:
            keyword_sentences[word] = []
            keyword_processor.add_keyword(word)
        for sentence in sentences:
            keywords_found = keyword_processor.extract_keywords(sentence)
            for key in keywords_found:
                keyword_sentences[key].append(sentence)

        for key in keyword_sentences.keys():
            values = keyword_sentences[key]
            values = sorted(values, key=len, reverse=True)
            keyword_sentences[key] = values
        return keyword_sentences


    def generateQuestion(keyword_sentence_mapping):
        question={}
        for each in keyword_sentence_mapping:
            sentence= keyword_sentence_mapping[each][0]     
            pattern=re.compile(each, re.IGNORECASE)
            output = pattern.sub( " _______ ", sentence)
            question[each] = output
        return question
    return generateQuestion(keyword_sentence_mapping=get_sentences_for_keyword(keywords=filter(keywords=get_nouns_multipartite(text),summarized_text=summarizedText), sentences=tokenize_sentences(text=summarizedText)))
def summarize(text):
    model = Summarizer()
    result = model(text, min_length=60, max_length = 500 , ratio = 0.4)
    summarized_text = ''.join(result)
    return summarized_text
        