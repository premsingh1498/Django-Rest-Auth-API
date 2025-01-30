from rest_framework import serializers
from myapp.models import MyUser
from myapp.utils import Util

# for Sending eamils to users:
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.contrib.auth.tokens import PasswordResetTokenGenerator

# <-----------------            Users Register Serializer       ---------------------------->
 
class UserRegistrationSerializer(serializers.ModelSerializer):
    # for confirm password field in registration process:
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = MyUser
        fields = ['email', 'name', 'password', 'password2', 'tc']
        extra_kwargs = {
            'password':{'write_only':True}
        }
        
    # Validation for password and confirm password:
    
    def validate(self, atttrs):
        password = atttrs.get('password')
        password2 = atttrs.pop('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm password does not match !")
        return atttrs
    
    def create(self, validate_data):
        return MyUser.objects.create_user(**validate_data)
            
# <--------------------     Users login Serializers     ---------------------->

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)
    class Meta:
        model = MyUser
        fields = ['email', 'password']
        
# <----------------        User Profile Serializers     ---------------------->

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'email', 'name']
        
# <-----------------             User change Password               ----------------->

class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input-type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input-type':'password'}, write_only=True)

    class Meta:
        fields =['password', 'password2']
        
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm password does not match !")
        user.set_password(password)
        user.save()
        return attrs
    
# <--------------------------------        OLD Send Reset Email Password             ------------------------------->

'''
This Method is used to send Simple Email with text.
'''

# class SendPasswordResetMailSerializer(serializers.Serializer):
#     email = serializers.EmailField(max_length=255)
    
#     class Meta:
#         fields = ['email']

#     def validate(self, attrs):
#         email = attrs.get('email')
#         if MyUser.objects.filter(email=email).exists():
#             user = MyUser.objects.get(email=email)
#             uid = urlsafe_base64_encode(force_bytes(user.id))
#             print("Encoded uid is: ", uid)
#             token = PasswordResetTokenGenerator().make_token(user)
#             print('Password Reset Token: ', token)
#             link = 'http://localhost:8000/api/user/reset/'+uid+'/'+token
#             print("Reset password link is: ", link)
#             # Send email code:
#             body = f"Click this link to Reset Password {link}"
#             data = {
#                 "subject":"Reset your Password",
#                 "body":body,
#                 "to_email": user.email
#             }
#             Util.sendEmail(data)
            
#             return attrs
#         else:
#             raise serializers.ValidationError("Your Account is Not Registered !")


# <--------------------------   New Updated CODE     ---------------------------------->

'''
This Email Code is Used to send Email with template.
'''


from django.template.loader import render_to_string
class SendPasswordResetMailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if MyUser.objects.filter(email=email).exists():
            user = MyUser.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            reset_link = f"http://localhost:3000/api/user/reset/{uid}/{token}"

            # 🔹 Render the email template with user and reset link
            email_body = render_to_string("emails/verify_email.html", {
                "user": user,
                "verification_url": reset_link,
            })

            # 🔹 Send email with the rendered HTML template
            data = {
                "subject": "Reset Your Password",
                "body": email_body,
                "to_email": user.email
            }
            Util.sendEmail(data)

            return attrs
        else:
            raise serializers.ValidationError("Your account is not registered!")

# <----------------------       Users Reset Password Serializer       --------------------->

class UserResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input-type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input-type':'password'}, write_only=True)

    class Meta:
        fields =['password', 'password2']
        
    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            
            Uid = self.context.get('uid')
            Token = self.context.get('token')
            print("UID is: ", Uid)
            print("get Token is:", Token)

            if password != password2:
                raise serializers.ValidationError("Password and Confirm password does not match !")
            
            id = smart_str(urlsafe_base64_decode(Uid))
            user = MyUser.objects.get(id=id)
            print("user is: ", user)
            if not PasswordResetTokenGenerator().check_token(user, Token):
                raise serializers.ValidationError("Token is not valid or Expired")
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, Token)
            raise serializers.ValidationError("Token is not valid !")
            
# <---------------------------------         Code End           ------------------------------------>