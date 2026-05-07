from pydantic import BaseModel


class AddItem(BaseModel):
    first: int
    second: int

    def add(self):
        return self.first + self.second
