
import argparse
from googleapiclient import discovery
import httplib2
import json
from oauth2client.client import GoogleCredentials
import sys

DISCOVERY_URL = ('https://{api}.googleapis.com/'
                 '$discovery/rest?version={apiVersion}')

def main(tweet_timeline_json_file):
  with open(tweet_timeline_json_file) as f:
    tweets = json.load(f)

  tweets_analyzed =   0
  for tweet in tweets:
    tweet_analysis = anaylze_content(tweet['text'])
    tweet['analysis'] = tweet_analysis
    tweets_analyzed += 1
    if tweets_analyzed % 20 == 0:
      print "%s tweets analyzed so far." % tweets_analyzed

  with open('%s_analyzed.json' % tweet_timeline_json_file[:-5], 'wb') as f:
    json.dump(tweets, f)

def anaylze_content(text):
  '''Run a sentiment analysis request on text within a passed filename
  This function is a modified version of the tutorial at this link on 7/24/16
  https://cloud.google.com/natural-language/docs/sentiment-tutorial
  '''

  http = httplib2.Http()

  credentials = GoogleCredentials.get_application_default().create_scoped(
      ['https://www.googleapis.com/auth/cloud-platform'])
  http=httplib2.Http()
  credentials.authorize(http)

  service = discovery.build('language', 'v1beta1',
                            http=http, discoveryServiceUrl=DISCOVERY_URL)

  service_request = service.documents().annotateText(
    body={
            "document":{
              "type":"PLAIN_TEXT",
              "content": text
            },
            "features":{
              "extractEntities":True,
              "extractDocumentSentiment":True
            },
            "encodingType":"UTF8"
          })

  try:
    response = service_request.execute()
    return response
  except:
    return {"error_msg": str(sys.exc_info()[1])}


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument(
    'tweet_timeline_json_file', help='The filename of the tweets you want like to analyze.')
  args = parser.parse_args()
  main(args.tweet_timeline_json_file)