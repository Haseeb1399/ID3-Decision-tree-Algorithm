import numpy as np
import sys
import pprint


def check_purity(table):
    '''
    Checks Last Column of Table, If all values are equal (Pure Table) then length of values would be 1 (Only 1 value)
    If True, Table is pure and returns true, else false
    '''
    
    
    values = np.unique(table[:,-1]) 
    
    if len(values)==1:
        return True
    else:
        return False      
    

def system_entropy(table):
    
    '''
    Calculates System Entropy of the given table. 
    Counts Yes/No in last column and then returns systems entropy
    '''
    
    total_yes = int(np.count_nonzero(table[:,-1]))
    total_no = int(np.count_nonzero(table[:,-1]==0))
        
    yes_prob = -(total_yes/(total_yes+total_no)) * np.log2(total_yes/(total_yes+total_no))
    no_prob = -(total_no/(total_yes+total_no)) * np.log2(total_no/(total_yes+total_no))
    
    return yes_prob+no_prob


def simple_entropy(a,b):
    
    '''
    Takes Input of two integers, And calculates their entropy
    '''
    
    if a == 0 or b == 0:
        return 0
    total_sum = int(a)+int(b)
    
    entropy = -(int(a)/total_sum * np.log2(int(a)/total_sum))-(int(b)/total_sum * np.log2(int(b)/total_sum)) 
    return entropy


def calc_entropy(table,itter):
    
    '''
    Calculates entropy of a given heading (Passed into this function as Itter)
    Calls Simple_entropy to get entropies and returns sum for each heading
    '''
    
    
    values,counts = np.unique(table[:,itter],return_counts=True)
    temp_list = []
        
    for i in range(len(values)):
        temp = np.where(table[:,itter]==values[i])
        new_table = table[temp]
        yes = np.count_nonzero(new_table[:,-1])
        no = np.count_nonzero(new_table[:,-1]==0)
            
        entropy = simple_entropy(int(yes),int(no))
        prob = counts[i]/sum(counts)
            
        temp_list.append(prob*entropy)
                     
    return(sum(temp_list))
    

def selectRoot(table):
    '''
    For every heading in the table, calls Calc_entropy and gaves the information gain In a list along with index
    Returns Heading with Highest Information gain
    '''
    
    
    temp = np.array(table)
    col = np.shape(temp)[1]
    sys = system_entropy(table)
    
    info_gains = []
    index_info_gains = []
    
    for i in range (col-1):
        temp = calc_entropy(table,i)
        info_gains.append(float(sys-temp))
        index_info_gains.append(i)
    
            
    temp = info_gains.index(max(info_gains))  
    temp = index_info_gains[temp]
    return temp
    


def Tree(initial_dataset,heading,item):
    '''
    Encoding is done Using two Lists of Dictionaries, Where key is the heading index (which is returned by select Root)
    One List (Heading) holds all the column headings
    Second List holds all items Belonging to that heading 
    Each matching heading and item have same key in each list (root)
    
    Function recursively builds tree 
    '''
    
    
    tree = {}
    root=selectRoot(initial_dataset)
    tree[heading[root].get(root)]={} #Parent Node
    values,_ = np.unique(initial_dataset[:,root],return_counts=True) #Get Unique Values under Parent node heading
    
    for i in range(len(values)):
        #Iterate on those unique values and make subtables
        
        temp = np.where(initial_dataset[:,root]==values[i]) #Get index
        curr_subtable = initial_dataset[temp] #Make Subtable
                
        if check_purity(curr_subtable): #Checks if table pure or not
            ans = np.unique(curr_subtable[:,-1]) #Gets Yes/No Value from last column
            
            #if 0 (Which is No) returns No as value to the that specific key otherwise Yes
            
            if ans[0] == 0:
                tree[heading[root].get(root)][item[root].get(root)[values[i]]] = "No"
            else:
                tree[heading[root].get(root)][item[root].get(root)[values[i]]] = "Yes"  
        else:
            tree[heading[root].get(root)][item[root].get(root)[values[i]]] = Tree(curr_subtable,heading,item) #Recursive call
    
    return tree
    

def set_labels(labels):
    count = 0
    heading_dict = []
    item_dict=[]
    headings = labels[0].split(',')
    
    for item in headings:
        #Make List of dictionary for Headings
        heading_dict.append({count:item})
        count+=1
    
    count =0
    for i in range(1,len(labels)):
        #Make list of Dictionary for items
        temp = labels[i].split(',')
        item_dict.append({count:temp})
        count+=1
    
    return heading_dict,item_dict
             
    
    

def main():

    data = sys.argv[1]
    encoding = sys.argv[2]
    labels =""
    
    array = np.loadtxt(data,dtype=int,delimiter=",")
    
    with open(encoding) as f:
        labels = [line.rstrip() for line in f]
           
    headings,items = set_labels(labels)
    tree = Tree(array,headings,items)
    pprint.pprint(tree)
    
    

main()