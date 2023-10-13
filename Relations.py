class Relation:
    name = ""  
    columns = []
    rows = []
    filename = ""

    #initializes fields
    def __init__(self, name, filename = ""):
        self.name = name
        self.rows = []
        self.filename = filename

    #converts relation into string table
    def __str__(self):
        height = len(self.rows)
        width = len(self.columns)
        paddingIndex = []
        for column in self.columns:
            paddingIndex.append(len(column))

        for row in self.rows:
            i = 0
            for cell in row:
                if paddingIndex[i] < len(cell):
                    paddingIndex[i] = len(cell)
                i += 1

        totalWidth = sum(paddingIndex) + width + 1

        title = " " * ((totalWidth//2) - len(self.name)) + self.name + "\n" + totalWidth * "_" + "\n"
        
        ci = 0
        columnData = "|"
        for column in self.columns:

            columnString = column.ljust(paddingIndex[ci], " ")
            columnData += columnString + "|"
                
            ci += 1
        columnData += "\n"

        rowData = ""
        for row in self.rows:
            i = 0
            rowData += "|"
            for cell in row:
                cellString = cell.ljust(paddingIndex[i], " ")
                rowData += cellString + "|"
                
                i += 1
            rowData += "\n"

        return title + columnData + rowData
    
    #imports table from a csv file
    def importTable(self, filename):
        with open (filename, 'r') as file:
            x = 0
            for line in file:
                line = line.strip('\n').split(',')
                if x == 0:
                    #populates the column headers with the first row in the csv file
                    self.columns = line
                    x+=1
                else:
                    #populates row from csv file
                    self.rows.append(line)
            return
    
    #projects the selected fields into a new relation file
    #takes name of columns as array, takes output file name as string
    def projection(self, selectedColumns, filename):
        with open (filename, 'w') as file:
            file.write(",".join(selectedColumns) + "\n")
            for row in self.rows:
                newRow = []
                x = 0
                for column in self.columns:
                    if column in selectedColumns:
                        newRow.append(row[x])            
                    x+=1
                file.write(",".join(newRow) + "\n")

    #creates a new releation where rows that have matching values to the input are ported over
    #takes name of column, desired value of column, the operator to compare desired value vs real value, and the output filename
    def selection(self, selectedColumn, selectedValue, operator, filename):
        with open (filename, 'w') as file:
            file.write(",".join(self.columns) + "\n")
            i = self.columns.index(selectedColumn)

            if operator == "<=":
                for row in self.rows:
                    if(row[i] <= selectedValue):
                        file.write(",".join(row) + "\n")
            elif operator == "<":
                for row in self.rows:
                    if(row[i] < selectedValue):
                        file.write(",".join(row) + "\n")
            elif operator == ">=":
                for row in self.rows:
                    if(row[i] >= selectedValue):
                        file.write(",".join(row) + "\n")
            elif operator == ">":
                for row in self.rows:
                    if(row[i] > selectedValue):
                        file.write(",".join(row) + "\n")
            elif operator == "==":
                for row in self.rows:
                    if(row[i] == selectedValue):
                        file.write(",".join(row) + "\n")
            elif operator == "!=":
                for row in self.rows:
                    if(row[i] != selectedValue):
                        file.write(",".join(row) + "\n")
            else:
                pass
    
    #multiplies each row of the relation by another relation
    #takes another relation and an ouput file name
    def cartesianProduct(self, otherRelation, filename):
        with open (filename, 'w') as file:
            columns = ",".join(self.columns) + "," + ",".join(otherRelation.columns)
            file.write(columns + "\n")

            for row in self.rows:
                for otherRow in otherRelation.rows:
                    newRow = row+otherRow
                    file.write(",".join(newRow) + "\n")

    #currently not working at full functrionality, but will undo a cartesian product operation
    def division(self, otherRelation, filename):
        with open (filename, 'w') as file:
            width = len(self.columns) - len(otherRelation.columns)
            newColumns = self.columns[0:width]
            file.write(",".join(newColumns) + "\n")

            i = 0
            for row in self.rows:
                if i%len(otherRelation.rows) == len(self.rows)//len(otherRelation.rows):
                    newRow = row[0:width]    
                    file.write(",".join(newRow) + "\n")
                i += 1

    #joins two relations based off of matching key pairs
    #takes another relation, a key for itself, a key for the other relation, and the filename
    def join(self, otherRelation, key1, key2, filename):
        with open (filename, 'w') as file:
            columns = ",".join(self.columns) + "," + ",".join(otherRelation.columns)
            file.write(columns + "\n")

            key1Index = self.columns.index(key1)
            key2Index = otherRelation.columns.index(key2)

            for row in self.rows:
                for otherRow in otherRelation.rows:
                    if row[key1Index] == otherRow[key2Index]:
                        newRow = row+otherRow
                        file.write(",".join(newRow) + "\n")

    #creates a relation that is the matching components of two relations
    #takes the other relation and the output filename
    def intersection(self, otherRelation, filename):
        with open (filename, 'w') as file:
            file.write(",".join(self.columns) + "\n")
            if len(self.columns) != len(otherRelation.columns):
                return

            for row in self.rows:
                for otherRow in otherRelation.rows:
                    if row == otherRow:
                        file.write(",".join(row) + "\n")

    #creates a relation that is the complete non-duplicate components of two relations
    #takes the other relation and the output filename
    def union(self, otherRelation, filename):
        with open (filename, 'w') as file:
            file.write(",".join(self.columns) + "\n")
            if len(self.columns) != len(otherRelation.columns):
                return

            for row in self.rows:
                file.write(",".join(row) + "\n")

            for row in otherRelation.rows:
                if row not in self.rows:
                    file.write(",".join(row) + "\n")

    #removes all matching components of another relation from itself
    #takes the other relation and the output filename
    def minus(self, otherRelation, filename):
        with open (filename, 'w') as file:
            file.write(",".join(self.columns) + "\n")
            if len(self.columns) != len(otherRelation.columns):
                return

            for row in self.rows:
                if row not in otherRelation.rows:
                    file.write(",".join(row) + "\n")

# table1 = Relation("Base Test")
# table1.importTable("test.txt")
# table1.projection(["ID"],"testProjection.txt")
# table1.selection("Department", "CompSci", "==", "testSelection.txt")
# print(table1)

# table2 = Relation("Projection Test")
# table2.importTable("testProjection.txt")
# print(table2)

# table3 = Relation("Selection Test")
# table3.importTable("testSelection.txt")
# print(table3)

# employee = Relation("Employee")
# employee.importTable('employee.txt')
# print(employee)

# department = Relation("Department")
# department.importTable('department.txt')
# print(department)

# employee.join(department, 'dept', 'name', "joinTest.txt")
# table6 = Relation("Join Test")
# table6.importTable("joinTest.txt")
# print(table6)

# employee.cartesianProduct(department, "cartesianProduct.txt")
# table4 = Relation("Cartesian Product Test")
# table4.importTable("cartesianProduct.txt")
# print(table4)
# table4.division(department, "divisionProduct.txt")

# table5 = Relation("Division Test")
# table5.importTable("divisionProduct.txt")
# print(table5)


# employee2 = Relation("Employee2")
# employee2.importTable("employee2.txt")
# employee3 = Relation("Employee3")
# employee3.importTable("employee3.txt")

# employee2.intersection(employee3, "employee2intersect3.txt")
# employee2and3 = Relation("Employee 2 and 3")
# employee2and3.importTable("employee2intersect3.txt")
# print(employee2)
# print(employee3)
# print(employee2and3)

# employee2.union(employee3, "employee2union3.txt")
# employee2or3 = Relation("Employee 2 or 3")
# employee2or3.importTable("employee2union3.txt")
# print(employee2)
# print(employee3)
# print(employee2or3)

# employee2.minus(employee3, "employee2minus3.txt")
# employee2minus3 = Relation("Employee 2 minus 3")
# employee2minus3.importTable("employee2minus3.txt")
# print(employee2)
# print(employee3)
# print(employee2minus3)
