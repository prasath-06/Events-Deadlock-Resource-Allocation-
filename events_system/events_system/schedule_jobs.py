from events_system.events_system.doctype.events_allocation.events_allocation import EventsAllocation

def auto_update_cron():
    events_connector = EventsAllocation()
    events_connector.auto_update()

