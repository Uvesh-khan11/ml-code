

# Drf paypal code 
token = 'A21AALFdJQCrggsU-oYLBDvlba5OjCfynWE0UNvfx7ajwxCN6e_BmWHhPA5SjOCA4obD8LHFBiaVlwq05YZxUA39W-3tXPcnw'

def create_paypal_order(order):
    access_token = token
    print("token",access_token)
    # Serialize order to access final price and other details
    order_serializer = OrderSerializer(order)
    order_data = order_serializer.data  # Access serialized data
    final_price_str = f"{order_data['final_price']:.2f}"  # Format price as "10.00"
    print(final_price_str)
    # Prepare PayPal request headers and data
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',  # Replace with actual token management
    }

    # Define the JSON data payload for PayPal's API request
    data = {
        "intent": "AUTHORIZE",
        "purchase_units": [
            {
                "reference_id": str(order.id),
                "amount": {
                    "currency_code": "USD",
                    "value": final_price_str
                }
            }
        ],
        "application_context": {
            "return_url": "http://localhost:8000/return",  # URL to return to after approval
            "cancel_url": "http://localhost:8000/cancel"   # URL to return to if canceled
        }
    }

    # Send the POST request to create a PayPal order
    response = requests.post(
        'https://api-m.sandbox.paypal.com/v2/checkout/orders',  # PayPal sandbox endpoint
        headers=headers,
        json=data  # Send JSON data directly
    )
    print(response)
    print("response data",response.json())
    # Check response from PayPal API
    if response.status_code == 201:
        response_data = response.json()
        print(response_data,"paypal response")
        approval_url = next(link['href'] for link in response_data['links'] if link['rel'] == "approve")
        print("url",approval_url)
        payment_id = response_data['id']
        print("payment_id",payment_id)
        return Response({"approval_url": approval_url, "payment_id": payment_id}, status=status.HTTP_201_CREATED)
    else:
        return Response({"error": response.json()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    





@api_view(['POST'])
def checkout(request):
    token = request.query_params.get('token')
    source = request.query_params.get('source')

    if not token:
        return Response({'error':'Error','message':'token is missing'}, status=status.HTTP_400_BAD_REQUEST)

    result = verify_token(token)
    if 'error' in result and result['error']:
        return Response({'error':'Error',"message":'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

    if 'success' in result and result['success']:
        try:
            decode_token = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
            user_id = decode_token['user_id']
            print('user id ',user_id)
            
            try:
                user = get_object_or_404(CustomUser, id=user_id)
            except CustomUser.DoesNotExist:
                return Response({'error':'Error','message':'User not found'},status=status.HTTP_404_NOT_FOUND)
            print(f"i got the user {user} and it's id {user.id} token's user id {user_id}")
            addresses = Address.objects.filter(user=user)
            print(f"this is source {source} and this is addresses {addresses}")

            data = request.data  # Use DRF's request.data to access JSON data
            address = data.get('address')
            city = data.get('city')
            state = data.get('state')
            country = data.get('country')
            pincode = data.get('pincode')
            save_address = data.get('save_address', False)  # Check if the user wants to save the address

            if source == 'buynow':
                product_id = data.get('prod_id')
                product = get_object_or_404(Product, id=product_id)
                if product != None:
                    print("Product also found",product)
                # Create the order
                order = Order.objects.create(
                    user=user,
                    address=address,
                    city=city,
                    state=state,
                    country=country,
                    pin_code=pincode,
                    total_price=product.price
                )
                if order:
                    print("order created")
                # Create an order item
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=1,
                    price=product.price
                )

                # Optionally save the address
                if save_address and addresses.count()<5 :
                    Address.objects.create(
                        user=user,
                        address=address,
                        city=city,
                        country=country,
                        state=state,
                        pincode=pincode,
                        default=False
                    )
                    # Optionally send a success message
                    return Response({'success': True, 'message': 'Address saved successfully'}, status=status.HTTP_200_OK)
                now = datetime.now()
                order_number = "ECB" + str(user.id) + str(now.day)  + str(now.month) + str(now.year)  + str(order.id)
                order.order_number = order_number
                order.save()
                if order.save:
                    print("order saved")
                create_paypal_order(order)
                # Send confirmation email
                # send_confirmation_email(user, order)
                return Response({'success': True, 'message': 'Order placed successfully'}, status=status.HTTP_201_CREATED)

            # elif source == 'cart':
            #     cart = get_object_or_404(Cart, user=user)
            #     cart_items = CartItem.objects.filter(cart=cart)

            #     total_price = sum(item.product.price * item.quantity for item in cart_items)

            #     # Create the order
            #     order = Order.objects.create(
            #         user=user,
            #         address=address,
            #         city=city,
            #         state=state,
            #         country=country,
            #         pin_code=pincode,
            #         total_price=total_price
            #     )
            #     now = datetime.now()
            #     order_number = "ECB" + str(user.id) + str(now.day)  + str(now.month) + str(now.year)  + str(order.id)
            #     order.order_number = order_number
            #     order.save()
            #     # Create order items from the cart
            #     for item in cart_items:
            #         OrderItem.objects.create(
            #             order=order,
            #             product=item.product,
            #             quantity=item.quantity,
            #             price=item.product.price
            #         )
                
            #     # Clear the cart after placing the order
            #     cart_items.delete()

            #     # Optionally save the address
            #     if save_address and addresses.count()<5 :
            #         Address.objects.create(
            #             user=user,
            #             address=address,
            #             city=city,
            #             country=country,
            #             state=state,
            #             pincode=pincode,
            #             default=False
            #         )

                
            #     # Send confirmation email
            #     send_confirmation_email(user, order)

            #     return Response({'success': True, 'message': 'Order placed successfully'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': f"Internal server error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'error': 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)