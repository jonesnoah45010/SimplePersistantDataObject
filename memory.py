import os
from os import system
import getpass
import json
import csv
import sys
import platform
import atexit

myos = platform.system()

Home = ''
if myos == 'Windows':
	Home = os.path.join("C:\\Users",getpass.getuser())
elif myos == 'Linux':
	Home = os.path.join("/home",getpass.getuser())
else:
	Home = os.path.join("/Users",getpass.getuser())
Desktop = ''
if myos == 'Windows':
	Desktop = os.path.join("C:\\Users",getpass.getuser(),"Desktop")
elif myos == 'Linux':
	Desktop = os.path.join("/home",getpass.getuser(),"Desktop")
else:
	Desktop = os.path.join("/Users",getpass.getuser(),"Desktop")
Documents = ''
if myos == 'Windows':
	Documents = os.path.join("C:\\Users",getpass.getuser(),"Documents")
elif myos == 'Linux':
	Documents = os.path.join("/home",getpass.getuser(),"Documents")
else:
	Documents = os.path.join("/Users",getpass.getuser(),"Documents")
Downloads = ''
if myos == 'Windows':
	Downloads = os.path.join("C:\\Users",getpass.getuser(),"Downloads")
elif myos == 'Linux':
	Downloads = os.path.join("/home",getpass.getuser(),"Downloads")
else:
	Downloads = os.path.join("/Users",getpass.getuser(),"Downloads")

def Here():
	return os.getcwd()

MyUserName = getpass.getuser()


#_______________________________________________________FILE AND FOLDER/DIRECTORY MANIPULATION


# returns True if the given string parameter is a path
# is_path("/Users/Bob/Desktop/file_name") == True
# is_path("file_name") == False
# is_path(Desktop) == True
# is_path("Desktop") == False
def is_path(path_or_folder_or_file):
	if type(path_or_folder_or_file) != str:
		return False 
	if myos == 'Windows':
		if '\\' not in path_or_folder_or_file:
			return False
		else:
			return True
	else:
		if "/" not in path_or_folder_or_file:
			return False
		else:
			return True


# returns a string that represents the given string path parameter in a corrected format to account for spaces
# to be used when paths with spaces are not being recognized by your os
# fixed_path("/Users/Bob/Desktop/file name") == '/Users/Bob/Desktop/"file name"'
def fixed_path(path):
	answer = []
	if myos == 'Windows':
		for item in path.split("\\"):
			if " " in item:
				answer.append('"' + item + '"')
			else: 
				answer.append(item)
	else:
		for item in path.split("/"):
			if "'" in item:
				answer.append('"' + item + '"')
			elif " " in item:
				# answer.append('"' + item + '"')
				answer.append(item.replace(" ","' '"))
			else: 
				answer.append(item)
	final_answer = answer[0]
	for item in answer[1:]:
		if myos == 'Windows':
			final_answer += '\\' + item
		else:
			final_answer += '/' + item
	return final_answer


# returns a string path to the desired file
# path_to_file("file_name") == "/Users/YourUserName/FileLocation/file_name"
def path_to_file(file_name,rootPath = Home,fix_path = True):
	parts = file_name.split(".")
	name = ".".join(parts[0:-1])
	kind = "." + parts[-1]
	pattern = '*' + kind
	for root, dirs, files in os.walk(rootPath):
		for filename in fnmatch.filter(files, pattern):
			if filename == file_name:
				if fix_path:
					return fixed_path(str(os.path.join(root, filename)))
				else:
					return str(os.path.join(root, filename))			
	return None


# returns a string path to the desired directory/folder
# path_to_dir("folder_name") == "/Users/YourUserName/FolderLocation/folder_name"
def path_to_dir(dir_name,rootPath = Home,fix_path = True):
	username = getpass.getuser()
	for root, dirs, files in os.walk(rootPath):
		if dir_name in dirs:
			if fix_path:
				return fixed_path(str(os.path.join(root, dir_name)))
			else:
				return str(os.path.join(root, dir_name))			
	return None



