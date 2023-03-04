class Node:
    def __init__(self, val=1, next=None):
        self.value = val
        self.next = next



n1 = Node(1)
n2 = Node(2)
n1.next = n2
n3 = Node(3)
n2.next = n3

prev, curr = None, n1
while curr:
    nxt = curr.next
    curr.next = prev
    prev = curr
    curr = nxt
