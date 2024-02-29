from port_pulumi import Entity, EntityPropertiesArgs

create_repo = Entity(
    "arepo",
    identifier="arepo",
    title="A Repository",
    blueprint="service",
    properties=EntityPropertiesArgs(string_props={"language": "Python"}),
    relations={},
)
