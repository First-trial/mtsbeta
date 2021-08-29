class Category:
    name = "nameCategory"

    @classmethod
    def has_permission(cls, user_id):
        return True

class Minigames(Category):
    name = "minigames"