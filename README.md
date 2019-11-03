# Backtrack
### Starting the server: ###

`python manage.py runserver`

### Database updates: ###

`python manage.py makemigrations`

`python manage.py migrate`

### Schema for Sprint creation: ###

```
{
  "start_date": "2019-10-19",
  "end_date": "2019-10-31",
  "capacity": 80,
  "project": 1,
  "pbis": [
    { "pbi_id": 6,
      "tasks": [{"description":  "Create", "effort_hours": 10},
           {"developer":  "2", "description":  "New", "effort_hours": 8}
      ]
    },
    { "pbi_id":5,
      "tasks": [{"description":  "Create", "effort_hours": 5},
           {"developer":  "2", "description":  "New", "effort_hours": 6}
      ]
    }
  ]
}
```

### Available Endpoints for CRUD: ###
* /person
* /project
* /Sprint
* /pbi
* /tasks

