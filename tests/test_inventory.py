from src.common.models import check_inventory


class MockCursor:
    def __init__(self, return_value):
        self.return_value = return_value

    def execute(self, query, params):
        pass

    def fetchone(self):
        return self.return_value


def test_inventory_sufficient():
    cursor = MockCursor((10,))
    assert check_inventory(cursor, "prod-1", 2) == True


def test_inventory_insufficient():
    cursor = MockCursor((1,))
    assert check_inventory(cursor, "prod-1", 5) == False


def test_inventory_not_found():
    cursor = MockCursor(None)
    assert check_inventory(cursor, "prod-x", 2) == False
