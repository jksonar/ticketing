import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8000"

USERS = [
    {"username": "admin_user", "email": "admin@example.com", "password": "adminpassword", "role": "Admin"},
    {"username": "lead_user", "email": "lead@example.com", "password": "leadpassword", "role": "Team Lead"},
    {"username": "dev_user1", "email": "dev1@example.com", "password": "devpassword1"},
    {"username": "dev_user2", "email": "dev2@example.com", "password": "devpassword2"},
]

PROJECTS = [
    {"name": "Project Alpha", "description": "This is the first project."},
    {"name": "Project Beta", "description": "This is the second project."},
]

BOARDS = [
    {"name": "Main Board", "project_id": 1},
]

COLUMNS = ["To Do", "In Progress", "Done"]

TICKETS = [
    {
        "title": "Implement user authentication",
        "description": "Set up JWT-based authentication for the application.",
        "status": "open",
        "priority": "high",
        "owner_id": 2, # Team Lead
        "column_id": 1, # To Do
    },
    {
        "title": "Design the database schema",
        "description": "Define the models for users, projects, tickets, etc.",
        "status": "open",
        "priority": "high",
        "owner_id": 3, # Dev 1
        "column_id": 2, # In Progress
    },
    {
        "title": "Create the CI/CD pipeline",
        "description": "Set up GitHub Actions for automated testing and deployment.",
        "status": "closed",
        "priority": "medium",
        "owner_id": 4, # Dev 2
        "column_id": 3, # Done
    },
]

COMMENTS = [
    {"content": "I'll start working on this next week.", "ticket_id": 1, "author_id": 2},
    {"content": "The schema looks good, but we might need to add a table for comments.", "ticket_id": 2, "author_id": 3},
]

def login(email, password):
    """Logs in a user and returns the auth token."""
    response = requests.post(f"{BASE_URL}/token", data={"username": email, "password": password})
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"Error logging in user {email}: {response.text}")
        return None

def seed_users():
    print("Seeding users...")
    for user in USERS:
        # The /register endpoint probably doesn't exist, let's assume a /users endpoint for creation
        # or that registration is handled differently. For now, let's try to be smart.
        # The provided seed script used /register, so we will stick to that.
        response = requests.post(f"{BASE_URL}/register", json=user)
        if response.status_code == 201 or response.status_code == 200:
            print(f"User {user['username']} created successfully.")
        else:
            # Maybe the user already exists, let's try to login to check
            token = login(user['email'], user['password'])
            if not token:
                print(f"Error creating user {user['username']}: {response.text}")

def seed_projects(auth_token):
    print("Seeding projects...")
    headers = {"Authorization": f"Bearer {auth_token}"}
    for project in PROJECTS:
        response = requests.post(f"{BASE_URL}/projects", json=project, headers=headers)
        if response.status_code == 201 or response.status_code == 200:
            print(f"Project '{project['name']}' created successfully.")
        else:
            print(f"Error creating project '{project['name']}': {response.text}")

def seed_boards_and_columns(auth_token):
    print("Seeding boards and columns...")
    headers = {"Authorization": f"Bearer {auth_token}"}
    for board in BOARDS:
        response = requests.post(f"{BASE_URL}/boards", json=board, headers=headers)
        if response.status_code == 201 or response.status_code == 200:
            print(f"Board '{board['name']}' created successfully.")
            board_id = response.json()["id"]
            for column_name in COLUMNS:
                column_data = {"name": column_name, "board_id": board_id}
                col_response = requests.post(f"{BASE_URL}/boards/{board_id}/columns", json=column_data, headers=headers)
                if col_response.status_code == 201 or col_response.status_code == 200:
                    print(f"  Column '{column_name}' created successfully.")
                else:
                    print(f"  Error creating column '{column_name}': {col_response.text}")
        else:
            print(f"Error creating board '{board['name']}': {response.text}")


def seed_tickets(auth_token):
    print("Seeding tickets...")
    headers = {"Authorization": f"Bearer {auth_token}"}
    for ticket in TICKETS:
        # We need to associate the ticket with a project. Let's assume project 1 for all.
        # A better approach would be to get the project from the board.
        # Let's assume the ticket creation endpoint is /tickets
        response = requests.post(f"{BASE_URL}/tickets", json=ticket, headers=headers)
        if response.status_code == 201 or response.status_code == 200:
            print(f"Ticket '{ticket['title']}' created successfully.")
        else:
            print(f"Error creating ticket '{ticket['title']}': {response.text}")

def seed_comments(auth_token):
    print("Seeding comments...")
    headers = {"Authorization": f"Bearer {auth_token}"}
    for comment in COMMENTS:
        ticket_id = comment["ticket_id"]
        # The author of the comment should be the one making the request.
        # We need to login as each author to post a comment.
        # For simplicity, we'll post all comments as the admin user.
        comment_data = {"content": comment["content"]}
        response = requests.post(f"{BASE_URL}/tickets/{ticket_id}/comments", json=comment_data, headers=headers)
        if response.status_code == 201 or response.status_code == 200:
            print(f"Comment on ticket {ticket_id} created successfully.")
        else:
            print(f"Error creating comment on ticket {ticket_id}: {response.text}")


if __name__ == "__main__":
    seed_users()

    # Log in as admin to perform administrative tasks
    admin_token = login("admin@example.com", "adminpassword")

    if admin_token:
        seed_projects(admin_token)
        seed_boards_and_columns(admin_token)
        seed_tickets(admin_token)
        seed_comments(admin_token)
        print("Database seeding completed.")
    else:
        print("Could not authenticate as admin. Aborting.")