# MubiNotifier
A lambda to tweet out what is leaving or featured on Mubi.

Film ratings and short synopis provided by the Open Movie Database if they exist, otherwise the Mubi user rating and editorial is used instead.

https://twitter.com/LeavingMubiUK

## Usage
This app is designed to be ran in AWS lambda, and has been created to be an AWS-Sam deployable project. This means it can be ran in a container by SAM locally, which emulates AWS.

### Pre-requisites
In order to run the app, you will first need to have set up a Twitter account and [generated the associated OAuth credentials](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api).

Although technically optional since the code will fall-back to Mubi's information, you will also want to have a working OMDB API key, these can be requested [here](https://www.omdbapi.com/apikey.aspx).

### Set-up
Once you have the above codes the app needs to have access to them through the environment. If running through SAM these can be set in `template.yaml`and/or overridden for local runs in `environment.json`.  

If you wish to run the application locally, for instance in pyenv, you will need to populate the following environment variables:  
* omdb_api_key
* twitter_access_token_key
* twitter_access_token_secret
* twitter_consumer_key
* twitter_consumer_secret

You can also change the timezone (used for local 'midnight' to UTC time conversion) by setting `local_timezone`