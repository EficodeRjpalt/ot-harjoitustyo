```
self.summary = attributes['Summary']
self.description = attributes['Description']
self.gitlab_id = attributes['GitLab ID']
self.gl_url = attributes['GitLab Issue URL']
self.status = attributes['Status']
self.reporter = attributes['Reporter']
self.assignee = attributes['Assignee']
self.gl_username = attributes['GitLab Username']
self.created = attributes['Created']
self.closed = attributes['Closed']
self.due_date = attributes['Due Date']
self.labels = attributes['Labels']
self.epic_link = attributes['Epic Link']
self.estimate = attributes['Estimate']
self.time_spent = attributes['Time Spent']
```

In module testing for CSVReader
```
#cssv = CSVReader('src/resources/mapping.json', 'src/resources/sample.csv')
# print(cssv.read_csv_to_dict())
```