# CAB432_A2

## Assigned Tasks

### Michael
- [x] Data Persistence Services: S3 (3 marks)
- [x] Data Persistence Services: DynamoDB (3 marks)
- [ ] Statelessness (3 marks)

### Chris
- [x] DNS with Route53 (2 marks)
- [x] Secrets manager (2 marks)
- [ ] Infrastructure as Code (3 marks)
- [x] Authentication with Cognito (3 marks)

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
1. Create a new EC2 instance using the launch template 'A2_11'
2. Create these files in `gifmakerapi/`
    1. `app.py`
    2. `Dockerfile`
    3. `requirements.txt`
    4. Everything in `gma_code/` (directories already created)
3. Run `docker build -t gif-api .` in `gifmakerapi/`


4. Run `docker run --name gif-api -p 3000:3000 gif-api`

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
