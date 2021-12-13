"""
Task tool to maintain tasks.
type : "without using argparse"

Algorithm:
    1. Parse arguments
    2. If no arguments are provided, print the help message/Usage and exit
    3. If arguments are provided, load the tasks from the file
    4. If the first argument is "ls", print the incomplete tasks in the list
    5. If the first argument is "add", add the new task to the pending list text file
    6. If the first argument is "done", add the task to completed list text file
    7. If the first argument is "del", delete the task from the pending list text file
    8. If the first argument is "help", print the help message/Usage and exit
"""

# sys library for command line arguments
import sys

# os library for file system operations
import os

# commands to be parsed 
# commands = [ "help" , "add" , "ls" , "del" , "done", "report"]

# first function : help deals with printing the help message
help = lambda : print("""$ ./task help
Usage :-
$ ./task add 2 hello world    # Add a new item with priority 2 and text "hello world" to the list
$ ./task ls                   # Show incomplete priority list items sorted by priority in ascending order
$ ./task del INDEX            # Delete the incomplete item with the given index
$ ./task done INDEX           # Mark the incomplete item with the given index as complete
$ ./task help                 # Show usage
$ ./task report               # Statistics""" , end="")


"""
Task Format : <priority> <text>
Files : 
    1. task.txt  # task.txt is the file that stores the list of tasks
    2. completed.txt # completed.txt is the file that stores the list of completed tasks
File Format : <priority> <text> in each line one task
"""
def parseTasksFromFile(filename):
    """
    Parse the tasks from the file and return a list of tasks
    """
    tasks = {}
    with open(filename, "r") as f:
        for linecount,line in enumerate(f,1):
            line = line.strip().split(" ")
            tasks[linecount] = [" ".join(line[1:]),int(line[0])]
    return tasks

# second function : ls deals with listing the incomplete items in the list
def prettyTaskPrinter(tasks,printPriority=True):
    """
    ['task.py', 'ls']
    List incomplete priority list items sorted by priority in ascending order
    sample:
        $ ./task ls
        1. change light bulb [2]
        2. water the plants [5]
    """
    tasks = sortedItems(tasks)
    if printPriority:
        for i,taskLineNum in enumerate(tasks,1):
            print("{}. {} [{}]".format(i, taskLineNum[1][0], taskLineNum[1][1]),end = "" if i == len(tasks) else "\n")
    else:
        for i,taskLineNum in enumerate(tasks,1):
            print("{}. {}".format(taskLineNum[0], taskLineNum[1][0]),end = "" if i == len(tasks) else "\n")
        # print("{}. {} [{}]".format(taskLineNum, 
        #         pendingTasks[taskLineNum][0], pendingTasks[taskLineNum][1]))

# third function : add deals with adding a new item to the list
def add():
    """
        ['task.py', 'add', '2', 'hello world']
        priority : int from sys.argv[2]
        text : str from sys.argv[3:]
        Add a new item with priority 2 and text "hello world" to the list
        Example:
        $ ./task add 5 "the thing i need to do"
        Added task: "the thing i need to do" with priority 5
    """
    try:
        priority = int(sys.argv[2])
        text = " ".join(sys.argv[3:])
        if priority<0:
            raise ValueError
    except Exception as e:
        print("Error: Missing tasks string. Nothing added!")
        return False
    priority = sys.argv[2]
    text = " ".join(sys.argv[3:])
    # add the new task to the task.txt file as per the format with the priority and text
    with open("task.txt", "a" if pendingTasks else "w" ) as f:
        f.write("{} {}\n".format(priority, text))
    print("Added task: \"{}\" with priority {}".format(text, priority),end="")

# fourth function : delete deals with deleting an item from the list
def delete(printLog=True,itemIndex=None):
    """
        ['task.py', 'del', '2']
        index : int from sys.argv[2]
        Delete the incomplete item with the given index
        Example:
        $ ./task del 3
        Deleted task #3
    """
    try:
        itemIndex = int(sys.argv[2]) if not itemIndex else itemIndex
        if not 0<itemIndex<len(pendingTasks)+1:
            raise ValueError
        index = sortedItems(pendingTasks)[itemIndex-1][0]
        if index not in pendingTasks:
            raise IndexError
    # ArgumentError : if the index is not provided
    except IndexError:
        if printLog:
            print("Error: Missing NUMBER for deleting tasks.",end="")
        return False
    except Exception as e:
        if printLog:
            print("Error: task with index #{} does not exist. Nothing deleted.".format(sys.argv[2]),end="")
        return False

    # delete the task from the task.txt file at the given index line
    with open("task.txt", "r+") as f:
        # current lines in the file
        lines = f.readlines()
        # delete the line at the given index
        lines.pop(int(index)-1)
        # overwrite the file with the updated lines
        # bring the cursor to the beginning of the file
        f.seek(0)
        # write the updated lines
        f.writelines(lines)
        # truncate the file i.e remove the extra lines
        f.truncate()
    if printLog:
        print("Deleted task #{}".format(index),end="") 
    return pendingTasks.pop(index)
    # print("Deleted task: \"{}\" with priority {}".format(index, text))

def sortedItems(inputDict):
    """
    Sort the items in the dictionary by priority
    """
    return sorted(inputDict.items(), key=lambda x: x[1][1])

#fifth done : moves the item from task.txt to completed.txt
def done():
    """
        ['task.py', 'done', '2']
        index : int from sys.argv[2]
        Mark the incomplete item with the given index as complete
        Example:
        $ ./task done 3
        Marked item with index 3 as complete
    """
    try:
        index = int(sys.argv[2])
    except IndexError as e:
        print("Error: Missing NUMBER for marking tasks as done.",end="")
        return False
    item = delete(printLog=False,itemIndex=int(sys.argv[2]))
    if item:
        with open("completed.txt", "a" if completedTasks else "w" ) as f:
            f.write("{} {}\n".format(item[1], item[0]))
        print("Marked item as done.",end="")
        # print("Marked item with index {} as complete".format(sys.argv[2]),end="")
    else:
        # print("Error: item with index {} does not exist. Nothing marked as complete.".format(sys.argv[2]),end="")
        print("Error: no incomplete item with index #0 exists.",end="")

#sixth report : prints the statistics of the list
def report():
    """
    sample:
    $ ./task report
    Pending : 2
    1. this is a pending task [1]
    2. this is a pending task with priority [4]

    Completed : 3
    1. completed task
    2. another completed task
    3. yet another completed task
    """
    print("Pending : {}".format(len(pendingTasks)))
    prettyTaskPrinter(pendingTasks)
    print(end="\n\n")
    print("Completed : {}".format(len(completedTasks)))
    prettyTaskPrinter(completedTasks,printPriority=False)
    print()

if __name__ == '__main__':
    # print(sys.argv)
    # No command provided (no arguments) : print the help
    if len(sys.argv) < 2:
        help()
    else:
        # parse the txt files and store the tasks in a dictionary
        pendingTasks = parseTasksFromFile("task.txt") if os.path.exists("task.txt") else {}
        completedTasks = parseTasksFromFile("completed.txt") if os.path.exists("completed.txt") else {}
        if sys.argv[1] == "ls":
            prettyTaskPrinter(pendingTasks) if pendingTasks else print("There are no pending tasks!",end="")
            print()
        elif sys.argv[1] == "add":
            add()
        elif sys.argv[1] == "del":
            delete()
        elif sys.argv[1] == "done":
            done()
        elif sys.argv[1] == "report":
            report()
        else:
            help()