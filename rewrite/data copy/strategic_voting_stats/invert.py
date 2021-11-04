import os

# List all files in directory
def list_files(directory):
    files = []
    for file in os.listdir(directory):
        if not file.endswith(".py"):
            files.append(file)
    return files


# Read file and overwrite after inverting
def read_invert_write(file, directory):
    with open(directory + os.sep + file, "r") as f:
        number = 100 - float(f.readline())
        with open(directory + os.sep + file, "w") as f:
            f.writelines(str(number))

def main():
    files = list_files(os.getcwd())
    print(files)
    for file in files:
        read_invert_write(file, os.getcwd())


if __name__=="__main__":
    main()