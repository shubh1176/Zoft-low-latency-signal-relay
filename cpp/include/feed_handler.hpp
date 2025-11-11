#pragma once

#include "parity_engine.hpp"

#include <atomic>
#include <string>
#include <thread>
#include <vector>

namespace parity {

class FeedHandler {
public:
    explicit FeedHandler(ParityEngine& engine);
    ~FeedHandler();

    // Non-copyable / non-movable for now
    FeedHandler(const FeedHandler&) = delete;
    FeedHandler& operator=(const FeedHandler&) = delete;

    void start();
    void stop();

private:
    void run();

    ParityEngine& engine_;
    std::atomic<bool> running_{false};
    std::thread worker_;
};

} // namespace parity

