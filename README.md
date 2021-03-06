
# Welcome to your PDCA Serverless CDK Python project!

This is a PDCA serverless project for Python development with CDK.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the .env
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .env
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .env/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .env\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

Besides python, you also need to have node.js installed, because cdk is a node.js based application

consider using nvm https://github.com/nvm-sh/nvm for node.js installation and version management


Once node is installed, install cdk locally using

```
npm i
```

You also need to have aws credentials (token and secret) configured locally


After activating your environment, execute

```
aws configure
```

and provide aws credentials, provided to you by PDCA support personnel.

At this point you can now synthesize the CloudFormation template for this code.

```
$ npx cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `npx cdk ls`          list all stacks in the app
 * `npx cdk synth`       emits the synthesized CloudFormation template
 * `npx cdk deploy`      deploy this stack to your default AWS account/region
 * `npx cdk diff`        compare deployed stack with current state
 * `npx cdk docs`        open CDK documentation

Enjoy!
