# Very hacky script to write the descriptions for API key found. Write the descriptions
# with the the format that pleases you and then put it in the 'text' variable so that
# you get an escaped version that that you can put into the JSON data without having
# any issues.
#

text = """
There is a change this could be a Google Maps API key, so could try using 'gmapapiscanner'[1] or 'gap'[2]
to check which Google Maps service it is valid for and generate a PoC that you can show in your report. To
get a better understanding on the severity of having the Google Maps API key exposed, make sure to to to
read "Unauthorized Google Maps API Key Usage Cases, and Why You Need to Care"[3] written by Ozgur Alp (@ozguralp)

References:
 [1] https://github.com/ozguralp/gmapsapiscanner
 [2] https://github.com/joanbono/gap
 [3] https://ozguralp.medium.com/unauthorized-google-maps-api-key-usage-cases-and-why-you-need-to-care-1ccb28bf21e

API Documentation: https://developers.google.com/maps/documentation/javascript/get-api-key
"""
print(text.replace("\n", "\\n").replace("\"", "\\\""))

