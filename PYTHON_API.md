# API Functions

Functions which make interacting with the models easier.

## `create_document_file`

Creates a document and file

### Parameters

- `user` The user creating the document and file.
- `group` The group creating the document and file.
- `category` models.Category,
- `document_title` Name of the document
- `file_name` Name of the file
- `file_content` File object
- `mime_type` File mime type
- `file_size` File size 
- `additional_document_attributes` A dictionary containing the optional fields for the document.
- `additional_file_attributes` A dictionary containing the optional fields for the file.

### Return

- A tuple containing the created document and file.

## `create_file`

Creates a file with thumbnail

### Parameters

- `document` The document associated with the file.
- `user` The user who created the file.
- `group` The group who created the file.
- `name` Name of the file
- `content` File object
- `mime_type` File mime type
- `size` File size
- `additional_attributes` Kwargs containing the optional fields for the file. 

### Return

- The created file object.
