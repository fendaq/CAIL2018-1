import json 
import pandas as pd
import re
data_train_read=open("./json/Big.json",encoding="UTF-8")
data={}
data['fact']=[] #text
data['accusation']=[] #罪名
data['relevant_articles_label']=[]#相关法条
data['death_penalty']=[]#是否死刑
data['life_imprisonment']=[]#是否无期
data['imprisonment']=[]# 有期徒刑刑期



for (i,line) in  enumerate(data_train_read):
    if i%10000==0:
        print("processed {} of 1710000".format(i))
    try:
        a=json.loads(line)
    except:
        print("error json")
        continue
    data['fact'].append(a['fact'])
    data['accusation'].append(a['meta']['accusation'])
    data['relevant_articles_label'].append(a['meta']['relevant_articles'])
    data['death_penalty'].append(a['meta']['term_of_imprisonment']['death_penalty'])
    data['life_imprisonment'].append(a['meta']['term_of_imprisonment']['life_imprisonment'])
    data['imprisonment'].append(a['meta']['term_of_imprisonment']['imprisonment'])
    
data=pd.DataFrame(data)

import re
import jieba








def preprocessing_fact(text):
    #just keep wd
    text = text.replace(" ","")
    text = re.sub(r"\d*年", "", text)
    text = re.sub(r'\d*月','',text)
    text = re.sub(r'\d*日','',text)
    text = re.sub(r'\d*时','',text)
    text = re.sub(r"\d*分", "", text)
    text = re.sub(r"\r\n", "", text)
    text = re.sub(r"\.\d+","",text)
    text = re.sub(r".\d某","某某",text)
    text = re.sub(r".某\d","某某",text)
    text = re.sub(r'万.','万元',text)
    # g
    text=re.sub(r'(?<=\d)g','克',text)
    #inphone规整
    text = re.sub(r'inphone\d?[a-zA-Z]?','inphone',text)
    #手机号码的规整
    text = re.sub(r'\d+×+\d+','SJHAO',text)
 
    
    #车牌规整
    text = re.sub(r'[a-wy-zA-WY-Z]+\d?(×|x|X)+','CHEPAIHAO',text)
    text = re.sub(r'[a-wy-zA-WY-Z]+\d+[a-zA-Z]?','CHEPAIHAO',text)
    
    
    #jieba无法shibie mg/ml需要添加自定义字典
    jieba.add_word('mg')
    jieba.add_word('kg')
    jieba.add_word('ml')
    jieba.add_word('iPhone')
    
    
    ch2num={}
    ch2num['一']=1
    ch2num['二']=2
    ch2num['三']=3
    ch2num['四']=4
    ch2num['五']=5
    ch2num['六']=6
    ch2num['七']=7
    ch2num['八']=8
    ch2num['九']=9

    text=[i for i in jieba.lcut(text)]
    text_len=len(text)
    normal_words=['市','县','镇','村','区','街道']
    for  i  in  range(text_len-1):
        
        #对地区规则化
        for j in  normal_words:
            if j in  text[i]:
                text[i]=j
                
        #人名规则化
        
        if '某' in text[i]:
            text[i]='某某'
            
        if len(text[i])==1 and  '某' in text[i+1]:
            text[i]=''
            
        
        if 'x' in  text[i+1] and len(text[i])==1:
            text[i]='某某'
            text[i+1]=''
        
        
        key_wd=['万元','元','美元','克','mg','kg','千克','公斤','斤']
        
        
    
                
        if text[i+1] in key_wd and text[i].isdigit():
            text[i]=str(text[i][0])+"0"*(len(text[i])-1)
            num_i=float(text[i])
            
            for i in num_thr_list:
                if i>num_thr_list:
                    text[i]=i
                    break
            text[i]=text[i]+“ ”+str(num_i)
            

                
       

        
        if len(text[i])==1 and text[i].isdigit()==False and text[i]  not in ['克','元','刀','性','斤','枪']:
            text[i]=''
                 
    text=[i for i in text if i!='']                    
                    
                
    return " ".join(text)


data['fact_cut_wd']=data['fact'].map(lambda x:preprocessing_fact(x))

    


# In[ ]:


data.to_csv('./csv/Big.csv',index=False)

