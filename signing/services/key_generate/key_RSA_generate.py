from Crypto.PublicKey import RSA

def generate_keys(public_key_location,private_key_location):
    key = RSA.generate(4096)

    private_key = key.exportKey()

    with (open(private_key_location, "wb")) as file:
        file.write(private_key)

    public_key = key.public_key().exportKey()

    with (open(public_key_location, "wb")) as file:
        file.write(public_key)



