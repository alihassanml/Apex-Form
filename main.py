from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

app = FastAPI()

# Static + Template setup
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
templates = Jinja2Templates(directory="templates")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "contact@apexaihome.com"
EMAIL_PASSWORD = "dvbauvfhntwbqrpo"   # Use Gmail App Password

def create_beautiful_email_html(name, email, company, message):
    """Create a beautiful HTML email template"""
    current_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>New Contact Form Submission</title>
    </head>
    <body style="margin: 0; padding: 0; background-color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; box-shadow: 0 10px 25px rgba(0,0,0,0.1);">
            
            <!-- Header -->
            <div style="background: linear-gradient(135deg, #f97316 0%, #ea580c 100%); padding: 40px 30px; text-align: center;">
               
                <h1 style="color: white; margin: 0; font-size: 28px; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    New Contact Form Submission
                </h1>
                <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0; font-size: 16px;">
                    Apex AI Contact Form
                </p>
            </div>

            <!-- Content -->
            <div style="padding: 40px 30px;">
                
                <!-- Contact Info Card -->
                <div style="background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); border-radius: 12px; padding: 25px; margin-bottom: 25px; border-left: 4px solid #f97316;">
                    <h2 style="color: #1e293b; margin: 0 0 20px; font-size: 20px; font-weight: 600;">
                        📋 Contact Information
                    </h2>
                    
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 8px 0; width: 100px; vertical-align: top;">
                                <strong style="color: #64748b; font-size: 14px;">👤 NAME:</strong>
                            </td>
                            <td style="padding: 8px 0; color: #1e293b; font-size: 16px; font-weight: 500;">
                                {name}
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; vertical-align: top;">
                                <strong style="color: #64748b; font-size: 14px;">📧 EMAIL:</strong>
                            </td>
                            <td style="padding: 8px 0;">
                                <a href="mailto:{email}" style="color: #f97316; text-decoration: none; font-weight: 500; font-size: 16px;">
                                    {email}
                                </a>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; vertical-align: top;">
                                <strong style="color: #64748b; font-size: 14px;">🏢 COMPANY:</strong>
                            </td>
                            <td style="padding: 8px 0; color: #1e293b; font-size: 16px; font-weight: 500;">
                                {company if company else 'Not provided'}
                            </td>
                        </tr>
                    </table>
                </div>

                <!-- Message Card -->
                <div style="background: linear-gradient(135deg, #fef3e2 0%, #fef2e2 100%); border-radius: 12px; padding: 25px; margin-bottom: 25px; border-left: 4px solid #22d3ee;">
                    <h2 style="color: #1e293b; margin: 0 0 15px; font-size: 20px; font-weight: 600;">
                        💬 Message
                    </h2>
                    <div style="background-color: white; padding: 20px; border-radius: 8px; border: 1px solid #e2e8f0;">
                        <p style="color: #374151; line-height: 1.6; margin: 0; font-size: 15px; white-space: pre-wrap;">
                            {message if message else 'No message provided.'}
                        </p>
                    </div>
                </div>

                <!-- Action Buttons -->
                <div style="text-align: center; margin: 30px 0;">
                    <a href="mailto:{email}" style="display: inline-block; background: linear-gradient(135deg, #f97316 0%, #ea580c 100%); color: white; padding: 12px 30px; text-decoration: none; border-radius: 8px; font-weight: 600; margin: 0 10px; box-shadow: 0 4px 12px rgba(249,115,22,0.3);">
                        Reply to {name.split()[0]}
                    </a>
                    <a href="mailto:{email}?cc=bwells@apexcapitalco.com" style="display: inline-block; background: linear-gradient(135deg, #22d3ee 0%, #06b6d4 100%); color: white; padding: 12px 30px; text-decoration: none; border-radius: 8px; font-weight: 600; margin: 0 10px; box-shadow: 0 4px 12px rgba(34,211,238,0.3);">
                        Reply with CC
                    </a>
                </div>

                <!-- Footer Info -->
                <div style="background-color: #f8fafc; border-radius: 8px; padding: 20px; text-align: center; margin-top: 30px;">
                    <p style="color: #64748b; margin: 0; font-size: 14px;">
                        📅 Received on <strong>{current_date}</strong>
                    </p>
                    <p style="color: #64748b; margin: 5px 0 0; font-size: 12px;">
                        This email was automatically generated from the Apex AI contact form.
                    </p>
                </div>
            </div>

            <!-- Footer -->
            <div style="background-color: #1e293b; color: white; padding: 25px 30px; text-align: center;">
                <h3 style="margin: 0 0 10px; font-size: 18px; font-weight: 600;">
                    🏠 Apex AI
                </h3>
                <p style="margin: 0; opacity: 0.8; font-size: 14px;">
                    Smart Home Solutions • Adaptive • Secure • Effortless
                </p>
                <div style="margin-top: 15px;">
                    <a href="mailto:bwells@apexcapitalco.com" style="color: #22d3ee; text-decoration: none; font-size: 14px;">
                        bwells@apexcapitalco.com
                    </a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html_template

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/send-email")
async def send_email(
    Name: str = Form(...),
    Email: str = Form(...),
    Company: str = Form(""),
    Message: str = Form("")
):
    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS  # Only send to your email
        msg["Subject"] = f"🏠 New Apex AI Contact: {Name} from {Company if Company else 'Individual'}"
        
        # Create plain text version (fallback)
        text_body = f"""
New Contact Form Submission - Apex AI

Contact Information:
👤 Name: {Name}
📧 Email: {Email}
🏢 Company: {Company if Company else 'Not provided'}

💬 Message:
{Message if Message else 'No message provided.'}

📅 Received: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

---
This email was automatically generated from the Apex AI contact form.
        """
        
        # Create HTML version
        html_body = create_beautiful_email_html(Name, Email, Company, Message)
        
        # Attach both versions
        text_part = MIMEText(text_body, "plain", "utf-8")
        html_part = MIMEText(html_body, "html", "utf-8")
        
        msg.attach(text_part)
        msg.attach(html_part)
        
        # Send email - FIXED: Send to correct recipient(s)
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.set_debuglevel(1)  # Shows Gmail response in console
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            
            # Send only to your email address (recommended for contact forms)
            server.sendmail(EMAIL_ADDRESS, [EMAIL_ADDRESS], msg.as_string())
            
            # Alternative: If you want to send to both you and the sender:
            # server.sendmail(EMAIL_ADDRESS, [EMAIL_ADDRESS, Email], msg.as_string())
        
        return {"status": "success", "message": "Message sent successfully! We'll get back to you soon."}
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"SMTP Authentication Error: {str(e)}")
        return {"status": "error", "message": "Authentication failed. Please check email credentials."}
    except smtplib.SMTPException as e:
        print(f"SMTP Error: {str(e)}")
        return {"status": "error", "message": "Failed to send email due to server error."}
    except Exception as e:
        print(f"General Error: {str(e)}")
        return {"status": "error", "message": "Failed to send message. Please try again or email us directly at bwells@apexcapitalco.com"}