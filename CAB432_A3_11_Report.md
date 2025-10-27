---
title: "CAB432 Project Report"
author:
- "Michael Mallett - n11963131"
- "Christopher Nicholson - n11811749"
---

# Application overview

Our application uses a FastAPI backend that allows the user to upload multiple images, covert images to GIFs, retrieve
data related to images and gifs along with downloading the gifs or uploading to GIPHY. The app has been containerised
with Docker and deployed on AWS.

# Application architecture

<img width="972" height="621" alt="CAB432_A3_Architecture_Diagram drawio" src="https://github.com/user-attachments/assets/53a28f61-3bff-45e9-9e92-8a3985f89bcf" />

*Briefly discuss the use of each service*

- API microservice: This microservice holds the core logic of our application and is responsible for handling public API requests.
- Compute microservice: This microservice is used to convert user uploaded images to gifs (through automatic polling of an SQS queue).
- EC2: used as a virtual computer to run the above microservices.
- ECR: used to store the Docker images that EC2 can run.
- DynamoDB: used to store metadata related to images and gifs, such as the user who uploaded a set of images or how many times a gif has been downloaded.
- S3: used to store raw image and gif files, organised by name prefixes.
- Parameter store: used to store non-critical information such as the URL of the external API.
- Secrets manager: used to store security-critical information such as the external API key.
- SQS: holds information relating to requests to convert a gif. A dead-letter queue stores failed conversions.
- Route 53: Routes user traffic via a registered domain to our API
- AWS Private Certificate Authority: Provides us the private certificate to allow encrypted TLS communication, along with authenticating users.
- Application Load Balancer: Distributes incoming traffic across multiple healthy EC2 instances increasing the availability of our application
- Auto Scaling Group: Collection of ec2 instances that scales in and out depending on CPU demand ensuring dynamic scaling.

## Project Core - Microservices

- **First service functionality:** Public facing API server
- **First service compute:** [eg. EC2/Lambda/ECS, instance ID/name]
- **First service source files:**
  - `app/app.py`
  - `app/Dockerfile`
  - `app/requirements.txt`
  - Everything in `app/gma_code/`

- **Second service functionality:** Gif conversion microservice
- **Second service compute:**
- **Second service source files:**
  - Everything in `gif_conversion/`
  
- **Video timestamp:**


## Project Additional - Additional microservices

- **Third service functionality:**
- **Third service compute:**
- **Third service source files:**

- **Fourth service functionality:**
- **Fourth service compute:**
- **Fourth service source files:**
  - .
- **Video timestamp:**


## Project Additional - Serverless functions

- **Service(s) deployed on Lambda:**
- **Video timestamp:**
- **Relevant files:**
    


## Project Additional - Container orchestration with ECS 

- **ECS cluster name:**
- **Task definition names:**
- **Video timestamp:**
- **Relevant files:**
    


## Project Core - Load distribution

- **Load distribution mechanism:** SQS
- **Mechanism instance name:** `a3-11`
- **Video timestamp:**
- **Relevant files:**
    - `app/gma_code/dao/sqs.py`
    - `gif_conversion/gc_code/polling.py`


## Project Additional - Communication mechanisms

- **Communication mechanism(s):** [eg. SQS, EventBridge, ...]
- **Mechanism instance name:** [eg. n1234567-project-sqs]
- **Video timestamp:**
- **Relevant files:**
    


## Project Core - Autoscaling

- **EC2 Auto-scale group or ECS Service name:** Group11-A3-Second & Group11-A3
- **Video timestamp:**
- **Relevant files:**
    - Nil relevant files as all done within AWS


## Project Additional - Custom scaling metric

- **Description of metric:** [eg. age of oldest item in task queue]
- **Implementation:** [eg. custom cloudwatch metric with lambda]
- **Rationale:** [discuss both small and large scales]
- **Video timestamp:**
- **Relevant files:**
    


## Project Core - HTTPS

- **Domain name:** https://a2group11.cab432.com
- **Certificate ID:** `6cf36afb-550e-47b8-bda3-4aa09997a4b1`
- **ALB/API Gateway name:** Group11-gifmaker
- **Video timestamp:**
- **Relevant files:**
    - Nil relevant files as all done within AWS


