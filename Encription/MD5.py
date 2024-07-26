import hashlib

# initializing string
str1hash = "Hello cool cyber class"

str2hash = "Hello cool cyber class."

# encoding string using encode() and then sending to md5()
result = hashlib.md5(str1hash.encode())

result2 = hashlib.md5(str2hash.encode())

# printing the equivalent hexadecimal value.
print("The hexadecimal equivalent of hash is: ", result.hexdigest())

print("The hexadecimal equivalent of hash is: ", result2.hexdigest())
