from fastapi import HTTPException
import boto3
from botocore.exceptions import ClientError
import os
import time
from gma_code.dao.parameter_store import get_parameter

dynamodb = boto3.client("dynamodb", region_name=get_parameter("aws_region"))
qut_user = "n11963131@qut.edu.au"
table_name = 'a2-11'
DEV_MODE = os.getenv("DEV_MODE", "false").lower() == "true"

def check_authorised(
    name: str,
    data_type: str,
    username: str
):
    """Raises a HTTPException if not authorised"""
    # Gets data based on datatype
    data = set()
    if (data_type == "images"):
        data = read_images(name)
    else:
        data = read_gif(name)

    # Check if authorised
    if not(data['public']['BOOL']) and not(data['username']['S'] == username):
        raise HTTPException(status_code=403, detail=f"You are unauthorised to interact with {name}")
    

# CREATE
def create_images(
    name: str,
    username: str,
    public: bool,
    file_names: list[str]
):    
    file_names_w_attr = []
    for file_name in file_names:
        file_names_w_attr.append({"S": file_name})

    data = {
                "qut-username": {"S": qut_user},
                "name": {"S": "images_" + name},
                "username": {"S": username},
                "public": {"BOOL": public},
                "file_names": {"L": file_names_w_attr},
                "time_created": {"N": str(int(time.time()))}
            }

    try:
        if not DEV_MODE:
            dynamodb.put_item(
                TableName=table_name,
                Item=data,
                ConditionExpression='attribute_not_exists(#n)',
                ExpressionAttributeNames={"#n":"name"}
            )
        # Allow overwriting if in dev mode
        else:
            dynamodb.put_item(
                TableName=table_name,
                Item=data
            )

    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            raise HTTPException(status_code=400, detail=f"{name} already exists")
        else:
            raise RuntimeError(f"Unexpected error: {e}")


# READ ALL
def read_all_images(
    ignore_restrictions: bool = False,  # never expose this to the API
    username: str = "",
    limit: int = 0,
    page: int = 1
):
    images_list = []
    try:
        response = dynamodb.query(
            TableName=table_name,
            KeyConditionExpression="#pk = :username AND begins_with(#sk, :nameStart)",
            ExpressionAttributeNames={"#pk": "qut-username", "#sk": 'name'},
            ExpressionAttributeValues={":username": {"S": qut_user}, ":nameStart": {"S": "images_"}},
        )
        images_list = response.get("Items")
    except ClientError as e:
        raise RuntimeError(f"Unexpected error: {e}")

    for images in images_list:
        images.pop("qut-username")
    
    if ignore_restrictions:
        # Return an unmodified, unfiltered set of images data for use internally
        return images_list

    images_list_p = []
    for images in images_list:
        if (username == ""):
            # Get public images
            if images['public']['BOOL'] == True:
                images_list_p.append(images)
        else:
            # Get user-made images
            if images['username']['S'] == username:
                images_list_p.append(images)
    images_list = images_list_p

    # Pagination
    if not(limit == 0):
        skip = (page * limit) - limit
        images_list = images_list[skip: skip + limit]

    # Filtering/sorting not needed due to limited metadata

    return images_list

# READ FROM NAME
def read_images(
    name: str
):
    try:
        response = dynamodb.get_item(
            TableName=table_name,
            Key={
                "qut-username": {"S": qut_user},
                "name": {"S": "images_" + name},
            },
        ).get("Item")
        if response is not None:
            response.pop("qut-username")
        return response
    except ClientError as e:
        raise RuntimeError(f"Unexpected error: {e}")

# DELETE
def delete_images(
    name: str
):
    try:
        dynamodb.delete_item(
            TableName=table_name,
            Key={
                "qut-username": {"S": qut_user},
                "name": {"S": "images_" + name},
            }
        )
    except ClientError as e:
        raise RuntimeError(f"Unexpected error: {e}")

