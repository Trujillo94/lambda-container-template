--+-> .devcontainer                     # [Dir] Configuration to work with VScode & Docker
  |-> .vscode                           # [Dir] Vscode Debuging configuration
  |-> data                              # [Dir] Configuration files with static non-sensitive content
  |-> .logs                             # [Dir] Folder to store log files
  |-> logs                              # [Dir] Where logs will be stored, empty
  |-> src                               # [Dir] Code resources folder
  |   |-> config                        # [Dir] Environment variable loader/manager
  |   |   |-> __init__.py               # [File] Mandatory file to load .env files
  |   |   L-> [module_name].py          # [File] File to load the module environment variables
  |   |-> utils                         # [Dir] Contains utilities for the rest of the code
  |   |   L-> toolbox.py                # [File] File containing the most common utility functions used by the code
  |   |-> integrations                  # [Dir] Contains the integrations of modules/libraries with our project
  |   |   L-> [integration_name].py     # [File] Contains the code to integrate a module with our project, "the code here is specific to the project"
  |   L-> wrappers                      # [Dir] Contains wrappers to ease the utilization of modules in our code
  |   |   L-> db                        # [Dir] Contains all the wrappers for a certain module
  |   |   |   L-> connection.py         # [File] Contains the code to integrate a module with our project, "the code here is specific to the project"
  |   |   |   L-> controllers.py        # [File] Contains the code to integrate a module with our project, "the code here is specific to the project"
  |   |   |   L-> entities.py           # [File] Contains the code to integrate a module with our project, "the code here is specific to the project"
  |   |   L-> aws                       # [Dir] Contains all the wrappers for a certain module
  |   |   L-> [wrapper_name]            # [Dir] Contains all the wrappers for a certain module
  |   |       L> [wrapper_file].py      # [File] Code to ease a certain module utilization in our code, "the code here is project independent"
  |-> tests                             # [Dir] Contains files to perform testing
  |-> .gitignore                        # [File] Gitignore file
  |-> bitbucket-pipelines.yml           # [File] Bitbucket pipelines definition
  |-> Dockerfile                        # [File] Docker image build instructions
  |-> main.py                           # [File] Main file to be executed (lambda handler)
  |-> requirements.txt                  # [File] Pip requirements file