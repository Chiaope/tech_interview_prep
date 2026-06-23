class MyParent:
    __secret = "Parent Secret"

    def get_secret(self):
        return self.__secret

    def set_secret(self, new_secret):
        self.__secret = new_secret

    def __secret_method(self):
        print("Parent Secret Method")

    def access_secret_method(self):
        self.__secret_method()

    def _protected_method(self):
        print("Parent Protected Method")


class MyChild(MyParent):
    __secret = "Child Secret"
    _protected = "Child Protected"

    def get_parent_secret(self):
        return super().get_secret()

    def set_parent_secret(self, new_secret):
        return super().set_secret(new_secret)

    def access_parent_secret_method(self):
        super().access_secret_method()

    def _parent_protected_method(self):
        super()._protected_method()

    def get_secret(self):
        return self.__secret

    def set_secret(self, new_secret):
        self.__secret = new_secret

    def __secret_method(self):
        print("Child Secret Method")

    def access_secret_method(self):
        self.__secret_method()

    def _protected_method(self):
        print("Child Protected Method")


if __name__ == "__main__":
    child = MyChild()
    print(child.get_secret())  # output: Child Secret
    print(child.get_parent_secret())  # output: Parent Secret
    print(child._protected)  # output: Child Protected
    child.access_secret_method()  # output: Child Secret Method
    child.access_parent_secret_method()  # output: Parent Secret Method
    child._protected_method()  # output: Child Protected Method
    child._parent_protected_method()  # output: Parent Protected Method
    try:
        print(child.__secret)
    except Exception as e:
        print(e)  # output: 'MyChild' object has no attribute '__secret'
        print(child._MyChild__secret)  # output: Child Secret

    try:
        child.__secret_method()
    except Exception as e:
        print(e)  # output: 'MyChild' object has no attribute '__secret_method'
        child._MyChild__secret_method() # output: Child Secret Method

    child.set_secret("Child New Secret")
    child.set_parent_secret("Parent New Secret")
    print(child.get_secret())  # output: Child New Secret
    print(child.get_parent_secret())  # output: Parent New Secret
    child._protected = "Child New Protected"
    print(child._protected)  # output: Child New Protected
