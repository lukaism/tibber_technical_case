def parse_env_variable(variable):
    variable = variable.replace("'", "")
    variable = variable.replace('"', "")
    return variable
