import argparse, json, os, sys, datetime

DB_FILE = "workspace/.workflow.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return {"tickets": [], "roles": {"architect": True, "developer": True, "tester": True, "reviewer": True}}
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
        "assigned_to": None,
        "dependencies": dependencies,
        "created_at": str(datetime.datetime.now()),
        "comments": []
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
        
    if ticket["status"] not in ["PENDING", "REJECTED"]:
        print(f"❌ Ticket #{ticket_id} is already {ticket['status']}.")
        sys.exit(1)

    can_start, reason = check_dependencies(ticket, db)
    if not can_start:
        print(f"❌ Cannot start #{ticket_id}: Dependency {reason}")
        sys.exit(1)
        
    ticket["status"] = "IN_PROGRESS"
    save_db(db)
    print(f"🚀 Started Ticket #{ticket_id}: {ticket['title']}")

def submit_ticket(ticket_id, notes=""):
    """Developer submits work for review."""
    db = load_db()
    ticket = next((t for t in db["tickets"] if t["id"] == ticket_id), None)
    if not ticket or ticket["status"] != "IN_PROGRESS":
        print(f"❌ Ticket #{ticket_id} not IN_PROGRESS.")
        sys.exit(1)
        
    ticket["status"] = "NEEDS_REVIEW"
    if notes: ticket["comments"].append(f"[DEV]: {notes}")
    save_db(db)
    print(f"📩 Ticket #{ticket_id} submitted for REVIEW.")

def review_ticket(ticket_id, decision, notes=""):
    """Reviewer approves or rejects work."""
    if decision not in ["approve", "reject"]:
        print("❌ Decision must be 'approve' or 'reject'.")
        sys.exit(1)

    db = load_db()
    ticket = next((t for t in db["tickets"] if t["id"] == ticket_id), None)
    
    if not ticket or ticket["status"] != "NEEDS_REVIEW":
        print(f"❌ Ticket #{ticket_id} not ready for review (status: {ticket['status']}).")
        sys.exit(1)
        
    if decision == "approve":
        ticket["status"] = "DONE"
        ticket["comments"].append(f"[REVIEWER]: APPROVED - {notes}")
        print(f"✅ Ticket #{ticket_id} APPROVED & DONE.")
    else:
        ticket["status"] = "REJECTED"
        ticket["comments"].append(f"[REVIEWER]: REJECTED - {notes}")
        print(f"🚫 Ticket #{ticket_id} REJECTED. Sent back to Developer.")
        
    save_db(db)

def list_tickets():
    db = load_db()
    print("📋 Workflow Board:")
    for t in db["tickets"]:
        deps = f"(Deps: {t['dependencies']})" if t['dependencies'] else ""
        print(f"#{t['id']} [{t['status']}] {t['role']}: {t['title']} {deps}")
        if t["comments"]:
            print(f"   Last Comment: {t['comments'][-1]}")

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="cmd", required=True)
    
    subparsers.add_parser("list")
    
    create = subparsers.add_parser("create")
    create.add_argument("role", choices=["architect", "developer", "tester", "reviewer", "product_owner"])
    create.add_argument("title")
    create.add_argument("--deps", type=int, nargs="*", default=[])
    
    subparsers.add_parser("start").add_argument("id", type=int)
    
    submit = subparsers.add_parser("submit")
    submit.add_argument("id", type=int)
    submit.add_argument("--notes", default="")

    review = subparsers.add_parser("review")
    review.add_argument("id", type=int)
    review.add_argument("decision", choices=["approve", "reject"])
    review.add_argument("--notes", default="")
    
    args = parser.parse_args()
    
    if args.cmd == "list": list_tickets()
    elif args.cmd == "create": create_ticket(args.title, args.role, args.deps)
    elif args.cmd == "start": start_ticket(args.id)
    elif args.cmd == "submit": submit_ticket(args.id, args.notes)
    elif args.cmd == "review": review_ticket(args.id, args.decision, args.notes)

if __name__ == "__main__":
    main()
