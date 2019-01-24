'''
use tweepy 3.6.0

In binder.py add the following:
        def build_parameters(self, args, kwargs):
            # ------------------------------------added 3 new lines-------------------------------------------------
            if '/direct_messages/events/new.json' in self.path:
                print("building params...")
                args = ()
                kwargs = {}
            # -------------------------------------not a part of src code!!----------------------------------------

In api.py add the following:
  import json
   
   #------------------------------------------new code added inside the class!!-------------------------------------------------------
    def send_direct_message_new(self, messageobject):
        """ :reference: https://developer.twitter.com/en/docs/direct-messages/sending-and-receiving/api-reference/new-event.html
        """
        headers, post_data = API._buildmessageobject(messageobject)
        return bind_api(
            api=self,
            path = '/direct_messages/events/new.json',
            method='POST',
            require_auth=True
        )(self, post_data=post_data, headers=headers)

    """ Internal use only """
    @staticmethod
    def _buildmessageobject(messageobject):
        body = json.dumps(messageobject)
        # build headers
        headers = {
            'Content-Type': 'application/json',
            'Content-Length': str(len(body))
        }
        return headers, body


    #--------------------------------new code ends here-----------------------------------------


'''


import tweepy



# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key=""
consumer_secret=""

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located
# under "Your access token")
access_token=""
access_token_secret=""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)





api = tweepy.API(auth)

# If the authentication was successful, you should
# see the name of the account print out
print(api.me().id)
test = "Hello parashara!! testing from tweepy!!"
print("sending..")

event = {
  "event": {
    "type": "message_create",
    "message_create": {
      "target": {
        "recipient_id": api.me().id#screen_name
      },
      "message_data": {
        "text": test
      }
    }
  }
}
api.send_direct_message_new(event)
print("message sent")