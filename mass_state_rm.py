#!/usr/bin/env python3

"""
This application aids in the mass-removal of Terraform resources from state. Currently, this
application only supports the mass-removal of resources of a given resource type, i.e. removing
multiple aws_route53_records all at once. This tool assumes that you have set up the AWS CLI and,
if managing remote state, that you have the necessary permissions to access the Terraform state 
buckets and DynamoDB tables through the CLI.

These are destructive actions, so please use this at your own risk. The author claims no 
responsibility for any harm done through the use of this script.

Copyright, Senna Lang (Aeternitaas on Github)
"""

import os

def get_resources():
    print("Welcome to the Mass-State Remover tool.")
    resources_raw = input("Please enter the resources you wish to remove, delimited by spaces:")
    resources = resources_raw.rstrip().split(" ")
    return resources

def get_resource_type():
    resource_type = input("Which type of resource is this (e.g. aws_route53_record):").rstrip()
    return resource_type

def fmt_resources(resources, resource_type):
    fmt_resources = ""

    for resource in resources:
        fmt_resources += (resource_type + "." + resource + " ")

    return fmt_resources

def init_terraform():
    os.system("echo \" -------------------------------- \"")
    os.system("echo \" --> Running \`terraform init\` <-- \"")
    os.system("terraform init")
    return

def rm_resources_terraform(fmtted_resources):
    print("Removing the following items, do you consent? (Y/N)")
    print(fmtted_resources.replace(' ', '\n'))

    if input() in ["Y", "y"]:
        os.system("terraform state rm " + fmtted_resources)
    else:
        print("Exiting.")
        return

if __name__ == "__main__":
    resources = get_resources()
    resource_type = get_resource_type()
    
    init_terraform()
    fmtted_resources = fmt_resources(resources, resource_type)
    rm_resources_terraform(fmtted_resources)
