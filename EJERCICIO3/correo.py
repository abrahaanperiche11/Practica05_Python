#configuracion del servidor y credenciales
import os

smtp_server= 'smtp.gmail.com' 
smtp_port = 587
sender_email = 'abrahaanperiche71@gmail.com' #mi correo
sender_password = '' #token dado por gmail

#Detalles del correo electronico
receiver_email = 'chinguelmaricielo@gmail.com'
subject = 'Envio reporte de REACTIVA'
body = 'Adjunto solicitado'

# Crear el objeto MIMEMultipart
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain'))

#adjuntar archivo
file_path = './DATA/REACTIVA.xlsx'
with open(file_path, 'rb') as file:
    attachment = MIMEApplication(file.read(), _subtype='xlsx')
    attachment.add_header('Content-Disposition', 'attachment', filename=file_path)
    msg.attach(attachment)

#Iniciar la conexion con el servidor smtp
with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()
    server.login(sender_email,sender_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())

print('Correo enviado exitosamente')
