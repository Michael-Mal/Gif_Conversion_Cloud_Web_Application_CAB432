# CAB432_A2

## Assigned Tasks

### Michael
- Data Persistence Services: S3 (3 marks)
- Data Persistence Services: DynamoDB (3 marks)

### Icemonk
- DNS with Route53 (2 marks)
- Secrets manager (2 marks)
- Infrastructure as Code (3 marks)

## Helpful Info

### How to test the program
1. Run the main program either in VS Code or EC2
2. Open `load_testing_script/` in VS Code in a new window
3. In `api-requests.py`, assign variable `url_name` to the URL (eg. `localhost` if testing locally)
4. Uncomment the function calls you want to test, and then run the program. Hopefully everything is kind of self-explanatory.
5. After I run a test, I like to delete the `uns_data/` directory (in the main program) so that I can run another test without getting errors saying the file already exists.

### How to build the Docker Image on EC2
-I will create a launch template to make it easier for us.
#### Files to include
- 'app.py'
- 'Dockerfile'
- 'requirements.txt'
- Everything in /gm_code/
#### Commands
`docker build -t gif-api .`

`docker run --name gif-api -p 3000:3000 gif-api`

ctrl + c to exit.

### Storing on ECR
-Should we make a new ECR repo?
#### Login 
`aws ecr get-login-password --region ap-southeast-2 | docker login --username AWS --password-stdin 901444280953.dkr.ecr.ap-southeast-2.amazonaws.com`
#### Push
Tag if not already tagged:
`docker tag {image id} 901444280953.dkr.ecr.ap-southeast-2.amazonaws.com/n11963131-assignment-1-0.0.1:gif-api`

`docker push 901444280953.dkr.ecr.ap-southeast-2.amazonaws.com/n11963131-assignment-1-0.0.1:gif-api`
#### Pull
`docker pull 901444280953.dkr.ecr.ap-southeast-2.amazonaws.com/n11963131-assignment-1-0.0.1:gif-api`