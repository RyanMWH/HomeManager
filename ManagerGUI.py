# Imports
import tkinter as tk
import tkinter.font as tkFont
import requests
import threading
from tkcalendar import *
from datetime import datetime


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky= tk.NSEW)

        self.master.rowconfigure(0, weight=0)
        self.master.rowconfigure(1, weight=1)
        self.master.rowconfigure(2, weight=0)

        self.master.columnconfigure(0, weight=1)

        self.currentContent = None
        self.fetch_job = None
        self.fetch_running = False

        self.createFrames()
        self.createMenuWidgets()

# Intializing Functions
    def createFrames(self):
        
        # Content Area
        self.contentArea = tk.Frame(self.master, bg="#494949")
        self.contentArea.grid(column= 0, row=1, sticky=tk.NSEW)
        self.contentArea.columnconfigure(0, weight=1)
        self.contentArea.rowconfigure(0, weight=1)
        print("Creating Content Area...")

        # Top Menu Bar for changing between to do lists, grocery lists, car maintence and calendar.
        self.topMenu = tk.Frame(self.master)
        self.topMenu.grid(column=0, row=0, sticky=tk.EW)
        print("Creating Top Menu...")

        for x in range(7):
            self.topMenu.columnconfigure(x, weight=1)
            print("Creating column ", x ,"...")
        
        # Bottom Menu that contains the fetch data and the quit button
        self.bottomMenu = tk.Frame(self.master)
        self.bottomMenu.grid(column=0, row=2, sticky=tk.EW)
        print("Creating Bottom Menu...")

        for x in range(10):
            self.bottomMenu.columnconfigure(x, weight=1)
            print("Creating column ", x ,"...")

    def createMenuWidgets(self):

        # Bottom Menu buttons
        self.quitButton = tk.Button(self.bottomMenu, text='Quit',command= self.quit)
        self.quitButton.grid(column= 9, row= 0, padx=5, pady=5)
        print("Creating the Quit button...")

        self.fetchButton = tk.Button(self.bottomMenu, text="Fetch Data", command= lambda: self.startFetch(self.currentContent))
        self.fetchButton.grid(column= 0,row= 0, padx=5, pady=5)
        print("Creating the Fetch Data button...")

        # Top Menu buttons
        self.calendarButton = tk.Button(self.topMenu, text="Calendar", command=self.calendarContent)
        self.calendarButton.grid(column= 1, row=0, pady= 5)
        print("Creating the Calendar button...")

        self.toDoButton = tk.Button(self.topMenu, text="To-do", command=self.todoContent)
        self.toDoButton.grid(column= 2, row=0, pady= 5)
        print("Creating the To-do button...")

        self.carMaintenanceButton = tk.Button(self.topMenu, text="Car Maintenance", command=self.carMaintenanceContent)
        self.carMaintenanceButton.grid(column= 3, row=0, pady= 5)
        print("Creating the Car Maintenance button...")

        self.shoppingListButton = tk.Button(self.topMenu, text="Shopping List", command=self.shoppingListsContent)
        self.shoppingListButton.grid(column= 4, row=0, pady= 5)
        print("Creating the Shopping List button...")

        self.projectsButton = tk.Button(self.topMenu, text="Projects", command=self.projectsContent)
        self.projectsButton.grid(column= 5, row=0, pady= 5)
        print("Creating the Projects button...")

