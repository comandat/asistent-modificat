import argparse, json, os, sys

DB_FILE = "workspace/.workflow.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return {"tickets": [], "roles": {"architect": True, "developer": False, "tester": False, "reviewer": False}}
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def create_ticket(title, role, dependencies=[]):
    db = load_db()
    ticket_id = len(db["tickets"]) + 1
    ticket = {
        "id": ticket_id,
        "title": title,
        "role": role,
        "status": "PENDING",
        "dependencies": dependencies
    }
    db["tickets"].append(ticket)
    save_db(db)
    print(f"🎫 Ticket #{ticket_id} created: [{role}] {title}")

def check_dependencies(ticket, db):
    for dep_id in ticket["dependencies"]:
        dep_ticket = next((t for t in db["tickets"] if t["id"] == dep_id), None)
        if not dep_ticket or dep_ticket["status"] != "DONE":
            return False, f"Ticket #{dep_id} is not DONE."
    return True, ""

def start_ticket(ticket_id):
    db = load_db()
    ticket = next((t for t in db["tickets"] if t["id"] == ticket_id), None)
    if not ticket:
        print(f"❌ Ticket #{ticket_id} not found.")
        sys.exit(1)
        
    can_start, reason = check_dependencies(ticket, db)
    if not can_start:
        print(f"❌ Cannot start #{ticket_id}: Dependency {reason}")
        sys.exit(1)
        
    ticket["status"] = "IN_PROGRESS"
    save_db(db)
    print(f"🚀 Started Ticket #{ticket_id}: {ticket['title']}")

def finish_ticket(ticket_id):
    db = load_db()
    ticket = next((t for t in db["tickets"] if t["id"] == ticket_id), None)
    if not ticket:
        print(f"❌ Ticket #{ticket_id} not found.")
        sys.exit(1)
        
    ticket["status"] = "DONE"
    save_db(db)
    print(f"✅ Finished Ticket #{ticket_id}")

def list_tickets():
    db = load_db()
    print("📋 Workflow Board:")
    for t in db["tickets"]:
        deps = f"(Deps: {t['dependencies']})" if t['dependencies'] else ""
        print(f"#{t['id']} [{t['status']}] {t['role']}: {t['title']} {deps}")

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="cmd", required=True)
    
    subparsers.add_parser("list")
    
    create = subparsers.add_parser("create")
    create.add_argument("role", choices=["architect", "developer", "tester", "reviewer"])
    create.add_argument("title")
    create.add_argument("--deps", type=int, nargs="*", default=[])
    
    subparsers.add_parser("start").add_argument("id", type=int)
    subparsers.add_parser("finish").add_argument("id", type=int)
    
    args = parser.parse_args()
    
    if args.cmd == "list": list_tickets()
    elif args.cmd == "create": create_ticket(args.title, args.role, args.deps)
    elif args.cmd == "start": start_ticket(args.id)
    elif args.cmd == "finish": finish_ticket(args.id)

if __name__ == "__main__":
    main()
