from abc import ABC, abstractmethod


class INode(ABC):
    @abstractmethod
    def check_password(self, password: str) -> bool:
        pass

class ANode(INode):
    def __init__(self, next: INode=None):
        self.next = next

    @abstractmethod
    def true_check(self, password: str) -> bool:
        pass

    def check_password(self, string: str) -> bool:
        result = self.true_check(string)
        if self.next and result:
            return self.next.check_password(string)
        return result

class LengthNode(ANode):
    min_length = 1
    max_length= 50
    def true_check(self, string: str) -> bool:
        return  self.min_length <= len(string) <= self.max_length

class ValidCharsNode(ANode):
    invalid_chars = "!@#$%^&*()_+=~ <>?/\|[]{};:"
    def true_check(self, string: str) -> bool:
        return not any(char in self.invalid_chars for char in string)

class RegisterNode(ANode):
    def true_check(self, password: str) -> bool:
        return not password.islower() and not password.isupper()
