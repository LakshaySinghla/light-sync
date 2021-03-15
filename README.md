# light-sync

This is python script which sync 2 folders. The folders can be present either on same machine or on different machines. 

light-sync is very useful while debugging on remote machine as you can use your preferred IDE on local machine to make changes and that changes gets sync to remote machine in no time.

### Command
```
$python sync.py /path/to/source/folder /path/to/destination/folder
```

### Key features:
- Create destination path if it doesn't exist.
- You can provide a file containing path to files which are needed to be ignnored.
- If destination folder exist and contains some other files than source folder, then that files are not altered/deleted.
