# Face-unlock-for-windows

##Python version : 3.7.7 64bit

Steps to setup face unlock for windows :
1. Create a file named dataset in the FacialRecognition folder.
2. Run the setup.bat file
3. After the message trigger training done , go to task scheduler.
4. There will be a task called "face unlock" , in the triggers tab select "on workstation unlock" in the drop down.
5. In the Actions tab,edit the action,and add the path to the project folder,change other settings according to your requirements.
6. Face Unlocking should be up and running. 