# Helper Functions
    def clearFrame(self, frame):
        
        if not frame or not frame.winfo_exists():
            return
        
        for widget in frame.winfo_children():
            widget.destroy()
        print(f"Clearing {frame} frame...")

    def startFetch(self, contentToFetch, project_id= None):
        print("Starting fetch...")
        if self.currentContent != contentToFetch:
            return
        
        if self.fetch_running:
            print("Fetch already running, skipping")
            return
        
        self.fetch_running = True
        
        match contentToFetch:

            case "calendar":
                selectedDate = self.cal.get_date()
                print("Starting thread for calendar events...")
                threading.Thread(
                    target=self.fetchDateEvents,
                    args=(selectedDate,),
                    daemon= True
                ).start()

                self.fetch_job = self.after(60000, lambda: self.startFetch(contentToFetch, selectedDate))

            case "shoppingLists":
                print("Starting thread for shopping list items...")
                threading.Thread(
                    target=self.fetchItems,
                    daemon= True
                ).start()
                self.fetch_job = self.after(60000, lambda: self.startFetch(contentToFetch))

            case "carMaintenance":
                print("Fetching Car Maintenance")

                self.fetch_job = self.after(60000, lambda: self.startFetch(contentToFetch))

            case "todo":
                print("Starting thread for to do tasks...")
                threading.Thread(
                    target=self.fetchTasks,
                    daemon= True
                ).start()
                self.fetch_job = self.after(60000, lambda: self.startFetch(contentToFetch))

            case "projects":
                print("Starting thread for projects...")
                threading.Thread(
                    target=self.fetchProjects,
                    daemon= True
                ).start()
                self.fetch_job = self.after(60000, lambda: self.startFetch(contentToFetch))

            case "projectsubtasks":
                print(f"Starting thread for project {project_id}'s, subtasks")
                threading.Thread(
                    target=self.fetchProjectSubtasks,
                    args=(project_id,),
                    daemon= True
                ).start()
                self.fetch_job = self.after(60000, lambda: self.startFetch(contentToFetch, project_id))

            case default:
                print("Unknown case!")

    def manualFetch(self):
        self.stopFetchLoop()          # reset timer
        self.startFetch(self.currentContent)

    def stopFetchLoop(self):
        if self.fetch_job is not None:
            self.after_cancel(self.fetch_job)
            self.fetch_job = None
            self.fetch_running = False
        
    def on_date_selected(self, event):
        selected_date = self.cal.get_date()
        self.startFetch("calendar", selected_date)

    def delete(self, file, id=None, pid=None, stid=None):
        print('test')

# Maintenance Functions
    def weeklyCleanUp():
        print('Coming soon')

