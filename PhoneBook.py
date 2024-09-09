import re

class Node:
    def __init__(self, key, value=None):
        self.number = key
        self.value = value
        self.next = None
        self.prev = None

class LRUCache:
    def __init__(self, capacity=5):
        self.cap = capacity
        self.siz = 0
        self.head = None
        self.dir = {}
    
    def get(self, key):
        if key not in self.dir:
            return None
        if self.head.number == key:
            return key
        curr = self.dir[key]
        prev = curr.prev
        next_node = curr.next
        if prev:
            prev.next = next_node
        if next_node:
            next_node.prev = prev
        curr.next = self.head
        curr.prev = None
        if self.head:
            self.head.prev = curr
        self.head = curr
        return key

    def put(self, key):
        if key not in self.dir:
            new_node = Node(key)
            new_node.next = self.head
            if self.head:
                self.head.prev = new_node
            self.head = new_node
            self.dir[key] = new_node
            self.siz += 1
            if self.siz > self.cap:
                tail = self.head
                while tail.next:
                    tail = tail.next
                del self.dir[tail.number]
                if tail.prev:
                    tail.prev.next = None
                self.siz -= 1
        else:
            self.get(key)
    
    def printlist(self):
        node = self.head
        while node:
            print(node.number, end=" ")
            node = node.next
        print()

class HashMap:
    def __init__(self, size=100):
        self.size = size
        self.table = [None] * size
        self.lru_cache = LRUCache()

        default_contacts = {
            100: ["Police Emergency", "police@india.gov.in"],
            101: ["Fire Brigade Emergency", "fire@india.gov.in"],
            102: ["Ambulance Emergency", "ambulance@india.gov.in"],
            9711077372: ["NDRF Emergency", "controlroom@ndrf.nic.in"],
            1091: ["Women’s Helpline", "ncw@nic.in"],
            1098: ["Child Helpline", "info@childlineindia.org.in"],
            14567: ["Senior Citizen Helpline", "elderline@elderline.gov.in"],
            139: ["Railway Helpline", "care@irctc.co.in"],
            103: ["Traffic Police Emergency", "traffic@india.gov.in"],
            1554: ["Coast Guard Emergency", "dte-info@indiancoastguard.nic.in"]
        }
        
        for number, details in default_contacts.items():
            self.add(number, details)

    def _hash_function(self, key):
        return hash(key) % self.size

    def add(self, key, value):
        index = self._hash_function(key)
        new_node = Node(key, value)
        if self.table[index] is None:
            self.table[index] = new_node
        else:
            current = self.table[index]
            while current.next is not None:
                if current.number == key:
                    return "Number Already Exists!"
                current = current.next
            if current.number == key:
                return "Number Already Exists!"
            current.next = new_node
        self.lru_cache.put(key)
        return f"Contact {value[0]} has been added."

    def get(self, key):
        index = self._hash_function(key)
        current = self.table[index]
        while current is not None:
            if current.number == key:
                self.lru_cache.put(key)
                return current.value
            current = current.next
        return None

    def update(self, old_key, new_key, new_value):
        index = self._hash_function(old_key)
        current = self.table[index]
        prev = None

        while current is not None:
            if current.number == old_key:
                if prev:
                    prev.next = current.next
                else:
                    self.table[index] = current.next
                self.add(new_key, new_value)
                return "Contact Details Updated"
            prev = current
            current = current.next

        return "Contact Not Found!"

    def delete(self, key):
        index = self._hash_function(key)
        current = self.table[index]
        prev = None

        while current is not None:
            if current.number == key:
                if prev:
                    prev.next = current.next
                else:
                    self.table[index] = current.next
                self.lru_cache.put(key)
                return "Contact deleted successfully"
            prev = current
            current = current.next

        return "Contact Not Found!"

    def get_all_contacts(self):
        contacts = []
        for i in range(self.size):
            current = self.table[i]
            while current is not None:
                contacts.append((current.number, current.value))
                current = current.next
        return contacts
    
    def search(self, search_term):
        results = []
        for i in range(self.size):
            current = self.table[i]
            while current is not None:
                name, email = current.value
                if search_term.lower() in name.lower():
                    results.append((current.number, name, email))
                    self.lru_cache.put(current.number)
                current = current.next
    
        return results


