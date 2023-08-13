from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import serialization

publicKey, privateKey = rsa.newkeys(
  public_exponent=65537,
    key_size=4096,
    backend=default_backend()
)

def write_keys_to_file(publicKey, privateKey):
    with open('public.pem', 'wb') as pub_file:
        pub_file.write(publicKey.save_pkcs1())

    with open('private.pem', 'wb') as priv_file:
        priv_file.write(privateKey.save_pkcs1())


message = "Hello World!"
 
encMessage = rsa.encrypt(message.encode(),
                         publicKey)
decMessage = rsa.decrypt(encMessage, privateKey).decode()

assert message == decMessage

write_keys_to_file(publicKey, privateKey)

print("Keys generated!")