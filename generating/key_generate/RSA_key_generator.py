from Crypto.PublicKey import RSA

##
# @brief Generate public/private key pairs.
#
# @details The function reads locations for public and private keys, keys generated with RSA algorithm.
#
# @param public_key_location Path to save generated a public key
# @param private_key_location Path to save generated a private key
#
# @return True if RSA generation was successful; False if the RSA generation thrown exception.
#
def generate_keys(public_key_location: str, private_key_location: str) -> bool:
    try:
        key = RSA.generate(4096)

        private_key = key.exportKey()

        with (open(private_key_location, "wb")) as file:
            file.write(private_key)

        public_key = key.public_key().exportKey()

        with (open(public_key_location, "wb")) as file:
            file.write(public_key)

        return True

    except Exception as e:
        print(e)
        return False
