import glob
import re
import os
import hcl

STACK_ID_MAX_LENGTH = 22

# regex to validate the stack id doesn't have any whitespace, capital letters or underscores
stack_id_validator = re.compile('[A-Z\s\_]')

# regex to validate the region
region_validator = re.compile('(us(-gov)?|ap|ca|cn|eu|sa)-(central|(north|south)?(east|west)?)-?(1|2)')

file = glob.glob('Master_Definition/*/terraform.tfvars')

for f in file:
    with open(f, 'r') as fp:
        obj = hcl.load(fp)
        errors = []

        if 'region' not in obj:
            errors.append("The variable 'region' not defined")

        region = obj['region']
        if region_validator.search(region) is None:
            errors.append("Invalid Region")

        if 'project_name' not in obj:
            errors.append("Master name is not defined")

        stack_id = obj['project_name']
        if stack_id_validator.search(stack_id) is not None:
            errors.append("Invalid value for 'Master Node' - No uppercase characters, whitespace or underscores allowed")

        if len(stack_id) > STACK_ID_MAX_LENGTH:
            errors.append("'Master node's name' cannot be greater than {} characters long".format(STACK_ID_MAX_LENGTH))

        if 'master_instance_type' not in obj:
            errors.append("Instance type is not defned")

fp.close()

if len(errors) > 0:
    for error in errors:
        print(error)
    exit(1)
else:
    print("All the check passed!")
