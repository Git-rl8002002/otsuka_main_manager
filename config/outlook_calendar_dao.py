from O365 import Account , MSGraphProtocol
import datetime , calendar

client_id = '742334e8-b1de-4b48-b941-0608684c9858'
secret_id = 'HLX8Q~OOUWbONd4yhF5EsttsK-Twdolm5211JcNT'

credentials = (client_id , secret_id)

protocol = MSGraphProtocol() 
#protocol = MSGraphProtocol(defualt_resource='<sharedcalendar@domain.com>') 
scopes = ['Calendars.Read.Shared']
account = Account(credentials, protocol=protocol)

if account.authenticate(scopes=scopes):
   print('Authenticated!')


schedule = account.schedule()
calendar = schedule.get_default_calendar()
events = calendar.get_events(include_recurring=False) 
#events = calendar.get_events(query=q, include_recurring=True) 

for event in events:
    print(event)

