#pragma once

#include <atomic>
#include <cstddef>
#include <cstdint>
#include <optional>
#include <type_traits>

namespace parity {

// Single-producer single-consumer lock-free ring buffer.
template <typename T, std::size_t Capacity>
class RingBuffer {
    static_assert((Capacity & (Capacity - 1)) == 0, "Capacity must be a power of two");

public:
    RingBuffer() : head_(0), tail_(0) {
        static_assert(std::is_trivially_copyable_v<T>, "RingBuffer requires trivially copyable types");
    }

    bool push(const T& value) {
        auto head = head_.load(std::memory_order_relaxed);
        auto next_head = head + 1;
        if (next_head - tail_.load(std::memory_order_acquire) > Capacity) {
            return false; // buffer full
        }
        buffer_[head & mask_] = value;
        head_.store(next_head, std::memory_order_release);
        return true;
    }

    std::optional<T> pop() {
        auto tail = tail_.load(std::memory_order_relaxed);
        if (tail == head_.load(std::memory_order_acquire)) {
            return std::nullopt; // buffer empty
        }
        T value = buffer_[tail & mask_];
        tail_.store(tail + 1, std::memory_order_release);
        return value;
    }

    bool empty() const {
        return head_.load(std::memory_order_acquire) == tail_.load(std::memory_order_acquire);
    }

private:
    static constexpr std::size_t mask_ = Capacity - 1;
    T buffer_[Capacity];
    std::atomic<std::uint64_t> head_;
    std::atomic<std::uint64_t> tail_;
};

} // namespace parity

