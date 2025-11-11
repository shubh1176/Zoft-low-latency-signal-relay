#include "feed_handler.hpp"

#include <chrono>
#include <iostream>
#include <thread>

namespace parity {

FeedHandler::FeedHandler(ParityEngine& engine) : engine_(engine) {}

FeedHandler::~FeedHandler() {
    stop();
}

void FeedHandler::start() {
    if (running_.exchange(true)) {
        return;
    }
    worker_ = std::thread(&FeedHandler::run, this);
}

void FeedHandler::stop() {
    if (!running_.exchange(false)) {
        return;
    }
    if (worker_.joinable()) {
        worker_.join();
    }
}

void FeedHandler::run() {
    using namespace std::chrono_literals;
    std::uint64_t ts = 0;
    while (running_.load()) {
        QuoteUpdate quote{
            ts++,
            100.0,
            100.5,
            "SIM_A",
            "DEMO"
        };
        engine_.on_quote(quote);
        std::this_thread::sleep_for(1ms);
    }
}

} // namespace parity

