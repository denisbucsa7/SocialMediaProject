#Social Media Project 
import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
from datetime import datetime
from collections import deque
import json
from collections import deque

class Node:
    def __init__(self,key,value):
        self.key = key
        self.value = value
        self.next = None

class HashTable:
    def __init__(self,size=50):
        self.size = size
        self.table = [None] * size

    def hash(self,key):
        return hash(key) % self.size
    
    def insert(self,key, value):
        index = self.hash(key)
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
        index = self.hash(key)
        current = self.table[index]

        while current:
            if current.key == key:
                return current.value
            current = current.next
        return None
    
    def delete(self,key):
        index = self.hash(key)
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
    
    def total_users(self):
        count = 0
        for bucket in self.table:
            current = bucket
            while current:
                count +=1
                current = current.next
        return count
    
    def total_items(self):
        count = 0
        for bucket in self.table:
            current = bucket
            while current:
                count+=1
                current = current.next
        return count

class FriendRequest:
    def __init__(self,sender,receiver,timestamp):
        self.sender = sender
        self.receiver = receiver
        self.timestamp = timestamp

#System Clases:
class User:
    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.posts = []
        self.friends = []
        self.friend_requests = []

    def add_friend(self,username):
        if username not in self.friends:
            self.friends.append(username)

    def add_post(self, post):
        self.posts.append(post)

class Post:
    def __init__(self,author, content, timestamp):
        self.author = author
        self.content = content
        self.timestamp = timestamp

class Queue:
    def __init__(self):
        self.items = deque()

    def enqueue(self,item):
        self.items.append(item) # adds to the end

    def dequeue(self):
        return self.items.popleft() if self.items else None # remove from front in O(1)
    
    def is_empty(self):
        return len(self.items) == 0

