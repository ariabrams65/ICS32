import nacl.utils, json, os, copy
from nacl.public import PrivateKey, PublicKey, Box
from Profile import Profile, Post
from NaClDSEncoder import NaClDSEncoder
from pathlib import Path

class NaClProfile(Profile):
    def __init__(self, dsuserver=None, username=None, password=None):
        '''
        Generates all class variables and populates the keys.
        '''
        super().__init__(dsuserver, username, password)
        
        self.generate_keypair()

        

    def generate_keypair(self) -> str:
        '''
        Generates a new public encryption key using NaClDSEncoder.
        Returns keypair    
        '''
        encoder = NaClDSEncoder()
        encoder.generate()
        
        self.public_key = encoder.public_key
        self.private_key = encoder.private_key
        self.keypair = encoder.keypair

        return self.keypair

    

    def import_keypair(self, keypair: str):
        '''
        Imports an existing keypair. Useful when keeping encryption keys in a location other than the
        dsu file created by this class.
        '''
        self.keypair = keypair
        
        keys = keypair.split("=")
        self.public_key = keys[0] + "="
        self.private_key = keys[1] + "="
        


    def add_post(self, post: Post) -> None:
        '''
        Encrypts post and adds it to _posts.
        '''
        bencrypted_msg = self._encrypt(post.get_entry(), self.public_key).decode(encoding='UTF-8')
        post.set_entry(bencrypted_msg)
        super().add_post(post)



    def get_posts(self) -> list:
        '''
        Returns list of decrypted posts.
        '''
        posts = copy.deepcopy(super().get_posts()) #creates a copy to keep _posts unaffected

        encoder = NaClDSEncoder()
        box = Box(encoder.encode_private_key(self.private_key), encoder.encode_public_key(self.public_key))

        for post in posts:
            bencrypted_message = post.get_entry().encode(encoding='UTF-8')

            bmsg = box.decrypt(bencrypted_message, encoder=nacl.encoding.Base64Encoder)
            msg = bmsg.decode(encoding='UTF-8')
            post.set_entry(msg)

        return posts

    

    def load_profile(self, path: str) -> None:
        '''
        load_profile will populate the current instance of Profile with data stored in a DSU file.
        '''
        p = Path(path)

        if os.path.exists(p) and p.suffix == '.dsu':
            try:
                f = open(p, 'r')
                obj = json.load(f)
                self.username = obj['username']
                self.password = obj['password']
                self.dsuserver = obj['dsuserver']
                self.bio = obj['bio']
                self.public_key = obj['public_key']
                self.private_key = obj['private_key']
                self.keypair = obj['keypair']
                
                for post_obj in obj['_posts']:
                    post = Post(post_obj['entry'], post_obj['timestamp'])
                    self._posts.append(post)
                f.close()
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()

    def encrypt_entry(self, entry:str, public_key:str) -> bytes:
        '''
        Used to encrypt messages using a 3rd party public key.
        '''
        return self._encrypt(entry, public_key)

    

    def _encrypt(self, msg:str, public_key:str) -> bytes:
        '''
        Returns the message encrypted with the given key as bytes.
        '''
        encoder = NaClDSEncoder()
        
        bmsg = msg.encode(encoding='UTF-8')
        box = Box(encoder.encode_private_key(self.private_key), encoder.encode_public_key(public_key))

        return box.encrypt(bmsg, encoder=nacl.encoding.Base64Encoder)



        
        
