Assignment 2 - Cloud Services Exercises - Response to Criteria
================================================

Instructions
------------------------------------------------
- Keep this file named A2_response_to_criteria.md, do not change the name
- Upload this file along with your code in the root directory of your project
- Upload this file in the current Markdown format (.md extension)
- Do not delete or rearrange sections.  If you did not attempt a criterion, leave it blank
- Text inside [ ] like [eg. S3 ] are examples and should be removed


Overview
------------------------------------------------

- **Name:** Michael Mallett
- **Student number:** n11963131
- **Partner name (if applicable):** Christopher Nicholson
- **Partner Student number:** n11811749
- **Application name:** GifMakerAPI
- **Two line description:** We implemented an application that allows users to upload images and then convert them into customised gifs. Some other features include creating an account to make files private, retrieving metadata, and uploading gifs to GIPHY.
- **EC2 instance name or ID:** i-09b477efc9b257957 (Group11-Assessment2)

------------------------------------------------

### Core - First data persistence service

- **AWS service name:**  S3
- **What data is being stored?:** Images and gif files.
- **Why is this service suited to this data?:** Files are typically best stored on blob storage services such as S3 due to their large size and unstructured nature.
- **Why is the other service used not suitable for this data?:** DynamoDB is not suitable for storing files as it doesn't really support large file uploads, and only works best with semi-structured data.
- **Bucket name:** `a2-11`
- **Video timestamp:**
- **Relevant files:**
    - `gma_code/dao/s3.py`

### Core - Second data persistence service

- **AWS service name:**  DynamoDB
- **What data is being stored?:** Metadata related to images and gifs 
- **Why is this service suited to this data?:** DynamoDB is a NoSQL database service, which means that it stores semi-structured data in the form of key-value pairs, perfect for metadata.
- **Why is the other service used not suitable for this data?:** S3 is not suitable for storing structured data due to the fact that it only supports unstructured data.
- **Table name:** `a2-11`
- **Video timestamp:**
- **Relevant files:**
    - `gma_code/dao/dynamo_db.py`

### Third data service

- **AWS service name:**  [eg. RDS]
- **What data is being stored?:** [eg video metadata]
- **Why is this service suited to this data?:** [eg. ]
- **Why is are the other services used not suitable for this data?:** [eg. Advanced video search requires complex querries which are not available on S3 and inefficient on DynamoDB]
- **Bucket/instance/table name:**
- **Video timestamp:**
- **Relevant files:**
    -

### S3 Pre-signed URLs

- **S3 Bucket names:**
- **Video timestamp:**
- **Relevant files:**
    -

### In-memory cache

- **ElastiCache instance name:**
- **What data is being cached?:** [eg. Thumbnails from YouTube videos obatined from external API]
- **Why is this data likely to be accessed frequently?:** [ eg. Thumbnails from popular YouTube videos are likely to be shown to multiple users ]
- **Video timestamp:**
- **Relevant files:**
    -

### Core - Statelessness

- **What data is stored within your application that is not stored in cloud data services?:** [eg. intermediate video files that have been transcoded but not stabilised]
- **Why is this data not considered persistent state?:** [eg. intermediate files can be recreated from source if they are lost]
- **How does your application ensure data consistency if the app suddenly stops?:** [eg. journal used to record data transactions before they are done.  A separate task scans the journal and corrects problems on startup and once every 5 minutes afterwards. ]
- **Relevant files:**
    -

### Graceful handling of persistent connections

- **Type of persistent connection and use:** [eg. server-side-events for progress reporting]
- **Method for handling lost connections:** [eg. client responds to lost connection by reconnecting and indicating loss of connection to user until connection is re-established ]
- **Relevant files:**
    -


### Core - Authentication with Cognito

- **User pool name:** A2-Group11
- **How are authentication tokens handled by the client?:** On the client side, authentication tokens are handled by first obtaining one via the `authenticate` function. Which calls on Cognito's `InitiateAuth` and returns an `Authentication Result` that contains the AccessToken, IdToken and RefreshToken. The client then stores these in memory and attached the AuthenticationToken in the `Authorization: Bearer <token>` header on every API request. FastAPI then extracts that header on any requests and ensures the JWT signature is verified and the AccessToken hasn't expired.
- **Video timestamp:**
- **Relevant files:**
    - `gma_code/auth.py`
    - `gma_code/routes.py`

### Cognito multi-factor authentication

- **What factors are used for authentication:** password, email code and Authenticator app (eg. Microsoft Authenticator)
- **Video timestamp:**
- **Relevant files:**
    - `gma_code/mfa_auth.py`
    - `gma_code/auth.py`

### Cognito federated identities

- **Identity providers used:**
- **Video timestamp:**
- **Relevant files:**
    -

### Cognito groups

- **How are groups used to set permissions?:** [eg. 'admin' users can delete and ban other users]
- **Video timestamp:**
- **Relevant files:**
    -

### Core - DNS with Route53

- **Subdomain**:  a2group11.cab432.com
- **Video timestamp:**

### Parameter store

- **Parameter names:** [eg. n1234567/base_url]
- **Video timestamp:**
- **Relevant files:**
    -

### Secrets manager

- **Secrets names:** [eg. n1234567-youtube-api-key]
- **Video timestamp:**
- **Relevant files:**
    - `gma_code/dao/secrets_loader.py`
    - `app.py` - secrets used
    - `gma_code/auth.py` - secrets used
    - `gma_code/api/v3.py` - secrets used

### Infrastructure as code

- **Technology used:**
- **Services deployed:**
- **Video timestamp:**
- **Relevant files:**
    -

### Other (with prior approval only)

- **Description:**
- **Video timestamp:**
- **Relevant files:**
    -

### Other (with prior permission only)

- **Description:**
- **Video timestamp:**
- **Relevant files:**
    -