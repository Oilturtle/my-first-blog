
import datetime
import matplotlib.pyplot as plt

def transformtime(arg_list):
    for i in range(0,len(arg_list)):
        arg_list[i]= int(arg_list[i])

    time = datetime.datetime(arg_list[0],arg_list[1],arg_list[2],arg_list[3],arg_list[4])
    return time

def dataget():
    import re
    file_contents = []
    filelist= ["./data/data.csv"]
    mode = "r"
    for x in filelist:
        filepath = x    
        try:
            f=open(filepath,mode)
            if ".csv" in filepath:
                while True:
                    keyword = False
                    line = f.readline()
                    if not line: 
                        f.close()
                        break
                    line = line.replace(":",",")
                    line = line.replace(".",",")
                    line = line.replace("-",",")
                    line = line.replace(" ",",")

                    split_line = re.split(",",line)
                    for i in range(0,len(split_line)):
                        split_line[i] = split_line[i].replace("\n","")
                        split_line[i] = split_line[i].replace("\ufeff","")
                        if split_line[i] =="leaving" or split_line[i] =="breaking":
                            keyword = True
                        
                    if keyword:
                        pass
                    else:
                        file_contents.append(split_line)
            else:
                pass
        except FileExistsError:
            print ("It cannot find your file : " + filepath)
        finally:
            pass
            

    return file_contents

def datamodify (alist,length,date):
    daylist = []
    newdata = []
    moddata = []
    for x in alist:
        time1 = transformtime(x[0:5])
        time2 = transformtime(x[5:10])
        status = x[10]
        newdata.append([time1, time2, status])
    for i in range(0,length):
        temp = date + datetime.timedelta(i)
        daylist.append(temp)
    
    for x in newdata:
        
        day = x[0].date()
        starttime = x[0]
        endtime = x[1]
        temp = endtime - starttime
        duration = int(temp.total_seconds()/60)
        index = daylist.index(day)
        if duration ==0:
            pass
        else:
            moddata.append([index, starttime.hour, starttime.minute, duration, "working"])

    return moddata

def drawinggraphg(adata,length,acolor,date):
    daylist= []
    
    colors_choice = acolor
    for i in range(0,length):
        temp = date + datetime.timedelta(i)
        daylist.append(temp)
    input_files= [adata]
    day_labels = ['Week']
    

    for input_file, day_label in zip(input_files, day_labels):
        fig=plt.figure(figsize=(10,5.89))
        for data in input_file:
            #event= data[-1]
            
            room= data[0] - 0.48
            start= data[1] + data[2]/60
            end=start + data[3]/60
            # plot event
            plt.fill_between([room, room+0.96], [start, start], [end,end], color=colors_choice, edgecolor='k', linewidth=0.5)
            # plot beginning time
            #plt.text(room+0.02, start+0.05 ,'{0}:{1:0>2}'.format(int(data[1]),int(data[2])), va='top', fontsize=7)
            # plot event name
            #plt.text(room+0.48, (start+end)*0.5, event, ha='center', va='center', fontsize=11)
    
        # Set Axis
        ax=fig.add_subplot(111)
        ax.yaxis.grid()
        ax.set_xlim(-0.5,len(daylist)-0.5)
        ax.set_ylim(25.1, 7.9)
        ax.set_xticks(range(0,len(daylist)))
        ax.set_xticklabels(daylist)
        ax.set_ylabel('Time')
    
        # Set Second Axis
        ax2=ax.twiny().twinx()
        ax2.set_xlim(ax.get_xlim())
        ax2.set_ylim(ax.get_ylim())
        ax2.set_xticks(ax.get_xticks())
        ax2.set_xticklabels(daylist)
        ax2.set_ylabel('Time')

    
        plt.title(day_label,y=1.07)
        plt.savefig('{0}.png'.format(day_label), dpi=200)
        return True





data = dataget()
data_modify = datamodify(data,7,datetime.date(2018,10,12))
colors=['pink', 'lightgreen', 'lightblue', 'wheat', 'salmon', 'blue','red']
drawinggraphg(data_modify,7,colors[0],datetime.date(2018,10,12))
test = 123
