from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings

def send_booking_confirmation(booking):
    message = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=booking.user.email,
        subject=f'F8 Autos - Booking Confirmation #{booking.id}',
        html_content=f'''
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h1 style="color: #1a1a1a;">F8 Autos</h1>
                <h2>Booking Confirmation</h2>
                <p>Hi {booking.user.username},</p>
                <p>Your booking has been received and is currently <strong>{booking.status}</strong>.</p>
                <div style="background: #f5f5f5; padding: 20px; border-radius: 5px; margin: 20px 0;">
                    <h3>Booking Details</h3>
                    <p><strong>Booking ID:</strong> #{booking.id}</p>
                    <p><strong>Service:</strong> {booking.service.name}</p>
                    <p><strong>Date:</strong> {booking.booking_date}</p>
                    <p><strong>Time:</strong> {booking.booking_time}</p>
                    <p><strong>Price:</strong> £{booking.service.price}</p>
                    {f"<p><strong>Notes:</strong> {booking.notes}</p>" if booking.notes else ""}
                </div>
                <p>We will confirm your booking shortly. If you have any questions, please contact us.</p>
                <p>Thank you for choosing F8 Autos!</p>
            </div>
        '''
    )

    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        sg.send(message)
        print(f"Confirmation email sent to {booking.user.email}")
    except Exception as e:
        print(f"Failed to send email: {e}")