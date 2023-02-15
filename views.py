#package for webscraping
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
browser = webdriver.Remote(
    command_executor='http://selenium:4444/wd/hub',
    desired_capabilities=DesiredCapabilities.CHROME.copy(),
    options=options
)

#library for html 
from flask import Blueprint, render_template, request

views = Blueprint(__name__,"views")


            
# boutorderdata = (
#     (1,"WANG Ziqi (yoyo)","","","KIM Zoe L.",2),
#     (3,"CHANG Abigail","","","BUSH emma",4),
#     (5,"LEREE Fernanda","","","WANG Ziqi (yoyo)",1),
#     (3,"CHANG Abigail","","","KIM Zoe L.",2),
#     (5,"LEREE Fernanda","","","BUSH emma",4),
#     (3,"CHANG Abigail","","","WANG Ziqi (yoyo)",1),
#     (5,"LEREE Fernanda","","","KIM Zoe L.",2),
#     (4,"BUSH emma", "","","WANG Ziqi (yoyo)",1),
#     (3,"CHANG Abigail", "","","LEREE Fernanda",5),
#     (4,"BUSH emma", "","","KIM Zoe L.",2),
# )

# poolmatrixdata = (
# ("WANG Ziqi (yoyo)",1,"S","D4","V5","V5","V5","","","3","0.75","19","13","+6"),
# ("KIM Zoe L.",2,"V5","S","V5","D4","V5","","","3","0.75","19","11","+8"),
# ("CHANG Abigail",3,"D3","D0","S","D2","V5","","","1","0.25","10","16","-6"),
# ("BUSH emma",4,"D2","V5","V5","S","V5","","","3","0.75","17","14","+3"),
# ("LEREE Fernanda",5,"D3","D2","D1","D3","S","","","0","0.00","9","20","-11"),
# ("YOUSSEF Caroline",6,"","","","","","","","","","","",""),
# )



# define initial data
headings = ("#","RIght Fencer","Score","Score","Left Fencer","#")
fencers = []
filtered_data = []
poolmatrixdata = []
boutorder=[]
pooltable=[]
# number dropdown box in bout order table 
dropdown_values = ['0', '1', '2', '3', '4', '5']
num_bout = 0     
warning=""       
            
