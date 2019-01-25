'''
README:

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
class TwitterPoster:
    def __init__(self,tokens):
        '''
        tokens = {"consumer":[consumerkey, consumetoken],"access":[[akey,asecret],..]}
        '''
        self.tokens = tokens
    
    def authenticate_consumer(self):
        consumer_key = self.tokens["consumer"][0]
        consumer_secret = self.tokens["consumer"][1]
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        return auth

    def authenticate_client(self,i):
        '''
        authenticate the i'th client in the tokens["access"] list
        '''
        auth = self.authenticate_consumer()
        access_token = self.tokens["access"][i][0]
        access_token_secret = self.tokens["access"][i][1]
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        return api

    def send_direct_message(self,i,message):
        api = self.authenticate_client(i)
        print("sending DM....")
        #get the twitter user id of the authenticated user
        recipient_id = api.me().id
        event = {
            "event": {
                "type": "message_create",
                "message_create": {
                "target": {
                    "recipient_id": recipient_id
                },
                "message_data": {
                    "text": message
                }
                }
            }
        }
        #this specific function should be changed whenever a new tweepy module comes out
        #refer to the readme for looking at how to write this specific function in tweepy module itself
        api.send_direct_message_new(event)
        print("DM sent..")
        return 

if __name__ == "__main__":
    consumer_key = ""
    consumer_secret = ""
    access_token = ""
    access_token_secret = ""
    access_info = [access_token,access_token_secret]
    tokens = {"consumer":[consumer_key,consumer_secret],"access":[access_info]}
    twt = TwitterPoster(tokens)
    url = "https://www.google.com"
    message = input("write a message below to be sent as DM!\n")
    twt.send_direct_message(0,message+url)
