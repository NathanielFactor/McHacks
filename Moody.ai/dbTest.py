import htmloperations as htop

userId = "midgetlaser"

print(htop.checkTodayEntry(userId))

print(htop.addUser(userId))

print(htop.addMessage(userId, "Hey there nice to meet you I feel amazing today"))

print(htop.get_messages_by_month(userId,2024,1))