# CREATE
def create_gif(
    gif_name: str,
    username: str,
    public: bool,
    images_name: str,
    width: int,
    height: int,
    duration: int,
    loop: int
):
    data = {
                "qut-username": {"S": qut_user},
                "name": {"S": "gif_" + gif_name},
                "username": {"S": username},
                "public": {"BOOL": public},
                "images_name": {"S": images_name},
                "width": {"N": str(width)},
                "height": {"N": str(height)},
                "duration": {"N": str(duration)},
                "loop": {"N": str(loop)},
                "downloads": {"N": "0"},
                "time_created": {"N": str(int(time.time()))}
            }

    try:
        if not DEV_MODE:
            dynamodb.put_item(
                TableName=table_name,
                Item=data,
                ConditionExpression='attribute_not_exists(#n)',
                ExpressionAttributeNames={"#n":"name"}
            )
        # Allow overwriting if in dev mode
        else:
            dynamodb.put_item(
                TableName=table_name,
                Item=data
            )

    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            raise HTTPException(status_code=400, detail=f"{gif_name} already exists")
        else:
            raise RuntimeError(f"Unexpected error: {e}")

# READ ALL
def read_all_gif(
    ignore_restrictions: bool = False,  # never expose this to the API
    username: str = "",
    limit: int = 0,
    page: int = 1,
    filter_by_images: str = "",
    sort_by_field: str = "",
    sort_descending: bool = False,
):
    gif_list = []
    try:
        gif_list = dynamodb.query(
            TableName=table_name,
            KeyConditionExpression="#pk = :username AND begins_with(#sk, :nameStart)",
            ExpressionAttributeNames={"#pk": "qut-username", "#sk": 'name'},
            ExpressionAttributeValues={":username": {"S": qut_user}, ":nameStart": {"S": "gif_"}},
        ).get("Items")
    except ClientError as e:
        raise RuntimeError(f"Unexpected error: {e}")

    for gif in gif_list:
        gif.pop("qut-username")

    if ignore_restrictions:
        # Return an unmodified, unfiltered set of gif data for use internally
        return gif_list

    gif_list_p = []
    for gif in gif_list:
        if (username == ""):
            # Get public gifs
            if gif['public']['BOOL'] == True:
                gif_list_p.append(gif)
        else:
            # Get user-made gifs
            if gif['username']['S'] == username:
                gif_list_p.append(gif)
    gif_list = gif_list_p

    # Pagination
    if not(limit == 0):
        skip = (page * limit) - limit
        gif_list = gif_list[skip: skip + limit]

    # Filtering by image name
    if not(filter_by_images == ""):
        gifs_to_remove = []
        for gif in gif_list:
            if not(gif["images_name"]['S'] == filter_by_images):
                gifs_to_remove.append(gif)
        for gif in gifs_to_remove:
            gif_list.remove(gif)

    # Sorting
    if not(sort_by_field == ""):
        gif_list = sorted(gif_list, key=lambda item: item[sort_by_field]['S'], reverse=sort_descending)

    return gif_list

# READ FROM NAME
def read_gif(
    name: str
):
    try:
        response = dynamodb.get_item(
            TableName=table_name,
            Key={
                "qut-username": {"S": qut_user},
                "name": {"S": "gif_" + name},
            },
        ).get("Item")
        if response is not None:
            response.pop("qut-username")
        return response
    except ClientError as e:
        raise RuntimeError(f"Unexpected error: {e}")

# UPDATE
def increment_gif_downloads(
    name: str
):
    try:
        response = dynamodb.update_item(
            TableName=table_name,
            Key={
                "qut-username": {"S": qut_user},
                "name": {"S": "gif_" + name},
            },
            UpdateExpression="SET downloads = downloads + :one",
            ExpressionAttributeValues={
                ":one": {"N": "1"}
            }
        )
    except ClientError as e:
        raise RuntimeError(f"Unexpected error: {e}")

# DELETE
def delete_gif(
    name: str
):
    try:
        dynamodb.delete_item(
            TableName=table_name,
            Key={
                "qut-username": {"S": qut_user},
                "name": {"S": "gif_" + name},
            }
        )
    except ClientError as e:
        raise RuntimeError(f"Unexpected error: {e}")
