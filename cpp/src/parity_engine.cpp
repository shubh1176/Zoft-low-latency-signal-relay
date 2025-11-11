#include "parity_engine.hpp"

#include <algorithm>
#include <utility>

namespace parity {

ParityEngine::ParityEngine(double threshold_ticks, Callback cb)
    : threshold_ticks_(threshold_ticks), callback_(std::move(cb)) {}

void ParityEngine::on_quote(const QuoteUpdate& quote) {
    auto& venue_map = book_state_[quote.instrument];
    auto& state = venue_map[quote.venue];

    state.best_bid = quote.best_bid;
    state.best_ask = quote.best_ask;
    state.initialized = true;

    for (const auto& [other_venue, other_state] : venue_map) {
        if (other_venue == quote.venue || !other_state.initialized) {
            continue;
        }

        double spread = state.best_bid - other_state.best_ask;
        if (spread > threshold_ticks_) {
            ParityViolation violation{
                quote.timestamp_ns,
                quote.venue,
                other_venue,
                quote.instrument,
                state.best_bid,
                other_state.best_ask,
                spread
            };
            callback_(violation);
        }

        double reverse_spread = other_state.best_bid - state.best_ask;
        if (reverse_spread > threshold_ticks_) {
            ParityViolation violation{
                quote.timestamp_ns,
                other_venue,
                quote.venue,
                quote.instrument,
                other_state.best_bid,
                state.best_ask,
                reverse_spread
            };
            callback_(violation);
        }
    }
}

} // namespace parity

