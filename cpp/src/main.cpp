#include "feed_handler.hpp"
#include "parity_engine.hpp"

#include <iostream>

namespace {

void violation_logger(const parity::ParityViolation& violation) {
    std::cout << "Parity violation: "
              << violation.instrument << " buy " << violation.buy_venue
              << " @ " << violation.bid_price << " vs sell "
              << violation.sell_venue << " @ " << violation.ask_price
              << " spread " << violation.spread << '\n';
}

} // namespace

int main() {
    parity::ParityEngine engine{0.01, violation_logger};
    parity::FeedHandler handler{engine};

    handler.start();

    std::cout << "Press Enter to stop..." << std::endl;
    std::cin.get();

    handler.stop();
    return 0;
}

