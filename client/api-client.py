import linecache
import json
import requests 



#set starting id and ending id
start = 1
end = 30

# Loop over the JSON file
i=start

while i <= end:     
    
    # read a specific line
    line = linecache.getline('./client/output.txt', i)

    # write the line to the API
    myjson = json.loads(line)
    
    response = requests.post('http://localhost:80/EnergyItem', json=myjson)

    # Use this for dedbugging
    #print("Status code: ", response.status_code)
    #print("Printing Entire Post Request")


    print(response.json())

    # increase i
    i+=1
