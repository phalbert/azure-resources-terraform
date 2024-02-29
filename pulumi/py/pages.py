import json
from port_pulumi import Page


# Widget Helper Functions
def generate_widget_id(title, widget_type):
    """
    Generates a unique widget ID based on the title and widget type.

    Args:
        title (str): The title of the widget.
        widget_type (str): The type of the widget (e.g., "markdown", "table-entities-explorer").

    Returns:
        str: The generated widget ID, e.g., "microservicesGuideMarkdown".
    """
    # Convert title to camelCase
    title_words = title.split()
    camel_case_title = title_words[0].lower() + "".join(
        word.capitalize() for word in title_words[1:]
    )

    # Combine camelCase title and widget type
    base_id = f"{camel_case_title}{widget_type.capitalize()}"

    # Ensure the length does not exceed the limit
    max_length = len("QlUwO3VRBMQ3HjdH")
    return base_id[:max_length]


def create_markdown_widget(title, description, markdown_content):
    """
    Creates a markdown widget configuration.

    Args:
        title (str): The title of the widget.
        subtitle (str): The subtitle of the markdown content.
        description (str): A description for the widget.

    Returns:
        tuple: A tuple containing:
            * widget_config (dict): The widget configuration dictionary.
            * widget_id (str): The generated widget ID.
    """
    widget_id = generate_widget_id(title, "markdown")
    widget_config = {
        "title": title,
        "icon": "BlankPage",
        "markdown": markdown_content,
        "type": "markdown",
        "description": description,
        "id": widget_id,
    }
    return widget_config, widget_id


def create_table_explorer_widget(title, dataset, excludedFields=["properties.readme"]):
    widget_id = generate_widget_id(title, "table-entities-explorer")
    widget_config = {
        "displayMode": "widget",
        "title": title,
        "type": "table-entities-explorer",
        "dataset": dataset,
        "id": widget_id,
        "excludedFields": excludedFields,
    }
    return widget_config, widget_id


def create_entities_pie_chart_widget(title, dataset, property):
    widget_id = generate_widget_id(title, "entities-pie-chart")
    widget_config = {
        "title": title,
        "icon": "PieChart",
        "type": "entities-pie-chart",
        "dataset": dataset,
        "property": property,
        "id": widget_id,
    }
    return widget_config, widget_id


def create_iframe_widget(title, url, url_type="public", description=""):
    widget_id = generate_widget_id(title, "iframe-widget")
    widget_config = {
        "title": title,
        "description": description,
        "icon": "Code",
        "urlType": url_type,
        "url": url,
        "type": "iframe-widget",
        "id": widget_id,
    }
    return widget_config, widget_id


def create_entities_number_chart_widget(
    title,
    blueprint_id,
    dataset=[],
    func="average",
    measure_time_by="$createdAt",
    averageOf="day",
    description="",
):
    """
    Creates an entities number chart widget configuration.

    Args:
      title (str):  The title of the widget.
      dataset:  The dataset for the widget.
      func (str, optional): The aggregation function to use. Options: "average", "count", "sum". Defaults to "average".
      measure_time_by (str, optional): The property to use for time-based aggregations. Defaults to "$createdAt".
      averageOf (str, optional): The time period for averaging. Options: "day", "week", "month". Defaults to "day".
      description (str, optional): A description for the widget.

    Returns:
      tuple: A tuple containing the widget configuration dictionary and its ID.
    """

    widget_id = generate_widget_id(title, "entities-number-chart")
    widget_config = {
        "blueprint": blueprint_id,
        "calculationBy": "entities",
        "title": title,
        "description": description,
        "type": "entities-number-chart",
        "icon": "Calculator",
        "dataset": dataset,
        "func": func,
        "measureTimeBy": measure_time_by,
        "averageOf": averageOf,
        "unit": "custom",
        "unitCustom": "per day",
        "id": widget_id,
    }
    return widget_config, widget_id


# Other helper functions
def read_markdown_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        markdown_content = file.read()
        return markdown_content

