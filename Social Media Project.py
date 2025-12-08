#Social Media Project 
import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
from datetime import datetime
from collections import deque
import json
#Algorithms:
#Node class used for chaining in the HashTable
class Node:
    def __init__(self,key,value):
        self.key = key #key of the node
        self.value = value ##user object
        self.next = None #pointer to the next node in linked list

class HashTable:
    def __init__(self,size=50):
        self.size = size  # number of buckets (slots inside the table where data is stored)
        self.table = [None] * size  # initialise empty buckets 

    # hash function to map key to index
    def hash(self,key):
        return hash(key) % self.size
    
    #insert or update a key value pair
    def insert(self,key, value):
        index = self.hash(key)
        head = self.table[index]

        current = head
        while current: # traverse linked list to check if key exists
            if current.key == key:
                current.value = value # update value if key exists
                return
            current = current.next

        new_node = Node(key,value) # otherwise make a new node
        new_node.next = head
        self.table[index] = new_node # insert at the head, this is chaining

    #retrieve value by the key
    def get(self,key):
        index = self.hash(key)
        current = self.table[index]

        while current:
            if current.key == key:
                return current.value # return value if key is matched
            current = current.next
        return None # return none if not found
    
    #delete key value pair
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

        return False # return false if key not found
    
    # count total users in the hash table
    def total_users(self):
        count = 0
        for bucket in self.table:
            current = bucket
            while current:
                count +=1
                current = current.next
        return count
    
    #count total items 
    def total_items(self):
        count = 0
        for bucket in self.table:
            current = bucket
            while current:
                count+=1
                current = current.next
        return count

# Queue for notifications using deque for O(1) enqueue/dequeue
class Queue:
    def __init__(self):
        self.items = deque()

    def enqueue(self,item):
        self.items.append(item) # adds notification to the end

    def dequeue(self):
        return self.items.popleft() if self.items else None # remove from front in O(1)
    
    def is_empty(self):
        return len(self.items) == 0
    
#merge sort algorithm for sorting posts
class Sorter:
    @staticmethod # this is because it does not receive self, its a regular function
    #avoids making unnecessary objects
    def merge_sort(arr, key=lambda x:x): # defines small function in one line
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = Sorter.merge_sort(arr[:mid], key)
        right = Sorter.merge_sort(arr[mid:],key)

        return Sorter.merge(left,right,key)
    
    @staticmethod # # groups related functions together
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
# search classes
class Search:
    @staticmethod 
    def binary_search(arr, target, key=lambda x:x): # binary search on a sorted list
        low = 0 # index of search range
        high = len(arr) -1 # ending index range

        while low <= high:
            mid = (low + high) // 2

            # check if middle matches target
            if key(arr[mid]) == target:
                return mid
            #if less than
            elif key (arr[mid]) < target:
                low = mid + 1
            #if greater than
            else:
                high = mid - 1

        return -1
#FriendRequest object to store requests between users
class FriendRequest:
    def __init__(self,sender,receiver,timestamp):
        self.sender = sender
        self.receiver = receiver
        self.timestamp = timestamp

# User class to store information about each user
class User:
    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.posts = [] # list of users posts
        self.friends = [] # list of friend usernames
        self.friend_requests = [] # list of incoming friend requests

    # add a friend if not already added
    def add_friend(self,username):
        if username not in self.friends:
            self.friends.append(username)

    ##add a post to the users posts
    def add_post(self, post):
        self.posts.append(post)

# post object to store posts made by users
class Post:
    def __init__(self,author, content, timestamp):
        self.author = author
        self.content = content
        self.timestamp = timestamp

