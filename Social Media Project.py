#Social Media Project 
class Node:
    def __init__(self,key,value):
        self.key = key
        self.value = value
        self.next = None

class HashTable:
    def __init__(self,size=50):
        self.size = size
        self.table = None * size

    def hash(self,key):
        return hash(key) % self.size
    
    def insert(self,key, value):
        index = self._hash(key)
        head = self.table[index]

        current = head
        while current:
            if current.key == key:
                current.value = value
                return
            current = current.next

        new_node = Node(key,value)
        new_node.next = head
        self.table[index] = new_node

    def get(self,key):
        index = self._hash(key)
        current = self.table[index]

        while current:
            if current.key == key:
                return current.value
            current = current.next
        return None
    
    def delete(self,key):
        index = self._hash(key)
        current = self.table[index]
        previous = None

        while current:
            if current.key == key:
                if previous:
                    previous.next = current.next
                else:
                    self.table[index] = current.next
                return True
            previous = current
            current = current.next

        return False
    
#System Clases:
class User:
    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.posts = []
        self.friends = []

    def add_friend(self,username):
        if username not in self.friends:
            self.friends.append(username)

    def add_post(self, content):
        self.posts.append(content)

class Post:
    def __init__(self,author, content, timestamp):
        self.author = author
        self.content = content
        self.timestamp = timestamp

class SocialMediaApp:
    def __init__(self):
        self.users = HashTable()
        self.posts = []

    def register(self, username, password):
        if self.users.get(username) is not None:
            return "Username already taken"
        
        new_user = User(username.password)
        self.users.insert(username, new_user)
        return "User registered"
    
    def login(self,username,password):
        user = self.users.get(username)
        if user and user.password == password:
            return "Log in succesful"
        return "Invalid Information"
    
    def create_post(self,username,content):
        user = self.users.get(username)
        if user:
            new_post = Post(username,content)
            user.add_post(new_post)
            self.posts.append(new_post)
            return "Post uploaded"
        return "User not found"

class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self,item):
        self.items.appen(item) #O(1)

    def dequeue(self):
        if not self.is_emptty():
            return self.items.pop(0) # O(n)
        return None
    
    def is_empty(self):
        return len(self.items) == 0
    
class Sorter:
    @staticmethod
    def merge_sort(arr, key=lambda x:x):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = Sorter.merge_sort(arr[:mid], key)
        right = Sorter.merge_sort(arr[mid:],key)

        return Sorter.merge(left,right,key)
    
    @staticmethod
    def merge(left,right,key):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if key(left[i]) <= key(right[j]):
                result.append(left[i])
                i+=1
            else:
                result.append(right[j])
                j+=1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

class Search:
    @staticmethod
    def binary_search(arr, target, key=lambda x:x):#
        low = 0
        high = len(arr) -1

        while low <= high:
            mid = (low + high) // 2

            if key(arr[mid]) == target:
                return mid
            elif key (arr[mid]) < target:
                low = mid + 1
            else:
                high = mid - 1

        return -1