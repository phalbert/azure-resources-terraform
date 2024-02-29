/* eslint-disable max-len */
import {
    Action, ActionArgs, Blueprint, Provider,
} from '@port-labs/port';
interface Parameters {
    provider: Provider,
    microservice: Blueprint,
    tribe: Blueprint,
    account: Blueprint,
    webhookMethodUrl: string,
    identifier?: string,
    user: Blueprint,
}

function createMicroserviceAction({
    provider,
    microservice,
    tribe,
    account,
    webhookMethodUrl,
    identifier = 'createService',
    user,
}: Parameters): Action {
    const args: ActionArgs = {
        identifier,
        title: 'Create Project',
        icon: 'Package',
        userProperties: {
            stringProps: {
                BT_TRIBE: {
                    title: 'Tribe',
                    format: 'entity',
                    blueprint: tribe.identifier,
                    description: 'The tribe that this project is being created for',
                },
                BT_GROUP_ID: {
                    title: 'Sub Group',
                    format: 'entity',
                    blueprint: account.identifier,
                    description: 'The sub group of the tribe that this project is being created for',
                    dataset: {
                        combinator: 'and',
                        rules: [
                            {
                                operator: 'relatedTo',
                                blueprint: 'tribe',
                                value: {
                                    jqQuery: '.form.BT_TRIBE.identifier',
                                },
                            },
                        ],
                    },
                },
                BT_APP_TYPE: {
                    title: 'BT APP Type',
                    description: 'The application type for the project',
                    pattern: '^[A-Za-z_][A-Za-z0-9@_-]*$',
                    enums: [
                        'node-lambda-microservice',
                        'java-lambda-microservice',
                        'node-eks-microservice',
                        'java-eks-microservice',
                        'generic-cloud-resource',
                        'shared-api-gateway',
                        'node-static-site',
                    ],
                },
                SHARED_API_GATEWAY_PROJECT_NAME: {
                    title: 'Select Shared API Gateway Project',
                    blueprint: microservice.identifier,
                    format: 'entity',
                    dataset: {
                        combinator: 'and',
                        rules: [
                            {
                                property: 'projectType',
                                operator: '=',
                                value: {
                                    jqQuery: '"shared-api-gateway"',
                                },
                            },
                            {
                                property: 'tribe',
                                operator: '=',
                                value: {
                                    jqQuery: '.form.BT_TRIBE.identifier',
                                },
                            },
                        ],
                    },
                    visibleJqQuery: '.form.ENABLE_SHARED_API_GATEWAY',
                },
                STATIC_SITE_CLOUDFRONT_DISTRIBUTION: {
                    title: 'Select Cloudfront Distribution for Static Site',
                    description: 'The Cloudfront Distribution to use for this static site',
                    default: 'business-bt-com-shared-cloudfront',
                    enums: [
                        'business-bt-com-shared-cloudfront',
                        'Create new un-shared distribution',
                    ],
                    visibleJqQuery: '.form.BT_APP_TYPE | IN("node-static-site")',
                },
                BT_PROJECT_NAME: {
                    title: 'Project Name',
                    description: 'The name of the project being created',
                    pattern: '^[A-Za-z_][A-Za-z0-9@_-]*$',
                },
                BT_PROJECT_DESCRIPTION: {
                    title: 'Project Description',
                    description: 'The description of the project being created',
                },
                BT_TEAM_NAME: {
                    title: 'Owning Team',
                    description: 'The team that owns the project being created',
                    enumJqQuery: '.user.teams | map(.name | select(contains("Approvers") | not))',
                },
                BT_APP_ID: {
                    title: 'EDR APPID',
                    pattern: '^APP[0-9]{5}$',
                    description: 'The App ID for the project being created',
                },
            },
            arrayProps: {
                BT_APPROVERS: {
                    title: 'Approvers',
                    description: 'The email addresses of the people who can approve edits to the project being created',
                    stringItems: {
                        blueprint: user.identifier,
                        format: 'entity',
                    },
                    dataset: {
                        combinator: 'and',
                        rules: [
                            {
                                blueprint: 'team',
                                operator: 'relatedTo',
                                value: {
                                    jqQuery: '.form.BT_TEAM_NAME.identifier',
                                },
                            },
                        ],
                    },
                },
                BT_CODE_OWNERS: {
                    title: 'Code Owners',
                    description: 'The email addresses of the code owners of the project being created',
                    stringItems: {
                        blueprint: user.identifier,
                        format: 'entity',
                    },
                    dataset: {
                        combinator: 'and',
                        rules: [
                            {
                                blueprint: 'team',
                                operator: 'relatedTo',
                                value: {
                                    jqQuery: '.form.BT_TEAM_NAME.identifier',
                                },
                            },
                        ],
                    },
                },
            },
            booleanProps: {
                BT_POC: {
                    title: 'BT POC',
                    description: 'The BT POC flag used to clean up this project after 7 days',
                    default: false,
                },
                ENABLE_SHARED_API_GATEWAY: {
                    title: 'Enable Shared API Gateway',
                    description: 'Use a shared API Gateway Project',
                    default: false,
                    visibleJqQuery: '.form.BT_APP_TYPE | IN("node-lambda-microservice", "java-lambda-microservice")',
                },
                ENABLE_DYNATRACE_MONITORING: {
                    title: 'Enable Dynatrace monitoring',
                    description: 'Choice of whether to allow Dynatrace within the project being created',
                    default: true,
                    dependsOns: [
                        'BT_POC',
                    ],
                },
                ENABLE_PUBLIC_ACCESS: {
                    title: 'Enable public access',
                    description: 'Choice of whether to allow public access within the project being created',
                    default: true,
                    visibleJqQuery: '.form.BT_APP_TYPE | IN("node-eks-microservice", "java-eks-microservice")',
                    dependsOns: ['BT_APP_TYPE'],
                },
            },
        },
        orderProperties: [
            'BT_TRIBE',
            'BT_GROUP_ID',
            'BT_APP_TYPE',
            'ENABLE_SHARED_API_GATEWAY',
            'SHARED_API_GATEWAY_PROJECT_NAME',
            'BT_PROJECT_NAME',
            'BT_PROJECT_DESCRIPTION',
            'BT_TEAM_NAME',
            'BT_APP_ID',
            'BT_APPROVERS',
            'BT_CODE_OWNERS',
            'BT_POC',
            'ENABLE_DYNATRACE_MONITORING',
            'ENABLE_PUBLIC_ACCESS',
            'STATIC_SITE_CLOUDFRONT_DISTRIBUTION',
        ],
        blueprint: microservice.identifier,
        trigger: 'CREATE',
        webhookMethod: {
            url: webhookMethodUrl,
            agent: false,
        },
        requiredJqQuery: 'if .form.ENABLE_SHARED_API_GATEWAY then ["SHARED_API_GATEWAY_PROJECT_NAME", "BT_TRIBE", "BT_GROUP_ID", "BT_APP_TYPE", "BT_PROJECT_NAME", "BT_PROJECT_DESCRIPTION", "BT_TEAM_NAME", "BT_APPROVERS", "BT_CODE_OWNERS", "ENABLE_DYNATRACE_MONITORING"] else [ "BT_TRIBE", "BT_GROUP_ID", "BT_APP_TYPE", "BT_PROJECT_NAME", "BT_PROJECT_DESCRIPTION", "BT_TEAM_NAME", "BT_APPROVERS", "BT_CODE_OWNERS", "ENABLE_DYNATRACE_MONITORING"] end',
        // eslint-disable-next-line max-len
        description: 'Quickly and easily set up the foundation for a new service. Get a pre-configured starting point that is ready for you to begin building upon',
    };
    return new Action(
        identifier,
        args,
        {
            provider,
            dependsOn: [
                microservice,
                tribe,
                account,
            ],
        },
    );
}


function createSampleAction({
    identifier = 'createRunningService',
}: any): Action {
    const args: ActionArgs = {
        identifier: identifier,
        title: "Deploy running service to a cluster",
        icon: "Cluster",
        blueprint: "service",
        userProperties: {
            stringProps: {
                "service": {
                    "format": "entity",
                    "blueprint": "service",
                    "required": true,
                    "dataset": {
                        "combinator": "and",
                        "rules": [
                            {
                                // "property": "$team",
                                "blueprint": "{{blueprint}}",
                                "operator": "=",
                                "value": {
                                    "jqQuery": ".title"
                                }
                            }
                        ]
                    },
                    "title": "Service"
                }
            }
        },
        trigger: "CREATE",
        description: "This will deploy a running service to a cluster",
        webhookMethod: {
            "url": "https://example.com"
        },
    }

    return new Action(
        identifier,
        args,
    );
}

const sampleAction = createSampleAction("createRunningService");

export {
    sampleAction
}