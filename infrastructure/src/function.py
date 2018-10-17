import troposphere as tp
from troposphere import Ref, Parameter, GetAtt
from troposphere.awslambda import Function, Code, Alias
from troposphere.iam import PolicyType, Role
from awacs.aws import Allow, Statement, Principal, Policy
from awacs.sts import AssumeRole

t = tp.Template()

handler = t.add_parameter(Parameter(
    "LambdaHandler",
    Type="String",
    Default="handler",
    Description="The name of the function (within your source code) "
                "that Lambda calls to start running your code."
))

memory_size = t.add_parameter(Parameter(
    "LambdaMemorySize",
    Type="Number",
    Description="The amount of memory, in MB, that is allocated to "
                "your Lambda function."
))

timeout = t.add_parameter(Parameter(
    "LambdaTimeout",
    Type="Number",
    Default="15",
    Description="The function execution time (in seconds) after which "
                "Lambda terminates the function. "
))

env = t.add_parameter(Parameter(
    "LambdaEnv",
    Default="test",
    Description="Environment this lambda represents - used for alias name",
    Type="String",
))

function_role = t.add_resource(
    Role(
        "FunctionRole",
        AssumeRolePolicyDocument=Policy(
            Statement=[
                Statement(
                    Effect=Allow,
                    Action=[AssumeRole],
                    Principal=Principal(
                        "Service", ["lambda.amazonaws.com"]
                    )
                )
            ]
        )
    )
)

aws_lambda = t.add_resource(
    Function(
        "LambdaFunction",
        Code=Code(
            ZipFile="exports.handler = function(event,context){}"
        ),
        Description="A function template",
        Handler=Ref(handler),
        MemorySize=Ref(memory_size),
        Role=GetAtt(function_role, "Arn"),
        Runtime="nodejs8.10",
        Timeout=Ref(timeout)

    )
)

function_policy = t.add_resource(
    PolicyType(
        "FunctionPolicy",
        PolicyDocument={
            "Id": "FunctionPolicy",
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Action": [
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents"
                ],
                "Resource": ["arn:aws:logs:*:*:*"]
            }]
        },
        PolicyName="function-policy",
        Roles=[Ref(function_role)]
    )
)

alias = t.add_resource(Alias(
    "LambdaAlias",
    Description="Cosmos Alias",
    FunctionName=Ref(aws_lambda),
    FunctionVersion="$LATEST",
    Name=Ref(env)
))

print(t.to_json())
