# import required modules
import sys
import os
import subprocess



if len(sys.argv) < 2:
    print("Please enter one or more URLs as arguments.\nURLs must be enclosed in double quotation marks and separated by a space.")
else:
    # assign directories from command line arguments, add them to a list
    folders = []
    failures = []
    for argument in sys.argv[1:]:
        folders.append(argument)

    #iterate over the folders list, any sub-folders are automatically added to the end of the list
    for pathways in folders:
        # iterate over files in the current directory
        for filename in os.listdir(pathways):
            f = os.path.join(pathways, filename)
            # checking if it is a file. If it is, run the ffmpeg commands
            if os.path.isfile(f):
                # Try to run the ffmpeg command. If it fails, throw an error and log it, then move on to next file. All failures will print out at the end of execution 
                try:
                    subprocess.run(f'ffmpeg -i "{f}" -metadata title=  -c:v h264 -c:a ac3 -c:s copy -y -map 0:a -map 0:v -map 0:s?  -preset slower -crf 22 "{pathways}\\output.mkv"', shell=True, check=True)
                except:
                    failures.append(f)
                    continue
                # Delete the original file, then rename the output file to replace the original. These won't run if there's an error, so no worry of deleting a file that wasn't encoded 
                subprocess.run(f'del {f}', shell=True)
                subprocess.run(f'MOVE "{pathways}\\output.mkv" "{f}"', shell=True)
                print(f"Encoded {filename}")
            elif os.path.isdir(f):
                folders.append(f)

    # printing out errors to the command line, and saving them to a file for later troubleshooting
    if len(failures) != 0:
        failFile = open("EncodingFailures.txt", "w")
        print("The following files failed to encode:")
        failFile.write("The following files failed to encode:")
        for item in failures:
            print(item)
            failFile.write("\n" + item)
        failFile.close()