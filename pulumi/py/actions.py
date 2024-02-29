from port_pulumi import Action

def create_pulumi_bootstrap_action():
    return Action(
        resource_name="pulumi-action",
        identifier="pulumi-bootstrap-action",
        title="Pulumi Bootstrap",
        blueprint="service",
        description="A Pulumi bootstrapped action",
        user_properties={
            "string_props": {
                "name": {"title": "Name", "icon": "GitLab"},
                "language": {
                    "icon": "GitLab",
                    "title": "Language",
                    "type": "string",
                    "enums": ["python", "javascript"],
                },
                "namespace": {
                    "type": "string",
                    "format": "entity",
                    "blueprint": "namespace",
                    "required": True,
                },
                "SDK": {"depends_ons": ["language"]},
                "pythonRunArguments": {"visible_jq_query": '.form.language == "python"'},
                "nodeRunArguments": {"visible_jq_query": '.form.language == "javascript"'},
            },
        },
        trigger="DAY-2",
        webhook_method={"url": "https://myserver.com"},
    )

def create_budding_action():
    return Action(
        resource_name="bud-action",
        identifier="budding-action",
        title="Budding Action",
        blueprint="service",
        description="A budding Pulumi action",
        user_properties={
            "string_props": {
                "alwaysRequiredInput": {"type": "string"},
                "inputRequiredBasedOnData": {"type": "string"},
            },
        },
        required_jq_query='if .entity.properties.conditionBooleanProperty then ["alwaysRequiredInput", "inputRequiredBasedOnData"] else ["alwaysRequiredInput"] end',
        trigger="DAY-2",
        webhook_method={"url": "https://myserver.com"},
    )

# Create instances of the actions
pulumi_bootstrap_action = create_pulumi_bootstrap_action()
budding_action = create_budding_action()
