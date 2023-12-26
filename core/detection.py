import requests
import json
from requests_futures.sessions import FuturesSession
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests.exceptions import RequestException

roblox_cookie = {".ROBLOSECURITY": "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_21D39839B154DF323C6EC9568AE8D5BD26DC4F42C98C8E6A6BB417408EB6D4AF2934195170DE4DF946697A130E06F27FB7A747F1BE8D83AE7549C70CC7C6BBEBD457F1240363FDF9C57D75ABDF1122FD5FAD7E14C249063287A7679E86809CB057222E09F51B9FFFAC704506027AD351B33A35BCE429BF654A63DCC69AB5063B9EDEF709D9D6FF82821E2B1B572A205F8FBEB29E882BF1C17DE00821D2AC16882151970A131CEE9C98349CA2AD5E98B71D47CD2B938ADF80FF6BC4608AF72772EDBA176AC1B3BD666D47AAABF900605915D564CB9797DBDB5A590C471E424C84DB9F2DB84908384C28E5F1502232A7A0EE1F78430CBF0F2023330509596C714440CE0C53D2D09BF630C06BC9A77695F14B72103FBE6A2B553E37FAD62CBA07B77CD006930379E3BFD0A85EFC15A24D31731E2E2F2A03621E61B2C415B566EF4BC3C2FE830199090A141EF104447FE66F633956B11BEBA96A93EBB94D99D0F9BDD3C43048902AAE3468627E48D4C6215E55DD14C62C53E9CA0DC6D2712A847BC40C8A92A62B5864567C022844FC6C66D3BF5E73F55388E6B98098AC5109EA20D5418DF87A5F8E54CCA48A4980A963BE2549995EA874A551758863604885EEE00184623583027E7E20CDCB74B45B7F9709D9BB43C12F9EA717A2F3EC7617DF209087E56F908E208A43352695253665AE7EAECF79AF7C3BF4C67AC0E78A86D549E586AFB3F7ECEEB221D51ABA879220368D504286E8F967A5EC6137CFDD233CD0BBFE49A05F9F96A05C7F7760619BB994238C784487FA042351DE522990C851764B7B1DB10BD09112E94C423275FE6EB4714DEC104873A8A2F9A8B1364D2878719B3E01A3E57C4D0D65927394FD01AD420301FBEA4BA57BE347F4A5A788781E9AC6A6E9C015A4E865984ADB0B87A79DF4F6296CF47CAD9489F8298DC0FF3F0D34E1F3DD732E1606940C3A7D4C74BCBAC7E50369EF31E73E331CA5BB3246A7785D86A74B4B274F25EDBAA36193E2E77BC430EFED5A05D7EB2DF3D65426DF1A4FD80AB558D3CC555BC0B4F1864B94F96DB7315516A438D00C40BD41B7C3EC19260F8A9EFC19C0"}
def clothings(id):
  clothings = 0
  session = FuturesSession()
  retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
  session.mount('https://', HTTPAdapter(max_retries=retries))
  try:
    check = session.get(f"https://catalog.roblox.com/v1/search/items/details?Category=3&CreatorTargetId={id}&CreatorType=2&Limit=30").result()
    check = check.json()
  except RequestException as e:
    print(e)
    return 0

  def get_page(cursor=None):
      nonlocal check
      try:
        if cursor:
          url = f"https://catalog.roblox.com/v1/search/items/details?Category=3&CreatorTargetId={id}&CreatorType=2&Limit=30&cursor={cursor}"
        else:
          url = f"https://catalog.roblox.com/v1/search/items/details?Category=3&CreatorTargetId={id}&CreatorType=2&Limit=30"
        check = session.get(url).result().json()
      except RequestException as e:
        print(e)
        return 0
      return check

  while True:
      if "data" in check:
          clothings += len(check['data'])
      if "nextPageCursor" not in check or not check['nextPageCursor']:
          break
      else:
          check = get_page(check['nextPageCursor'])
  return clothings

def robux(id):
  # Import Local Cookie Variable
  global roblox_cookie
  session = FuturesSession()
  retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
  session.mount('https://', HTTPAdapter(max_retries=retries))
  try:
      # Send the request asynchronously and return a Future object
      future = session.get(f'https://economy.roblox.com/v1/groups/{id}/currency', cookies=roblox_cookie, timeout=5)
  except RequestException as e:
    print(e)
    return 0
  try:
    response = future.result()
    data = json.loads(response.text)
    if "robux" in data:
      robux = data.get("robux", 0)
    else:
      robux = 0
  except RequestException as e:
    print(e)
    return 0
  return robux

def gamevisits(id):
  # Create a FuturesSession object
  session = FuturesSession()
  retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
  session.mount('https://', HTTPAdapter(max_retries=retries))

  # Make the API request asynchronously
  try:
    future = session.get(f'https://games.roblox.com/v2/groups/{id}/games?accessFilter=All&sortOrder=Asc&limit=100', timeout=5)
  except RequestException as e:
    print(e)
    return 0

  # Wait for the request to complete and load the response into a dictionary
  try:
    response = future.result()
    os = json.loads(response.text)
    if "data" in os:
      data = os["data"]
    else:
      data = 0
      
  except RequestException as e:
    print(e)
    return 0

  # If there are no games, return "None"
  if not data:
    return 0
  
  # Find the total number of visits for all games
  total_visits = 0
  for game in data:
    visits = game["placeVisits"]
    total_visits += visits
  return total_visits
  
def gamecount(id):
  session = FuturesSession()
  retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
  session.mount('https://', HTTPAdapter(max_retries=retries))
  try:
      # Send the request asynchronously and return a Future object
      future = session.get(f'https://games.roblox.com/v2/groups/{id}/games?accessFilter=All&sortOrder=Asc&limit=100', timeout=5)
  except RequestException as e:
    print(e)
    return 0
  try:
    response = future.result()
    os = json.loads(response.text)
    if "data" in os:
      data = os["data"]
    else:
      data = 0
  except RequestException as e:
    print(e)
    return 0
  if not data:
    return 0
  else:
    return len(data)

def groupimage(id):
  # Create a session with retries enabled
  session = FuturesSession()
  retry = Retry(connect=3, backoff_factor=0.5, status_forcelist=[502, 503, 504])
  adapter = HTTPAdapter(max_retries=retry)
  session.mount('https://', adapter)

  # Send the request asynchronously and return a Future object
  future = session.get(f'https://thumbnails.roblox.com/v1/groups/icons?groupIds={id}&size=150x150&format=Png&isCircular=false', timeout=5)

  # Wait for the request to complete and handle any errors that may occur
  try:
    response = future.result()
    icon_url = response.json()
    if "data" in icon_url and len(icon_url["data"]) > 0:
       image = icon_url["data"][0]["imageUrl"]
    else:
       image = "https://cdn.discordapp.com/attachments/1008516436840431636/1083821033846485043/nigger.jpeg"

  except RequestException as e:
    print(e)
    image = "https://cdn.discordapp.com/attachments/1008516436840431636/1083821033846485043/nigger.jpeg"
  return image 
