#!/bin/python3
tracklist=[]
position=0
loading=True
selected_track=None
import os,sys,copy

class Track:
 def command(self):
  rls=" "
  cl=["-a:" + self.name, "-i " + self.track_in, "-o " + self.track_out]
  rl=["-epp " + str(self.pan), "-ea " + str(self.amp)]
  if self.track_out=="alsa":
   rls+=' '.join(rl)
  return ' '.join(cl) + rls
  
 def set_take(self):
  if loading==True:
   return
  if self.track_in=="alsa":
   ts=self.track_out
  else:
   ts=self.track_in
  i=ts.find("_")
  j=ts.find(".")
  print(ts[i+1:j])
  self.take=int(ts[i+1:j])
  
 def get_info(self):
  rl=[self.name,"Input",self.track_in,"output",self.track_out,"Take",str(self.take),"pan",str(self.pan),"volume",str(self.amp)]
  return " ".join(rl)
 def __init__(self,name,ti,to):
  self.name=name
  self.track_in=ti
  self.track_out=to
  self.take=1
  self.pan=50
  self.amp=100
  

def parse_script(n):
 print("Parsing script " + n)
 fin=open(n,"r")
 pl= fin.readline().split()
 for i in range(0,len(pl)):
  if pl[i].find("-a:")>=0:
   tracklist.append(Track(pl[i][3:],pl[i+2],pl[i+4]))
   tracklist[-1].set_take()
   i=i+4
   continue
  elif pl[i]=="-epp":
   tracklist[-1].pan=int(pl[i+1])
   i+=1
   continue
  elif pl[i]=="-ea":
   tracklist[-1].amp=int(pl[i+1])
   i+=1
   continue
 fin.close()
 
def print_tracklist():
 if len(tracklist)==0:
  return
 for i in tracklist:
  if i==selected_track:
   print("*",end=" ")
  print(i.get_info())


if len(sys.argv)==2:
 parse_script(sys.argv[1])
print("Ecaterm ready")
if len(tracklist)>0:
 selected_track=tracklist[0]
while True:
 if loading==True:
  print("Load mode.")
 else:
  print("Write mode")
 if position>0:
  print("Position " + str(position))
 print_tracklist()
 i=input(">")
 if i=="":
  if len(tracklist)==0:
   continue
  if selected_track!=None and selected_track.track_in=="alsa":
   print("rm " + selected_track.name + "_" + str(selected_track.take) + ".wav")
  commandstr = "ecasound -f:16,2,48000 " + "-E \"setpos " + str(position) + "\" "
  for i in tracklist:
   commandstr += i.command() + " "
  print(commandstr)
  os.system(commandstr)
  continue
 il=i.split()
 if il[0]=="add":
  if loading==True:
   selected_track=Track(il[1],il[1] + ".wav","alsa")
  else:
   selected_track=Track(il[1],"alsa",il[1] + "_1.wav")
  tracklist.append(selected_track)
  print("Track added.")
 elif il[0]=="del":
  found=False
  for i in tracklist:
   if il[1] in i.name:
    if selected_track==i:
     selected_track=None
    tracklist.remove(i)
    found=True
    print("Removed.")
    break
  if found==False:
   print("Not found.")
  continue  
 elif il[0]=="save":
  fout=open(il[1],"w+")
  fout.write("ecasound -f:16,2,48000 ")
  for i in tracklist:
   fout.write(i.command() + " ")
  print("Saved to " + il[1])
  fout.close()       
 elif il[0]=="select":
  for i in tracklist:
   if il[1] in i.name:
    selected_track=i
    print(i.name + " selected.")
    break
 elif il[0]=="s":
  temp=selected_track.track_in
  selected_track.track_in=selected_track.track_out
  selected_track.track_out=temp
  print("Swapped.")
 elif il[0]=="t":
  if len(il)==1:
   selected_track.take+=1
  else:
   selected_track.take=int(il[1])
  print("Take " + str(selected_track.take))
  nn=selected_track.name + "_" + str(selected_track.take) + ".wav"
  if selected_track.track_in=="alsa":
   selected_track.track_out=nn
  else:
   selected_track.track_in=nn
 elif il[0]=='p':
  selected_track.pan=int(il[1])
 elif il[0]=='a':
  selected_track.amp=int(il[1])
 elif il[0]=="out":
  selected_track.track_out=il[1]
 elif il[0]=="in":
  selected_track.track_in=il[1]
 elif il[0]=="name":
  selected_track.name=il[1]
 elif il[0]=="pos":
  position=int(il[1])
 elif il[0]=="load":    
  loading=True
  print("Loading enabled.")
 elif il[0]=="write":
  loading=False
  print("Writing enabled.")
 elif il[0]=="ls":
  os.system("ls")
 if il[0]=="q":
  exit()
  
     
  
