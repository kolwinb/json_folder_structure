import os
import json

class PathFinder():
    def __init__(self):
        self.dirpath="/media/data/video/"
        self.channels=["grade-05","grade-06","grade-07","grade-08","grade-09","grade-10","grade-11","vocational-education","higher-education","dharmavahini"]
	self.quality=["38k.mp4","130k.mp4","268k.mp4","512k.mp4"]
        self.dhammaqty=["144p.mp4","360p.mp4","480p.mp4","720p.mp4"]
        self.dhammachannel=["dharmavahini","bhavana"]

    def getTree(self):
	dict0={}
	dict0["vod"]=[self.getFirstLevel(channel) for channel in self.channels] # find sub directory of all channels, set dictionary for subdirectory and assign them
	return dict0


    def getFirstLevel(self,channel):
	dict1={}

        #find subdirectory again and set dictionary with subject, ignore thumb folder.
	dict1["directory"]=channel
	dict1["image"]=""
        if channel == "dharmavahini":
	    # got to subdirectory
	    dict1["contents"]=[self.getDir(os.path.join(self.dirpath+channel,dirname),channel) for dirname in os.listdir(self.dirpath+channel) if os.path.isdir(os.path.join(self.dirpath+channel,dirname)) if not dirname == "fillers"]
	else:
	    #list all files and assign quality
    	    dict1["contents"]=[self.getChannel(os.path.join(self.dirpath+channel,dirname),channel,self.quality[:]) for dirname in os.listdir(self.dirpath+channel) if os.path.isdir(os.path.join(self.dirpath+channel,dirname)) if not dirname == "thumb"]
	return dict1

    def getDir(self,path,channel):
	dict5={}
	dict5["directory"]=os.path.basename(path)
	dict5["image"]=""
	#list all files and assign quality
      	dict5["contents"]=[self.getChannel(os.path.join(path,dirname),channel,self.dhammaqty[:]) for dirname in os.listdir(path) if os.path.isdir(path) if not dirname == "thumb"]
	return dict5	

    #switch different quality channel
    def getChannel(self,path,channel,qty):
	dict2={}
	dict2["directory"]=os.path.basename(path)
	dict2["image"]="im-url"	
	dict2["xsmall"]=[self.getFile(os.path.join(path,filename),channel) for filename in os.listdir(path) if os.path.isfile(os.path.join(path,filename)) if self.getOnlyExtension(os.path.join(path,filename)) == qty[0] ]
	dict2["small"]=[self.getFile(os.path.join(path,filename),channel) for filename in os.listdir(path) if os.path.isfile(os.path.join(path,filename)) if self.getOnlyExtension(os.path.join(path,filename)) == qty[1] ]
	dict2["medium"]=[self.getFile(os.path.join(path,filename),channel) for filename in os.listdir(path) if os.path.isfile(os.path.join(path,filename)) if self.getOnlyExtension(os.path.join(path,filename)) == qty[2] ]
	dict2["large"]=[self.getFile(os.path.join(path,filename),channel) for filename in os.listdir(path) if os.path.isfile(os.path.join(path,filename)) if self.getOnlyExtension(os.path.join(path,filename)) == qty[3] ]
	return dict2
    
    #extract only 38k.mp4
    def getOnlyExtension(self,path):
	fname=os.path.basename(path)
        qty=fname.split("-")[-1:]
        return "".join(qty)
    
    '''
    #dharmavahin has subdirectory, learntv doesn't have, so eg: sermon:["sinhala","english"],sinhala["files"]
    def getChannelDir(self,path,channel):
	if channel == "dharmavahini":
	    return self.getDhammaFile(path,channel)
	else:
	    return self.getFile(path,channel)

    def getDhammaFile(self,path,channel):
        dict5={}
        dict5["directory"]=os.path.basename(path)
        #dict5
    '''
	    
    #qty=38k.mp4,channel=grade-05,path=/media/data/video/grade-05/revision/revision-05-1-38k.mp4
    def getFile(self,path,channel):
	dict3={}
	dict3["file"]=self.removeMp4Extension(os.path.basename(path),"-") # get last field
	dict3["image"]="http://www.learntv.lk/"+self.getThumb(channel,path,os.path.basename(path)) # get thumb image by calling function. required channel name, filename, path
	dict3["video"]="http://www.learntv.lk/"+self.getVideoPath(path)
	return dict3
    
    def getVideoPath(self,path):
	vpath=path.split("/")[3:]
	return "/".join(vpath)

    #thumb processer
    def getThumb(self,channel,path,fname):
	root_path=self.splitPath(path) #get only /video/grade-05/revision, others are remove
	if channel == "dharmavahini":
	    thumb_name=self.removeMp4Extension(fname,"-")+"-168x105-1.jpg"
        else:
	    thumb_name=self.removeMp4Extension(fname,"-")+".d.jpg"
        return root_path+"/thumb/"+thumb_name	

    def splitPath(self,path):
	#pathlist=[] #initialize list array
	pathlist=path.split("/")[3:-1]	# split from 3rd column
        return "/".join(pathlist) # join list array values

    def removeMp4Extension(self,fname,pattern):
	namelist=[]
        namelist=fname.split(pattern)
	return "-".join(namelist[:-1])

pathwalker=PathFinder()
#json_file = json.dumps(pathwalker.getTree(),sort_keys=False,indent=4)
#file = open("/media/data/video/vod.json",'w')
#file.write(json_file['vod.json'])
with open('/media/data-2/vod.json','w') as jsonfile:
    json.dump(pathwalker.getTree(),jsonfile)

