"""A Python Pulumi program"""

import pulumi
from port_pulumi import Entity, EntityPropertiesArgs, Action, ActionUserPropertiesArgs

entity = Entity(
    "arepo",
    identifier="arepo",
    title="A Repository",
    blueprint="service",
    properties=EntityPropertiesArgs(string_props={"language": "Python"}),
    relations={},
)

action = Action(
    "an-pulumi-action",
    identifier="pulumi-action",
    title="A Pulumi Act",
    blueprint="service",
    description="A pulumi bootstraped action",
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
                # "dataset": {
                #     "combinator": "and",
                #     "rules": [
                #         {
                #             "property": "$team",
                #             "operator": "containsAny",
                #             "value": "value here. this can also be a 'jqQuery' object",
                #         }
                #     ],
                # },
            },
            "SDK": {"depends_ons": ["language"]},
            "pythonRunArguments": {"visible_jq_query": '.form.language == "python"'},
            "nodeRunArguments": {"visible_jq_query": '.form.language == "javascript"'},
        },
    },
    trigger="DAY-2",
    webhook_method={"url": "https://myserver.com"},
)

action2 = Action(
    "budding-action",
    identifier="budding-action",
    title="A Budding Act",
    blueprint="service",
    description="A pulumi budding action",
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

pulumi.export("name", entity.title)
pulumi.export("name", action.title)
pulumi.export("name", action2.title)
