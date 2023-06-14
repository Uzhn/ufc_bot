from bs4 import BeautifulSoup
import requests
import json


def parse_events():
    url = "https://ufc.ru/events"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    events = []

    event_elements = soup.find_all("div", class_="b-events__item")

    for event_element in event_elements:
        title_element = event_element.find("div", class_="b-events__title")
        location_element = event_element.find("div", class_="b-events__location")
        date_element = event_element.find("div", class_="b-events__date")

        title = title_element.text.strip()
        location = location_element.text.strip()
        date = date_element.text.strip()

        event = {
            "title": title,
            "location": location,
            "date": date
        }

        events.append(event)

    return events


if __name__ == "__main__":
    events = parse_events()

    with open("test.json", "w") as file:
        json.dump(events, file)