#Main Social Media App Logic System
class SocialMediaApp:
    def __init__(self):
        self.users = HashTable() # Users stored in hash table
        self.posts = [] # all posts across all users
        self.notification_queue = Queue() # Queue for notifications
        self.load_data() # Loads saved data if it only exists

    # saves all users, posts, and requests to json file
    def save_data(self):
        data = {"users":{},
                "posts":[]}
        for bucket in self.users.table:
            current = bucket # (slots inside the table where data is stored)
            while current:
                user = current.value
                data["users"][user.username]= {
                    "password": user.password,
                    "friends": user.friends,
                    "posts": [
                        {
                            "content": p.content, # post variable 
                            "timestamp": p.timestamp.strftime("%d-%m-%Y %H:%M:%S") 
                        }
                        for p in user.posts
                    ],
                    "friend_requests":[
                        {
                            "sender": fr.sender, # friendrequest variable
                            "receiver": fr.receiver,
                            "timestamp": fr.timestamp.strftime("%d-%m-%Y %H:%M:%S") # formats date and time to readable string
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
        with open("database.json","w") as f: # opens json file and writes in
            json.dump(data, f, indent=4) 

    # loads data from json file
    def load_data(self):
        try:
            with open("database.json", "r") as f: # f is file
                data = json.load(f) # loads all data from the file
        except (FileNotFoundError, json.JSONDecodeError): # shows errors up if file not there
            return #no data found
        
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
    # register a new user            
    def register(self, username, password):
        if self.users.get(username):
            return "Username already taken"
        new_user = User(username, password)
        self.users.insert(username, new_user)
        self.save_data()
        return "User registered"
    #login check
    def login(self,username,password):
        user = self.users.get(username)
        if user and user.password == password:
            return "Log in succesful"
        return "Invalid Information"
    #create a post
    def create_post(self,username,content):
        user = self.users.get(username)
        if not user:
            return "user not found"
        post = Post(username, content, datetime.now())
        user.add_post(post)
        self.posts.append(post)
        self.save_data()
        return "post has been uploaded"
    #get all notifications and clear queue
    def get_notifications(self):
        notifications = []
        while not self.notification_queue.is_empty():
            notifications.append(self.notification_queue.dequeue())
        return notifications
    #send friend request to another user
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
    #accept friend request
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
    #decline a driend request
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
    # get feed sorted by timestamp (recent first)
    def get_feed(self,username):
        user = self.users.get(username)
        if not user:
            return []
        sorted_posts = Sorter.merge_sort(self.posts,key=lambda p: p.timestamp)
        return sorted_posts[::-1]
    # search posts of a user containing keyword
    def search_user_posts(self,username, keyword):
        user = self.users.get(username)
        if not user:
            return []
        results = []
        for post in user.posts:
            if keyword.lower() in post.content.lower():
                results.append(post)
        return results
    #search a post by exact timestamp using binary serach
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
    # delete a post by timestamp 
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
    # total number of users
    def total_users(self) -> int:
        return self.users.total_users()
    #total number of posts
    def total_posts(self) -> int:
        return len(self.posts)

#Social media GUI
class SocialMediaGUI:
    def __init__(self, app):
        self.app = app
        self.current_user = None
        #root and frames
        self.root = tk.Tk()
        self.root.title("Social Media App")

        self.frame_top = tk.Frame(self.root)
        self.frame_top.pack(pady=10)

        self.frame_middle = tk.Frame(self.root)
        self.frame_middle.pack(pady=10)

        self.frame_bottom = tk.Frame(self.root)
        self.frame_bottom.pack(pady=10)
        #entries and labels
        tk.Label(self.frame_top, text = "Username: ").grid(row=0, column = 0)
        self.entry_username = tk.Entry(self.frame_top)
        self.entry_username.grid(row = 0, column =1)
        tk.Label(self.frame_top,text="Password: ").grid(row=1,column=0)
        self.entry_password = tk.Entry(self.frame_top,show = "*")
        self.entry_password.grid(row=1,column=1)

        tk.Button(self.frame_top, text="Register", command = self.register).grid(row=2,column=0)
        tk.Button(self.frame_top, text ="Login", command = self.login).grid(row=2,column=1)
        tk.Button(self.root, text ="Logout", command = self.logout, width = 20).pack(pady=5)
        
        self.label_current_user = tk.Label(self.frame_top, text = "Not signed in")
        self.label_current_user.grid(row = 3, columnspan = 2, pady=5)

        self.entry_post = tk.Entry(self.frame_middle, width = 50)
        self.entry_post.pack(side=tk.LEFT)
        tk.Button(self.frame_middle, text = "Post", command = self.create_post).pack(side=tk.LEFT)
        #display for post feed
        self.feed_box = scrolledtext.ScrolledText(self.frame_bottom,width =60, height =20)
        self.feed_box.pack()

        #screen buttons
        tk.Button(self.root, text ="Send Friend Request", command = self.send_friend_request).pack(pady=5)
        tk.Button(self.root, text ="Show Friend Requests",command = self.show_friend_requests).pack(pady=5)
        tk.Button(self.root, text ="Show Notifications", command = self.show_notifications).pack(pady=5)
        tk.Button(self.root, text="Search Post By Timestamp", command = self.search_post_gui).pack(pady=5)
        tk.Button(self.root, text ="Search User by username", command= self.search_user_gui).pack(pady=5)
        tk.Button(self.root, text ="Refresh Feed", command= self.refresh_feed).pack(pady=5)
        tk.Button(self.root, text ="Delete Post", command= self.delete_post_gui).pack(pady=5)
        self.root.mainloop()
    #register through GUI
    def register(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        msg = self.app.register(username,password)
        messagebox.showinfo("Register",msg)

        self.entry_username.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
    #login through GUI
    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        msg = self.app.login(username,password)
        if "succesful" in msg:
            self.current_user = username
            self.label_current_user.config(text= f"Signed in as {username}")
            messagebox.showinfo("Login", f"{msg} as {username}")
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
            self.refresh_feed()
        else:
            messagebox.showerror("Login Failed",msg)
            
        #logout through GUI
    def logout(self):
        if messagebox.askyesno("Logout","Are you sure you want to log out?"):
            self.current_user = None
            self.label_current_user.config(text="Not signed in")
            messagebox.showinfo("Logged out", "You have been logged out")
                
    #create a post through GUI
    def create_post(self):
        if not self.current_user:
            messagebox.showwarning("Not Logged in", "please log in first")
            return
        content = self.entry_post.get()
        msg = self.app.create_post(self.current_user,content)
        messagebox.showinfo("Post",msg)
        self.entry_post.delete(0, tk.END)
        self.refresh_feed()
    #delete post through GUI
    def delete_post_gui(self):
        if not self.current_user:
            messagebox.showwarning("Not logged in","log in first")
            return
        #timestamp string
        ts_str = simpledialog.askstring("Delete Post", "Enter timestamp of post to delete (dd-mm-yyyy HH:MM:SS)")
        if not ts_str:
            return
        try:
            target_ts = datetime.strptime(ts_str,"%d-%m-%Y %H:%M:%S")
        except ValueError:
            messagebox.showerror("Error", "Invalid timestamp format")
            return
        msg = self.app.delete_post(self.current_user,target_ts)
        messagebox.showinfo("Delete Post", msg)
        self.refresh_feed()
    #search for post through GUI
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
    #search user through GUI
    def search_user_gui(self):
        username = simpledialog.askstring("Search user", "Enter username: ")
        if not username:
            return
        user = self.app.users.get(username)
        if user:
            #builds user information string
            friends = ", ".join(user.friends) if user.friends else "No friends yet.."
            posts = "\n".join([f"[{p.timestamp.strftime('%d-%m-%Y %H:%M:%S')}] {p.content}" for p in user.posts]) \
                    if user.posts else "No posts yet"
            messagebox.showinfo(f"User: {username}", f"Friends: {friends}\nPosts:\n{posts}")
        else:
            messagebox.showinfo("Not found", f"No user found with username '{username}'")
    ## refresh feedbox
    def refresh_feed(self):
        if not self.current_user:
            return
        posts = self.app.get_feed(self.current_user)
        self.feed_box.delete("1.0",tk.END)

        for p in posts:
            self.feed_box.insert(tk.END,f"{p.author} [{p.timestamp.strftime('%d-%m-%Y %H:%M:%S')}]: {p.content}\n")
    #send friend request through GUI
    def send_friend_request(self):
        if not self.current_user:
            messagebox.showwarning("Not logged in", "please login first")
            return
        receiver = simpledialog.askstring("Friend request", "enter username to request to: ")

        if receiver:
            msg = self.app.send_friend_request(self.current_user,receiver)
            messagebox.showinfo("Friend Request", msg)
    #show incoming friend requests
    def show_friend_requests(self):
        if not self.current_user:
            messagebox.showwarning("Not logged in", "please login first")
            return
        user_obj = self.app.users.get(self.current_user)
        requests = user_obj.friend_requests
        for fr in requests.copy(): # makes copy so it doesnt amend
            answer = messagebox.askyesno("Friend Request", f"{fr.sender} sent you a request. Accept?")
            if answer:
                self.app.accept_friend_request(self.current_user, fr.sender)
            else:
                self.app.decline_friend_request(self.current_user, fr.sender)
        self.refresh_feed()
    #show notifications
    def show_notifications(self):
        notifications = self.app.get_notifications()
        if notifications:
            messagebox.showinfo("Notifications", "\n".join(notifications))
        else:
            messagebox.showinfo("Notifcations", "No new notifications")
#run the app/system
if __name__ == "__main__":
    app = SocialMediaApp()
    gui = SocialMediaGUI(app)