## Project Additional - Container orchestration features

- **First additional ECS feature:** [eg. service discovery]
- **Second additional ECS feature:**
- **Video timestamp:**
- **Relevant files:**
    


## Project Additional - Infrastructure as Code

- **Technology used:** [eg. CloudFormation, Terraform, ...]
- **Services deployed:** [eg. ALB, SQS, ....  Only Block 3 services need to be listed]
- **Video timestamp:**
- **Relevant files:**
    


## Project Additional - Dead letter queue

- **Technology used:** SQS
- **Services deployed:** SQS (queue name is `a3-11-dlq`)
- **Video timestamp:**
- **Relevant files:**
    - `app/gma_code/gc.py`


## Project Additional - Edge Caching

- **Cloudfront Distribution ID:**
- **Content cached:**
- **Rationale for caching:**
- **Video timestamp:**
- **Relevant files:**
    


## Project Additional - Other (with prior permission only)

- **Description:**
- **Video timestamp:**
- **Relevant files:**
    


# Cost estimate

**Public Link:**https://calculator.aws/#/estimate?id=de06e3c8a7bca6f7423b5056e821f8a92e700bc9

- EC2: $18.76
- AWS Secrets Manager: $1.20
- Amazon Route 53: $0.90
- Amazon Cognito: $5.00
- AWS Certificate Manager: Nil Monthly (Upfront Cost of $15.00)
- Elastic Load Balancing: $25.41
- Amazon Elastic Container Registry: $0.02
- Amazon DynamoDB: $13.06
- Amazon Simple Storage Service (S3): 0.26
- AWS Systems Manager: Nil

# Scaling up


# Security

**Network Security**

Traffic is managed through an Application Load Balancer (ALB) that terminates TLS at the edge using a valid ACM certificate. 
Only ports 80 (for redirect) and 443 (HTTPS) are exposed publicly, while application traffic runs internally on port 3000.

**Least Privilege** 

To ensure once our application is published commercially that cyber breaches are prevented
adapting least privilege principal will be crucial. This can be achieved via IAM policies 
granting users, roles, and services with only the minimum permissions 
necessary to perform their specific tasks, without any additional access

**Secure by Design**

To ensure the application is secure by design only required endpoints are exposed. Input validation is handled through FastAPI
and Pydantic schemas, mitigating injection and parsing vulnerabilities. Container images are built once and deployed. 

**Confidentiality**

The application uses TLS encryption (HTTPS) through AWS ACM certificates to protect data in transit between users and the Application Load Balancer.
Internally, traffic between the ALB and EC2 instances also flows within the VPC, reducing exposure to external networks.

# Sustainability
The choices we can make while creating our application along with deployment to improve sustainability at the software level include utilising a different language that isn't as energy intensive (REFERENCE). 
We have Containerised our application with Docker and deploy via a Auto Scaling Group which ensures we only run what is required avoiding idle compute energy. We have optimised our build pipelines
by building images and then reusing them through the ECR reducing redundant compilation and deployment energy. To increase sustainability in the future we could introduce in-memory caching to reduce repeated processing for identical requests.
The use of S3 for file storage ensures any temporary files are cleaned up automatically, preventing the retainment of unused data.

At a hardware level ensuring the correct sized EC2 instance avoids overprovisioning the CPU and memory resources. The implementation of Auto Scaling ensures that at any point in time 
the required number of instances we have running is only what's required to ensure the CPU usage stays at <= 80%. Thus, scaling down in during low periods of traffic. 
A change that could be conducted in the future is to utilise AWS Graviton which are ARM based instances. These instances are more energy-efficient and lower both costs and carbon footprint.

At a data centre level if our application was to continue to grow and require more resources we can utilise location shifting by deploying workloads to data centres where the climate is cooler as 
Summer in Australia would increase artificial cooling costs


At a resource level a big change that can be implemented is utilising a more green region as AWS Sydney location is one of the highest for CPU emissions. The fallback, however, is potential latency of having to use overseas servers.

# Bibliography

*Remove this section if not being used.*






