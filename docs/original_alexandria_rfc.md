# Rationale

Documents in Caluma can currently only be added to a form via file question. These do not provide search, tags, thumbnails and some other features needed for a document management service. File questions can only be used inside a form.

# Goal
Our goal is to implement an external document management service to hold and provide uploaded documents. Ideally the document management service would be independent of caluma.
Documents can be uploaded and, depending on user access, managed by internal as well as external users.

The goal is NOT to re implement a complex [DMS](https://en.wikipedia.org/wiki/Document_management_system) but rather to have a simple and user-friendly way of managing documents with different permissions.

All User Interface interactions should be as simple as possible and easily understandable.

# Core features

- Documents can be uploaded
- Documents can be downloaded
- Documents can be replaced
- Documents should be in categories.
- Documents can be tagged
- Documents have a version history
- Documents have an access history

How we handle permissions is still a point open for discussion.

# Design Concept

## Overview
![All Files](https://user-images.githubusercontent.com/15276514/86333957-e42e5700-bc4c-11ea-90ff-758793033788.png)
This view should provide an overview of all categories and documents available. The search as well as the categories navigation are visible on all views. All documents can have one or more tags. These tags can be filtered via the filters directly under the search bar.

## Files filtered by Category
![Files of Category](https://user-images.githubusercontent.com/15276514/86334326-5b63eb00-bc4d-11ea-95c2-5e447fcc8d01.png)
Displays all documents of a category. Documents can be moved to another category via drag and drop.

## File detail view
![File Detail](https://user-images.githubusercontent.com/15276514/86335399-bf3ae380-bc4e-11ea-8684-1992a4bc0af3.png)

The detail view should display general information about the file as well as some common interactions like downloading, deleting, replacing as well as managing the tags of a document.

A document also has a version and access history which should be displayed here.

If a document is replaced (a new version is uploaded), we add a version history entry instead of just replacing the document. This way we can track the history of a document.

If a user moves or downloads a document, this would be recorded in the access history.

## Context menu of document
![Context Menu of File](https://user-images.githubusercontent.com/15276514/86335738-2fe20000-bc4f-11ea-83e7-d04ea674903a.png)
The context menu should provide frequently used functionalities.

## Upload
![Upload](https://user-images.githubusercontent.com/15276514/86335820-4b4d0b00-bc4f-11ea-82f5-27228fbe2ef7.png)
Uploads should be handled via drag and drop. For users which do not want to use drag and drop, we provide a file upload button.

## List view
![List View](https://user-images.githubusercontent.com/15276514/86336001-864f3e80-bc4f-11ea-8d21-365307338269.png)
Users with limited screen space or power users can display the documents as list.

## Multiple selection
![Multiple Selection](https://user-images.githubusercontent.com/15276514/86336138-b991cd80-bc4f-11ea-9b9a-2d09c126795c.png)
Some actions can be performed on multiple documents at once. Multiple documents can be selected by checking each document in the left hand corner. Multiple documents can also be moved.

## Collapse nav
![Collapsed Nav](https://user-images.githubusercontent.com/15276514/86336292-f78ef180-bc4f-11ea-853b-a194850f866c.png)
To increase usable screen space, the navigation bar can be collapsed. Categories are distinguishable by color. Each category has a unique color. This should help users navigate the categories with a collapsed navigation.

# Name
I propose `alexandria` as the name for the new project. Alexandria is a City in Egypt which once hosted the [Library of Alexandria](https://en.wikipedia.org/wiki/Library_of_Alexandria), one of the largest and most significant libraries of the ancient world.
