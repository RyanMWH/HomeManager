# Need to come back and the try and excepts to this page so we can get a full understanding of what is happening when it happens.


from flask import Flask, request, jsonify, render_template_string
import json
app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to Home Task Manager!"
    
# Gets the regular tasks
@app.route('/lists/tasks', methods = ['GET'])
def getTasks():
    try:
        with open('lists.json', 'r') as listsFile:
            data = json.load(listsFile)

        tasks = data.get("To Do", [])
        return jsonify(tasks), 200
    
    except FileNotFoundError:
        return jsonify({"error": "Lists file not found."}), 500
    
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON file."}), 500

# Updates the completion of the tasks    
@app.route('/lists/tasks/update', methods = ['POST'])
def updateTaskComplete():
    try:
        payload = request.get_json()

        task_id = payload.get('id')
        completed = payload.get('completed')

        if task_id is None or completed is None:
            return jsonify({"error": "Missing required fields"}), 400
        
        with open('lists.json', 'r') as listsFile:
            data = json.load(listsFile)


        

        for task in data["To Do"]:
            if task["id"] == task_id:
                task["completed"] = bool(completed)

                with open('lists.json', 'w') as listsFile:
                    json.dump(data, listsFile, indent=2)

                return jsonify({"message": "Task updated"}), 200

    except FileNotFoundError:
        return jsonify({"error": "lists.json not found."}), 500
    
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON file."}), 500  

# Gets the shopping list items
@app.route('/lists/items', methods = ['GET'])
def getItems():
    try:
        with open('lists.json', 'r') as listsFile:
            data = json.load(listsFile)

        tasks = data.get("Groceries List", [])
        return jsonify(tasks), 200
    
    except FileNotFoundError:
        return jsonify({"error": "Lists file not found."}), 500
    
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON file."}), 500

# Updates the completion of the tasks    
@app.route('/lists/items/update', methods = ['POST'])
def updateItemGathered():
    try:
        payload = request.get_json()

        item_id = payload.get('id')
        gathered = payload.get('gathered')

        if item_id is None or gathered is None:
            return jsonify({"error": "Missing required fields"}), 400
        
        with open('lists.json', 'r') as listsFile:
            data = json.load(listsFile)


        

        for item in data["Groceries List"]:
            if item["id"] == item_id:
                item["gathered"] = bool(gathered)

                with open('lists.json', 'w') as listsFile:
                    json.dump(data, listsFile, indent=2)

                return jsonify({"message": "Item updated"}), 200

    except FileNotFoundError:
        return jsonify({"error": "lists.json not found."}), 500
    
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON file."}), 500  

# Gets the events for selected date.
@app.route('/calendar/<date>', methods = ['GET'])
def getEventsForDate(date):
    try:
        with open('calendarFile.json', 'r') as calendarFile:
            data = json.load(calendarFile)

        events = data.get(date, [])
        return jsonify(events), 200
    
    except FileNotFoundError:
        return jsonify({"error": "calendarFile not found."}), 500
    
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON file."}), 500

# Updates the completion of the event    
@app.route('/calendar/update', methods = ['POST'])
def updateEventComplete():
    try:
        payload = request.get_json()

        date = payload.get('date')
        event_id = payload.get('id')
        completed = payload.get('completed')

        if date is None or event_id is None or completed is None:
            return jsonify({"error": "Missing required fields"}), 400
        
        with open('calendarFile.json', 'r') as calendarFile:
            data = json.load(calendarFile)

        for event in data[date]:
            if event["id"] == event_id:
                event["completed"] = bool(completed)

                with open('calendarFile.json', 'w') as calendarFile:
                    json.dump(data, calendarFile, indent=2)

                return jsonify({"message": "Task updated"}), 200

    except FileNotFoundError:
        return jsonify({"error": "calendarFile not found."}), 500
    
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON file."}), 500        
        
# Gets all projects.
@app.route('/projects', methods = ['GET'])
def getProjects():
    try:
        with open('projects.json', 'r') as File:
            data = json.load(File)

        projects = data.get("Projects", [])
        return jsonify(projects), 200
    
    except FileNotFoundError:
        return jsonify({"error": "calendarFile not found."}), 500
    
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON file."}), 500

# Updates the completion of the projection    
@app.route('/projects/update', methods = ['POST'])
def updateProjectComplete():
    try:
        payload = request.get_json()

        project = payload.get('title')
        project_id = payload.get('id')
        completed = payload.get('completed')

        if project is None or project_id is None or completed is None:
            return jsonify({"error": "Missing required fields"}), 400
        
        with open('projects.json', 'r') as File:
            data = json.load(File)

        for project in data:
            if project["id"] == project_id:
                project["completed"] = bool(completed)

                with open('projects.json', 'w') as File:
                    json.dump(data, File, indent=2)

                return jsonify({"message": "Task updated"}), 200

    except FileNotFoundError:
        return jsonify({"error": "projects.json not found."}), 500
    
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON file."}), 500 

if __name__ == '__main__':
    app.run(debug=True)


    


