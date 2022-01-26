import binascii
import struct
from time import sleep

import libzkfp
class FingerPrint(object):

    db=None
    @classmethod
    def init_db(cls):
        if not cls.db:
            libzkfp.zkfp_init()
            cls.db=libzkfp.db_init()

    @classmethod
    def close_db(cls):
        if cls.db:
            libzkfp.db_close(cls.db)
            libzkfp.zkfp_terminate()


    @classmethod
    def re_init(cls):
        libzkfp.zkfp_init()


    def __init__(self, *args, **kwargs):
        self.device=None
        self.height=None
        self.width=None
        self.dpi=None
        self.image_buffer=None
        self.template_buffer_length = 2048
        self.template_buffer=bytearray(self.template_buffer_length)
        libzkfp.zkfp_init()

    def available_devices(self):
        return libzkfp.get_device_count()

    def is_connected(self):
        return self.device

    def open_device(self,device:int):
        if self.device:
            libzkfp.close_device(self.device)
        self.device = libzkfp.open_device(device)
        self.width=self.get_parameters(1)
        self.height=self.get_parameters(2)
        self.get_capture_params_ex()
        self.image_buffer=bytearray(self.width * self.height)
        self.template_buffer=bytearray(self.template_buffer_length)

    def close_device(self):
        if self.device:
            libzkfp.close_device(self.device)
            libzkfp.zkfp_terminate()
            self.device=None

    def __del__(self):
        self.close_device()

    def get_parameters(self,param_code:int):
        param_value=bytearray(4)
        param_value,_=libzkfp.get_parameters(self.device, param_code, param_value, cb_param_value=4)
        if not _ == 0:
            raise Exception(f"Device Return {_} expected code is 0")
        return struct.unpack('h', param_value)[0]

    def get_capture_params_ex(self):
        width,height,dpi=0,0,0
        width,height,self.dpi=libzkfp.get_capture_params_ex(self.device,width,height,dpi)


    def get_finger_print_image(self,file,attempts=None):
        if not attempts:
            attempts=10
        print("Reading Finger Print and Saving")
        sleep(1)
        while attempts>=0 :
            result = libzkfp.acquire_finger_print_image(self.device, self.image_buffer, self.width * self.height, )
            if result == 0:
                image = Image.frombytes('L', (self.width, self.height), bytes(self.image_buffer), 'raw')
                image.show()
                image.save(file)
                self.image_buffer = bytearray(self.width * self.height)
                self.template_buffer=bytearray(self.template_buffer_length)
                break
            attempts-=1

    def get_finger_print(self,attempts=None):
        if not attempts:
            attempts=100000
        print("Reading Finger Print")
        sleep(1)
        while attempts>=0 :
            result = libzkfp.acquire_finger_print(self.device, self.image_buffer, self.width * self.height,self.template_buffer,self.template_buffer_length )
            if result == 0:
                template=binascii.hexlify(self.template_buffer).decode('ascii')
                self.image_buffer = bytearray(self.width * self.height)
                self.template_buffer=bytearray(self.template_buffer_length)
                return template
            attempts-=1

    def get_template_from_image(self,path):
        fp_template=bytearray(2048)
        libzkfp.extract_from_image(self.device,bytearray(path.encode()),1,fp_template,2048)
        print(fp_template)
    @classmethod
    def match_finger_templates(cls,template_1,template_2):
        template_1=bytearray(binascii.unhexlify(template_1.encode()))
        template_2=bytearray(binascii.unhexlify(template_2.encode()))
        template_buffer_length=2048
        result = libzkfp.match_templates(cls.db,template_1,template_buffer_length,template_2,template_buffer_length)
        return result