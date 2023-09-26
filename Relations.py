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

    #converts relation into table
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
    
    #imports table from another file
    def importTable(self, filename):
        with open (filename, 'r') as file:
            x = 0
            for line in file:
                line = line.strip('\n').split(',')
                if x == 0:
                    self.columns = line
                    x+=1
                else:
                    self.rows.append(line)
            
            return
    
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
            
    def cartesianProduct(self, otherRelation, filename):
        with open (filename, 'w') as file:
            columns = ",".join(self.columns) + "," + ",".join(otherRelation.columns)
            file.write(columns + "\n")

            for row in self.rows:
                for otherRow in otherRelation.rows:
                    newRow = row+otherRow
                    file.write(",".join(newRow) + "\n")

    def division(self, otherRelation, filename):
        with open (filename, 'w') as file:
            width = len(self.columns) - len(otherRelation.columns)
            newColumns = self.columns[0:width]
            file.write(",".join(newColumns) + "\n")

            height = len(self.rows)

            i = 0
            for row in self.rows:
                if i%len(otherRelation.rows) == 0:
                    newRow = row[0:width]    
                    file.write(",".join(newRow) + "\n")
                i += 1

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

    def intersection(self, otherRelation, filename):
        with open (filename, 'w') as file:
            file.write(",".join(self.columns) + "\n")
            if len(self.columns) != len(otherRelation.columns):
                return

            for row in self.rows:
                for otherRow in otherRelation.rows:
                    if row == otherRow:
                        file.write(",".join(row) + "\n")

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