# NoteManager
Note managing application written in python tkinter. Uses a simple folder structure to automatically place files into their correct folders for easy note management.

## How it works
Upon adding a directory as a an area for NoteManager to manage it creates a .note_manager folder which contains a .json with information about that folder area, where notes will be automatically placed. 
Within that "area" each folder will have associated tags that can be added to or updates stored in the .json which is uses to correctly place the note files, by matching the contents of the notes to the tags associated with each folder. Currently mainly supports basic text files and markdown files

The folder structure will typically look like:
```
main_area/
├─ .note_manager/
│  ├─ settings.json
├─ subject1/
│  ├─ notes1.txt
│  ├─ notes2.md
├─ subject2/
│  ├─ notes1.txt
│  ├─ notes2.md
```
And the settings.json typically has the structure:
```
{
  "folders": {
    "subject1": {
      "name": "subject1",
      "tags": [
        "tag1",
        "tag2"
      ]
    },
    "subject2": {
      "name": "subject2",
      "tags": [
        "tag3",
        "tag4"
      ]
    }
  }
}
```