# Content Screen Flips
    def todoContent(self):
        self.stopFetchLoop()
        self.currentContent = "todo"
        self.clearFrame(self.contentArea)
        
        # Setting To-do Page Content Frame
        self.todoPageArea = tk.Frame(self.contentArea, bg="#262626")
        self.todoPageArea.grid(row=0, column=0, sticky="nsew")
        self.todoPageArea.columnconfigure(0, weight=1)
        self.todoPageArea.rowconfigure(0, weight=1)
        self.todoPageArea.rowconfigure(1, weight=8)

        # Creating Frames
        # Task Title Frame
        self.tasksTitleFrame = tk.Frame(self.todoPageArea, bg="#262626")
        self.tasksTitleFrame.grid(row=0, column=0, sticky="nsew")
        self.tasksTitleFrame.columnconfigure(0, weight=1)
        self.tasksTitleLabel = tk.Label(self.tasksTitleFrame,
                                       text="Tasks", 
                                       bg="#262626",
                                       fg="white",
                                       anchor="center",
                                       pady=10,
                                       font=("Helvetica", 18, "bold")
                                       )
        self.tasksTitleLabel.grid(row=0, column=0, sticky="ew")
        
        # Tasks Frame
        self.tasksFrame = tk.Frame(self.todoPageArea, bg="#262626")
        self.tasksFrame.grid(row=1, column=0, sticky="nsew")
        self.tasksFrame.columnconfigure(0, weight=0)
        self.tasksFrame.columnconfigure(1, weight=0)
        self.tasksFrame.columnconfigure(2, weight=0)
        self.tasksFrame.columnconfigure(3, weight=1)
        self.tasksFrame.columnconfigure(4, weight=0)
        self.tasksFrame.columnconfigure(5, weight=0)
        self.tasksFrame.columnconfigure(6, weight=0)
        


        self.startFetch(self.currentContent)
        self.fetchButton.config(command= lambda: self.manualFetch(self.currentContent))
    
    def calendarContent(self):
        # Basic Inits
        self.stopFetchLoop()
        self.currentContent = "calendar"
        self.clearFrame(self.contentArea)

        self.calendarPageArea = tk.Frame(self.contentArea, bg="#262626")
        self.calendarPageArea.grid(row=0, column=0, sticky="nsew")
        self.calendarPageArea.columnconfigure(0, weight=5)
        self.calendarPageArea.columnconfigure(1, weight=1)
        self.calendarPageArea.rowconfigure(0, weight=1)

        self.calendarContentFrame = tk.Frame(self.calendarPageArea, bg='blue')
        self.calendarContentFrame.grid(row=0, column=0, sticky="nsew")

        self.eventsFrame = tk.Frame(self.calendarPageArea, bg="#262626")
        self.eventsFrame.grid(row=0, column=1, sticky="nsew")
        self.eventsFrame.columnconfigure(0, weight=1)
        self.eventsFrame.rowconfigure(0, weight=1)
        self.eventsFrame.rowconfigure(1, weight=5)

        self.eventsTitleLabel = tk.Label(self.eventsFrame,
                                         bg="#262626",
                                         fg="white",
                                         font=("Helvetica", 14, "bold"))
        self.eventsTitleLabel.grid(row=0, column=0, sticky= tk.E + tk.W)


        self.eventsListFrame = tk.Frame(self.eventsFrame, bg="#262626")
        self.eventsListFrame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.eventsListFrame.columnconfigure(1, weight=1)
        

        self.today = datetime.now()
        self.cal = Calendar(self.calendarContentFrame,
                            selectmode="day",
                            date_pattern="yyyy-mm-dd",
                            year= self.today.year,
                            month= self.today.month,
                            day= self.today.day,
                            firstweekday= "sunday",
                            theme= 'classic',
                            background="white",
                            foreground="black",
                            bordercolor="black",
                            borderwidth=2,
                            normalbackground= "white",
                            normalforeground="blue",
                            weekendbackground="white",
                            weekendforeground="blue",
                            headersbackground="black",
                            headersforeground="black",
                            othermonthforeground="gray",
                            selectbackground="blue",
                            selectforeground="white",
                            showweeknumbers=False)
        
        self.cal.pack(fill="both", expand=True, padx=1, pady=1)
        self.cal.bind("<<CalendarSelected>>", self.on_date_selected)

        self.startFetch(self.currentContent)
        self.fetchButton.config(command= lambda: self.manualFetch())
        
    def carMaintenanceContent(self):
        self.stopFetchLoop()
        self.currentContent = "carMaintenance"
        self.clearFrame(self.contentArea)# Content Area labels.
        self.carMaintenanceLabel = tk.Label(self.contentArea, text="Car Maintenance")
        self.carMaintenanceLabel.grid(sticky="nw", padx=10, pady=10)
        print("Creating the Result label holder...")

        self.fetchButton.config(command= lambda: self.startFetch(self.currentContent))

    def shoppingListsContent(self):
        self.stopFetchLoop()
        self.currentContent = "shoppingLists"
        self.clearFrame(self.contentArea)

        # Setting Shopping List Page Content Frame
        self.shoppingListPageArea = tk.Frame(self.contentArea, bg="#262626")
        self.shoppingListPageArea.grid(row=0, column=0, sticky="nsew")
        self.shoppingListPageArea.columnconfigure(0, weight=1)
        self.shoppingListPageArea.rowconfigure(0, weight=1)
        self.shoppingListPageArea.rowconfigure(1, weight=8)

        # Creating Frames
        # Task Title Frame
        self.shoppingListsTitleFrame = tk.Frame(self.shoppingListPageArea, bg="#262626")
        self.shoppingListsTitleFrame.grid(row=0, column=0, sticky="nsew")
        self.shoppingListsTitleFrame.columnconfigure(0, weight=1)
        self.shoppingListsTitleLabel = tk.Label(self.shoppingListsTitleFrame,
                                       text="Shopping List", 
                                       bg="#262626",
                                       fg="white",
                                       anchor="center",
                                       pady=10,
                                       font=("Helvetica", 18, "bold")
                                       )
        self.shoppingListsTitleLabel.grid(row=0, column=0, sticky="ew")
        
        # Items Frame
        self.itemHolderFrame = tk.Frame(self.shoppingListPageArea, bg="#262626")
        self.itemHolderFrame.grid(row=1, column=0, sticky="nsew")
        self.itemHolderFrame.columnconfigure(0, weight=1)
        self.itemHolderFrame.columnconfigure(1, weight=1)

        self.leftItemsFrame = tk.Frame(self.itemHolderFrame, bg="#262626")
        self.leftItemsFrame.grid(row=0, column=0, sticky="nsew")
        self.leftItemsFrame.columnconfigure(0, weight=0)
        self.leftItemsFrame.columnconfigure(1, weight=0)
        self.leftItemsFrame.columnconfigure(2, weight=1)
        self.leftItemsFrame.columnconfigure(3, weight=0)

        self.rightItemsFrame = tk.Frame(self.itemHolderFrame, bg="#262626")
        self.rightItemsFrame.grid(row=0, column=1, sticky="nsew")
        self.rightItemsFrame.columnconfigure(0, weight=0)
        self.rightItemsFrame.columnconfigure(1, weight=0)
        self.rightItemsFrame.columnconfigure(2, weight=1)
        self.rightItemsFrame.columnconfigure(3, weight=0)
        

        
        self.startFetch(self.currentContent)
        self.fetchButton.config(command= lambda: self.manualFetch(self.currentContent))

    def projectsContent(self):
        self.stopFetchLoop()
        self.currentContent = "projects"
        self.clearFrame(self.contentArea)

        # Setting Project Page Content Frame
        self.projectsPageArea = tk.Frame(self.contentArea, bg="#262626")
        self.projectsPageArea.grid(row=0, column=0, sticky="nsew")
        self.projectsPageArea.columnconfigure(0, weight=1)
        self.projectsPageArea.rowconfigure(0, weight=1)
        self.projectsPageArea.rowconfigure(1, weight=8)

        # Creating Frames
        # Project Title Frame
        self.projectTitleFrame = tk.Frame(self.projectsPageArea, bg="#262626")
        self.projectTitleFrame.grid(row=0, column=0, sticky="nsew")
        self.projectTitleFrame.columnconfigure(0, weight=1)
        self.projectTitleLabel = tk.Label(self.projectTitleFrame,
                                       text="Projects", 
                                       bg="#262626",
                                       fg="white",
                                       anchor="center",
                                       pady=10,
                                       font=("Helvetica", 18, "bold")
                                       )
        self.projectTitleLabel.grid(row=0, column=0, sticky="ew")
        
        # Projects Frame
        self.projectsFrame = tk.Frame(self.projectsPageArea, bg="#262626")
        self.projectsFrame.grid(row=1, column=0, sticky="nsew")
        self.projectsFrame.columnconfigure(0, weight=0)
        self.projectsFrame.columnconfigure(1, weight=0)
        self.projectsFrame.columnconfigure(2, weight=1)
        self.projectsFrame.columnconfigure(3, weight=0)
        self.projectsFrame.columnconfigure(4, weight=0)
        self.projectsFrame.columnconfigure(5, weight=0)
        
        self.startFetch(self.currentContent)
        self.fetchButton.config(command= lambda: self.manualFetch(self.currentContent))

    def projectSubtasksContent(self, pid, title, desc):
            self.stopFetchLoop()
            self.currentContent = "projectsubtasks"
            self.clearFrame(self.contentArea)

            # Setting Project Subtasks Page Content Frame
            self.projectSubtasksPageArea = tk.Frame(self.contentArea, bg="#262626")
            self.projectSubtasksPageArea.grid(row=0, column=0, sticky="nsew")
            self.projectSubtasksPageArea.columnconfigure(0, weight=1)
            self.projectSubtasksPageArea.rowconfigure(0, weight=1)            
            self.projectSubtasksPageArea.rowconfigure(1, weight=0)
            self.projectSubtasksPageArea.rowconfigure(2, weight=1)
            self.projectSubtasksPageArea.rowconfigure(3, weight=8)

            # Creating Frames
            # Project Title Frame
            self.projectSubtasksTitleFrame = tk.Frame(self.projectSubtasksPageArea, bg="#262626")
            self.projectSubtasksTitleFrame.grid(row=0, column=0, sticky="nsew")
            self.projectSubtasksTitleFrame.columnconfigure(0, weight=1)
            self.projectSubtasksTitleLabel = tk.Label(self.projectSubtasksTitleFrame,
                                        text=title, 
                                        bg="#262626",
                                        fg="white",
                                        anchor="center",
                                        pady=10,
                                        font=("Helvetica", 18, "bold")
                                        )
            self.projectSubtasksTitleLabel.grid(row=0, column=0, sticky="ew")

            # Project Description Frame
            self.projectDescriptionFrame = tk.Frame(self.projectSubtasksPageArea, bg="#262626")
            self.projectDescriptionFrame.grid(row=1, column=0, sticky="nsew")
            self.projectDescriptionFrame.columnconfigure(0, weight=1)
            self.projectDescriptionFrame.columnconfigure(1, weight=6)
            self.projectDescriptionFrame.columnconfigure(2, weight=1)

            self.projectDescriptionLabel = tk.Label(self.projectDescriptionFrame,
                                        text=desc, 
                                        bg="#262626",
                                        fg="white"
                                        )
            self.projectDescriptionLabel.grid(row=0, column=1, sticky=tk.NW)
            
            # Subtasks Frame
            self.subtasksHolderFrame = tk.Frame(self.projectSubtasksPageArea, bg="#262626")
            self.subtasksHolderFrame.grid(row=3, column=0, sticky="nsew")
            self.subtasksHolderFrame.columnconfigure(0, weight=0)
            self.subtasksHolderFrame.columnconfigure(1, weight=0)
            self.subtasksHolderFrame.columnconfigure(2, weight=1)
            self.subtasksHolderFrame.columnconfigure(3, weight=0)

            

            print(pid)
            self.startFetch(self.currentContent, pid)
            self.fetchButton.config(command= lambda: self.manualFetch(self.currentContent))

