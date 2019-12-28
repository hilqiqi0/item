from cryptography.fernet import Fernet
import datetime
#cipher_key = Fernet.generate_key()
cipher_key = b"awhPia_uJT97kMQbkv95rWsOKkHRpSoXf6azl27qoGI="
#print(cipher_key)
cipher = Fernet(cipher_key)
mac_string = "7440bb1d232c"
mac_string = "c4b301c5e990"
#mac_string = "d5636dae740b"
mac_string = "bf2d5ced8350"
mac_string = input("输入电脑信息：")
time_string = datetime.datetime.now().strftime('%Y-%m-%d')
text = mac_string + time_string + "2310775309"
#print(text)
encrypted_text = cipher.encrypt(text.encode())
#print(encrypted_text)
print(bytes.decode(encrypted_text))

decrypted_text = cipher.decrypt(encrypted_text)
#print(decrypted_text)
input("回车结束")