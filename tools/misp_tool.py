from langchain.tools import tool
# import pymisp


from pymisp import PyMISP
from dotenv import load_dotenv
import os

load_dotenv(override=True)

URL = os.getenv('MISP_URL')
KEY = os.getenv('MISP_KEY')
verify_cert = False

print(URL, KEY)

misp = PyMISP(url=URL, key=KEY, ssl=verify_cert)

class MispTool():
    @tool("MISP search Tool by keyword")
    def search(keyword: str):
      """Useful tool to search for an indicator of compromise or an security event
      Parameters:
      - keyword: The keyword to search for
      Returns:
      - A list of events that match the keyword
      """

      events = misp.search(controller='attributes', value=keyword, limit=1, metadata=True, include_event_tags=False, include_context=False, return_format='json', sg_reference_only=True)
      results = """Answer user question using these search results:\n\n"""
      return results + str(events)
    
    @tool("MISP search Tool by date")
    def search_by_date(date_from: str = None, date_to: str = None, metadata=True):
      """Useful tool to retrieve events that match a specific date or date range, use this if you know the date of the event
      Parameters:
      - date_from: The start date of the event
      - date_to: The end date of the event
      Not necessary to provide both dates, you can provide one or the other

      Returns:
      - A list of events that match the date or date range
      """

      events = misp.search(date_from=date_from, date_to=date_to, limit=5)
      return events
    
    