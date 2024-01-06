# package import statement
from smartapi import SmartConnect #or from smartapi.smartConnect import SmartConnect
#import smartapi.smartExceptions(for smartExceptions)
import pyotp,requests,pandas as pd
import matplotlib.pyplot as plt
import numpy as np,datetime
import sys
import pandas as pd
from telethon import TelegramClient
import datetime

#create object of call
obj=SmartConnect(api_key="hqceuhyy")
               

#login api call
code=pyotp.TOTP("425E5RKH2ZZM3LHASQ6QQGGKKE").now()
print(code)
data = obj.generateSession("E28001","1970",code)
refreshToken= data['data']['refreshToken']

#fetch the feedtoken
#feedToken=obj.getfeedToken()

#fetch User Profile
#userProfile= obj.getProfile(refreshToken)
no_of_profit=no_of_loss=no_of_sl=no_of_tgt=no_of_neither=0



api_id = 29185715     #API ID (i have used mine it should be replaced)
api_hash = '4157dcf0d1f7d1bbe4287d6aeb985043'
 #API HASH should be inserted here
Messages=[]
df = pd.DataFrame()
with TelegramClient('test', api_id, api_hash) as client:
    for message in client.iter_messages('AngelOneAdvisory', offset_date=datetime.date.today(), reverse=True):
        if message.reply_markup!=None:
            if "INTRADAY" in message.reply_markup.rows[0].buttons[0].text:
                print(message.message+"\n")
                Messages.append(message.message)
            #elif statements can be added to handle other types of messages and not only intraday

        

check=1
porl=[]
risk_reward=[]
for i in Messages:
    token=""
    #if i == Messages[0]:#problem with banknifty
    #    continue
    try:
        message=[line for line in i.split('\n') if line.strip()]
        print(message)
        time=""
        for j in range(len(message)) :
            if "Created Date & Time" in message[j]:
                break
        print(message[j+1][-2:])
        if message[j+1][-2:] == "PM":
            time+=str(int(message[j+1][:2])+12)+":"+message[j+1][3:5]
        time=str(int(message[j+1][:2]))+":"+message[j+1][3:5]
        if len(time)==4:
            time="0"+time
        
        date=message[j+2].split("/")
        print(date)
        FROMDATE=date[2]+"-"+date[1]+"-"+date[0]+" "+time
        buyorsell=message[0].split()[1]
        #print(buyorsell)
        for j in range(len(message)):
            if "Message" in message[j]:
                SL=message[j].split()[message[j].split().index("SL")+1]
                TGT=message[j].split()[message[j].split().index("TGT")+1]

        SL=float(SL)
        TGT=float(TGT)
        i=i.split("\n")[0].split()
        print(i)

        SYM=i[2]
        PRICE=i[len(i)-1].rstrip(".")

        if PRICE!= "CMP":
            PRICE=float(PRICE)
    

    


        print(SYM)
        temp=0
        #Here we fetch the symbol token for the particular symbol(stock name).
        url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
        data_symbols = requests.get(url).json()
        data_symbols = pd.DataFrame.from_dict(data_symbols)
        #print(data_symbols)
        print(buyorsell,"check")
        if "NIFTY" in SYM:
            continue
        else:
            for index, row in data_symbols.iterrows():
                if row['symbol'] ==f"{SYM}-EQ":#-EQ specifies equity here only equity is handled
                    token=row['token']
                    print('GOT IT')
                    break
                if token =="":
                    continue  
    
        print(token,FROMDATE)

        historicParam={
        "exchange": "NSE",
        "symboltoken":token,
        "interval":  "FIVE_MINUTE",
        "fromdate":FROMDATE, 
        "todate": FROMDATE[:10]+" 15:20"
        }
        FLAG=True
        time=0
        data=obj.getCandleData(historicParam)['data']
        #print(data)
        if buyorsell=="BUY":
            if PRICE == "CMP" and check==0:
                    PRICE=float(data[0][1]) 
                    check=1
            risk_reward.append((TGT-PRICE)/(PRICE-SL))
            for i in data:
                print(i)
                if i[3]<SL:
                    no_of_sl+=1
                    no_of_loss+=1
                    print(f'STOP LOSS ATTAINED AT {i[0]}')
                    porl.append((SL-PRICE)/PRICE)
                    FLAG=False
                    break
                elif i[2]>TGT:
                    no_of_tgt+=1    
                    no_of_profit+=1
                    print(f'TARGET ATTAINED AT {i[0]}')
                    porl.append((TGT-PRICE)/PRICE)
                    FLAG=False
                    break
                else:
                    #print(i[0][11:])
                    if i[0][11:]=="15:20:00+05:30":
                        
                        temp=i[4]
                        time=i[0]
            if FLAG:            
                if temp>PRICE:
                    print(f"profit attained at closing time (3:20 PM) :",temp)
                    porl.append((temp-PRICE)/PRICE)
                    no_of_profit+=1
                elif temp<PRICE:
                    print(f"Loss attained at (3:20 PM) :",temp)
                    porl.append((temp-PRICE)/PRICE)
                    no_of_loss+=1
                else:
                    porl.append(0)
                    no_of_neither+=1    
        else:
            if PRICE == "CMP" and check==0:
                    PRICE=float(data[0][1]) 
                    check=1
            risk_reward.append((PRICE-TGT)/(SL-PRICE))
            for i in data:
                if i[2]>SL:
                    no_of_sl+=1
                    no_of_loss+=1
                    print(f'STOP LOSS ATTAINED AT {i[0]}')
                    porl.append((PRICE-SL)/PRICE)
                    FLAG=False
                    break
                elif i[3]<TGT:
                    no_of_tgt+=1    
                    no_of_profit+=1
                    print(f'TARGET ATTAINED AT {i[0]}')
                    porl.append((PRICE-TGT)/PRICE)
                    FLAG=False
                    break
                else:
                    #print(i[0][11:])
                    if i[0][11:]=="15:20:00+05:30":
                        
                        temp=i[4]
                        time=i[0]
            if FLAG:            
                if temp<PRICE:
                    print(f"max profit attained at {time}",temp)
                    no_of_profit+=1
                    porl.append((PRICE-temp/PRICE))
                elif temp>PRICE:
                    print(f"Least loss attained at {time}",temp)
                    porl.append((PRICE-temp)/PRICE)
                    no_of_loss+=1  
                else:
                    porl.append(0)
                    no_of_neither+=1          

        check=0
    
    except Exception as e:
        print("{}".format(e))
        continue


