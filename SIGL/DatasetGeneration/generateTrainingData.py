import os
import json
import sys
import uuid

def processSPADEJSON(fileName,directory):

    with open(directory) as line:
        graph = json.load(line)

    edges = [] # Edges in the graph represented as a list of tuples
    hashNames = {} # Maps hash of each node to it's path name
    process = {} # Stores if a node is a process or artifact
    
    for node in graph:
        # Handling nodes
        if "id" in node:
            if node['type'] == "Artifact":
                try:
                    hashNames[node['id']] = node['annotations']['path']
                    process[node['id']] = 0
                except: 
                    hashNames[node['id']] = node['annotations']['subtype'].replace(" ", "")
                    process[node['id']] = 0
            if node['type'] == "Process":  
                hashNames[node['id']] = node['annotations']['exe']
                process[node['id']] = 1
        # Handling edges
        else:
            if node["to"] != node["from"]:  #Remove self edge
                edges.append((node['to'],node['from']))

    jsonDict = {
        "name": fileName,
        "edges": edges,
        "hash": hashNames,
        "types": process
    }

    return jsonDict

def generate_uuid():
    generated_uuid = uuid.uuid4()# Generate a UUID4 (random) UUID
    uuid_hex = generated_uuid.hex #make a hex without dashes
    return uuid_hex

def processDNS(dnsFileDirectory):
  """
  Parses a DNS log file and returns a dictionary containing domains as keys and lists of resolved IPs as values.

  Args:
      filename: The path to the DNS log file.

  Returns:
      A dictionary containing domains as keys and lists of resolved IPs as values.
  """
  results = {}
  with open(dnsFileDirectory, 'r') as f:
    for line in f:
      parts = line.strip().split()
      domain = parts[0]
      if len(parts) == 1:
        # Domain name with no resolved IP yet
        pass
        # if domain not in results:
        #   results[domain] = []
      elif len(parts) > 1:
        # Domain name with resolved IP(s)
        ips = parts[1].split(',')  # Split multiple IPs if present
        if domain not in results:
          results[domain] = ips
        else:
          results[domain].extend(ips)  # Add IPs to existing list for the domain

    for k,v in results.items():
        results[k] = list(set(v))
  return results

def processSPADEJSONwithIPandDNS(fileName,directory,dnsFileDirectory):

    with open(directory) as line:
        graph = json.load(line)

    edges = [] # Edges in the graph represented as a list of tuples
    hashNames = {} # Maps hash of each node to it's path name
    process = {} # Stores if a node is a process or artifact
    sockets = {} # key:ip, value: list of ids
    
    for node in graph:
        # Handling nodes
        if "id" in node:
            if node['type'] == "Artifact":
                try:
                    hashNames[node['id']] = node['annotations']['path']
                    process[node['id']] = 0
                except: 
                    if node['annotations']['subtype']=='network socket':
                        try:
                            hashNames[node['id']] = 'networksocket_'+node['annotations']['remote address'] #adds ip as networksocket_192.168.33.13
                            if sockets.get(node['annotations']['remote address']):
                                sockets[node['annotations']['remote address']]=[node['id']]
                            else:
                                sockets[node['annotations']['remote address']].append(node['id'])
                        except: 
                            pass
                    else:
                        hashNames[node['id']] = node['annotations']['subtype'].replace(" ", "")
                    process[node['id']] = 0
            if node['type'] == "Process":  
                hashNames[node['id']] = node['annotations']['exe']
                process[node['id']] = 1
        # Handling edges
        else:
            if node["to"] != node["from"]:  #Remove self edge
                edges.append((node['to'],node['from']))

    # resolutions: {queried domain: [resolvedIPs]}
    resolutions=processDNS(dnsFileDirectory)
    for d,ips in resolutions.items():
        hash = generate_uuid()
        hashNames[hash] = d #hash -> queried domain
        process[hash] = 0
        
        for ip in ips: #all ips returned by the resolution
            if sockets.get(ip): #if a socket was opened on that ip
                for id in sockets[ip]:
                    edges.append((hash,id)) #edge between domain and socket

    jsonDict = {
        "name": fileName,
        "edges": edges,
        "hash": hashNames,
        "types": process
    }

    return jsonDict

def generateDataset():

    base = os.path.dirname(os.path.abspath(__file__))
    trainingDir = os.path.join(base,"trainingGraphs")

    graphsList = os.listdir(trainingDir)

    outputList = []

    for graph in graphsList:

        graphName = graph.split("-")

        directory = os.path.join(trainingDir, graph)

        jsonDict = processSPADEJSON(graphName[0]+graphName[1][0],directory)

        outputList.append(jsonDict)

 
    with open(os.path.join(base, "trainingDataset.json") , "w") as f:

        f.write("[\n")
        f.write(json.dumps(outputList[0]))
        if len(outputList) > 1:
            for obj in outputList[1:]:
                f.write(",\n" + json.dumps(obj))
        f.write("\n]")

def generateDatasetwithDNS():
    base = os.path.dirname(os.path.abspath(__file__))
    trainingDir = os.path.join(base, "trainingGraphsWithDNS")
    files = os.listdir(trainingDir)
    graphsList=[]
    dnsList=[]

    for f in files:
        if f.endswith('.txt'):
            dnsList.append(f)
        else:
            graphsList.append(f)

    outputList = []

    for graph in graphsList:
        graphName= graph.split('.') #gets you 'graph-1' for example from 'graph-1.json'
        graphDir = os.path.join(trainingDir, graph)
        dnsLogName= graphName[0]+'txt'
        dnsLogDir=None

        if dnsLogName in dnsList:
            dnsLogDir=os.path.join(trainingDir, dnsLogName)
        
        if dnsLogDir:
            jsonDict = processSPADEJSONwithIPandDNS(graphName[0].replace('-',''),graphDir,dnsLogDir)
            outputList.append(jsonDict)
        else:
            jsonDict = processSPADEJSON(graphName[0].replace('-',''),graphDir)
            outputList.append(jsonDict)

    with open(os.path.join(base, "trainingDataset.json") , "w") as f:
        f.write("[\n")
        f.write(json.dumps(outputList[0]))
        if len(outputList) > 1:
            for obj in outputList[1:]:
                f.write(",\n" + json.dumps(obj))
        f.write("\n]")

def main():
    generateDatasetwithDNS()

if __name__ == "__main__":
    main()