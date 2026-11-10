# GIF Maker API
*Create gifs from images!*

Using GIF Maker API, you can now convert your images to gifs easily and efficiently.
Features:
- Upload images
- Convert images to customised gifs
- Retrieve data related to images and gifs
- Download gifs or upload to GIPHY

## CAB432 Assignment Specifications
> This unit has three assessments which together form a single project implementing a web application on a cloud platform using cloud services and architecture. Each assessment represents a stage in the deployment of the application using increasingly sophisticated cloud services and architectures:
> 
> 1. REST API project: Implement and deploy a monolithic web application to a cloud virtual machine using a container
> 
> 2. Cloud Services Exercises: Use cloud services for persistence to make your application stateless, along with other cloud services to improve functionality (eg. user login services)
>
> 3. Cloud application: Use a microservice based cloud architecture together with cloud communication services to make your application modular and scalable

## Helpful Info
### How to login to AWS

1. Download the AWS CLI (already installed on EC2 launch template 'A2_11')
2. Run `aws configure sso  --use-device-code` with these details:
```
SSO session name (Recommended): default
SSO start URL [None]: https://d-97671c4bd0.awsapps.com/start/#/
SSO region [None]: ap-southeast-2
SSO registration scopes [sso:account:access]: sso:account:access
CLI default client Region [None]: ap-southeast-2
CLI default output format [None]:
CLI profile name [CAB432-STUDENT-901444280953]: default
```

3. If already configured AWS CLI can just use `aws sso login`

### How to test the program
1. Run the main program either in VS Code or EC2 (AWS login required)
2. Open `testing/` in VS Code in a new window
3. In `Python_Testing_Collection.py`, assign variable `API_HOST` to the URL (eg. `localhost` if testing locally)
4. Change to 'cli_interface.py', and run file - follow prompts provided

### How to build the Docker Image on EC2
#### Main App Microservice
1. Create a new EC2 instance using the launch template 'A2_11'
2. Create these files in `gifmakerapi/`
    1. `app.py`
    2. `Dockerfile`
    3. `requirements.txt`
    4. Everything in `gma_code/` (directories already created)
3. Run `docker build -t gif-api .` in `gifmakerapi/`
4. Run `docker run --name gif-api -p 3000:3000 gif-api`

#### Gif Conversion Microservice
1. Create a new EC2 instance using the launch template 'A2_11'
2. Create these files in a new directory `gif_conversion/`
    1. `app.py`
    2. `Dockerfile`
    3. `requirements.txt`
    4. Everything in `gc_code/`
3. Run `docker build -t gif_conversion .` in `gif_conversion/`
4. Run `docker run --name gif_conversion -p 3000:3000 gif_conversion`

ctrl + c to exit.

### Storing on ECR
-Should we make a new ECR repo?
#### Login 
Run `aws ecr get-login-password --region ap-southeast-2 | docker login --username AWS --password-stdin 901444280953.dkr.ecr.ap-southeast-2.amazonaws.com`
   
#### Push
Tag if not already tagged:
`docker tag {image id} 901444280953.dkr.ecr.ap-southeast-2.amazonaws.com/n11963131-assignment-1-0.0.1:gif-api`

`docker push 901444280953.dkr.ecr.ap-southeast-2.amazonaws.com/n11963131-assignment-1-0.0.1:gif-api`
#### Pull
`docker pull 901444280953.dkr.ecr.ap-southeast-2.amazonaws.com/n11963131-assignment-1-0.0.1:gif-api`
