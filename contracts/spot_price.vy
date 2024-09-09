# @version 0.3.10

interface AggregatorV3Interface:
    def latestRoundData() -> (uint256, int256, uint256, uint256, uint256): view
    def decimals() -> uint8: view


price_feed: public(address)


@external
def __init__(_price_feed: address):
    self.price_feed = _price_feed

@external
@view
def get_latest_price() -> int256:
    price_feed_contract: AggregatorV3Interface = AggregatorV3Interface(self.price_feed)
    round_id: uint256 = 0
    price: int256 = 0
    started_at: uint256 = 0
    updated_at: uint256 = 0
    answered_in_round: uint256 = 0
    round_id, price, started_at, updated_at, answered_in_round = price_feed_contract.latestRoundData()
    return price

@external
@view
def get_price_decimals() -> uint8:
    price_feed_contract: AggregatorV3Interface = AggregatorV3Interface(self.price_feed)
    return price_feed_contract.decimals()
