import json
import pulumi
from port_pulumi import Page, PagePermissions
from utils import ComplexEncoder

# Placeholder for base blueprint creation (if you have its definition)
base_blueprint = "service"


# Widget Helper Functions
def generate_widget_id(title, widget_type):
    base_id = title.lower().replace(" ", "_")
    return f"{base_id}_{widget_type}"


def create_markdown_widget(title, description, markdown_content):
    widget_id = generate_widget_id(title, "markdown")
    return {
        "title": title,
        "icon": "BlankPage",
        "markdown": markdown_content,
        "type": "markdown",
        "description": description,
        "id": widget_id,
    }


def create_table_explorer_widget(title, dataset=None):
    widget_id = generate_widget_id(title, "table-entities-explorer")
    return {
        "title": title,
        "type": "table-entities-explorer",
        "dataset": dataset
        or {
            "combinator": "and",
            "rules": [
                {"operator": "=", "property": "$blueprint", "value": "{{blueprint}}"}
            ],
        },
        "id": widget_id,
    }


def create_entities_pie_chart_widget(title, dataset, property):
    widget_id = generate_widget_id(title, "entities-pie-chart")
    return {
        "title": title,
        "icon": "PieChart",  # Or another suitable icon
        "type": "entities-pie-chart",
        "dataset": dataset,
        "property": property,
        "id": widget_id,
    }


def create_iframe_widget(title, url, url_type="public", description=""):
    widget_id = generate_widget_id(title, "iframe-widget")
    return {
        "title": title,
        "description": description,
        "icon": "Code",
        "urlType": url_type,
        "url": url,
        "type": "iframe-widget",
        "id": widget_id,
    }


def create_entities_number_chart_widget(title, dataset, func, measure_time_by):
    widget_id = generate_widget_id(title, "entities-number-chart")
    return {
        "title": title,
        "type": "entities-number-chart",
        "icon": "Calculator",  # Or a suitable icon
        "dataset": dataset,
        "func": func,
        "measureTimeBy": measure_time_by,
        # ... other properties as needed
        "id": widget_id,
    }


# Sample Datasets (Adjust these as needed)
def use_dataset(blueprint_id):
    return {  # Directly return the dataset
        "combinator": "and",
        "rules": [{"operator": "=", "property": "$blueprint", "value": blueprint_id}],
    }


table_view = json.dumps(
    {
        "id": "microservice-table-entities",
        "type": "table-entities-explorer",
        "dataset": {
            "combinator": "and",
            "rules": [
                {"operator": "=", "property": "$blueprint", "value": "{{blueprint}}"}
            ],
        },
    }
)

table2_view = json.dumps(
    {
        "id": "microservice-table-items",
        "type": "table-entities-explorer",
        "dataset": {
            "combinator": "and",
            "rules": [
                {"operator": "=", "property": "$blueprint", "value": "{{blueprint}}"}
            ],
        },
    }
)

# Create the Microservices Page
microservice_blueprint_page = Page(
    "microservice_blueprint_page",
    identifier="microservice_blueprint_page",
    title="Microservices",
    type="blueprint-entities",
    icon="Microservice",
    blueprint=base_blueprint,
    widgets=[table_view],
)

dashboard_widget = json.dumps(
    {  # JSON string for the widgets configuration
        "id": "dashboardWidget",
        "layout": [
            {"height": 400, "columns": [{"id": "microserviceGuide", "size": 12}]}
        ],
        "type": "dashboard-widget",
        "widgets": [
            {
                "title": "Microservices Guide",
                "icon": "BlankPage",
                "markdown": "# This is the new Microservice Dashboard",
                "type": "markdown",
                "description": "A helpful overview of our microservices",
                "id": "microserviceGuide",
            },
        ],
    }
)

piechart_widget = json.dumps(
    {
        "icon": "Service",
        "type": "entities-pie-chart",
        "description": "",
        "title": "Languages",
        "dataset": {
            "combinator": "and",
            "rules": [{"operator": "=", "value": "service", "property": "$blueprint"}],
        },
        "property": "property#language",
        "id": "languages",
    }
)

# Create the Microservices Dashboard Page
microservice_dashboard_page = Page(
    "microservice_dashboard_page",
    identifier="microservice_dashboard_page",
    title="Microservices",
    icon="GitHub",
    type="dashboard",
    after="microservice_blueprint_page",  # Using a Pulumi reference
    widgets=[dashboard_widget, table2_view],
)

# Allow read access to all admins and a specific user and team:
microservices_permissions = PagePermissions(
    "microservices_permissions",
    page_identifier="microservice_blueprint_page",
    read={
        "roles": [
            "Admin",
        ],
        "users": ["phalbert20@gmail.com"],
        "teams": ["Cognizant"],
    },
)

# get an existing object
# existing_permissions = PagePermissions.get("microservices_permissions", "microservice_blueprint_page")
# Access properties of the retrieved resource
# print(existing_permissions.read)

# existing_page = Page.get("microservice_blueprint_page", "microservice_blueprint_page")

# def collect_and_print_outputs(outputs):
#     for key, value in outputs.items():
#         if isinstance(value, pulumi.Output):
#             value.apply(lambda val: print(f"{key}: {val}"))
#         else:
#             print(f"{key}: {value}")

# pulumi.Output.all(existing_page).apply(collect_and_print_outputs)
