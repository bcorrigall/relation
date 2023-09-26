from Relations import *


def queryParser():
    inputQuery = input("Enter your Query: ")
    inputQuery = inputQuery.strip().replace(")","").split("(")
    while "" in inputQuery:
        inputQuery.remove("")
        
    layers = len(inputQuery)
    curLayer = layers
    while curLayer > 0:
        currentQuery = inputQuery[curLayer-1]
        if curLayer == layers: 
            currentQuery = currentQuery.strip().replace("]","").split("[")
            tableName = currentQuery[1]
            operation = currentQuery[0].split(" ")[0]
            action = currentQuery[0].split(" ")[1]
            initial = Relation(tableName)
            initial.importTable(tableName+".txt")
            print(initial)
        else: 
            tableName = "temptable" + str(curLayer + 1)
            operation = currentQuery.strip().split(" ")[0]
            action = currentQuery.strip().split(" ")[1]

        if operation == "select":
            querySelect(tableName, action, curLayer)
        elif operation == "project":
            queryProject(tableName, action, curLayer)
        elif operation == "product":
            queryCartesianProduct(tableName, action, curLayer)
        elif operation == "divide":
            queryDivision(tableName, action, curLayer)
        elif operation == "join":
            queryJoin(tableName, action, curLayer)
        elif operation == "intersect":
            queryIntersection(tableName, action, curLayer)
        elif operation == "union":
            queryUnion(tableName, action, curLayer)
        elif operation == "minus":
            queryMinus(tableName, action, curLayer)

        curLayer = curLayer - 1
        if curLayer == 0:
            finalTable = Relation("output")
            finalTable.importTable("temptable1.txt")
            print(finalTable)
    return

def querySelect(tableName, action, layer):
    tempTable = Relation("temp")
    tempTable.importTable(tableName+".txt")
    if "<=" in action:
        tempTable.selection(action.split("<=")[0], action.split("<=")[1], "<=", "temptable" +str(layer)+".txt")
    elif "<" in action:
        tempTable.selection(action.split("<")[0], action.split("<")[1], "<", "temptable" +str(layer)+".txt")
    elif ">=" in action:
        tempTable.selection(action.split(">=")[0], action.split(">=")[1], ">=", "temptable" +str(layer)+".txt")
    elif ">" in action:
        tempTable.selection(action.split(">")[0], action.split(">")[1], ">", "temptable" +str(layer)+".txt")
    elif "==" in action:
        tempTable.selection(action.split("==")[0], action.split("==")[1], "==", "temptable" +str(layer)+".txt")
    elif "!=" in action:
        tempTable.selection(action.split("!=")[0], action.split("!=")[1], "!=", "temptable" +str(layer)+".txt")
    return
        
def queryProject(tableName, action, layer):
    tempTable = Relation("temp")
    tempTable.importTable(tableName+".txt")
    tempTable.projection(action.split(","),"temptable" +str(layer)+".txt")
    return

def queryCartesianProduct(tableName, action, layer):
    tempTable1 = Relation("temp1")
    tempTable1.importTable(tableName+".txt")
    
    tempTable2 = Relation("temp2")
    tempTable2.importTable(action+".txt")

    tempTable1.cartesianProduct(tempTable2, "temptable" +str(layer)+".txt")

def queryDivision(tableName, action, layer):
    tempTable1 = Relation("temp1")
    tempTable1.importTable(tableName+".txt")
    
    tempTable2 = Relation("temp2")
    tempTable2.importTable(action+".txt")

    tempTable1.division(tempTable2, "temptable" +str(layer)+".txt")

def queryJoin(tableName, action, layer):
    tempTable1 = Relation("temp1")
    tempTable1.importTable(tableName+".txt")
    values = action.split(",")

    tempTable2 = Relation("temp2")
    tempTable2.importTable(values[0]+".txt")

    tempTable1.join(tempTable2, values[1], values[2], "temptable" +str(layer)+".txt")

def queryIntersection(tableName, action, layer):
    tempTable1 = Relation("temp1")
    tempTable1.importTable(tableName+".txt")
    
    tempTable2 = Relation("temp2")
    tempTable2.importTable(action+".txt")

    tempTable1.intersection(tempTable2, "temptable" +str(layer)+".txt")

def queryUnion(tableName, action, layer):
    tempTable1 = Relation("temp1")
    tempTable1.importTable(tableName+".txt")
    
    tempTable2 = Relation("temp2")
    tempTable2.importTable(action+".txt")

    tempTable1.union(tempTable2, "temptable" +str(layer)+".txt")

def queryMinus(tableName, action, layer):
    tempTable1 = Relation("temp1")
    tempTable1.importTable(tableName+".txt")
    
    tempTable2 = Relation("temp2")
    tempTable2.importTable(action+".txt")

    tempTable1.minus(tempTable2, "temptable" +str(layer)+".txt")

queryParser()