# returns a list of the contents of a given directory/folder
# contents_of("Desktop") == ["file1","file2","folder1","folder2"]
def contents_of(path_or_folder,include_file_paths = False):
	answer = []
	if not is_path(path_or_folder):
		path_or_folder = path_to_dir(path_or_folder)
	answer = os.listdir(path_or_folder)
	if include_file_paths:
		if myos == 'Windows':
			for i in range(len(answer)):
				answer[i] = fixed_path(path_or_folder + "\\" +answer[i])
		else:
			for i in range(len(answer)):
				answer[i] = fixed_path(path_or_folder + "/" +answer[i])
	if '.DS_Store' in answer:
		answer.remove('.DS_Store')
	return answer 



# returns a list of just the folders in a given directory/folder
# folders_in("Desktop") == ["folder1","folder2"]
def folders_in(path_or_folder,include_file_paths = False):
	if not is_path(path_or_folder):
		path_or_folder = path_to_dir(path_or_folder)
	answer = folders_in_helper(path_or_folder)
	new_answer = []
	if include_file_paths and answer != None:
		for item in answer:
			new_answer.append(fixed_path(os.path.join(path_or_folder,item)))
		return new_answer
	else:
		return answer




# helps folders_in()
def folders_in_helper(path_or_folder):
	if not is_path(path_or_folder):
		path_or_folder = path_to(path_or_folder)
	answer = []
	for root, dirs, files in os.walk(path_or_folder):
		if len(dirs) > 0:
			return dirs
	return []
	

# returns a list of just the files in a given directory/folder
# files_in("Desktop") == ["file1","file2"]
def files_in(path_or_folder,include_file_paths = False):
	answer = files_in_helper(path_or_folder)
	if '.DS_Store' in answer:
		answer.remove('.DS_Store')
	if include_file_paths:
		if not is_path(path_or_folder):
			path_or_folder = path_to(path_or_folder)
		new_answer = []
		for item in answer:
			new_answer.append(fixed_path(os.path.join(path_or_folder,item)))
		return new_answer
	else:
		return answer

# helps files_in()
def files_in_helper(path_or_folder):
	if not is_path(path_or_folder):
		path_or_folder = path_to(path_or_folder)
	answer = []
	for root, dirs, files in os.walk(path_or_folder):
		return files
	return []
	

# returns True if the given directory/folder is in fact a folder that exists on your computer
# is_folder("Desktop") == "True"
def is_folder(path_or_folder): 
	if not is_path(path_or_folder):
		if path_or_folder in folders_in(Here()):
			return True
		path_or_folder = path_to(path_or_folder)
	if myos == 'Windows':
		temp = path_or_folder.split("\\")
		folder_name = temp[-1]
		folder_location = "\\".join(temp[0:-1])
		print(folder_location)
		if folder_name in folders_in(folder_location):
			return True
		else:
			return False
	else:
		temp = path_or_folder.split("/")
		folder_name = temp[-1]
		folder_location = "/" + "/".join(temp[0:-1])
		if folder_name in folders_in(folder_location):
			return True
		else:
			return False


# returns True if the given files is in fact a file that exists on your computer
# is_folder("Desktop") == "True"
def is_file(path_or_file):
	return not is_folder(path_or_file)



# returns a string that is the path to given file of folder name
# path_to("Desktop") == "/Users/YourUserName/Desktop"
# path_to("FileOnDesktop") == /Users/YourUserName/Desktop/FileOnDesktop"
def path_to(file_or_dir,rootPath = Home, fix_path = True):
	check_locally = path_to_helper(file_or_dir,Here(),fix_path)
	if check_locally != None:
		return check_locally
	if not is_path(rootPath):
		rootPath = path_to_dir(rootPath)
	if myos == 'Windows':
		if file_or_dir == os.getcwd().split("\\")[-1]:
			return os.getcwd()
	else:
		if file_or_dir == os.getcwd().split("/")[-1]:
			return os.getcwd()
	if file_or_dir in contents_of(os.getcwd()):
		if fix_path:
			return fixed_path(os.path.join(os.getcwd(),file_or_dir))
		else:
			return os.path.join(os.getcwd(),file_or_dir)
	for root, dirs, files in os.walk(rootPath):
		if file_or_dir in dirs:
			if fix_path:
				return fixed_path(str(os.path.join(root, file_or_dir)))
			else:
				return str(os.path.join(root, file_or_dir))
		if file_or_dir in files:
			if fix_path:
				return fixed_path(str(os.path.join(root, file_or_dir)))
			else:
				return str(os.path.join(root, file_or_dir))
	return None


