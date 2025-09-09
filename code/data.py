images_data = {}

def images_authorised(
    name: str,
    username: str
):
    if (images_data[name]['public']) or (images_data[name]['username'] == username):
        return True
    else:
        return False

# CREATE
def create_images_data(
    name: str,
    username: str,
    public: bool     
):
    images_data[name] = {
            "username": username,
            "public": public
        }

# READ ALL
def read_all_images_data(
    username: str,
    public: bool,
    limit: int = 0,
    page: int = 1
):
    images_list = {}
    for images in images_data.keys():
        if public:
            if images_data[images]['public'] == True:
                images_list[images] = images_data[images]
        elif not public:
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
    return images_data[name]
    # Returns exception if not in images_data

# DELETE
def delete_images_data(
    name: str
):
    images_data.pop(name)

gif_data = {}

def gif_authorised(
    name: str,
    username: str
):
    if (gif_data[name]['public']) or (gif_data[name]['username'] == username):
        return True
    else:
        return False

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
    username: str,
    public: bool,
    limit: int = 0,
    page: int = 1,
    filter_by_images: str = "",
    sort_by_field: str = "",
    sort_descending: bool = False
):
    gifs = {}
    for gif in gif_data.keys():
        if public:
            if gif_data[gif]['public'] == True:
                gifs[gif] = gif_data[gif]
        elif not public:
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

# DELETE
def delete_gif_data(
    name: str
):
    gif_data.pop(name)