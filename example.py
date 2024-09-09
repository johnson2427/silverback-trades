from ape import project, accounts, networks


def main():
    deployer = accounts.load('ape_test')
    price_feed_address = "0x5f4ec3df9cbd43714fe2740f5e3616155c5b8419"
    with networks.parse_network_choice("ethereum:sepolia"):
        eth_price_consumer = deployer.deploy(project.spot_price, price_feed_address)
        print(f"Contract deployed at: {eth_price_consumer.address}")


if __name__ == "__main__":
    main()
