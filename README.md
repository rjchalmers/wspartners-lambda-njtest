# Overview
This is a sample Node.js lambda setup containing Cloudformation stacks for creating the lambda function and Makefile with targets for building and releasing the package to Cosmos.

# How to build the infrastructure
The Cloudformation templates are defined in python using troposphere in `infrastructure/src/*.py`. You can modify them whichever way you like and then recompile them running:
```
$ cd infrastructure
$ make all
```
Then use the templates under `infrastructure/templates/*.json` and build the stacks in your corresponding accounts.

# How to build the lambda package
In order to build the lambda package simply run:
```
$ make build
```

This will create a clean centos 7 environment, install npm, run `npm install` to grab any external dependencies, then zip the result and put it in `./package.zip`

## Why did it delete the AWS SDK?! I need that!
The AWS Lambda environment automatically provides the AWS SDK - you can add it as a dependency while developing and testing but adding it to the lambda is probably not needed. This saves you a couple of MB on your lambda package!

# How to release the package
In order to build and release the lambda package simply run:
```
$ make release
```

This will build the package running the target above and then use the `cosmos-release` tool to upload the package to the BBC lambda repository and post the release metadata to cosmos so you can deploy, provided you've given the `BUILD_NUMBER` environment variable.

If you want to autogenerate build nubmers, consider using the `cosmos-release generate-version ${COMPONENT_NAME}` command.
