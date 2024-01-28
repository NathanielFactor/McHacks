import htmloperations as htop

userId = "midgetlaser"

print(htop.checkTodayEntry(userId))

print(htop.addUser(userId))

print(htop.addMessage(userId, "Hello World!"))

print(htop.gptResponse("nfac", "I punched my little brother today"))

print(htop.get_messages_by_month("nfac",2024,1))
