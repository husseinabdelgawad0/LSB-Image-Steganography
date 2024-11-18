class User:
    """
    Class For Users, Attributes Are Username,Password, And Key (Used In Modification And Extraction Process)
    """
    #Array For Storing Users
    user_list=[] 

    def __init__(self,username):
        """
        Initializes User Parameters
        """
        self.username=username
        self.password=''
        self.key=""
        
    def set_key(self): 
        """
        Sets Key For Choosing Colour Channel To Edit In Image Pixels
        """
        key=int(input("Which is Your Favourite Fruit?\n1)Apple\n2)Pear\n3)Berries\n"))
        if key == 1:
            self.key="r"
        elif key == 2:
            self.key='g'
        elif key == 3:
            self.key="b"
        else:
            raise ValueError("Invalid Choice")
            
    def set_password(self, password):
        """
        Parameters: Password(Password User Wants To Set) 
        Ensures It Is Strong, Then Sets It For User
        """
        while len(password) < 8:
            print("Set a longer password")
            password=input("Enter Password: ")
        special = "!@#$%^&*()_+{}:<>?/[]"
        while not any(char in special for char in password):
            print("Include at least 1 special character")
            password=input("Enter Password: ")
        self.password = password

    def verify_user(self, username, password):
        """
        Parameters: username(User's username), password(User's Password)
        Checks If User Is Registered, And If Credentials Are Correct
        Returns: True(If Verification Succeeds), False(If It Fails)
        """
        for user in User.user_list:
            if user.username == username and user.password == password:
                print("Successful Verification")
                return True
        print("Invalid Credentials")
        return False

class Image:
    """
    Class For Image, Attributes Are Path and Receiver
    """
    def __init__(self,path,receiver):
        """
        Intializes Image Parameters
        """
        self.path=path
        self.receiver=receiver

def encode(message):
    """
    Parameter: message (Text To Be Encoded)
    Translates Text Into Binary
    Returns: binary_message (Binary Value Of Text)
    """
    while message=="":
        message=input("Please Enter A Valid Message: ")
    binary_message = ''
    for char in message:
        #Character's Ascii Value
        ascii_value = ord(char)
        binary = ''
        while ascii_value > 0:
            remainder = ascii_value % 2
            binary = str(remainder) + binary
            ascii_value //= 2
        #To Ensure Each Character Is Represented In 8 Bits
        binary = binary.zfill(8) 
        binary_message += binary
    #Checks If Encoding Is Correctly Performed
    if len(binary_message)%8 != 0:
        print("Incorrect Encoding, Try Again")
        return 
    return binary_message.strip()


def decode(binary):
    """
    Parameter: binary(Binary Value To Be Decoded)
    Translates Binary Into Text
    Returns: message(text message after being decoded)
    """
    binary.replace(" ","")
    message=""
    #Collects Each 8 Bits As A Byte
    for index in range(0,len(binary),8):
        byte=binary[index:index+8]
        ascii_value=int(byte,2)
        message+=chr(ascii_value)
    return message

def modify(path,binary,key):
    """
    Parameters: path(Image Path), binary(Binary Value Of Text), key(Color Channel Of Insertion)
    Alters LSB Bit Of Chosen Colour Channel
    Returns: new_path(New Image Path), index(Number Of Bits Inserted)
    """
    index=0
    try:
        with open(path,'rb') as file:
            pixels=bytearray(file.read())
            if len(binary)>len(pixels):
                print("Message Too Long")
                return path,0
            #Skips Header 
            for i in range(54,len(pixels)):
                #Checks If End Of File Is Reached
                if index<len(binary):
                    if key=="b":
                        #Sets Blue LSB Into Value Of binary[index]
                        pixels[i]= (pixels[i] & ~1) | int(binary[index])
                        index+=1
                    if key=="g":
                        #Sets Green LSB Into Value Of binary[index]
                        pixels[i+1]= (pixels[i+1] & ~1) | int(binary[index])
                        index+=1
                    if key=="r":
                        #Sets Red LSB Into Value Of binary[index]
                        pixels[i+2]= (pixels[i+2] & ~1) | int(binary[index])
                        print(f"{binary[index]} added to red bit")
                        index+=1
        file.close()
    #Handling If File Is Not Found
    except FileNotFoundError:
        raise FileNotFoundError(f"File {path} Does Not Exist")
    #Path Of Image After Modification
    new_path=r"C:\Users\nerme\Downloads\New_OLY.bmp"
    try:
        with open(new_path,'wb') as new_file:
            new_file.write(pixels)
        new_file.close()
    except IOError:
        raise IOError(f"File Writing Process Error")
    return new_path,index

def extract(path,num_bits,key):
    """
    Parameters: path(Image's Path), num_bits(Number Of Bits To Be Extracted, key(color channel of extraction)
    Extracts LSB Bit Of Chosen Colour Channel
    Returns: binary(Binary Message Extracted)
    """
    index=0
    binary=""
    try:
        with open(path,'rb') as file:
            pixels=bytearray(file.read())
            #Skips File Header
            for i in range(54,len(pixels)):
                #Checks If Wanted Number Of Bits Is Reached
                if index<num_bits:
                    if key=="b":
                        #Concatenates Blue LSB Value into binary
                        binary+=str(pixels[i]&1)
                        index+=1
                    if key=="g":
                        #Concatenates Green LSB Value into binary
                        binary+=str(pixels[i+1]&1)
                        index+=1
                    if key=="r":
                        #Concatenates Red LSB Value into binary
                        binary+=str(pixels[i+2]&1)
                        index+=1
                else:
                    break
    except FileNotFoundError:
        print("File Not Found")
    file.close()
    #Checks For Correct Number Of Extractions
    if len(binary)%8 != 0:
        print("Error In Bit Extraction, Try Again")
    return binary

#Users Initialization
name=input("Enter Username Or -1 To Terminate: ")
while name != "-1":
    sender=User(name)
    sender.set_password(input("Enter Password: "))
    sender.set_key()
    User.user_list.append(sender)
    name = input("Enter Username Or -1 To Terminate: ")


#Image Creation
path=input("Enter Image Path: ").strip('"').strip("'")
receiver_name=input("Enter Receiver's Username, (Has To Be Registered Before): ")
receiver=User(receiver_name)
image=Image(path,receiver_name)

#Encoding Text & Modifying Bits
message=""
while message != "":
    message=input("Enter Message To Be Encoded: ")
binary=encode(message)
new_path,num_modified_bits=modify(image.path,binary,sender.key)

#Verification Of Receiver For Extracting bits
password=input("Enter Receiver's Password: ")
receiver.set_key()
receiver.set_password(password)
if sender.verify_user(receiver.username,receiver.password):
    text=extract(new_path,num_modified_bits,receiver.key)

#Decoding Binary
message=decode(text)
print(message)