@views.route('/', methods=['GET', 'POST'])
def home():
    global headings,filtered_data, poolmatrixdata,num_bout,warning,fencers
    
    temp=[]
    if request.method== 'POST':
        
        # keep the slected values in bout order table
        for i in range(len(filtered_data)):
            row=[filtered_data[i][0]]
            row.append(filtered_data[i][1])
            row.append(request.form['rightscore_{}'.format(i)])
            row.append(request.form['leftscore_{}'.format(i)])
            row.append(filtered_data[i][4])
            row.append(filtered_data[i][5])
            temp.append(row)
            
        filtered_data = temp
        
        # calculate the pool matrix
        warning=""
        for row in filtered_data:
            if row[2] >= "0" and row[2] <= "5" and row[3] >= "0" and row[3] <= "5":
                if row[2] == row[3]:
                    warning="Tie Score in " + row[1] + " vs " + row[4]
                    poolmatrixdata[int(row[0]-1)][int(row[5])+1] = ""
                    poolmatrixdata[int(row[5]-1)][int(row[0])+1] = ""
                elif row[2] > row[3]:
                    poolmatrixdata[int(row[0]-1)][int(row[5])+1] = "V"+str(row[2])
                    poolmatrixdata[int(row[5]-1)][int(row[0])+1] = "D"+str(row[3])
                else:
                    poolmatrixdata[int(row[0]-1)][int(row[5])+1] = "D"+str(row[2])
                    poolmatrixdata[int(row[5]-1)][int(row[0])+1] = "V"+str(row[3])
            else:
                poolmatrixdata[int(row[0]-1)][int(row[5])+1] = ""
                poolmatrixdata[int(row[5]-1)][int(row[0])+1] = ""
                
        #to count match victory indicator
        for i in range(len(fencers)):
            victory = 0;match = 0;ts=0;tr=0;        
            for j in range(2,9):
                matrixcell=poolmatrixdata[i][j]
                print(i,j,matrixcell)
                if matrixcell !="":
                    match += 1
                    ts += int(matrixcell[1])
                    if matrixcell[0] =="V":
                        victory += 1
                print(i,j,match,matrixcell)
                                        
            for k in range(len(fencers)):
                matrixcell=str(poolmatrixdata[k][i+2])
                if matrixcell !="":
                    tr += int(matrixcell[1])    
            
            if match > 0:
                poolmatrixdata[i][9] = victory
                poolmatrixdata[i][10] = round(victory/match,2)
                poolmatrixdata[i][11] = ts
                poolmatrixdata[i][12] = tr                        
                poolmatrixdata[i][13] = ts-tr                        
                                  
    else:
        # fencing time live site
        urlCall = request.args.get('qsite')  # Get the search query from the URL parameter
        if urlCall is None:
            warning ='Not valid fencingtimelive.com page'
        elif 'fencingtimelive.com' not in urlCall:
            warning ='Not valid fencingtimelive.com page'
        else:
            warning=""
            if urlCall is None:
                filtered_data = []
                poolmatrixdata = [] 
                fencers=[]           
            elif urlCall is not None:      
                boutorder,pooltable=webpage(urlCall)
                
                filtered_data = []
                poolmatrixdata = []
                fencers=[]
                
                boutorderdata=boutorder[0]
                boutorderdata.columns = ['right_no', 'right_fencer', 'right_score', 'left_score', 'left_fencer','left_no']

                # print(boutorderdata)
                # print(type(boutorder))    
            
                pool_temp=pooltable[0]
                # print(pool_temp)
                # print(type(pooltable))
                
                for i in range(len(pool_temp)):    
                    row=[pool_temp.iloc[i,0].split('/')[0]]
                    fencers.append(row)
                    row.append(pool_temp.iloc[i,1])
                    for j in range(2,14):
                        row.append("")
                    poolmatrixdata.append(row)
            
                # Get the search query from the URL parameter    
                # not this version
                #query = request.args.get('q')  
                query = None
                    
                if query is None:
                #filtered_data = boutorderdata
                    for i in range(len(boutorderdata)):
                        row=[boutorderdata.iloc[i,0]]
                        row.append(boutorderdata.iloc[i,1])
                        row.append("")
                        row.append("")
                        row.append(boutorderdata.iloc[i,4])
                        row.append(boutorderdata.iloc[i,5])
                        filtered_data.append(row)
                        
                else:
                    for i in range(len(boutorderdata)):
                        if  str(query).lower() in boutorderdata.iloc[i,1].lower() or str(query).lower() in boutorderdata.iloc[i,1].lower():
                            row=[boutorderdata.iloc[i,0]]
                            row.append(boutorderdata.iloc[i,1])
                            row.append("")
                            row.append("")
                            row.append(boutorderdata.iloc[i,4])
                            row.append(boutorderdata.iloc[i,5])
                            filtered_data.append(row)
                            
                num_bout = len(filtered_data)            
          

    return render_template("table.html",headings=headings, filtered_data=filtered_data, fencers = fencers, poolmatrixdata=poolmatrixdata,dropdown_values=dropdown_values,warning=warning)

def webpage(urlget):
    global boutorder,pooltable
    
    url = str(urlget)
    
    #chromedriver_path= "/Users/.../chromedriver"
    #driver = webdriver.Chrome(chromedriver_path)
    #driver.get(url)
    browser.get(url)
    
    #time.sleep(3) #if you want to wait 3 seconds for the page to load
    #page_source = driver.page_source
    page_source = browser.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    
    # Boutorder table
    table = soup.find_all('table')[2]
    boutorder = pd.read_html(str(table))
    
    # Pool table
    table = soup.find_all('table')[1]
    pooltable = pd.read_html(str(table).replace('<br/>','/'))
    
    return boutorder,pooltable
    
