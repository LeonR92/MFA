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
USER_SECRET_SD = '3SLSWZPQQTT7WBRYDAQZ5J77W5D7I6GU'
USER_SECRET_UNI = '3SLSWZPQQTT7WBRYDAQZ5J66W5D7I6GU'




@app.route('/')
def index():
    return "hi"

@app.route('/setup')
def setup():
    """Generates a QR code for TOTP setup."""
    # This should be a user-specific email in a real app
    email = 'StundenDashboard@bld.de'
    totp_uri = pyotp.totp.TOTP(USER_SECRET_SD).provisioning_uri(name=email, issuer_name='Stunden Dashboard')
    qr_img = qrcode.make(totp_uri)
    img_io = BytesIO()
    qr_img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

@app.route('/setup2')
def setup2():
    """Generates a QR code for TOTP setup."""
    # This should be a user-specific email in a real app
    email = 'MAHUniversal@bld.de'
    totp_uri = pyotp.totp.TOTP(USER_SECRET_UNI).provisioning_uri(name=email, issuer_name='Universal Dashboard')
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
        # Change User_Secrets and session name both in this function and in dashboards
        if pyotp.TOTP(USER_SECRET_SD).verify(otp_input): 
            session['otp_verified_sd'] = True
            return redirect('/dash/')
        else:
            return 'Authentifizierung fehlgeschlagen. Bitte versuchen Sie es erneut.', 401

    return '''
        <form method="post">
            OTP: <input type="text" name="otp"><br>
            <input type="submit" value="Verify">
        </form>
    '''

@app.route('/verify2', methods=['GET', 'POST'])
def verify2():
    """A simple page to input OTP for verification."""
    if request.method == 'POST':
        otp_input = request.form['otp']
        if pyotp.TOTP(USER_SECRET_UNI).verify(otp_input):
            session['otp_verified_uni'] = True
            return redirect('/dash2/')
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
