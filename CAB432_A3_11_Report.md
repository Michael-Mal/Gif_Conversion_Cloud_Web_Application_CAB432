---
title: "CAB432 Project Report"
author:
- "<The first partner's name> - n1234567"
- "<The second partner's name> - n1234568"
---

# Application overview

Our application uses a FastAPI backend that allows the user to upload multiple images, covert images to GIFs, retrieve
data related to images and gifs along with downloading the gifs or uploading to GIPHY. The app has been containerised
with Docker and deployed on AWS.

# Application architecture

*Remove these instructions:*
*Your architecture diagram goes here*

*Briefly discuss the use of each service*
*Example:
* - S3: used to store user uploaded and transcoded video files, and video thumbnails*


## Project Core - Microservices

- **First service functionality:** [eg. Public facing API server]
- **First service compute:** [eg. EC2/Lambda/ECS, instance ID/name]
- **First service source files:**
  - [eg. source code filenames or directory]

- **Second service functionality:** 
- **Second service compute:**
- **Second service source files:**
  - 

- **Video timestamp:**


## Project Additional - Additional microservices

- **Third service functionality:**
- **Third service compute:**
- **Third service source files:**
  - 

- **Fourth service functionality:**
- **Fourth service compute:**
- **Fourth service source files:**
  - 

- **Video timestamp:**


## Project Additional - Serverless functions

- **Service(s) deployed on Lambda:**
- **Video timestamp:**
- **Relevant files:**
    -


## Project Additional - Container orchestration with ECS 

- **ECS cluster name:**
- **Task definition names:**
- **Video timestamp:**
- **Relevant files:**
    -


## Project Core - Load distribution

- **Load distribution mechanism:** [eg. SQS, ALB,...]
- **Mechanism instance name:** [eg. n1234567-project-alb]
- **Video timestamp:**
- **Relevant files:**
    -


## Project Additional - Communication mechanisms

- **Communication mechanism(s):** [eg. SQS, EventBridge, ...]
- **Mechanism instance name:** [eg. n1234567-project-sqs]
- **Video timestamp:**
- **Relevant files:**
    -


## Project Core - Autoscaling

- **EC2 Auto-scale group or ECS Service name:**
- **Video timestamp:**
- **Relevant files:**
    -


## Project Additional - Custom scaling metric

- **Description of metric:** [eg. age of oldest item in task queue]
- **Implementation:** [eg. custom cloudwatch metric with lambda]
- **Rationale:** [discuss both small and large scales]
- **Video timestamp:**
- **Relevant files:**
    -


## Project Core - HTTPS

- **Domain name:** https://a2group11.cab432.com
- **Certificate ID:** `6cf36afb-550e-47b8-bda3-4aa09997a4b1`
- **ALB/API Gateway name:** Group11-gifmaker
- **Video timestamp:**
- **Relevant files:**
    -


## Project Additional - Container orchestration features

- **First additional ECS feature:** [eg. service discovery]
- **Second additional ECS feature:**
- **Video timestamp:**
- **Relevant files:**
    -


## Project Additional - Infrastructure as Code

- **Technology used:** [eg. CloudFormation, Terraform, ...]
- **Services deployed:** [eg. ALB, SQS, ....  Only Block 3 services need to be listed]
- **Video timestamp:**
- **Relevant files:**
    -


## Project Additional - Dead letter queue

- **Technology used:** [eg. SQS, ...]
- **Services deployed:** [eg. SQS, ....  Only Block 3 services need to be listed]
- **Video timestamp:**
- **Relevant files:**
    -


## Project Additional - Edge Caching

- **Cloudfront Distribution ID:**
- **Content cached:**
- **Rationale for caching:**
- **Video timestamp:**
- **Relevant files:**
    -


## Project Additional - Other (with prior permission only)

- **Description:**
- **Video timestamp:**
- **Relevant files:**
    -


# Cost estimate

*Remove these instructions:*
*Include the public share link from the AWS cost calculator*
*Include a summary of the total price  per month for each AWS service that you use*
*eg:*
*- EC2: 25.75*

# Scaling up


# Security


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

