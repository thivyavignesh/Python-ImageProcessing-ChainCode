import os,sys,math

class CCimage: #image matrix creation 
    zeroFramedAry=[]
    numRows=numCols=0
    def __init__(self, input_file_name):
        order=0
        with open(input_file_name, 'r') as input_file:
            for line in input_file:
                if order==0:
                    header = (list(map(str, line.split(' '))))
                    self.numRows = int(header[0])
                    self.numCols = int(header[1])
                    self.zeroFramedAry = [[0] * (self.numCols+2) for i in range(self.numRows+2)]
                else:
                    temp_data = list(map(str, line.split(' ')))
                    for i in range(self.numCols):
                        self.zeroFramedAry[order][i+1] = int(temp_data[i])
                order += 1
        input_file.close()

class CCproperty:# property matrix creation
    maxCC=0
    property = []
    def __init__(self, input_file_name):
        with open(input_file_name, 'r') as input_file:
            for line in input_file:
                temp_data =(list(map(int, line.split(' '))))
                self.property.append(temp_data)
                self.maxCC += 1
        input_file.close()


class point(object): #coord
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def equal(self, p):
        if(self.row==p.row and self.col==p.col):
            return True
        else:
            return False

class Chain:
    __neighborAry = [[0] for i in range(8)]
    __neighborCoord = [point(0,0) for i in range(8)]
    __nextDirTable = [6,6,0,0,2,2,4,4]#preceding point
    __currentCC=lastQ=nextQ=0
    temp = 0
    fir = 0
    chain_data = []
    first_diff = []
    shape_num = []
    

    def __init__(self,image, pp):
        self.chain_data = [[] * (pp.maxCC + 1)]
	self.first_diff = [[] * (pp.maxCC + 1)]
        self.shape_num = [[] * (pp.maxCC + 1)]
	
        for i in range(pp.maxCC):
            self.currentCC=i+1 #objectno
            minRowOffset = pp.property[i][1]
            maxRowOffset = pp.property[i][3]
            minColOffset = pp.property[i][2]
            maxColOffset = pp.property[i][4]
            startRow = minRowOffset
            startCol = minColOffset
	    diff = []
            while(image.zeroFramedAry[startRow][startCol]!=self.currentCC):
                startCol+=1
            self.chain_data.append("Chain code "+str(self.currentCC)+ ": ")
            self.first_diff.append("First Diff "+str(self.currentCC)+ ": ")
	    self.shape_num.append("Shape Nums "+str(self.currentCC)+ ": ")
            startP = point(startRow, startCol)
            currentP = startP
            nextP = point(0,0)
            lastQ = 4
	    orde = 0
	    j = 0
            while(not(startP.equal(nextP))):
                self.loadNeighbors(image, currentP.row, currentP.col)
                nextQ = (lastQ+1)%8
                Pchain = self.findNextP(currentP,nextQ)#direction
		if (orde == 0 ) : fir = Pchain
		if (orde > 0) : 
			diff.insert(j, (Pchain - temp)%8)
			j += 1
		#if (orde > 0) : self.first_diff[self.currentCC]+=str((Pchain - temp)%8)+" "
		temp = Pchain
                nextP = self.__neighborCoord[Pchain]#point in direction             
		self.chain_data[self.currentCC]+=str(Pchain)+" "
                currentP=nextP
                lastQ=self.__nextDirTable[Pchain]#one step back
		orde += 1
	    #self.first_diff[self.currentCC]+=str((fir - temp)%8)+" "
	    diff.insert(j, (fir - temp)%8)
	    j += 1
	    k = j - 1
	    
	    num = pow(10,j)
	    #print num
	    #print (diff)
	    for i in range(0,j) : self.first_diff[self.currentCC]+=str(diff[i])+" "
	    while (k > 0) :
		nu = 0
		temp = diff[0]	    
		for i in range(1,j) : 
			diff[i-1] = diff[i]
		diff[j-1] = temp
		#print (diff)
		for i in range(0,j) :
			nu = nu + diff[i]*pow(10,j-1-i)		
		#print nu
		if(nu<num) : num = nu
		k -= 1
	    #print num
	    self.shape_num[self.currentCC]+=str(num)

    def loadNeighborCoord(self, r, c): #anticlockwise coord neighbors
        self.__neighborCoord[0].row = r
        self.__neighborCoord[0].col = c+1
        self.__neighborCoord[1].row = r-1
        self.__neighborCoord[1].col = c+1
        self.__neighborCoord[2].row = r-1
        self.__neighborCoord[2].col = c
        self.__neighborCoord[3].row = r-1
        self.__neighborCoord[3].col = c-1
        self.__neighborCoord[4].row = r
        self.__neighborCoord[4].col = c-1
        self.__neighborCoord[5].row = r+1
        self.__neighborCoord[5].col = c-1
        self.__neighborCoord[6].row = r+1
        self.__neighborCoord[6].col = c
        self.__neighborCoord[7].row = r+1
        self.__neighborCoord[7].col = c+1

    def findNextP(self, p, q):
        row=p.row
        col=p.col
        self.loadNeighborCoord(row,col)
        for i in range(8):
            if(self.__neighborAry[(q+i)%8]==self.currentCC):
                return (q+i)%8
        return 0

    def loadNeighbors(self, image, row, col): #object number neighbors
        self.__neighborAry[0] = image.zeroFramedAry[row][col + 1]
        self.__neighborAry[1] = image.zeroFramedAry[row - 1][col + 1]
        self.__neighborAry[2] = image.zeroFramedAry[row - 1][col]
        self.__neighborAry[3] = image.zeroFramedAry[row - 1][col - 1]
        self.__neighborAry[4] = image.zeroFramedAry[row][col - 1]
        self.__neighborAry[5] = image.zeroFramedAry[row + 1][col - 1]
        self.__neighborAry[6] = image.zeroFramedAry[row + 1][col]
        self.__neighborAry[7] = image.zeroFramedAry[row + 1][col + 1]

image = CCimage(sys.argv[1])
pp = CCproperty(sys.argv[2])
mychaincode = Chain(image,pp)
output_file=open(sys.argv[3],'w')
for i in range(1, pp.maxCC+1):
    output_file.write(mychaincode.chain_data[i])
    output_file.write('\n')
    output_file.write(mychaincode.first_diff[i])
    output_file.write('\n')
    output_file.write(mychaincode.shape_num[i])	
    output_file.write('\n')
    output_file.write('\n')
output_file.close()
print("Done!")