# Data retrival start
    def fetchDateEvents(self, date):
        print(f"Fetching events for {date}...")

        self.eventsTitleLabel.config(text= f"Events for {date}")

        response = requests.get(f"http://127.0.0.1:5000/calendar/{date}")
        data = response.json()

        print(f"API Response type: {type(data)}")
        print(f"API Response data: {data}")
        
        self.after(0, lambda: self.updateCalendarEvents(data))

        self.fetch_running = False

    def fetchTasks(self):
            print("Fetching tasks...")

            response = requests.get(f"http://127.0.0.1:5000/lists/tasks")
            data = response.json()

            print(f"API Response type: {type(data)}")
            print(f"API Response data: {data}")
            
            self.after(0, lambda: self.updateTasks(data))

            self.fetch_running = False

    def fetchItems(self):
            print("Fetching items...")

            response = requests.get(f"http://127.0.0.1:5000/lists/items")
            data = response.json()

            print(f"API Response type: {type(data)}")
            print(f"API Response data: {data}")
            
            self.after(0, lambda: self.updateItems(data))

            self.fetch_running = False

    def fetchProjects(self):
            print("Fetching projects...")

            response = requests.get(f"http://127.0.0.1:5000/projects")
            data = response.json()

            print(f"API Response type: {type(data)}")
            print(f"API Response data: {data}")
            
            self.after(0, lambda: self.updateProjects(data))

            self.fetch_running = False

    def fetchProjectSubtasks(self, pid):
        print("Fetching subtasks for project...")

        response = requests.get(f"http://127.0.0.1:5000/projects/{pid}/tasks")
        data = response.json()


        print(f"API Response type: {type(data)}")
        print(f"API Response data: {data}")
        
        self.after(0, lambda: self.updateProjectSubtasks(data, pid))

        self.fetch_running = False


