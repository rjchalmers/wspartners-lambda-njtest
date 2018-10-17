.PHONY: clean build test release

# PLEASE CHANGE THE FOLLOWING FOR YOUR COMPONENT
COMPONENT="cosmos-component-name-goes-here"

test:
	# Install all dependencies for test, including devDependencies
	npm install --prefix src --no-bin-links
	# Run the tests in a centos7 mock environment for access to a newer version of node
	# and to more closely mimic the target environment
	mock-run --os 7 --install "npm" --copyin src src --shell "npm test --prefix src"

clean:
	rm -rf src/node_modules package.zip

# NB: We don't need the aws-sdk package in the ZIP we're creating - it's automatically provided by AWS Lambda
# Removing it saves us a couple of MB per deployment!

build:
	mock-run --os 7 \
		--install "npm" \
		--copyin src src \
		--shell 'npm install --prefix src && rm -r src/node_modules/aws-sdk && zip -9 -r package.zip src' \
		--copyout package.zip package.zip

release: clean build
	cosmos-release lambda --lambda-version=${BUILD_NUMBER} "./package.zip" $(COMPONENT)
