#pragma once

#include <cstdint>
#include <functional>
#include <string>
#include <unordered_map>

namespace parity {

struct QuoteUpdate {
    std::uint64_t timestamp_ns{};
    double best_bid{};
    double best_ask{};
    std::string venue; // short identifier, e.g. "ZERODHA"
    std::string instrument; // symbol identifier
};

struct ParityViolation {
    std::uint64_t timestamp_ns{};
    std::string buy_venue;
    std::string sell_venue;
    std::string instrument;
    double bid_price{};
    double ask_price{};
    double spread{};
};

class ParityEngine {
public:
    using Callback = std::function<void(const ParityViolation&)>;

    explicit ParityEngine(double threshold_ticks, Callback cb);

    void on_quote(const QuoteUpdate& quote);

private:
    struct VenueState {
        double best_bid{0.0};
        double best_ask{0.0};
        bool initialized{false};
    };

    double threshold_ticks_;
    Callback callback_;
    std::unordered_map<std::string, std::unordered_map<std::string, VenueState>> book_state_;
};

} // namespace parity

