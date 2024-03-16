from flask import Flask, request, session, redirect, url_for, abort, send_file, render_template_string
import pyotp
import qrcode
from io import BytesIO
from dashboard.dashboard import dashboard
from datetime import datetime, timedelta
from dashboardtwo.dashboardtwo import dashboardtwo


app = Flask(__name__)
dashboard(app)
dashboardtwo(app)
app.config['SECRET_KEY'] = '12312312312312'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# In a real app, this should be dynamically associated with a user and stored securely
USER_SECRET = '3SLSWZPQQBB7WBRYDAQZ5J77W5D7I6GU'

@app.route('/')
def index():
    return "hi"

@app.route('/setup')
def setup():
    """Generates a QR code for TOTP setup."""
    # This should be a user-specific email in a real app
    email = 'MIC@bld.de'
    totp_uri = pyotp.totp.TOTP(USER_SECRET).provisioning_uri(name=email, issuer_name='M.I.C')
    qr_img = qrcode.make(totp_uri)
    img_io = BytesIO()
    qr_img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    """A simple page to input OTP for verification."""
    if request.method == 'POST':
        otp_input = request.form['otp']
        if pyotp.TOTP(USER_SECRET).verify(otp_input):
            session['otp_verified'] = True
            return redirect('/dash/')
        else:
            return 'Authentifizierung fehlgeschlagen. Bitte versuchen Sie es erneut.', 401

    return '''
        <form method="post">
            OTP: <input type="text" name="otp"><br>
            <input type="submit" value="Verify">
        </form>
    '''




if __name__ == '__main__':
    app.run(debug=True)
