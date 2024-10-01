import csv #it is used to read and write csv files
clean_data=[]
collected_project= {}

#======================== Functions ======================================

def getDataFromFile(file_path,file_name):
    #Gets Data from file, script works on specific documents, therefore it can handle the file size and amount of data
    with open('{}{}.csv'.format(file_path,file_name), mode='r')as file:
        csvFile= csv.reader(file,delimiter='!')
        for line in csvFile:
            for data in line:
                normalized_data=data.split(';')
                clean_data.append(list(normalized_data))
        file.close()

def normalizeData():
    #Normalizes data, fills empty cells with "null" string
    for row in clean_data:
        a=0
        for field in row:
            if field=='':
                row[a]='null'
            a+=1

def setDatas():
    #Filters and collects the required data in dictionary
    for row in clean_data[3:]:
        if row[0]=='Summe':
            break
        try:
            #print(row[6],row[10],row[11])
            project=row[3]
            hours=row[6]
            task=row[11]
            description=row[10]
            if not (task == 'null' and (description == 'null' or 'urlop' in description)):
                if (task,description,project) in collected_project.keys():
                    h=hours.replace(',','.')
                    h=float(h)
                    collected_project[(task, description, project)]+=h
                else:
                    h=hours.replace(',','.')
                    h=float(h)
                    collected_project[(task, description, project)]=h
        except:
            pass

def sortData():
    #Groups data by project, then by task and then by description
    collected_project_beta=list(collected_project.keys())
    collected_project_beta.sort(key=lambda a: (a[2],a[0],a[1]))
    collected_project_gamma={}
    for task, description, project in collected_project_beta:
        collected_project_gamma[(task, description, project)]=collected_project[(task, description, project)]
    return collected_project_gamma

def writeTheDoc(collected_project_gamma, file_path ,file_name):
    #writes the clean and grouped data into the file
    next_pro = ''
    file = open('{}{}.csv'.format(file_path,file_name), 'w', newline='')
    with file:
        header = ['Projekt', 'Task', 'Opis', 'Suma godzin']
        writer = csv.DictWriter(file, fieldnames=header, delimiter=';')
        writer.writeheader()
        for task, desc, pro, in collected_project_gamma:
            h = str(collected_project_gamma[task, desc, pro])
            h = h.replace('.', ',')
            if pro != next_pro:
                print('=' * 50)
                print('PROJEKT: {}'.format(pro))
                writer.writerow({
                    'Projekt': pro,
                    'Task': '',
                    'Opis': '',
                    'Suma godzin': ''
                })
                next_pro = pro
            writer.writerow({
                'Projekt': '',
                'Task': task,
                'Opis': desc,
                'Suma godzin': h

            })
            print('task: {}, opis: {}, suma godzin: {}'.format(task, desc, h))

#============== Test of the script ==============================

getDataFromFile("c:/temp/",'old_File') #name of a old file
normalizeData()
setDatas()
collected_project_gamma=sortData()
writeTheDoc(collected_project_gamma,'c:/temp/','new_file') #name of a new file