def use_dataset(blueprint_id):
    """
    Creates a dataset configuration that filters entities based on the provided blueprint ID.

    Args:
        blueprint_id (str): The ID of the blueprint to filter for.

    Returns:
        dict: The dataset configuration dictionary.
    """
    return {  # Directly return the dataset
        "combinator": "and",
        "rules": [{"operator": "=", "value": blueprint_id, "property": "$blueprint"}],
    }


# Sample Datasets
services_dataset = use_dataset("service")
github_pr_dataset = use_dataset("githubPullRequest")  # Example for the PRs widget

file_path = "microservices.md"  # Replace with the path to your Markdown file
markdown_content = read_markdown_file(file_path)

# Widget Creation (with IDs); we use the IDs to define the layout of the dashboard
markdown_config, markdown_id = create_markdown_widget(
    title="Service Guide",
    description="Services are typically organized around business capabilities. Each service is often owned by a single, small team.",
    markdown_content=markdown_content,
)

pie_chart_config, pie_chart_id = create_entities_pie_chart_widget(
    title="Languages", dataset=services_dataset, property="property#language"
)
table_config, table_id = create_table_explorer_widget(
    title="Services", dataset=services_dataset, excludedFields=["properties.readme", "properties.slack"],
)
quote_config, quote_id = create_iframe_widget(
    title="Quote of the Day", url="https://kwize.com/quote-of-the-day/embed/&txt=0"
)
pr_chart_config, pr_chart_id = create_entities_number_chart_widget(
    title="Avg Pull Requests",
    blueprint_id="githubPullRequest",
    description="Hpw many PRs do we open daily",
)

# Dashboard Layout Definition
dashboard_layout = {
    "id": "myDashboardWidget",  # This is optional, as Port can auto-generate IDs
    "type": "dashboard-widget",
    "layout": [
        {
            "columns": [
                {"id": markdown_id, "size": 6},
                {"id": pie_chart_id, "size": 6},
            ],
            "height": 400,
        },
        {
            "height": 400,
            "columns": [
                {"id": quote_id, "size": 6},
                {"id": pr_chart_id, "size": 6},
            ],
        },
        {"height": 400, "columns": [{"id": table_id, "size": 12}]},
    ],
}

widgets_config = {
    **dashboard_layout,  # Embed the layout structure
    "widgets": [
        markdown_config,
        pie_chart_config,
        quote_config,
        pr_chart_config,
        table_config
    ],
}

print(widgets_config)

# Page Creation
microservice_dashboard_page = Page(
    "microservice-overview-page-resource",
    identifier="microservice_overview_page",
    title="Microservices Dashboard",
    icon="Microservice",
    type="dashboard",
    widgets=[json.dumps(widgets_config)],
)

catalog_page_widgets = {
    "identifier": "our_services",
    "title": "Our Services",
    "blueprint": "service",
    "icon": "Airflow",
    "type": "blueprint-entities",
    "widgets": [
        {
            "id": "46bf2483-97b7-4c6f-88fb-8987c9875d98",
            "type": "table-entities-explorer",
            "excludedFields": ["properties.readme", "properties.slack"],
            "dataset": {
                "combinator": "and",
                "rules": [
                    {
                        "operator": "=",
                        "property": "$blueprint",
                        "value": "{{blueprint}}",
                    }
                ],
            },
        }
    ],
}

catalog_widget, catalog_widgets_id = create_table_explorer_widget(
    title="Services",
    dataset=services_dataset,
    excludedFields=["properties.readme", "properties.slack"],
)

print(catalog_widget)

catalog_page = Page(
    "my-catalog-page-resource",
    identifier="my_catalog_page",
    title="Our Services",
    blueprint="service",
    icon="Microservice",
    type="blueprint-entities",
    widgets=[
        json.dumps(
            {
                "displayMode": "widget",
                "title": "Services",
                "type": "table-entities-explorer",
                "dataset": {
                    "combinator": "and",
                    "rules": [
                        {"operator": "=", "value": "service", "property": "$blueprint"}
                    ],
                },
                "id": "servicesTable-en",
                "excludedFields": ["properties.readme", "properties.slack"],
            }
        )
    ],
)
