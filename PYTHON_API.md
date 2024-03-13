# API Functions

Functions which make interacting with the models easier.

`create_document_file`
Creates a document and file
Params:

- `user` The user creating the document and file.
- `group` The group creating the document and file.
- `document_attributes` A dictionary containing the fields for the document. (required: category, title)
- `file_attributes` A dictionary containing the fields for the file. (required: name, content, mime_type, size)
  Return:
- A tuple containing the created document and file.

`create_file`
Creates a file with thumbnail
Params:

- `document` The document associated with the file.
- `user` The user who created the file.
- `group` The group who created the file.
- `attributes` A dictionary containing the fields for the file. (required: name, content, mime_type, size)
  Return:
- The created file object.
