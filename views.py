#library for html 
from flask import Blueprint, render_template, request, g, redirect, url_for

views = Blueprint(__name__,"views")

# Store the user names in a dictionary
users = {}

@views.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        # Add the user to the dictionary
        username = request.form['username']
        users[username] = {'bout_data': []
                           ,'poolmatrixdata':[]
                           ,'warning_list':[]}
        
        # Redirect to the user's subpage
        return redirect(f'/{username}')
    else:
        # Render the index page
        return render_template('index.html')
    

# define initial data
headings = ("My Position","My Score","Opponent Score","Opponent Position","Name")
# number dropdown box in bout order table 
dropdown_values_position = ['','1', '2', '3', '4', '5','6','7']
dropdown_values = ['0', '1', '2', '3', '4', '5']
# Max number of fencer
numFencer=7

@views.route('/<username>', methods=['GET', 'POST'])

def user_page(username):
    # Get the user's table
    bout_data = users[username]['bout_data']
    poolmatrixdata = users[username]['poolmatrixdata']
    warning_list = users[username]['warning_list']
    MyName = username

    for i in range(numFencer): 
        bout_data.append(["","","","",""]) 
        poolmatrixdata.append(("",i,"","","","","","","","","","","",""))

    if request.method == 'POST':      
        warning=""
        
        if request.form['btn'] == 'reset':
            # warning_list=[]
            # bout_data=[]
            # MyName=""
            # for i in range(numFencer): 
            #     bout_data.append(["","","","",""])      
                
            # poolmatrixdata=[]      
            
            # print(request.host_url)
            # Redirect the user back to the root URL
            return redirect(url_for('views.index'))
            
        elif request.form['btn'] == 'calculate':  
             
            temp=[]
            for i in range(numFencer):
                row=[request.form['myPosition']]
                row.append(request.form['myScore_{}'.format(i)])
                row.append(request.form['opponentScore_{}'.format(i)])            
                row.append(request.form['opponentPosition_{}'.format(i)])
                row.append(request.form['opponentName_{}'.format(i)])
                temp.append(row)
                
            bout_data = temp      
            
            # print("bout_data")
            # print(bout_data)
            
            # duplicated fencer
            fencerList=[]
            for row in bout_data:
                if row[3]!='':
                    fencerList.append(row[3])
            # print("fencerList")
            # print(fencerList)
                    
            newlist = []                       
            duplist = [] 
            for row in fencerList:
                if row not in newlist:
                    newlist.append(row)
                elif row not in duplist:  
                    duplist.append(row) 
            
            # print('duplicate')
            # print(duplist)
            # print(len(duplist))
            
            if len(duplist) > 0:
                warning=warningMessage(warning,"Duplicate Opponent #"+','.join(duplist))
                
            poolmatrixdata=[]
            for i in range(numFencer): 
                poolmatrixdata.append(["",(i+1),"","","","","","","","","","","",""])
            
            
            row_cnt = 0
            # calculate the pool matrix
            for row in bout_data:
                myPos=bout_data[0][0]
                myScr=row[1]            
                oppoScr=row[2]
                oppoPos=row[3]            
                oppoName=row[4]
                #print("myScr: ",myScr, " myPos: ",myPos," oppoScr: ",oppoScr," oppoPos: ",oppoPos)
                #print("myScr: ",type(myScr), " myPos: ",type(myPos)," oppoScr: ",type(oppoScr)," oppoPos: ",type(oppoPos))
                
                row_cnt += 1
                if myPos==oppoPos and myPos!='':
                    warning=warningMessage(warning,"Same Position in Fencer and Opponent of row "+str(row_cnt))
                
                if myPos!="" and oppoPos!="":
                    mPos=int(myPos)
                    oPos=int(oppoPos)  
                    
                    poolmatrixdata[mPos-1][0] = MyName
                    poolmatrixdata[oPos-1][0] = oppoName
                    
                    if myScr >= "0" and myScr <= "5" and oppoScr >= "0" and oppoScr <= "5":  
                        if myScr == oppoScr:
                            warning=warningMessage(warning,"Tie Score with Fencer#" + oppoPos + " " + oppoName)
                            poolmatrixdata[mPos-1][oPos+1] = ""
                            poolmatrixdata[oPos-1][mPos+1] = ""
                        elif myScr > oppoScr:
                            poolmatrixdata[mPos-1][oPos+1] = "V"+myScr
                            poolmatrixdata[oPos-1][mPos+1] = "D"+oppoScr
                        else:
                            poolmatrixdata[mPos-1][oPos+1] = "D"+str(myScr)
                            poolmatrixdata[oPos-1][mPos+1] = "V"+oppoScr
                    else:
                        poolmatrixdata[mPos-1][oPos+1] = ""
                        poolmatrixdata[oPos-1][mPos+1] = ""
                    
            warning_list = warning.splitlines()
                            
            # print("poolmatrixdata")      
            # print(poolmatrixdata)
            
            #to count match victory indicator
            for i in range(len(poolmatrixdata)):
                victory = 0;match = 0;ts=0;tr=0;        
                for j in range(2,9):
                    matrixcell=poolmatrixdata[i][j]
                    #print(i,j,matrixcell)
                    if matrixcell !="":
                        match += 1
                        ts += int(matrixcell[1])
                        if matrixcell[0] =="V":
                            victory += 1
                    #print(i,j,match,matrixcell)
                                            
                for k in range(len(poolmatrixdata)):
                    matrixcell=str(poolmatrixdata[k][i+2])
                    if matrixcell !="":
                        tr += int(matrixcell[1])    
                
                if match > 0 and i==(int(myPos)-1):
                    poolmatrixdata[i][9] = victory
                    poolmatrixdata[i][10] = round(victory/match,2)
                    poolmatrixdata[i][11] = ts
                    poolmatrixdata[i][12] = tr                        
                    poolmatrixdata[i][13] = ts-tr                        

    users[username]['bout_data']        = bout_data
    users[username]['poolmatrixdata']   = poolmatrixdata
    users[username]['warning_list']     = warning_list

    return render_template("table.html",
                           headings=headings, 
                           bout_data=bout_data, 
                           poolmatrixdata=poolmatrixdata,
                           dropdown_values=dropdown_values,
                           numFencer = numFencer,
                           MyName=MyName,
                           dropdown_values_position=dropdown_values_position,
                           warning_list=warning_list)


def warningMessage(warningCol,msg):
    if warningCol=="":
        warningCol= msg
    else:
        warningCol=warningCol +'\n' + msg
    
    return warningCol