# Helps path_to() function
def path_to_helper(file_or_dir,rootPath = Home, fix_path = True):
	if not is_path(rootPath):
		rootPath = path_to_dir(rootPath)
	if myos == 'Windows':
		if file_or_dir == os.getcwd().split("\\")[-1]:
			return os.getcwd()
	else:
		if file_or_dir == os.getcwd().split("/")[-1]:
			return os.getcwd()
	if file_or_dir in contents_of(os.getcwd()):
		if fix_path:
			return fixed_path(os.path.join(os.getcwd(),file_or_dir))
		else:
			return os.path.join(os.getcwd(),file_or_dir)
	for root, dirs, files in os.walk(rootPath):
		if file_or_dir in dirs:
			if fix_path:
				return fixed_path(str(os.path.join(root, file_or_dir)))
			else:
				return str(os.path.join(root, file_or_dir))
		if file_or_dir in files:
			if fix_path:
				return fixed_path(str(os.path.join(root, file_or_dir)))
			else:
				return str(os.path.join(root, file_or_dir))
	return None




# returns a list of strings that are the different paths to all of the instances of a files or folder with the given name
# paths_to("examplefile") == ["/Users/YourUserName/Location1/examplefile","/Users/YourUserName/Location2/examplefile"]
def paths_to(file_or_dir,rootPath = Home, fix_path = True):
	if not is_path(rootPath):
		rootPath = path_to_dir(rootPath)
	answer = []	
	for root, dirs, files in os.walk(rootPath):
		if file_or_dir in dirs:
			if fix_path:
				answer.append(fixed_path(str(os.path.join(root, file_or_dir))))
			else:
				answer.append(str(os.path.join(root, file_or_dir)))
		if file_or_dir in files:
			if fix_path:
				answer.append(fixed_path(str(os.path.join(root, file_or_dir))))
			else:
				answer.append(str(os.path.join(root, file_or_dir)))
	return answer



# creates a folder in the given directory with the given name
# create_folder("foldername") creates a folder called foldername in the current directory/folder
# create_folder("foldername","Desktop")
def create_folder(folder,to_dir = Here()):
	if not is_path(to_dir):
		to_dir = path_to(to_dir)
	if myos == 'Windows':
		if to_dir != None:
			os.system("md " + fixed_path(to_dir + "\\" + folder))
			return fixed_path(to_dir + "\\" + folder)
	else:
		if to_dir != None:
			os.system("mkdir " + fixed_path(to_dir + "/" + folder))
			return fixed_path(to_dir + "/" + folder)


# creates a file given the file name and directory/folder where() it should be created
# if no directory/folder is given, it will be created in the current working directory(i.e. Here())
# create_file("test.txt") == creates a test.txt file in the current working directory/folder
# create_file("test.txt","Desktop") == creates a test.txt file in the Desktop directory/folder
def create_file(file_name_or_path,to_dir = Here()):
	if myos == 'Windows':
		if not is_path(file_name_or_path):
			if not is_path(to_dir):
				to_dir = path_to(to_dir)
			file_name_or_path = fixed_path(to_dir + "\\" + file_name_or_path)
		if file_name_or_path != None:
			os.system("fsutil file createnew " + file_name_or_path + " 1000")
			return file_name_or_path
	else:
		if not is_path(file_name_or_path):
			if not is_path(to_dir):
				to_dir = path_to(to_dir)
			file_name_or_path = fixed_path(to_dir + "/" + file_name_or_path)
		if file_name_or_path != None:
			os.system("touch " + file_name_or_path)
			return file_name_or_path


