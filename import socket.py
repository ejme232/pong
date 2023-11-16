paddlepos=[0,0]
status='1,1,1,1,1,1,1'
recstring=[]
for i in status.split(","):
    recstring.append(int(float(i)))
paddlepos[0], paddlepos[1], x, y, lScore, rScore, sync = recstring
print(recstring)