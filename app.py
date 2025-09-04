import smtplib

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login("contact@apexaihome.com", "dvbauvfhntwbqrpo")
server.sendmail("contact@apexaihome.com", "alihassanbscs99@gmail.com", "Test email from Python")
server.quit()
