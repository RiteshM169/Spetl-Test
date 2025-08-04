import frappe

def create_additional_kanban_boards():
    boards = [
        {
            "kanban_board_name": "Test Task Kanban",
            "reference_doctype": "Task",
            "field_name": "status",
            "filters": [["Task", "project", "=", "PROJ-0002"]],
            "columns": [
                ("Open", "Cyan", []),
                ("Working", "Light Blue", []),
                ("Pending Review", "Light Blue", []),
                ("Overdue", "Gray", []),
                ("Template", "Gray", []),
                ("Completed", "Gray", []),
                ("Cancelled", "Gray", [])
            ]
        },
        {
            "kanban_board_name": "test kanban",
            "reference_doctype": "Opportunity",
            "field_name": "custom_test_spetl_kanban",
            "filters": None,
            "columns": [
                ("Spetl", "Gray", ["CRM-OPP-2025-00003"]),
                ("ICVR", "Gray", ["CRM-OPP-2025-00002"]),
                ("Company", "Gray", ["CRM-OPP-2025-00001"])
            ]
        }
    ]

    for board in boards:
        name = board["kanban_board_name"]
        if frappe.db.exists("Kanban Board", name):
            frappe.logger().info(f"Kanban board '{name}' already exists. Skipping.")
            continue

        if not frappe.db.has_column(board["reference_doctype"], board["field_name"]):
            frappe.logger().warning(
                f"Field '{board['field_name']}' not found in {board['reference_doctype']}. Skipping board '{name}'"
            )
            continue

        kanban_doc = frappe.get_doc({
            "doctype": "Kanban Board",
            "kanban_board_name": name,
            "reference_doctype": board["reference_doctype"],
            "field_name": board["field_name"],
            "filters": frappe.as_json(board["filters"]) if board["filters"] else None,
            "columns": [
                {
                    "column_name": col_name,
                    "indicator": color,
                    "order": frappe.as_json(order)
                }
                for col_name, color, order in board["columns"]
            ]
        })

        kanban_doc.insert(ignore_permissions=True)
        frappe.logger().info(f"✅ Created Kanban board: {name}")
