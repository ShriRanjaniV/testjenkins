import uploader
from unittest import mock, TestCase, main

class Test(TestCase):
    @mock.patch('uploader.create_folder')
    def test_uploader_pass_200(self, create):
        create.return_value = {
                    'status' : 'success',
                    'desc' : '',
                    'result' : {
                        'uid': '1234567890123456'
                    }
                },200   
        response, value = uploader.create_folder()
        assert_value = {'status':'success', 'desc' : '', 'result': {'uid': '1234567890123456'}}
        self.assertEqual(response, assert_value)
        self.assertEqual(value,200)
    
    @mock.patch('uploader.create_folder')
    def test_uploader_fail_201(self, create):
        create.return_value = {
            'status' : 'fail',
            'desc' : 'Error occured while generating UID',
            'result' : {}
            }, 201
        response, value = uploader.create_folder()
        assert_value = {'status':'fail', 'desc' : 'Error occured while generating UID', 'result': {}}
        self.assertEqual(response, assert_value)
        self.assertEqual(value,201)
if __name__ == '__main__':
    main()