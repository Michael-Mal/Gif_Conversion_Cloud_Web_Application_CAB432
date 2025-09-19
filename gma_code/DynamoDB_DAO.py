from fastapi import HTTPException
import boto3
from botocore.exceptions import ClientError
import os

dynamodb = boto3.client("dynamodb", region_name='ap-southeast-2')
qut_user = "n11963131@qut.edu.au"
DEV_MODE = os.getenv("DEV_MODE", "false").lower() == "true"

images_data = {}
gif_data = {}

def check_exists(
    name: str,
    data_type: str,
    desired_outcome: bool = True
):
    """Raises a HTTPException if desired outcome is not true"""

    # Gets data based on datatype
    data = set()
    if (data_type == "images"):
        data = images_data.keys()
    else:
        data = gif_data.keys()

    # Check if name in data
    if(name in data):
        if (desired_outcome == False):
            raise HTTPException(status_code=400, detail=f"{name} already exists")
    else:
        if (desired_outcome == True):
            raise HTTPException(status_code=404, detail=f"{name} cannot be found")
        

def check_authorised(
    name: str,
    data_type: str,
    username: str
):
    """Raises a HTTPException if not authorised"""

    # Gets data based on datatype
    data = set()
    if (data_type == "images"):
        data = images_data[name]
    else:
        data = gif_data[name]

    # Check if authorised
    if not(data['public']) and not(data['username'] == username):
        raise HTTPException(status_code=403, detail=f"You are unauthorised to interact with {name}")

# CREATE
def create_images_data(
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
                "file_names": {"L": file_names_w_attr}
            }

    try:
        if not DEV_MODE:
            dynamodb.put_item(
                TableName='a2-11',
                Item=data,
                ConditionExpression='attribute_not_exists(#n)',
                ExpressionAttributeNames={"#n":"name"}
            )
        # Allow overwriting if in dev mode
        else:
            dynamodb.put_item(
                TableName='a2-11',
                Item=data
            )

    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            raise HTTPException(status_code=400, detail=f"{name} already exists")
        else:
            raise RuntimeError(f"Unexpected error: {e}")


# READ ALL
def read_all_images_data(
    username: str = "",
    limit: int = 0,
    page: int = 1
):
    images_list = {}
    for images in images_data.keys():
        if (username == ""):
            # Get public images
            if images_data[images]['public'] == True:
                images_list[images] = images_data[images]
        else:
            # Get user-made images
            if images_data[images]['username'] == username:
                images_list[images] = images_data[images]

    # Pagination
    if not(limit == 0):
        all_items = list(images_list.items())
        skip = (page * limit) - limit
        paginated_items = all_items[skip: skip + limit]
        images_list = dict(paginated_items)

    # Filtering/sorting not needed due to limited metadata

    return images_list

# READ FROM NAME
def read_images_data(
    name: str
):
    try:
        response = dynamodb.get_item(
            TableName='a2-11',
            Key={
                "qut-username": {"S": qut_user},
                "name": {"S": "images_" + name},
            },
        )
        return response.get("Item")
    except ClientError as e:
        raise RuntimeError(f"Unexpected error: {e}")

# DELETE
def delete_images_data(
    name: str
):
    images_data.pop(name)

# CREATE
def create_gif_data(
    gif_name: str,
    username: str,
    public: bool,
    images_name: str,
    width: int,
    height: int,
    duration: int,
    loop: int
):
    gif_data[gif_name] = {
        "username": username,
        "public": public,
        "images_name": images_name,
        "width": width,
        "height": height,
        "duration": duration,
        "loop": loop,
        "downloads": 0
    }

# READ ALL
def read_all_gif_data(
    username: str = "",
    limit: int = 0,
    page: int = 1,
    filter_by_images: str = "",
    sort_by_field: str = "",
    sort_descending: bool = False
):
    gifs = {}
    for gif in gif_data.keys():
        if (username == ""):
            # Get public images
            if gif_data[gif]['public'] == True:
                gifs[gif] = gif_data[gif]
        else:
            # Get user-made images
            if gif_data[gif]['username'] == username:
                gifs[gif] = gif_data[gif]

    # Pagination
    if not(limit == 0):
        all_items = list(gifs.items())
        skip = (page * limit) - limit
        paginated_items = all_items[skip: skip + limit]
        gifs = dict(paginated_items)

    # Filtering by image name
    if not(filter_by_images == ""):
        gifs_to_remove = []
        for gif_name in gifs.keys():
            if not(gifs[gif_name]["images_name"] == filter_by_images):
                gifs_to_remove.append(gif_name)
        for gif_name in gifs_to_remove:
            gifs.pop(gif_name)

    # Sorting
    if not(sort_by_field == ""):
        gifs = sorted(gifs.items(), key=lambda item: item[1][sort_by_field], reverse=sort_descending)

    return gifs

# READ FROM NAME
def read_gif_data(
    name: str
):
    return gif_data[name]
    # Returns exception if not in gif_data

# UPDATE
def increment_gif_downloads(
    name: str
):
    gif_data[name]["downloads"] = gif_data[name]["downloads"] + 1

# DELETE
def delete_gif_data(
    name: str
):
    gif_data.pop(name)