# Functions to keep data up to date with variable changes, and check list toggle.
    def updateCalendarEvents(self, events):
        self.clearFrame(self.eventsListFrame)

        if not events:
            tk.Label(
                self.eventsListFrame,
                text="No Events",
                bg="#262626",
                justify= "center"
            ).grid(sticky="ew")
            return
        
        for row, event in enumerate(events):
            # The variable below is like an on/off switch for the checkbox 
            Var = tk.IntVar(value=1 if event.get("completed") else 0)

            # Create a font object for this label
            Font = tkFont.Font(family="Helvetica", size=12)    
            Font.configure(overstrike=1 if event.get("completed") else 0)


            eventTextLabel = tk.Label(self.eventsListFrame,
                                      text=event['title'],
                                      bg="#262626",
                                      font=Font)
            event_id = event["id"]

            # This is the main toggle that use the on/off switch in unison with the text label
            def toggle(var=Var,font=Font, eid=event_id):
                font.configure(overstrike= var.get())
                requests.post(
                    "http://127.0.0.1:5000/calendar/update",
                    json={
                        "date": self.cal.get_date(),
                        "id": eid,
                        "completed": bool(var.get())
                    },
                    timeout=2
                )


            completedCheckBox = tk.Checkbutton(self.eventsListFrame,
                                               variable=Var,
                                               command=toggle,
                                               bg="#262626")
            
            completedCheckBox.grid(row=row, column=0, sticky="w", padx=(0, 8)) 
            eventTextLabel.grid(row=row, column=1, sticky="w")

            deleteButton = tk.Button(self.eventsListFrame,
                                     text= 'X',
                                     bg="#262626",
                                     highlightthickness= 0,
                                     bd= 0)
            deleteButton.grid(row=row, column= 3, padx= (2, 8))       

    def updateTasks(self, tasks):

        if not tasks:
            tk.Label(
                self.tasksFrame,
                text="No Tasks",
                bg="#262626",
                justify= "center"
            ).grid(sticky="ew")
            return
        
        sortedtasks = sorted(tasks, key= lambda item: item['important'], reverse= True)

        for row, task in enumerate(sortedtasks):
            # The variable below is like an on/off switch for the checkbox 
            Var = tk.IntVar(value=1 if task.get("completed") else 0)

            # Create a font object for this label
            Font = tkFont.Font(family="Helvetica", size=12)    
            Font.configure(overstrike=1 if task.get("completed") else 0)


            taskTextLabel = tk.Label(self.tasksFrame,
                                      text=task['title'],
                                      bg="#262626",
                                      font=Font)
            task_id = task["id"]

            # This is the main toggle that use the on/off switch in unison with the text label
            def toggle(var=Var,font=Font, tid=task_id):
                font.configure(overstrike= var.get())
                requests.post(
                    "http://127.0.0.1:5000/lists/tasks/update",
                    json={
                        "id": tid,
                        "completed": bool(var.get())
                    },
                    timeout=2
                )


            completedCheckBox = tk.Checkbutton(self.tasksFrame,
                                               variable=Var,
                                               command=toggle,
                                               bg="#262626")
            
            completedCheckBox.grid(row=row, column=0, sticky="nw", padx=(0, 8)) 

            if task["important"]:
                importantLabel = tk.Label(self.tasksFrame, text="⚠", bg="#262626", fg="#F60E0E").grid(row=row, column=1, sticky="nw", padx=(0, 8))
            
            taskTextLabel.grid(row=row, column=2, sticky="nw")

            if task["owner"] is not None:
                ownerLabel = tk.Label(self.tasksFrame, text= task["owner"], bg="#005CFC").grid(row=row, column=4, sticky="w")

            if task["duedate"] is not None:
                dateLabel = tk.Label(self.tasksFrame, text= task["duedate"], bg="#FF3700", fg="#000000").grid(row=row, column=5, sticky="ew")

            deleteButton = tk.Button(self.tasksFrame,
                                     text= 'X',
                                     bg="#262626",
                                     highlightthickness= 0,
                                     bd= 0)
            deleteButton.grid(row=row, column= 6, padx= (2, 8))

    def updateItems(self, items):

        if not items:
            tk.Label(
                self.itemsFrame,
                text="No Items",
                bg="#262626",
                justify= "center"
            ).grid(sticky="ew")
            return
        
        itemAmount = len(items)
        print(f"Amount of Items: {itemAmount}")

        halfamount = int(itemAmount / 2)
        starterColumn = 0
        removeRows = 0
        column = self.leftItemsFrame
        sorteditems = sorted(items, key= lambda item: item['category'])

        for row, item in enumerate(sorteditems):
            if row >= halfamount:
                column = self.rightItemsFrame
                removeRows = halfamount
            # The variable below is like an on/off switch for the checkbox 
            Var = tk.IntVar(value=1 if item.get("gathered") else 0)

            # Create a font object for this label
            Font = tkFont.Font(family="Helvetica", size=12)    
            Font.configure(overstrike=1 if item.get("gathered") else 0)


            itemTextLabel = tk.Label(column,
                                      text=item['item'],
                                      bg="#262626",
                                      font=Font)
            item_id = item["id"]

            # This is the main toggle that use the on/off switch in unison with the text label
            def toggle(var=Var,font=Font, iid=item_id):
                font.configure(overstrike= var.get())
                requests.post(
                    "http://127.0.0.1:5000/lists/items/update",
                    json={
                        "id": iid,
                        "gathered": bool(var.get()),
                        "category": item["category"]
                    },
                    timeout=2
                )


            gatheredCheckBox = tk.Checkbutton(column,
                                               variable=Var,
                                               command=toggle,
                                               bg="#262626")
            
            gatheredCheckBox.grid(row=row-removeRows, column=0, sticky="nw", padx=(0, 8)) 

            itemTextLabel.grid(row=row-removeRows, column=1, sticky="nw")

            if item["category"] is not None:
                categoryLabel = tk.Label(column, anchor="e", text= item["category"], bg="#005CFC").grid(row=row-removeRows, column=2, sticky="e")

            deleteButton = tk.Button(column,
                                     text= 'X',
                                     bg="#262626",
                                     highlightthickness= 0,
                                     bd= 0)
            deleteButton.grid(row=row-removeRows, column= 3, padx= (2, 8))

    def updateProjects(self, projects):

        if not projects:
            tk.Label(
                self.projectsFrame,
                text="No Projects",
                bg="#262626",
                justify= "center"
            ).grid(sticky="ew")
            return

        for row, project in enumerate(projects):
            # The variable below is like an on/off switch for the checkbox 
            Var = tk.IntVar(value=1 if project.get("completed") else 0)

            # Create a font object for this label
            Font = tkFont.Font(family="Helvetica", size=12)    
            Font.configure(overstrike=1 if project.get("completed") else 0)


            projectTextLabel = tk.Label(self.projectsFrame,
                                      text=project['title'],
                                      bg="#262626",
                                      font=Font)
            project_id = project["id"]

            # This is the main toggle that use the on/off switch in unison with the text label
            def toggle(var=Var,font=Font, pid=project_id):
                font.configure(overstrike= var.get())
                requests.post(
                    "http://127.0.0.1:5000/projects/update",
                    json={
                        "id": pid,
                        "completed": bool(var.get())
                    },
                    timeout=2
                )


            completedCheckBox = tk.Checkbutton(self.projectsFrame,
                                               variable=Var,
                                               command=toggle,
                                               bg="#262626")
            
            completedCheckBox.grid(row=row, column=0, sticky="nw", padx=(0, 8)) 

            projectTextLabel.grid(row=row, column=1, sticky="nw")
            
            print(project_id)

            subTasksButton = tk.Button(self.projectsFrame,
                                    text= "View Sub-Tasks",
                                    bg="#262626",
                                    highlightthickness= 0,
                                    bd= 0,
                                    command= lambda pid=project_id,
                                                    title=project['title'],
                                                    desc=project['description']:
                                                    self.projectSubtasksContent(int(pid), title, desc))
            subTasksButton.grid(row=row, column= 4)
            deleteButton = tk.Button(self.projectsFrame,
                                     text= 'X',
                                     bg="#262626",
                                     highlightthickness= 0,
                                     bd= 0)
            deleteButton.grid(row=row, column= 5, padx= (2, 8))

    def updateProjectSubtasks(self, subtasks, pid):

        if not subtasks:
            tk.Label(
                self.subtasksHolderFrame,
                text="No Tasks",
                bg="#262626",
                justify= "center"
            ).grid(sticky="ew")
            return
        
        for row, subtask in enumerate(subtasks):
            # The variable below is like an on/off switch for the checkbox 
            Var = tk.IntVar(value=1 if subtask.get("completed") else 0)

            # Create a font object for this label
            Font = tkFont.Font(family="Helvetica", size=12)    
            Font.configure(overstrike=1 if subtask.get("completed") else 0)


            subtaskTextLabel = tk.Label(self.subtasksHolderFrame,
                                      text=subtask['title'],
                                      bg="#262626",
                                      font=Font)
            subtask_id = subtask["id"]

            # This is the main toggle that use the on/off switch in unison with the text label
            def toggle(var=Var,font=Font, stid=subtask_id):
                font.configure(overstrike= var.get())
                requests.post(
                    "http://127.0.0.1:5000/projects/tasks/update",
                    json={
                        "pid": pid,
                        "stid": stid,
                        "completed": bool(var.get())
                    },
                    timeout=2
                )


            completedCheckBox = tk.Checkbutton(self.subtasksHolderFrame,
                                               variable=Var,
                                               command=toggle,
                                               bg="#262626")
            
            completedCheckBox.grid(row=row, column=0, sticky="nw", padx=(0, 8)) 

            subtaskTextLabel.grid(row=row, column=1, sticky="nw")

            deleteButton = tk.Button(self.subtasksHolderFrame,
                                     text= 'X',
                                     bg="#262626",
                                     highlightthickness= 0,
                                     bd= 0)
            deleteButton.grid(row=row, column= 5, padx= (2, 8))


app = Application()
app.master.title('Home Task Manager')
screen_width = app.master.winfo_screenwidth()
screen_height = app.master.winfo_screenheight()

# Calculate position x, y to center
x = (screen_width // 2) - (800 // 2)
y = (screen_height // 2) - (600 // 2)

app.master.geometry(f"800x600+{x}+{y}")
app.calendarContent()
app.mainloop()

