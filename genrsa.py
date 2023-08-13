from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization


# publicKey, privateKey = rsa.newkeys(
#   public_exponent=65537,
#     key_size=4096,
#     backend=default_backend()
# )

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=4096,
    backend=default_backend()
)
public_key = private_key.public_key()

def write_keys_to_file(public_key, private_key):
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open('public.pem', 'wb') as pub_file:
        pub_file.write(public_pem)

    with open('private.pem', 'wb') as priv_file:
        priv_file.write(private_pem)


message = "Hello World!"
 
encMessage = public_key.encrypt(
    message.encode(),
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
decMessage = private_key.decrypt(encMessage, padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )).decode()

assert message == decMessage

write_keys_to_file(public_key, private_key)

print("Keys generated!")