package com.example.analysis.model;

/**
 * DTO representing aggregated statistics of the housing dataset.
 */
public class PropertyStats {
    private long count;
    private double averagePrice;
    private double minPrice;
    private double maxPrice;

    public PropertyStats() {
    }

    public PropertyStats(long count, double averagePrice, double minPrice, double maxPrice) {
        this.count = count;
        this.averagePrice = averagePrice;
        this.minPrice = minPrice;
        this.maxPrice = maxPrice;
    }

    public long getCount() {
        return count;
    }

    public void setCount(long count) {
        this.count = count;
    }

    public double getAveragePrice() {
        return averagePrice;
    }

    public void setAveragePrice(double averagePrice) {
        this.averagePrice = averagePrice;
    }

    public double getMinPrice() {
        return minPrice;
    }

    public void setMinPrice(double minPrice) {
        this.minPrice = minPrice;
    }

    public double getMaxPrice() {
        return maxPrice;
    }

    public void setMaxPrice(double maxPrice) {
        this.maxPrice = maxPrice;
    }
}
