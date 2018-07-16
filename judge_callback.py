
from keras.callbacks import Callback
import numpy as np
import pickle
from math import  log


with open("class_2_imp.dict",'rb') as f:
    class2imp=pickle.load(f)

class Task3_Judge(Callback):
    def __init__(self, validation_data, interval=1):
        super(Callback, self).__init__()
        self.interval = interval
        self.x_val = validation_data[0]
        self.y_val = validation_data[1]
        with open("class_2_imp.dict",'rb') as f:
            self.class2imp=pickle.load(f)
        
        
    def on_epoch_end(self, epoch, logs={}):
        if epoch % self.interval == 0:
            y_pred = self.model.predict(self.x_val, verbose=0)
            
            score = self.caculate_task3(self.y_val, y_pred)
            info='Task3 - epoch:%d - score:%.6f ' % (epoch+1, score)
            logs['Task3_Score']=score
            print(info)
     

    def  caculate_task3(self,y_val,y_pre):
        
        size=y_val.shape[0]

        s=0
        
        for i  in  range(y_val.shape[0]):
            
            val_num=y_val[i]
        
            pre_num=self.class2imp[np.argmax(y_pre[i])]
            
       
            
            if val_num<0 or pre_num<0:
                if  pre_num==val_num:
                    s+=1.0
                    continue
                else:
                    continue
            v = abs(log(val_num + 1) - log(pre_num + 1))
            
            if v<=0.2:
                
                s+=1.0
            elif v<=0.4:
                s+=0.8
            elif v<=0.6:
                s+=0.6
            elif v<=0.8:
                s+=0.4
            elif s<=1.0:
                s+=0.2
            else:
                continue

        
        
        score=s/size
        return score
            
        
        
