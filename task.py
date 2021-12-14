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
help = lambda : sys.stdout.write("""Usage :-
$ ./task add 2 hello world    # Add a new item with priority 2 and text "hello world" to the list
$ ./task ls                   # Show incomplete priority list items sorted by priority in ascending order
$ ./task del INDEX            # Delete the incomplete item with the given index
$ ./task done INDEX           # Mark the incomplete item with the given index as complete
$ ./task help                 # Show usage
$ ./task report               # Statistics\n""")


"""
Task Format : <priority> <text>
Files : 
    1. task.txt  # task.txt is the file that stores the list of tasks
    File Format : <priority> <text> in each line one task with priority
    2. completed.txt # completed.txt is the file that stores the list of completed tasks
    File Format : <text> in each line one task
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
def prettyTaskOutput(returnEmptyMsg=True):
    """
    ['task.py', 'ls']
    List incomplete priority list items sorted by priority in ascending order
    sample:
        $ ./task ls
        1. change light bulb [2]
        2. water the plants [5]
    """
    output = ""
    if os.path.exists("task.txt"):
        with open("task.txt", "r") as f:
            for linenumber,line in enumerate(f,1):
                line = line.strip().split(" ")
                output += "{}. {} [{}]\n".format(linenumber, " ".join(line[1:]), line[0])
    if not output:
        if returnEmptyMsg:
            return ("There are no pending tasks!")
        else:
            return False
    return output

def getInsertionIndex(priority):
    """
    Return the insertion index of the new task 
    Approach : linear Search
    """
    if not os.path.isfile("task.txt"):
        return 0
    else:
        lineCount = 0
        try:
            with open("task.txt", "r") as f:
                for index,line in enumerate(f,1):
                    line = line.strip().split(" ")
                    if int(line[0])>=priority:
                        return index
                    lineCount = index
                return lineCount+1
        except Exception as e:
            print("Error:Unable to read the task file!\n{}".format(e))
            sys.exit(1)

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
        if not sys.argv[3]: # tries to access the text from the sys.argv[3]
            raise IndexError
        text = " ".join(sys.argv[3:])
        if priority<0:
            raise ValueError
    except Exception as e:
        print("Error: Missing tasks string. Nothing added!")
        return False
    # add the new task to the task.txt file as per the format with the priority and text
    # The files should always be sorted in order of the priority, ie, the task with the highest priority(lowest priority numerical value) should be first item in the file.
    # The tasks should be sorted in ascending order of priority.
    index = getInsertionIndex(priority)
    with open("task.txt", "r+" if os.path.isfile("task.txt") else "w+") as f:
        # read lines until the index
        for i in range(index):  f.readline()
        # write the new task
        f.write("{} {}\n".format(priority, text))
        # read the rest of the lines
        for line in f:  f.write(line)
    # or the below method overwriting complete file
    """ with open("task.txt", "r+" if os.path.isfile("task.txt") else "w+") as f:
        # read the file and store the lines in a list
        lines = f.readlines()
        # insert the new task at the index
        lines.insert(index, str(priority)+" "+text+"\n")
        # write the list back to the file
        f.seek(0)
        f.write("".join(lines)) """

    print("Added task: \"{}\" with priority {}".format(text, priority))

# fourth function : delete deals with deleting an item from the list
def delete(printLog=True,index=None):
    """
        ['task.py', 'del', '2']
        index : int from sys.argv[2] or line number of the task to be deleted
        Delete the incomplete item with the given index
        Example:
        $ ./task del 3
        Deleted task #3
    """
    try:
        index = int(sys.argv[2]) if not index else index
        if index<1:
            raise ValueError
    except ValueError:
        if printLog:
            print("Error: task with index #{} does not exist. Nothing deleted.".format(sys.argv[2]))
        return False
    except Exception as e:
        if printLog:
            print("Error: Missing NUMBER for deleting tasks.")
        return False
    try:
        # delete the task from the task.txt file at the given index line number [read until the index and overwrite the rest of the file] finally truncate the file
        with open("task.txt", "r+") as f:
            # read the lines until the index
            cursorPosition=0
            for i in range(index-1):  
                cursorPosition+=len(f.readline())
            # read the next line
            target = f.readline()
            if not target: raise IndexError
            # read the rest of the lines
            lines=f.readlines()
            # write the lines back to the file
            f.seek(cursorPosition)
            f.write("".join(lines))
            f.truncate()
        # or the below method overwriting complete file
        """ with open("task.txt", "r+") as f:
            # read the file and store the lines in a list
            lines = f.readlines()
            # delete the task at the index
            del lines[index]    # del lines[index]
            # write the list back to the file
            f.seek(0)
            f.write("".join(lines)) """
        if printLog:
            print("Deleted task #{}".format(index)) 
            # print("Deleted task: \"{}\" with priority {}".format(index, text))
        return " ".join(target.strip().split(" ")[1:]) # return the text of the deleted task
    except Exception as e:
        if printLog:
            print("Error: task with index #{} does not exist. Nothing deleted.".format(sys.argv[2]))
        return False

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
        3. Completed task are writted to a completed.txt file. Each task occupies a single line in this file. Each line in the file should be in this format :
        ```
        task
        ```
        where task is the task description.
        Here is an example file that has 2 items.
        ```
        Buy milk
        Complete the project
        ```
    """
    try:
        index = int(sys.argv[2])
    except IndexError as e:
        print("Error: Missing NUMBER for marking tasks as done.")
        return False
    # use the delete function to delete the task from the task.txt file and store the returned value 'task text'  in the variable item to be written to the completed.txt file
    item = delete(printLog=False,index=int(sys.argv[2]))
    if item:
        with open("completed.txt", "a" if os.path.isfile("completed.txt") else "w+") as f:
            f.write(item+"\n")
        print("Marked item as done.")
        # print("Marked item with index {} as complete".format(sys.argv[2]))
    else:
        print("Error: no incomplete item with index #0 exists.")
        # print("Error: item with index {} does not exist. Nothing marked as complete.".format(sys.argv[2]))

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
    completedTasks = [str(linenumber)+". "+line.strip() 
                            for linenumber,line in enumerate(open("completed.txt", "r"),1)
                    ] if os.path.exists("completed.txt") else []
    pendingTasksOutput = prettyTaskOutput()
    print("Pending : {}".format( len(pendingTasksOutput.split("\n"))-1  if pendingTasksOutput else 0 ))
    print(pendingTasksOutput)
    print("Completed : {}".format(len(completedTasks)))
    print(*completedTasks, sep="\n")

if __name__ == '__main__':
    # print(sys.argv)
    # No command provided (no arguments) : print the help
    if len(sys.argv) < 2:
        help()
    else:
        if sys.argv[1] == "ls":
            print(prettyTaskOutput())
        elif sys.argv[1] == "add":
            add()
        elif sys.argv[1] == "del":
            print(delete())
        elif sys.argv[1] == "done":
            done()
        elif sys.argv[1] == "report":
            report()
        else:
            help()