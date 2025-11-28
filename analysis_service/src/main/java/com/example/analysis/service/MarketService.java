package com.example.analysis.service;

import com.example.analysis.model.PropertyStats;
import com.opencsv.CSVReader;
import org.springframework.stereotype.Service;

import javax.annotation.PostConstruct;
import java.io.InputStream;
import java.io.InputStreamReader;

/**
 * Service responsible for computing statistics on the housing dataset.
 */
@Service
public class MarketService {
    private PropertyStats stats;

    /**
     * Load the dataset and compute statistics once during application startup.
     */
    @PostConstruct
    public void init() {
        try {
            stats = computeStats();
        } catch (Exception e) {
            // In production you might want to log this and handle it gracefully
            throw new RuntimeException("Failed to compute statistics", e);
        }
    }

    public PropertyStats getStats() {
        return stats;
    package com.example.analysis.service;

import com.example.analysis.model.PropertyStats;
import com.opencsv.CSVReader;
import org.springframework.stereotype.Service;

import javax.annotation.PostConstruct;
import java.io.InputStream;
import java.io.InputStreamReader;

/**
 * Service responsible for computing statistics on the housing dataset.
 */
@Service
public class MarketService {
    private PropertyStats stats;

    /**
     * Load the dataset and compute statistics once during application startup.
     */
    @PostConstruct
    public void init() {
        try {
            stats = computeStats();
        } catch (Exception e) {
            // In production you might want to log this and handle it gracefully
            throw new RuntimeException("Failed to compute statistics", e);
        }
    }

    public PropertyStats getStats() {
        return stats;
    }

    private PropertyStats computeStats() throws Exception {
        // Load CSV file from classpath
        InputStream is = getClass().getClassLoader().getResourceAsStream("HousePriceDataset.csv");
        if (is == null) {
            throw new IllegalStateException("Dataset resource not found");
        }
        try (CSVReader reader = new CSVReader(new InputStreamReader(is))) {
            String[] header = reader.readNext(); // skip header
            long count = 0;
            double sum = 0;
            double minPrice = Double.MAX_VALUE;
            double maxPrice = Double.MIN_VALUE;
            String[] line;
            while ((line = reader.readNext()) != null) {
                if (line.length < 9) continue;
                double price = Double.parseDouble(line[8]);
                sum += price;
                count++;
                if (price < minPrice) {
                    minPrice = price;
                }
                if (price > maxPrice) {
                    maxPrice = price;
                }
            }
            double average = count == 0 ? 0 : sum / count;
            return new PropertyStats(count, average, minPrice, maxPrice);
        }
    }
}
}

    private PropertyStats computeStats() throws Exception {
        // Load CSV file from classpath
        InputStream is = getClass().getClassLoader().getResourceAsStream("HousePriceDataset.csv");
        if (is == null) {
            throw new IllegalStateException("Dataset resource not found");
        }
        try (CSVReader reader = new CSVReader(new InputStreamReader(is))) {
            String[] header = reader.readNext(); // skip header
            long count = 0;
            double sum = 0;
            double minPrice = Double.MAX_VALUE;
            double maxPrice = Double.MIN_VALUE;
            String[] line;
            while ((line = reader.readNext()) != null) {
                if (line.length < 9) continue;
                double price = Double.parseDouble(line[8]);
                sum += price;
                count++;
                if (price < minPrice) {
                    minPrice = price;
                }
                if (price > maxPrice) {
                    maxPrice = price;
                }
            }
            double average = count == 0 ? 0 : sum / count;
            return new PropertyStats(count, average, minPrice, maxPrice);
        }
    }
}
