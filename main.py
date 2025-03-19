import requests
import click
from fewsats.core import Fewsats

# Constants
WEATHER_BASE_URL="https://weather.l402.org"

def create_user():
    resp = requests.post(f"{WEATHER_BASE_URL}/signup")
    resp.raise_for_status()
    data = resp.json()
    print(f"New UserID: {data['user_id']}")
    return data["user_id"]


def pay_with_cc(l402Offers, FEWSATS_API_KEY):
    fs = Fewsats(api_key=FEWSATS_API_KEY)

    # Make sure that our backend uses cc as payment method
    l402Offers["offers"][1]["payment_methods"] = ["credit_card"]
    
    # Get the offer ID before modifying the data structure
    offer_id = l402Offers["offers"][1]["id"]
    
    resp = fs.pay_offer(offer_id, dict(l402Offers))
    resp.raise_for_status()
    return resp.json()
    

def get_weather(user_id, location, fs_api_key):
    url_encoded_location = location.replace(" ", "%20")
    url = f"{WEATHER_BASE_URL}/weather?location={url_encoded_location}"
    response = requests.get(url, headers={"Authorization": f"Bearer {user_id}"})
    if response.status_code == 402:
        if fs_api_key == "":
            print("No credits left and no API key provided")
            return
        return pay_with_cc(response.json(), fs_api_key)
    else:
        return response.json()


@click.group()
def cli():
    """CLI for interacting with L402 services"""
    pass


@cli.command("create-user")
def create_user_command():
    """Create a new user"""
    create_user()


@cli.command("check-weather")
@click.option("--user-id", default="", help="User ID to use")
@click.option("--location", default="San Francisco", help="Location to check weather for")
@click.option("--api-key", default="", help="API Key to use")
def check_weather_command(user_id, location, api_key):
    """Check weather for a location"""
    if user_id == "":
        raise Exception("User ID is required")
    weather_data = get_weather(user_id, location, api_key)
    click.echo(weather_data)


@cli.command("check-payment")
@click.option("--payment-id", default="", help="Payment ID to check")
@click.option("--api-key", default="", help="API Key to use")
def check_payment_command(payment_id, api_key):
    """Check payment status (placeholder)"""
    if api_key == "":
        raise Exception("API Key is required")
    if payment_id == "":
        raise Exception("Payment ID is required")
    
    fs = Fewsats(api_key=api_key)
    resp = fs.payment_info(payment_id)
    resp.raise_for_status()
    click.echo(resp.json())


if __name__ == "__main__":
    cli()