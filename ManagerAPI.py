
from flask import Flask, request, jsonify, render_template_string
import json
import os
app = Flask(__name__)

# Helper Functions
def readJSON(file):

    if not os.path.exists(f'data/{file}'):
        raise FileNotFoundError(f'{file} not found in data folder or does not exist.')

    try:
        with open(f'data/{file}', 'r') as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError:
        raise ValueError(f"Error decoding JSON from file: {file}")
    
def writeJSON(file, data):
    try:
        with open(f'data/{file}', 'w') as f:
            json.dump(data, f, indent=2)
    except IOError:
        raise IOError(f"Error writing to file {file}")

@app.route('/')
def home():
    return "Welcome to Home Task Manager!"
    
# Gets the regular tasks
@app.route('/lists/tasks', methods = ['GET'])
def getTasks():
    
    data =  readJSON('tasks.json')
    tasks = data.get("To Do", [])
    return jsonify(tasks), 200

# Updates the completion of the tasks    
@app.route('/lists/tasks/update', methods=['POST'])
def updateTaskComplete():
    
    payload = request.get_json()
    task_id = payload.get('id')
    completed = payload.get('completed')

    if task_id is None or completed is None:
        return jsonify({"error": "Missing required fields"}), 400

    data = readJSON('tasks.json')

    for task in data["To Do"]:
        if task["id"] == task_id:
            task["completed"] = bool(completed)

            writeJSON('tasks.json', data)

            return jsonify({"message": "Task updated"}), 200

    return jsonify({"error": "Task not found"}), 404

# Delete task from To-Do list
@app.route('/lists/tasks/delete', methods=['DELETE'])
def deleteTask():

    payload = request.get_json()
    
    task_id = payload.get('id')

    data = readJSON('tasks.json')

    olddata = len(data["To Do"])
    if task_id is None:
        return jsonify({"error": "Missing required fields"}), 400

    # Find project

    data["To Do"]= [task for task in data["To Do"] if int(task["id"]) != int(task_id)]
    writeJSON('tasks.json', data)
    newdata = len(data["To Do"])
    if len(olddata) == len(newdata):
        return jsonify({"message": "Task was not removed"}), 500
    
    return jsonify({"message": "Task deleted"}), 200

# Gets the shopping list items
@app.route('/lists/items', methods = ['GET'])
def getItems():

    data = readJSON('shopping.json')
    tasks = data.get("Groceries List", [])
    return jsonify(tasks), 200

# Updates the completion of the tasks    
@app.route('/lists/items/update', methods = ['POST'])
def updateItemGathered():
    
    payload = request.get_json()
    item_id = payload.get('id')
    gathered = payload.get('gathered')

    if item_id is None or gathered is None:
        return jsonify({"error": "Missing required fields"}), 400
    
    data = readJSON('shopping.json')        

    for item in data["Groceries List"]:
        if item["id"] == item_id:
            item["gathered"] = bool(gathered)

            writeJSON('shopping.json', data)

            return jsonify({"message": "Item updated"}), 200

    return jsonify({"error": "Item not found"}), 404

# Delete item from shopping list
@app.route('/lists/items/delete', methods=['DELETE'])
def deleteItem():

    payload = request.get_json()
    
    item_id = payload.get('iid')

    data = readJSON('shopping.json')

    olddata = len(data["Groceries List"])
    if item_id is None:
        return jsonify({"error": "Missing required fields"}), 400

    # Find project

    data["Groceries List"]= [item for item in data["Groceries List"] if int(item["id"]) != int(item_id)]
    writeJSON('shopping.json', data)
    newdata = len(data["Groceries List"])
    if len(olddata) == len(newdata):
        return jsonify({"message": "Item was not removed"}), 500
    
    return jsonify({"message": "Item deleted"}), 200

# Gets the events for selected date.
@app.route('/calendar/<date>', methods = ['GET'])
def getEventsForDate(date):

    data = readJSON('calendar.json')
    events = data.get(date, [])
    return jsonify(events), 200

