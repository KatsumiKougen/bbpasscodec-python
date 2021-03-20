import sys

pwstring="BAIFJCGEDH"

def clamp(value,start,end):
	if start<=value<=end:return value
	elif start>value:return start
	elif value>end:return end

def decode(password):
	numstr="".join([str(pwstring.index(char)) for char in password]);passbuffer=[0]*5
	for i in range(4,0,-1):passbuffer[i]=str(int(numstr[i])^int(numstr[i-1]))
	passbuffer[0]=numstr[0]
	return "".join(passbuffer)

def encode(lv,sp,st):
	datatemp="0%s";numstr,password=[datatemp]*5,[]
	data=(
		"0"*(7-len(bin(lv)[2:]))+bin(lv)[2:],
		str(sp),
		"0"*(2-len(bin(st)[2:]))+bin(st)[2:],
	)
	sum=bin(int(data[0][:3],2)+int(data[0][3:6],2)+int(data[0][6],2)+int(data[1]+data[2],2))[2:]
	checksum="0"*(5-len(sum))+sum
	numstr[0]=numstr[0]%(data[0][:3])
	numstr[1]=numstr[1]%(data[0][3:6])
	numstr[2]=numstr[2]%(checksum[:2]+data[0][6])
	numstr[3]=numstr[3]%(data[1]+data[2])
	numstr[4]=numstr[4]%(checksum[2:])
	password.append(int(numstr[0],2))
	for i in range(1,5):password.append(int(numstr[i],2)^password[i-1])
	return "".join([pwstring[int(i)] for i in password])

def gameAttr(num):
	bit=["0"*(4-len(bin(int(i))[2:]))+bin(int(i))[2:] for i in num]
	checksum=int(bit[0][1:],2)+int(bit[1][1:],2)+int(bit[2][3],2)+int(bit[3][1]+bit[3][2:],2)
	attribute={
		"LevelNum":int(bit[0][1:]+bit[1][1:]+bit[2][3],2),
		"SuperFlag":int(bit[3][1],2),
		"Something":int(bit[3][2:],2),
		"ChecksumCorrect":int(bit[2][1:3]+bit[4][1:],2)==checksum
	}
	return attribute

def formatstr(obj):
	if obj["SuperFlag"]==0:print("\nHere's your game!\nBubble Bobble - Level %d - Something %d\n"%(obj["LevelNum"],obj["Something"]))
	elif obj["SuperFlag"]==1:print("\nHere's your game!\nSuper Bubble Bobble - Level %d - Something %d\n"%(obj["LevelNum"],obj["Something"]))
	if not obj["ChecksumCorrect"]:print("Warning! The checksum does not match.\n")

print("BUBBLE BOBBLE PASSWORD ENCODER/DECODER - Python Edition\nOriginal concept by Joel \"Bisqwit\" Yliluoma\nConversion to Python by Katsumi Kougen\n")
mode=sys.argv[1]
if mode=="-encode":
	try:
		levelnum,issuper,something=int(sys.argv[2]),sys.argv[3].lower(),int(sys.argv[4])
		levelnum=clamp(levelnum,1,159);something=clamp(something,0,3)
		if issuper=="y":super=1
		elif issuper=="n":super=0
		else:super=0
		if super==0:print("\nHere's your password!\nBubble Bobble - Level %d - Something %d\nPassword: %s\n"%(levelnum,something,encode(levelnum,super,something)))
		elif super==1:print("\nHere's your password!\nSuper Bubble Bobble - Level %d - Something %d\nPassword: %s\n"%(levelnum,something,encode(levelnum,super,something)))
	except:print("Error! Invalid input.")
elif mode=="-decode":
	pw=sys.argv[2]
	try:formatstr(gameAttr(decode(pw)))
	except:print("Error! %s is not a valid password."%(pw))