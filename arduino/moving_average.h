// moving_average.h
#ifndef MOVING_AVERAGE_H
#define MOVING_AVERAGE_H

template<typename T, size_t N>
class MovingAverage {
private:
    T values[N];
    size_t index = 0;
    size_t count = 0;
    T sum = 0;
    
    // Exponential smoothing coefficient (0 to 1)
    // Lower alpha means more smoothing
    float alpha = 0.2;
    T lastExponentialAvg = 0;
    bool firstExp = true;
    
public:
    MovingAverage() {
        reset();
    }
    
    void reset() {
        index = 0;
        count = 0;
        sum = 0;
        firstExp = true;
        for (size_t i = 0; i < N; i++) {
            values[i] = 0;
        }
    }
    
    // Simple moving average
    T addSample(T value) {
        // Subtract oldest value if buffer is full
        if (count == N) {
            sum -= values[index];
        } else {
            count++;
        }
        
        // Add new value
        values[index] = value;
        sum += value;
        
        // Update index
        index = (index + 1) % N;
        
        // Return average
        return sum / count;
    }
    
    // Exponential moving average
    T addSampleExp(T value) {
        if (firstExp) {
            lastExponentialAvg = value;
            firstExp = false;
            return value;
        }
        
        // Exponential moving average formula:
        // avg = α * current + (1 - α) * lastAvg
        lastExponentialAvg = alpha * value + (1 - alpha) * lastExponentialAvg;
        return lastExponentialAvg;
    }
    
    // Set exponential smoothing factor
    void setAlpha(float newAlpha) {
        if (newAlpha >= 0 && newAlpha <= 1) {
            alpha = newAlpha;
        }
    }
    
    // Get current average without adding new sample
    T getCurrentAverage() const {
        if (count == 0) return 0;
        return sum / count;
    }
    
    T getCurrentExpAverage() const {
        return lastExponentialAvg;
    }
};

#endif // MOVING_AVERAGE_H