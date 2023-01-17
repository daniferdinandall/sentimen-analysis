from django.shortcuts import render
import numpy as np
from django.shortcuts import redirect


from .utils import *
# Create your views here.
def index(request):
    return render(request,'posting/index.html')

def riwayat(request):
    # print(getTopics())
    return render(request,'posting/riwayat.html',{'topics':getTopics()})

def visual(request):
    
    query = request.POST['query']
    max = int(request.POST['max'])
    date_start = str(request.POST['dateStart'])
    date_end = str(request.POST['dateEnd'])
    # ===============
    list_t=get_data(query,max,date_start,date_end)
    
    result=modelNB(list_t)
    
    positive=np.count_nonzero(result['score'] == 1)
    netral=np.count_nonzero(result['score'] == 0)
    negative=np.count_nonzero(result['score'] == -1)
    total=len(result['tweets'])
    tweets=result['tweets']
    # ===============

    chart=pie_chart(negative,positive,netral)
    # print(result['score'])
    
    all=[]
    for i, element in enumerate(result['tweets']):
        sen=''
        if(result['score'][i]==1):
            sen='positive'
        elif(result['score'][i]==0):
            sen='netral'
        else:
            sen='negative'
        all.append({'tweet':element, 'score':result['score'][i],'sentimen':sen, 'date':result['date'][i]})
    # print(all)
    # insert DB
    insertTweets(query,all,date_start,date_end,total,positive,negative,netral)
    return render(request, 'posting/visual.html',{
        'chart':chart,
        'query':query,
        'date_start':date_start,
        'date_end':date_end,
        'all':all,
        'negative':negative,
        'total':total,
        'positive':positive,
        'netral':netral
    })
    
def visualRiwayat(request,param):
    # print(param)
    topic=getTopic(param)
    hasil=getHasil(param)
    all=getTweets(param)
    
    query=topic[1]
    date_start=topic[2]
    date_end=topic[3]
    chart=pie_chart(hasil[3],hasil[2],hasil[4])
    return render(request, 'posting/visualRiwayat.html',{
        'chart':chart,
        'query':query,
        'date_start':date_start,
        'date_end':date_end,
        'all':all,
        'negative':hasil[3],
        'total':hasil[1],
        'positive':hasil[2],
        'netral':hasil[4]
    })
    
def remove(request,param):
    removeTopic(param)
    return redirect('riwayat')