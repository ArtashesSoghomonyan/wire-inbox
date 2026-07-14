def verification_email_html(username: str, code: str) -> tuple[str, str]:
    email_title = "[Wire Inbox] Complete your account creation – one-time verification code"
    email_content = f"""
<p>Hello <b>{username}!</b></p>
<p>Thanks for joining Wire Inbox. Your verification code is:</p>
<h1>{code}</h1>
<p>Navigate back to your browser and enter the code. This code will expire in 20 minutes.</p>
<p>If you didn't create an account, you can safely ignore this email. No further action is required.</p>
<p>Thank you, </p>
<p>The Wire Inbox Team</p>
"""

    return email_title, email_content
