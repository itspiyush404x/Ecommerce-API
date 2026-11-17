from ..models import User, Address







def InitUsers():
    user1 = User.objects.create_user(
        username="user1", email="user1@gmail.com", password="pass12345", phone=1234567890
    )
    user2 = User.objects.create_user(
        username="user2", email="user2@gmail.com", password="pass12345"
    )
    return user1, user2

def InitAddress(user):
    ADDRESS_DATA = {
        "name": "Home",
        "phone": "9999999999",
        "address": "12 MG Road",
        "city": "Jaipur",
        "state": "Rajasthan",
        "postal_code": "302001",
    }
    return Address.objects.create(user=user, **ADDRESS_DATA) 