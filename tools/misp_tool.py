from langchain.tools import tool
# import pymisp


from pymisp import PyMISP


URL = "https://9589-197-230-122-195.ngrok-free.app"
KEY = "DDL2X1VilJzgLvDSo58OMhVHYlnRRg9ShHaiadpA"
verify_cert = False

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

      events = misp.search(value=keyword, limit=5)
      return events
    
    @tool("MISP search Tool by date")
    def search_by_date(date_from: str = None, date_to: str = None):
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
    
    