# reads in the contents of a file and returns it as a string
# unless the file is a .csv, in which case a 2d array will be returned
# read_file("file_name.txt") == the data saved in file_name.txt
def read_file(file_name_or_path):
	if file_name_or_path in contents_of(Here()):
		file_name_or_path = fixed_path(os.path.join(Here(),file_name_or_path))
	if len(file_name_or_path) > 4 and file_name_or_path[-4:] == ".csv":
		if not is_path(file_name_or_path):
			file_name_or_path = path_to(file_name_or_path)
		data = list(csv.reader(open(file_name_or_path)))
		return data
	if not is_path(file_name_or_path):
		with open(path_to(file_name_or_path), 'r') as myfile: 
			data = myfile.read()
		return data
	else:
		with open(file_name_or_path, 'r') as myfile: 
			data = myfile.read()
		return data

# rewrites the data stored in a given file
# write_file("file_name.txt","new content") == resets to data stored in file_name.txt to be "new content"
def write_file(file_name_or_path, content):
	if file_name_or_path in contents_of(Here()):
		file_name_or_path = os.path.join(Here(),file_name_or_path)
	if len(file_name_or_path) > 4 and file_name_or_path[-4:] == ".csv" and type(content) == list:
		to_write = ''
		for line in content:
			to_write += ",".join(str(line)) + '\n'
		content = to_write
	if not is_path(file_name_or_path):
		with open(path_to(file_name_or_path), 'w') as myfile: 
			myfile.write(content)
	else:
		with open(file_name_or_path, 'w') as myfile: 
			myfile.write(content)


# adds text to the end of a file
# example: update_file("file.txt","this will be added to the end")
def update_file(file_name_or_path,content):
	if file_name_or_path in contents_of(Here()):
		file_name_or_path = os.path.join(Here(),file_name_or_path)
	if not is_path(file_name_or_path):
		file_name_or_path = path_to_file(file_name_or_path)
	cur_content = read_file(file_name_or_path)
	if len(file_name_or_path) > 4 and file_name_or_path[-4:] == ".csv" and type(content) == list and type(cur_content) == list:
		for i in range(len(content)):
			content[i] = str(content[i])
		write_file(file_name_or_path,cur_content + [content])
	else:
		write_file(file_name_or_path,cur_content + content)


# deletes a specified file
def delete_file(file_name_or_path):
	if file_name_or_path in contents_of(Here()):
		file_name_or_path = os.path.join(Here(),file_name_or_path)
	if myos == 'Windows':
		if not is_path(file_name_or_path):
			file_name_or_path = path_to_file(file_name_or_path)
			if file_name_or_path != None:
				os.system("del " + file_name_or_path)
		else:
			os.system("del " + file_name_or_path)
	else:
		if not is_path(file_name_or_path):
			file_name_or_path = path_to_file(file_name_or_path)
			if file_name_or_path != None:
				os.system("rm " + file_name_or_path)
		else:
			os.system("rm " + file_name_or_path)

def delete_folder(folder_or_path):
	if folder_or_path in contents_of(Here()):
		folder_or_path = os.path.join(Here(),folder_or_path)
	if myos == 'Windows':
		if not is_path(folder_or_path):
			folder_or_path = path_to_dir(folder_or_path)
			if folder_or_path != None:
				os.system("rmdir /Q /S " + folder_or_path)
		else:
			os.system("rmdir /Q /S " + folder_or_path)
	else:
		if not is_path(folder_or_path):
			folder_or_path = path_to_dir(folder_or_path)
			if folder_or_path != None:
				os.system("rm -r " + folder_or_path)
		else:
			os.system("rm -r " + folder_or_path)


def move_file(file_name_or_path,to_dir):
	if file_name_or_path in contents_of(Here()):
		file_name_or_path = fixed_path(os.path.join(Here(),file_name_or_path))
	if myos == 'Windows':
		if not is_path(file_name_or_path):
			file_name_or_path = path_to(file_name_or_path)
		if not is_path(to_dir):
			to_dir = path_to(to_dir)
		if to_dir != None and file_name_or_path != None:
			os.system("move " + file_name_or_path + " " + to_dir)
	else:
		if not is_path(file_name_or_path):
			file_name_or_path = path_to(file_name_or_path)
		if not is_path(to_dir):
			to_dir = path_to(to_dir)
		if to_dir != None and file_name_or_path != None:
			os.system("mv " + file_name_or_path + " " + to_dir)

