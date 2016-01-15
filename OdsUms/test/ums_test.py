__author__ = 'ty'

import unittest
from OdsUms.controller import LoginController, AddUserController, GetAllUserController, getOneUserController

class TestLoginController(unittest.TestCase):
    def test_init(self):
        login = LoginController("paul", "123456")
        self.assertEquals(login.username, "paul")
        self.assertEqual(login.password, "123456")

    def test_authenticate(self):
        login = LoginController("paul", "123456")
        self.assertTrue(login.authenticate())

class TestAddUserController(unittest.TestCase):
    def test_init(self):
        add = AddUserController("test01", "123456", "nothing special", "2016-01-01")
        self.assertEqual(add.username, "test01")
        self.assertEqual(add.password, "123456")
        self.assertEqual(add.memo, "nothing special")
        self.assertEqual(add.expire_time, "2016-01-01")

    def test_Validation(self):
        add = AddUserController("test01", "123456", "nothing special", "2016-01-01")
        self.assertTrue(add.usernameValidation())
        self.assertTrue(add.memoValidation())
        self.assertTrue(add.passwordValidation())

    def test_add(self):
        add = AddUserController("test01", "123456", "nothing special", "2016-01-01")
        self.assertTrue(add.addUser())

class TestGetAllUserController(unittest.TestCase):
    def test_getUserInfo(self):
        getAllUser = GetAllUserController()
        self.assertIsNotNone(getAllUser.getUserInfo())

class TestGetOneUserController(unittest.TestCase):
    def test_getUserInfo(self):
        getOneUser = getOneUserController()
        self.assertIsNotNone(getOneUser.getUserInfo(1))

    def test_getUserInfoByName(self):
        getOneUser = getOneUserController()
        self.assertIsNotNone(getOneUser.getUserInfo("taoye"))

    def test_getUserEntitlement(self):
        getOneUser = getOneUserController()
        self.assertIsNotNone(getOneUser.getUserEntitlement(1))

    def test_infoToJson(self):
        getOneUser = getOneUserController()
        self.assertTrue(isinstance(getOneUser.infoToJson(getOneUser.getUserInfoByName("taoye"))))

if __name__ == "__main__":
    unittest.main()

