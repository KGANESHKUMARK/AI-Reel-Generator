from flask import Flask, request, jsonify
import razorpay
import stripe

app = Flask(__name__)

# Razorpay Configuration
razorpay_client = razorpay.Client(auth=("YOUR_RAZORPAY_KEY", "YOUR_RAZORPAY_SECRET"))

# Stripe Configuration
app.config['STRIPE_SECRET_KEY'] = "YOUR_STRIPE_SECRET_KEY"
stripe.api_key = app.config['STRIPE_SECRET_KEY']

@app.route('/')
def welcome():
    return "Welcome to the AI Reel Generator API!"

@app.route('/create_order', methods=['POST'])
def create_order():
    data = request.json
    amount = data.get('amount', 1000)  # ₹10 in paisa (1000 paise = ₹10)
    
    order = razorpay_client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })
    
    return jsonify(order)

@app.route('/stripe_payment', methods=['POST'])
def stripe_payment():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': 'AI Reel Premium'},
                    'unit_amount': 1000,  # $10
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://127.0.0.1:5000/success',
            cancel_url='http://127.0.0.1:5000/cancel',
        )
        return jsonify({'id': session.id})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/get_example', methods=['GET'])
def get_example():
    return jsonify({'message': 'This is a GET request example'})

@app.route('/get_data', methods=['GET'])
def get_data():
    data = {
        'name': 'AI Reel Generator',
        'version': '1.0',
        'description': 'An API for generating AI reels'
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)