# Updates the completion of the event    
@app.route('/calendar/update', methods = ['POST'])
def updateEventComplete():
        
    payload = request.get_json()

    date = payload.get('date')
    event_id = payload.get('id')
    completed = payload.get('completed')

    if date is None or event_id is None or completed is None:
        return jsonify({"error": "Missing required fields"}), 400
    
    data = readJSON('calendar.json')

    for event in data[date]:
        if event["id"] == event_id:
            event["completed"] = bool(completed)

            writeJSON('calendar.json', data)

            return jsonify({"message": "Task updated"}), 200
            
    return jsonify({"error": "Event not found"}), 404     

# Deletes the event under a specified date
@app.route('/calendar/date/delete', methods=['DELETE'])
def deleteEvent():

    payload = request.get_json()
    
    date = payload.get('date')
    event_id = payload.get('eid')

    data = readJSON('calendar.json')

    if date is None or event_id is None:
        return jsonify({"error": "Missing required fields"}), 400

    # Find project
    for events in data.get(date, []):
        if int(events["id"]) == int(event_id):
            # Remove matching event
            data[date].remove(events)
            writeJSON('calendar.json', data)
            return jsonify({"message": "Event deleted"}), 200

    return jsonify({"error": "Event not found"}), 404

# Gets all projects.
@app.route('/projects', methods = ['GET'])
def getProjects():
    
    data = readJSON('projects.json')

    projects = data.get("Projects", [])
    return jsonify(projects), 200

# Updates the completion of the projection    
@app.route('/projects/update', methods = ['POST'])
def updateProjectComplete():
        
    payload = request.get_json()

    project_id = payload.get('id')
    completed = payload.get('completed')

    if project_id is None or completed is None:
        return jsonify({"error": "Missing required fields"}), 400
    
    data = readJSON('projects.json')

    for project in data.get("Projects", []):
        if project["id"] == project_id:
            project["completed"] = bool(completed)

            writeJSON('projects.json', data)

            return jsonify({"message": "Task updated"}), 200
        
    return jsonify({"error": "Task not found"}), 404

@app.route('/projects/delete', methods=['DELETE'])
def deleteProject():

    payload = request.get_json()
    
    project_id = payload.get('pid')

    data = readJSON('projects.json')

    if project_id is None:
        return jsonify({"error": "Missing required fields"}), 400

    # Find project

    data["Projects"]= [project for project in data.get("Projects", []) if int(project["id"]) != int(project_id)]
    writeJSON('projects.json', data)
    return jsonify({"message": "Project deleted"}), 200


@app.route('/projects/<pid>/tasks', methods = ['GET'])
def getSubtasksForProject(pid):

    data = readJSON('projects.json')
    
    projects = data.get("Projects", [])

    subtasks = []
    print(type(projects))
    print(projects)

    for project in projects:
        if int(project['id']) == int(pid):
            subtasks = project.get("tasks", [])
            break
        
    return jsonify(subtasks), 200

# Update Project Subtasks
@app.route('/projects/<pid>/tasks/update', methods= ['POST'])
def updateProjectSubtaskComplete():

    payload = request.get_json()

    project_id = payload.get('pid')
    subtask_id = payload.get('stid')
    completed = payload.get('completed')

    if project_id is None or subtask_id is None or completed is None:
        return jsonify({"error": "Missing required fields"}), 400
    
    data = readJSON('projects.json')

    for project in data:
        if project['id'] == project_id:
            for task in project['tasks']:
                if task['id'] == subtask_id:
                    task['completed'] = bool(completed)

            writeJSON('projects.json', data)

            return jsonify({"message": "Task updated"}), 200

    return jsonify({"error": "Subtask not found"}), 404

# Delete Project Subtasks

##########################
# !!! CLEAN UP LATER !!! #
##########################
@app.route('/projects/tasks/delete', methods=['DELETE'])
def delete_subtask():

    payload = request.get_json()
    
    project_id = payload.get('pid')
    subtask_id = payload.get('stid')

    data = readJSON('projects.json')

    if project_id is None or subtask_id is None:
        return jsonify({"error": "Missing required fields"}), 400

    # Find project
    for project in data.get("Projects", []):
        if int(project["id"]) == int(project_id):
            # Remove matching subtask
            project["tasks"] = [task for task in project.get("tasks", []) if int(task["id"]) != int(subtask_id)]
            writeJSON('projects.json', data)
            return jsonify({"message": "Subtask deleted"}), 200

    return jsonify({"error": "Project or Subtask not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)


    