def move_folder(folder_or_path,to_dir):
	if folder_or_path in contents_of(Here()):
		folder_or_path = fixed_path(os.path.join(Here(),folder_or_path))
	if myos == 'Windows':
		if not is_path(folder_or_path):
			folder_or_path = path_to(folder_or_path)
		if not is_path(to_dir):
			to_dir = path_to(to_dir)
		if to_dir != None and folder_or_path != None:
			os.system("move " + folder_or_path + " " + to_dir)
	else:		
		if not is_path(folder_or_path):
			folder_or_path = path_to(folder_or_path)
		if not is_path(to_dir):
			to_dir = path_to(to_dir)
		if to_dir != None and folder_or_path != None:
			os.system("mv " + folder_or_path + " " + to_dir)


def rename_file(file_name_or_path, new_name):
	if myos == 'Windows':
		if not is_path(file_name_or_path) and file_name_or_path not in Here():
			file_name_or_path = path_to(file_name_or_path)
		os.system("rename " + file_name_or_path + " " + new_name)
	else:
		if not is_path(file_name_or_path):
			file_name_or_path = path_to(file_name_or_path)
		os.system("mv " + file_name_or_path + " " + "/".join(file_name_or_path.split("/")[:-1]) + "/" + new_name)


def rename_folder(folder_name_or_path, new_name):
	if myos == 'Windows':
		if not is_path(folder_name_or_path) and file_name_or_path not in Here():
			folder_name_or_path = path_to(folder_name_or_path)
		os.system("move " + folder_name_or_path + " " + new_name)

	if not is_path(folder_name_or_path):
		folder_name_or_path = path_to(folder_name_or_path)
	os.system("mv " + folder_name_or_path + " " + "/".join(folder_name_or_path.split("/")[:-1]) + "/" + new_name)



def open_file(file_name_or_path):
	if file_name_or_path in contents_of(Here()):
		file_name_or_path = fixed_path(os.path.join(Here(),file_name_or_path))
	if not is_path(file_name_or_path):
		file_name_or_path = path_to(file_name_or_path)
	if file_name_or_path != None:
		if myos == 'Windows':
			os.system(file_name_or_path)
		else:
			os.system("open " + file_name_or_path)


def get_files(kind,path = Here()):
	if not is_path(path):
		path = path_to(path)
	files = []
	if path != None:
		for file in contents_of(path):
			if kind.lower() in file.lower():
				files.append(file)
	return files


def find_files(kind,path = Home):
	if not is_path(path):
		path = path_to(path)
	answer = []
	rootPath = path
	pattern = kind
	for root, dirs, files in os.walk(rootPath):
		for filename in files:
			if kind.lower() in filename.lower():
				answer.append(fixed_path(str(os.path.join(root, filename))))
	return answer



def copy_file(file_name_or_path,to_dir = Here()):
	if file_name_or_path in contents_of(Here()):
		file_name_or_path = os.path.join(Here(),file_name_or_path)
	if myos == 'Windows':
		if not is_path(file_name_or_path):
			file_name_or_path = path_to(file_name_or_path)
		if not is_path(to_dir):
			to_dir = path_to(to_dir)
		if file_name_or_path != None:
			os.system("copy " + file_name_or_path + " " + to_dir)
	else:
		if not is_path(file_name_or_path):
			file_name_or_path = path_to(file_name_or_path)
		if not is_path(to_dir):
			to_dir = path_to(to_dir)
		if file_name_or_path != None:
			os.system("cp " + file_name_or_path + " " + to_dir)

