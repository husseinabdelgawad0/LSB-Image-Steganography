import unittest
from Latest_Stegano import User,Image,encode,decode,modify,extract
class Tests(unittest.TestCase):

    def Weak_Password(self):
        user=User("Test")
        with self.assertRaises(ValueError):
            user.set_password("Weak")

    def Invalid_Key(self):
        user=User("Test")
        with self.assertRaises(ValueError):
            user.set_key(4)

    def Empty_Message(self):
        with self.assertRaises(ValueError):
            encode("")

    def String_Conversion(self):
        message="TestCase"
        binary=encode(message)
        new_m=decode(binary)
        self.assertEqual(message,new_m)

    def Integer_Conversion(self):
        message=5863
        binary=encode(message)
        new_m=decode(binary)
        self.assertEqual(message,new_m)

    def Float_Conversion(self):
        message=58.63
        binary=encode(message)
        new_m=decode(binary)
        self.assertEqual(message,new_m)

    def All_Type_Conversion(self):
        message="Test,0,Case@_ID_58.63"
        binary=encode(message)
        new_m=decode(binary)
        self.assertEqual(message,new_m)

    def Add_Long_Msg(self):
        path="test.bmp"
        binary="1"*1000000
        key='b'
        new_path,index=modify(path,binary,key)
        self.assertEqual(new_path,path)
        self.assertEqual(index,0)

    def Invalid_Name(self):
        user=User("Me")
        user.set_password("Valid@Pass")
        User.user_list.append(user)
        self.assertFalse(user.verify_user("NotMe","Valid@Pass"))

    def Invalid_Password(self):
        user=User("Me")
        user.set_password("Valid@Pass")
        User.user_list.append(user)
        self.assertFalse(user.verify_user("Me","NotValid@Pass"))

    def Case_Senstivity(self):
        user=User("Me")
        user.set_password("Valid@Pass")
        User.user_list.append(user)
        self.assertFalse(user.verify_user("Me","valid@Pass"))

    def Key_Mismatch(self):
        path="any.bmp"
        key="r"
        num_bits=16
        binary=extract(path,num_bits,key)
        self.assertEqual(binary,"")

    def Modify_Invalid_Path(self):
        path="Invalid.bmp"
        binary="01010101"
        key="r"
        new_path,index=modify(path,binary,key)
        self.assertEqual(new_path,path)
        self.assertEqual(index,0)

    def Extract_Invalid_Path(self):
        path="Invalid.bmp"
        key="b"
        num_bits=8
        binary=extract(path,num_bits,key)
        self.assertEqual(binary,"")

    def Invalid_Format(self):
        path="path.jpg"
        binary="10101010"
        key="g"
        with self.assertRaises(ValueError):
            modify(path,binary,key)

    

        

