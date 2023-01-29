import json
from sklearn.externals import joblib

class IssueReporter:
    def __init__(self):
        self.issue_log = []
        self.model = joblib.load("issue_classifier.pkl")

    def report_issue(self, issue_description):
        self.issue_log.append(issue_description)
        print("Issue reported: " + issue_description)
        self.analyze_issues()

    def analyze_issues(self):
        if len(self.issue_log) >= 10:
            print("High number of issues reported. Sending alert to team.")
            self.send_alert()
        else:
            issue_type = self.model.predict([issue_description])[0]
            self.assign_issue(issue_type)
            
    def send_alert(self):
        data = {"issues": self.issue_log}
        headers = {"Content-type": "application/json"}
        response = requests.post("http://alerts.example.com/new_alert", data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            print("Alert sent successfully.")
        else:
            print("Error sending alert.")
            
    def assign_issue(self, issue_type):
        data = {"issue_type": issue_type, "issue_description": issue_description}
        headers = {"Content-type": "application/json"}
        response = requests.post("http://assigner.example.com/assign_issue", data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            print("Issue assigned successfully.")
        else:
            print("Error assigning issue.")

class IssueAssigner:
    def __init__(self):
        self.issue_queue = {}

    def receive_issue(self, issue_type, issue_description):
        if issue_type not in self.issue_queue:
            self.issue_queue[issue_type] = []
        self.issue_queue[issue_type].append(issue_description)
        print("Issue received: " + issue_description)
        
    def assign_issues(self):
        for issue_type, issues in self.issue_queue.items():
            print(f"Assigning {len(issues)} {issue_type} issues...")
            for issue in issues:
                print("Assigning issue: " + issue)
                self.assign_to_expert(issue_type, issue)

    def assign_to_expert(self, issue_type, issue):
        expert = self.find_expert(issue_type)
        data = {"issue_type": issue_type, "issue_description": issue}
        headers = {"Content-type": "application/json"}
        response = requests.post(f"http://{expert}.example.com/assign_issue", data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            print("Issue assigned to expert successfully.")
        else:
            print("Error assigning issue")