def copy_folder(folder_name_or_path,to_dir = Here()):
	if folder_name_or_path in contents_of(Here()):
		folder_name_or_path = fixed_path(os.path.join(Here(),folder_name_or_path))

	if myos == 'Windows':
		if not is_path(folder_name_or_path):
			folder_name_or_path = path_to(folder_name_or_path)
		if not is_path(to_dir):
			to_dir = path_to(to_dir)
		if folder_name_or_path != None:
			copyname = folder_name_or_path.split("\\")[-1]
			create_folder(copyname,to_dir)
			os.system("xcopy /E " + folder_name_or_path + " " + to_dir + "\\" + copyname)
	else:
		if not is_path(folder_name_or_path):
			folder_name_or_path = path_to_dir(folder_name_or_path)
		if not is_path(to_dir):
			to_dir = path_to_dir(to_dir)
		if folder_name_or_path != None:
			os.system("cp -r " + folder_name_or_path + " " + to_dir)




def fix_names(folder_or_path):
	if not is_path(folder_or_path):
		folder_or_path = path_to(folder_or_path)
	files = files_in(folder_or_path)
	folders = folders_in(folder_or_path)
	if files != None:
		for item in files:
			rename_file(fixed_path(os.path.join(folder_or_path,item)),item.replace(" ","_").replace("(","_").replace(")","_"))

	if folders != None:
		for item in folders:
			rename_folder(fixed_path(os.path.join(folder_or_path,item)),item.replace(" ","_").replace("(","_").replace(")","_"))

# returns to date last modified for the given file. 
def file_date(file_name_or_path):
	if not is_path(file_name_or_path):
		file_name_or_path = path_to(file_name_or_path)
	return float_to_date(os.path.getmtime(file_name_or_path))














