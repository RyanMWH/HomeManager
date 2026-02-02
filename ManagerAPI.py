# Need to come back and the try and excepts to this page so we can get a full understanding of what is happening when it happens.


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

    project = payload.get('title')
    project_id = payload.get('id')
    completed = payload.get('completed')

    if project is None or project_id is None or completed is None:
        return jsonify({"error": "Missing required fields"}), 400
    
    data = readJSON('projects.json')

    for project in data:
        if project["id"] == project_id:
            project["completed"] = bool(completed)

            writeJSON('projects.json', data)

            return jsonify({"message": "Task updated"}), 200
        
    return jsonify({"error": "Task not found"}), 404

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


if __name__ == '__main__':
    app.run(debug=True)


    