if check==1:
    sys.exit(0)
x_labels = [f" trade {i+1}" for i in range(len(porl))]
x = np.arange(len(porl))
width = 0.35
colors = ['red' if value < 0 else 'blue' for value in porl]
fig, (ax1, ax2) = plt.subplots(1, 2)






porlp =[f"{round(round(i,4)*100,2)}%" for  i in porl]

ax1.bar(x, porl, width, color=colors)
ax1.set_ylabel("Profit/Loss")
ax1.set_xlabel("Trades")
ax1.set_xticks(x, x_labels)
ax1.set_yticks(porl,porlp)

ax2.plot(risk_reward)
ax2.set_ylabel("Risk-Reward Ratio")
ax2.set_xlabel("Trades")
ax2.set_xticks(x, x_labels)
ax2.set_yticks(risk_reward)

# Adjust the layout to prevent overlapping
plt.tight_layout()

plt.show()

print(f"Net profit or lose percentage = {round(sum(porl),2)*100}")
print(f"Profit % = {no_of_profit/len(porl)*100}")
#print(risk_reward)
with open('days.txt', 'r') as file:
    # Read the lines into a list
    lines = file.readlines()




day = datetime.date.today().strftime("%A")

if day == "Monday":
    print('1')
    temp=lines[0].split()
    lines[0] =f"Monday {int(temp[1])+len(porl)} {float(temp[2])+round(sum(porl),2)}\n"
elif day == "Tuesday":
    print('2')  
    temp=lines[1].split()
    lines[1] =f"Tuesday {int(temp[1])+len(porl)} {float(temp[2])+round(sum(porl),2)}\n"
elif day == "Wednesday":
    print('3')  
    temp=lines[2].split()
    lines[2] =f"Wednesday {int(temp[1])+len(porl)} {float(temp[2])+round(sum(porl),2)}\n"
elif day == "Thursday":
    print('4')  
    temp=lines[3].split()
    lines[3] =f"Thursday {int(temp[1])+len(porl)} {float(temp[2])+round(sum(porl),2)}\n"
elif day == "Friday":
    print('5') 
    temp=lines[4].split()
    lines[4] =f"Friday {int(temp[1])+len(porl)} {float(temp[2])+round(sum(porl),2)}\n"     
else:
    print("0")          



# Open the file in write mode
with open('days.txt', 'w') as file:
    # Write the modified lines back into the file
    file.writelines(lines)
#logout
try:
    logout=obj.terminateSession('E28001')
    print("Logout Successfull")
except Exception as e:
    print("Logout failed: {}".format(e.message))