class memory:
	def __init__(self,file_name = "memory",file_location = Here(),start_data = None):
		if not is_path(file_location):
			file_location = path_to(file_location)
		self.data = start_data
		self.file_name = file_name + ".txt"
		self.file_location = file_location
		self.file_path = os.path.join(self.file_location,self.file_name)
		if self.file_name not in contents_of(self.file_location):
			create_file(self.file_path)
			self.save()
		else:
			self.data = eval(read_file(self.file_path))
		atexit.register(self.save)

	def __getattr__(self,name):
		def method(*args):
			print("try using memory.data." + name + " instead")
		return method

	def save(self):
		write_file(self.file_path,str(self.data.__repr__()))

	def load(self):
		self.data = eval(read_file(self.file_path))

	def set(self,val):
		self.data = val
		# self.save()

	def is_new(self):
		return self.data == None

	def is_empty(self):
		return self.is_new()

	def __repr__(self):
		return self.data.__repr__()

	def __str__(self):
		return str(self.data)

	def __int__(self):
		return int(self.data)

	def __float__(self):
		return float(self.data)

	def __getitem__(self,i):
		self.set(self.data)
		return self.data[i]

	def __setitem__(self,i,value):
		if type(i) == int and self.data == None:
			self.data = []
		if type(i) == str and self.data == None:
			self.data = {}
		self.data[i] = value
		self.set(self.data)

	def __len__(self):
		return len(self.data)

	def __ior__(self,val):
		self.set(val)
		return self

	def type(self):
		return type(self.data)

	def __eq__(self,other):
		if type(other) == memory:
			return self.data == other.data
		else:
			return self.data == other

	def __lt__(self,other):
		if type(other) == memory:
			return self.data < other.data
		else:
			return self.data < other

	def __gt__(self,other):
		if type(other) == memory:
			return self.data > other.data
		else:
			return self.data > other


	def __add__(self,other):
		if type(other) == memory:
			return self.data + other.data
		else:
			return self.data + other

	def __radd__(self,other):
		if type(other) == memory:
			return self.other + self.data
		else:
			return other + self.data

	def __iadd__(self,other):
		if self.data == None and type(other) == int or self.data == None and type(other) == float:
			self.data = 0
		if self.data == None and type(other) == list:
			self.data = []
		if type(other) == memory:
			self.set(self.data + other.data)
			return self
		else:
			self.set(self.data + other)
			return self


	def __sub__(self,other):
		if type(other) == memory:
			return self.data - other.data
		else:
			return self.data - other

	def __rsub__(self,other):
		if type(other) == memory:
			return self.other - self.data
		else:
			return other - self.data

	def __isub__(self,other):
		if self.data == None and type(other) == int or self.data == None and type(other) == float:
			self.data = 0
		if type(other) == memory:
			self.set(self.data - other.data)
			return self
		else:
			self.set(self.data - other)
			return self



	def __mul__(self,other):
		if type(other) == memory:
			return self.data * other.data
		else:
			return self.data * other

	def __rmul__(self,other):
		if type(other) == memory:
			return self.other * self.data
		else:
			return other * self.data

	def __imul__(self,other):
		if type(other) == memory:
			self.set(self.data * other.data)
			return self
		else:
			self.set(self.data * other)
			return self



	def __truediv__(self,other):
		if type(other) == memory:
			return self.data / other.data
		else:
			return self.data / other

	def __rtruediv__(self,other):
		if type(other) == memory:
			return self.other / self.data
		else:
			return other / self.data

	def __itruediv__(self,other):
		if type(other) == memory:
			self.set(self.data / other.data)
			return self
		else:
			self.set(self.data / other)
			return self

	def keys(self):
		if self.data == None:
			self.data = {}
			# self.save()
			return []
		if self.data == {}:
			return []
		return list(self.data.keys())

	def items(self):
		if self.data == None:
			self.data = {}
			# self.save()
			return []
		if self.data == {}:
			return []
		return list(self.data.items())

	def values(self):
		if self.data == None:
			self.data = {}
			return []
		if self.data == {}:
			return []
		vals = []
		for key, value in self.items():
			vals.append(value)
		return vals

	def contains(self,item):
		if self.data == None:
			self.data = {}
			return False
		if self.data == {}:
			return False
		if item in self.keys():
			return True
		else:
			return False

	def key_with_val(self,val): 
		if self.data == None:
			self.data = {}
		for key, value in self.items(): 
			if val == value: 
				return key 
		return None

	def keys_with_val(self,val):
		if self.data == None:
			self.data = {}
		keys = []
		for key, value in self.items(): 
			if val == value: 
				keys += [key]
		if len(keys) > 0:
			return keys
		else: 
			return None

	def average(self):
		if self.type() == dict:
			vals = self.values()
			total = len(vals)
			s = sum(vals)
			return s/total
		if self.type() == list or self.type == tuple:
			s = sum(self.data)
			t = len(self.data)
			return s/t

	def max(self):
		if self.type() == dict:
			val = max(self.values())
			key = self.key_with_val(val)
			return (key,val)
		if self.type() == list or self.type() == tuple:
			return max(self.data)

	def min(self):
		if self.type() == dict:
			val = min(self.values())
			key = self.key_with_val(val)
			return (key,val)
		if self.type() == list or self.type() == tuple:
			return min(self.data)

	def append(self,item):
		if self.data == None:
			self.data = []
		self.data.append(item)
		# self.save()

	def pop(self,i):
		if self.data == None:
			self.data = []
		return self.data.pop(i)

	def remove(self,index):
		if index == len(self.data) - 1 or index == -1:
			self.set(self.data[:-1])
		elif index == 0:
			self.set(self.data[1:])
		else:
			self.set(self.data[0:index] + self.data[index + 1:])

	def insert(self,item,index):
		if self.type() == list:
			if index == 0:
				self.set([item] + self.data)
			elif index == len(self.data):
				self.append(item)
			else:
				self.set(self.data[:index] + [item] + self.data[index:])
		if self.type() == str:
			if index == 0:
				self.set(item + self.data)
			elif index == len(self.data):
				self.set(self.data + item)
			else:
				self.set(self.data[:index] + item + self.data[index:])


	def split(self,by = " "):
		return self.data.split(by)

	def join(self,by = " "):
		return by.join(self.data)

	def sort(self,funct = None,rev = False):
		if funct == None:
			self.data.sort(reverse = rev)
			# self.save()
		else:
			self.data.sort(reverse = rev,key = funct)
			# self.save()


	def lower(self):
		return self.data.lower()

	def upper(self):
		return self.data.upper()

	def replace(self,this,that):
		return self.data.replace(this,that)



































#_______________________________________________________FILE AND FOLDER/DIRECTORY MANIPULATION