class SocialMediaApp:
    def __init__(self):
        self.users = HashTable()
        self.posts = []
        self.notification_queue = Queue()
        self.load_data()

    def save_data(self):
        data = {"users":{},
                "posts":[]}
        for bucket in self.users.table:
            current = bucket
            while current:
                user = current.value
                data["users"][user.username]= {
                    "password": user.password,
                    "friends": user.friends,
                    "posts": [
                        {
                            "content": p.content,
                            "timestamp": p.timestamp.strftime("%d-%m-%Y %H:%M:%S")
                        }
                        for p in user.posts
                    ],
                    "friend_requests":[
                        {
                            "sender": fr.sender,
                            "receiver": fr.receiver,
                            "timestamp": fr.timestamp.strftime("%d-%m-%Y %H:%M:%S")
                        }
                        for fr in user.friend_requests
                    ]
                }
                current = current.next
        for p in self.posts:
            data["posts"].append({
                "author":p.author,
                "content":p.content,
                "timestamp":p.timestamp.strftime("%d-%m-%Y %H:%M:%S")
            })
        with open("database.json","w") as f:
            json.dump(data, f, indent=4)

    def load_data(self):
        try:
            with open("database.json", "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return
        
        for username, udata in data["users"].items():
            user = User(username,udata["password"])
            user.friends = udata["friends"]

            for p in udata["posts"]:
                post = Post(username,p["content"], datetime.strptime(p["timestamp"], "%d-%m-%Y %H:%M:%S"))
                user.posts.append(post)
                self.posts.append(post)
            
            for fr in udata["friend_requests"]:
                req = FriendRequest(fr["sender"], fr["receiver"], datetime.strptime(fr["timestamp"], "%d-%m-%Y %H:%M:%S"))
                user.friend_requests.append(req)

            self.users.insert(username,user)
                
    def register(self, username, password):
        if self.users.get(username):
            return "Username already taken"
        new_user = User(username, password)
        self.users.insert(username, new_user)
        self.save_data()
        return "User registered"
    
    def login(self,username,password):
        user = self.users.get(username)
        if user and user.password == password:
            return "Log in succesful"
        return "Invalid Information"
    
    def create_post(self,username,content):
        user = self.users.get(username)
        if not user:
            return "user not found"
        post = Post(username, content, datetime.now())
        user.add_post(post)
        self.posts.append(post)
        self.save_data()
        return "post has been uploaded"
    
    def get_notifications(self):
        notifications = []
        while not self.notification_queue.is_empty():
            notifications.append(self.notification_queue.dequeue())
        return notifications
    
    def send_friend_request(self,sender,receiver):
        sender_user = self.users.get(sender)
        receiver_user = self.users.get(receiver)

        if not sender_user or not receiver_user:
            return "User not found"
        
        fr = FriendRequest(sender,receiver,datetime.now())
        receiver_user.friend_requests.append(fr)
        self.notification_queue.enqueue(f"{sender} sent a friend request to {receiver}")
        self.save_data()
        return "Friend Request sent"
    
    def accept_friend_request(self, receiver, sender):
        user = self.users.get(receiver)
        if not user:
            return "user not been found"
        
        for fr in user.friend_requests:
            if fr.sender == sender:
                user.friend_requests.remove(fr)
                user.add_friend(sender)
                self.users.get(sender).add_friend(receiver)
                self.notification_queue.enqueue(f"{receiver} accepted {sender}'s friend request")
                self.save_data()
                return "friend request accepted"
            
        return "friend request not found"
    
    def decline_friend_request(self,receiver,sender):
        user = self.users.get(receiver)
        if not user:
            return "user not been found"
        
        for fr in user.friend_requests:
            if fr.sender == sender:
                user.friend_requests.remove(fr)
                self.notification_queue.enqueue(f"{receiver} declined {sender}'s friend request")
                self.save_data()
                return "friend request has been declined"
            
        return "friend request not found"
    
    def get_feed(self,username):
        user = self.users.get(username)
        if not user:
            return []
        sorted_posts = Sorter.merge_sort(self.posts,key=lambda p: p.timestamp)

        return sorted_posts[::-1]
    
    def search_user_posts(self,username, keyword):
        user = self.users.get(username)
        if not user:
            return []
        results = []

        for post in user.posts:
            if keyword.lower() in post.content.lower():
                results.append(post)

        return results
    
    def search_post_by_timestamp(self,username, target_timestamp):
        #uses binary search to find post by the timestamp, returns post object if found, else none
        user = self.users.get(username)
        if not user:
            return None
        sorted_posts = Sorter.merge_sort(user.posts, key=lambda p: p.timestamp)

        index = Search.binary_search(sorted_posts, target_timestamp, key=lambda p: p.timestamp)
        if index != -1:
            return sorted_posts[index]
        return None
    
    def delete_post(self, username, timestamp):
        user = self.users.get(username)
        if not user:
            return "user not found"
        
        for p in user.posts:
            if p.timestamp == timestamp:
                user.posts.remove(p)
                self.posts.remove(p)
                self.save_data()
                return "post has been delete"
            
        return "post not been found"
    
    
    def total_users(self) -> int:
        return self.users.total_users()
    
    def total_posts(self) -> int:
        return len(self.posts)
    
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
    
class SocialMediaGUI:
    def __init__(self, app):
        self.app = app
        self.current_user = None

        self.root = tk.Tk()
        self.root.title("Social Media App")

        self.frame_top = tk.Frame(self.root)
        self.frame_top.pack(pady=10)

        self.frame_middle = tk.Frame(self.root)
        self.frame_middle.pack(pady=10)

        self.frame_bottom = tk.Frame(self.root)
        self.frame_bottom.pack(pady=10)

        tk.Label(self.frame_top, text = "Username").grid(row=0, column = 0)
        self.entry_username = tk.Entry(self.frame_top)
        self.entry_username.grid(row = 0, column =1)
        tk.Label(self.frame_top,text="Password").grid(row=1,column=0)
        self.entry_password = tk.Entry(self.frame_top,show = "*")
        self.entry_password.grid(row=1,column=1)

        tk.Button(self.frame_top, text="Register", command = self.register).grid(row=2,column=0)
        tk.Button(self.frame_top, text ="Login", command = self.login).grid(row=2,column=1)

        self.entry_post = tk.Entry(self.frame_middle, width = 50)
        self.entry_post.pack(side=tk.LEFT)
        tk.Button(self.frame_middle, text = "Post", command = self.create_post).pack(side=tk.LEFT)

        self.feed_box = scrolledtext.ScrolledText(self.frame_bottom,width =60, height =20)
        self.feed_box.pack()

        tk.Button(self.root, text ="Send Friend Request", command = self.send_friend_request).pack(pady=5)
        tk.Button(self.root, text ="Show Friend Requests",command = self.show_friend_requests).pack(pady=5)
        tk.Button(self.root, text ="Show Notifications", command = self.show_notifications).pack(pady=5)
        tk.Button(self.root, text="Search Post By Timestamp", command = self.search_post_gui).pack(pady=5)

        self.root.mainloop()

    def register(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        msg = self.app.register(username,password)
        messagebox.showinfo("Register",msg)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        msg = self.app.login(username,password)
        if "succesful" in msg:
            self.current_user = username
            messagebox.showinfo("Login", f"{msg} as {username}")
            self.refresh_feed()
        else:
            messagebox.showerror("Login Failed",msg)

    def create_post(self):
        if not self.current_user:
            messagebox.showwarning("Not Logged in", "please log in first")
            return
        content = self.entry_post.get()
        msg = self.app.create_post(self.current_user,content)
        messagebox.showinfo("Post",msg)
        self.entry_post.delete(0, tk.END)
        self.refresh_feed()

    def search_post_gui(self):
        #GUI interface to search for post by timestamp
        if not self.current_user:
            messagebox.showwarning("Not logged in", "log in first")
            return
        ts_str = simpledialog.askstring("Search post", "enter timestamp (dd-mm-yyyy HH:MM:SS): ")
        if not ts_str:
            return
        try:
            target_ts = datetime.strptime(ts_str, "%d-%m-%Y %H:%M:%S")
        except ValueError:
            messagebox.showerror("Error", "Invalid timestamp formatting")
            return
        post = self.app.search_post_by_timestamp(self.current_user, target_ts)
        if post:
            messagebox.showinfo("Post found",f"{post.author} [{post.timestamp.strftime('%d-%m-%Y %H:%M:%S')}]: {post.content}")#
        else:
            messagebox.showinfo("Post not found", "No post at that current timestamp")


    def refresh_feed(self):
        if not self.current_user:
            return
        posts = self.app.get_feed(self.current_user)
        self.feed_box.delete("1.0",tk.END)

        for p in posts:
            self.feed_box.insert(tk.END,f"{p.author} [{p.timestamp.strftime('%d-%m-%Y %H:%M:%S')}]: {p.content}\n")
    
    def send_friend_request(self):
        if not self.current_user:
            messagebox.showwarning("Not logged in", "please login first")
            return
        receiver = simpledialog.askstring("Friend request", "enter username to request to: ")

        if receiver:
            msg = self.app.send_friend_request(self.current_user,receiver)
            messagebox.showinfo("Friend Request", msg)
    
    def show_friend_requests(self):
        if not self.current_user:
            messagebox.showwarning("Not logged in", "please login first")
            return
        user_obj = self.app.users.get(self.current_user)
        requests = user_obj.friend_requests
        for fr in requests.copy():
            answer = messagebox.askyesno("Friend Request", f"{fr.sender} sent you a request. Accept?")
            if answer:
                self.app.accept_friend_request(self.current_user, fr.sender)
            else:
                self.app.decline_friend_request(self.current_user, fr.sender)
        self.refresh_feed()

    def show_notifications(self):
        notifications = self.app.get_notifications()
        if notifications:
            messagebox.showinfo("Notifications", "\n".join(notifications))
        else:
            messagebox.showinfo("Notifcations", "No new notifications")

if __name__ == "__main__":
    app = SocialMediaApp()
    gui = SocialMediaGUI(app)