def valid_number_checker(num):
    return len(str(num)) == 10 and str(num)[0] in "6789"

def is_valid_email(email):
    email_regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    return re.match(email_regex, email) is not None

def search_contact_by_prefix(phonebook):
    """Search contacts by name or email prefix, display results, and trigger LRU cache."""
    prefix = input("Please enter the name to search: ").lower()
    
    # Get all contacts
    contacts = phonebook.get_all_contacts()
    results = [contact for contact in contacts if contact[1][0].lower().startswith(prefix) or contact[1][1].lower().startswith(prefix)]
    
    if results:
        print(f"Contacts with prefix '{prefix}':")
        for index, (number, details) in enumerate(results, start=1):
            print(f"{index}. Phone Number: {number}, Name: {details[0]}, Email: {details[1]}")
        
        try:
            selected_index = int(input("Select the number of the contact you want to store in history (enter the number): "))
            if 1 <= selected_index <= len(results):
                selected_number = results[selected_index - 1][0]
                print(f"Contact selected: Phone Number: {selected_number}, Name: {results[selected_index - 1][1][0]}, Email: {results[selected_index - 1][1][1]}")
                
                # Trigger the LRU cache
                phonebook.lru_cache.put(selected_number)
                print("Contact added to LRU cache.")
            else:
                print("Invalid selection. Please enter a number from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    else:
        print(f"No contacts found with prefix '{prefix}'.")

def main():
    phonebook = HashMap()

    while True:
        print("\nPhone Book Management System")
        print("1. Add Contact")
        print("2. Update Contact")
        print("3. Delete Contact")
        print("4. View All Contacts")
        print("5. Search Contact")
        print("6. View Search History")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter Name: ")
            email = input("Enter Email: ")
            phone_number = input("Enter Phone Number: ")
            if valid_number_checker(phone_number) and is_valid_email(email):
                result = phonebook.add(int(phone_number), [name, email])
                print(result)
            else:
                print("Invalid phone number or email.")
        
        elif choice == '2':
            old_phone_number = input("Enter Old Phone Number: ")
            new_phone_number = input("Enter New Phone Number (Leave blank if no change): ")
            new_name = input("Enter New Name (Leave blank if no change): ")
            new_email = input("Enter New Email (Leave blank if no change): ")
            
            if valid_number_checker(old_phone_number):
                if new_phone_number and not valid_number_checker(new_phone_number):
                    print("Invalid new phone number.")
                elif new_email and not is_valid_email(new_email):
                    print("Invalid new email.")
                else:
                    result = phonebook.update(
                        int(old_phone_number),
                        int(new_phone_number) if new_phone_number else int(old_phone_number),
                        [new_name if new_name else phonebook.get(int(old_phone_number))[0],
                         new_email if new_email else phonebook.get(int(old_phone_number))[1]]
                    )
                    print(result)
            else:
                print("Invalid old phone number.")
        
        elif choice == '3':
            delete_phone_number = input("Enter Phone Number to Delete: ")
            if valid_number_checker(delete_phone_number):
                result = phonebook.delete(int(delete_phone_number))
                print(result)
            else:
                print("Invalid phone number.")
        
        elif choice == '4':
            contacts = phonebook.get_all_contacts()
            if contacts:
                for number, info in contacts:
                    print(f"Phone Number: {number}, Name: {info[0]}, Email: {info[1]}")
            else:
                print("No contacts found.")
        elif choice=='5':
            search_contact_by_prefix(phonebook)


        elif choice == '6':
            print("Search History (Least Recently Used):")
            phonebook.lru_cache.printlist()

        
        elif choice == '7':
            print("Exiting the Phone Book Management System.")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
