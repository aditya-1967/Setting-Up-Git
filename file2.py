import random
from collections import defaultdict
import datetime

class User:
    def __init__(self, username):
        self.username = username
        self.friends = set()
        self.messages = []
        self.groups = set()

    def send_message(self, recipient, content):
        timestamp = datetime.datetime.now()
        message = Message(sender=self.username, recipient=recipient.username, content=content, timestamp=timestamp)
        self.messages.append(message)
        recipient.messages.append(message)
        print(f"{self.username} sent a message to {recipient.username}: {content}")

    def add_friend(self, friend):
        if friend != self and friend not in self.friends:
            self.friends.add(friend)
            friend.friends.add(self)
            print(f"{self.username} and {friend.username} are now friends!")

    def join_group(self, group):
        self.groups.add(group)
        group.add_member(self)
        print(f"{self.username} joined the group '{group.name}'")

    def __repr__(self):
        return f"User({self.username})"

class Group:
    def __init__(self, name):
        self.name = name
        self.members = set()

    def add_member(self, user):
        if user not in self.members:
            self.members.add(user)

    def send_group_message(self, sender, content):
        if sender in self.members:
            for member in self.members:
                if member != sender:
                    sender.send_message(member, f"(Group: {self.name}) {content}")
            print(f"{sender.username} sent a message to group '{self.name}': {content}")
        else:
            print(f"{sender.username} is not a member of '{self.name}' group!")

    def __repr__(self):
        return f"Group({self.name})"

class Message:
    def __init__(self, sender, recipient, content, timestamp):
        self.sender = sender
        self.recipient = recipient
        self.content = content
        self.timestamp = timestamp

    def __repr__(self):
        return f"[{self.timestamp}] {self.sender} -> {self.recipient}: {self.content}"

class SocialNetwork:
    def __init__(self):
        self.users = {}
        self.groups = {}

    def add_user(self, username):
        if username not in self.users:
            self.users[username] = User(username)
            print(f"User '{username}' added to the network.")

    def add_group(self, group_name):
        if group_name not in self.groups:
            self.groups[group_name] = Group(group_name)
            print(f"Group '{group_name}' created.")

    def get_user(self, username):
        return self.users.get(username)

    def get_group(self, group_name):
        return self.groups.get(group_name)

    def connect_users(self, username1, username2):
        user1 = self.get_user(username1)
        user2 = self.get_user(username2)
        if user1 and user2:
            user1.add_friend(user2)

    def simulate_activity(self, num_actions=10):
        """Simulates random interactions between users."""
        for _ in range(num_actions):
            action_type = random.choice(["message", "friend", "group_message"])
            user = random.choice(list(self.users.values()))

            if action_type == "message" and user.friends:
                recipient = random.choice(list(user.friends))
                content = f"Hello, {recipient.username}!"
                user.send_message(recipient, content)

            elif action_type == "friend":
                potential_friend = random.choice(list(self.users.values()))
                if potential_friend != user:
                    user.add_friend(potential_friend)

            elif action_type == "group_message" and user.groups:
                group = random.choice(list(user.groups))
                content = f"Hi everyone in {group.name}!"
                group.send_group_message(user, content)

# Create the social network and add users
network = SocialNetwork()
for username in ["Alice", "Bob", "Charlie", "Dana", "Eve"]:
    network.add_user(username)

# Connect users randomly as friends
network.connect_users("Alice", "Bob")
network.connect_users("Alice", "Charlie")
network.connect_users("Bob", "Dana")
network.connect_users("Dana", "Eve")

# Add groups and have users join
network.add_group("Developers")
network.add_group("Designers")

network.get_user("Alice").join_group(network.get_group("Developers"))
network.get_user("Bob").join_group(network.get_group("Developers"))
network.get_user("Charlie").join_group(network.get_group("Designers"))
network.get_user("Dana").join_group(network.get_group("Designers"))

# Simulate random activity in the network
print("\n--- Simulating random activity ---")
network.simulate_activity(num_actions=10)

# Display messages in the network
print("\n--- Messages in the network ---")
for user in network.users.values():
    print(f"\nMessages for {user.username}:")
    for message in user.messages:
        print(message)
